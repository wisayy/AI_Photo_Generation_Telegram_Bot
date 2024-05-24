from aiogram.types import CallbackQuery
from config_reader import config
from aiogram import Router
from aiogram import types
from __main__ import Bot
from db.models import User, Transaction
from bot.handlers.keyboards import get_credits, get_price_rub, get_price_usd
from bot.handlers.callback import get_user_language
from bot.handlers.credits_images import get_image_link




router_payment = Router()

#get price from keyboards


STRIPE = config.STRIPE_API_KEY.get_secret_value()

#YOOMONEY = config.YOOMONEY_API_KEY.get_secret_value()

@router_payment.callback_query(lambda query: query.data.startswith("10_credits") or query.data.startswith("20_credits") or query.data.startswith("50_credits") or query.data.startswith("100_credits") or query.data.startswith("500_credits") or query.data.startswith("1000_credits") or query.data.startswith("3000_credits"))
async def process_pay_callback(query: CallbackQuery, bot: Bot):


    selected_credit_option = query.data.split("_")[0]

    #print(selected_credit_option)

    language = await get_user_language(query.from_user.id)
    #print (language)

    prices = get_credits(language)
    #print(prices)

    # if language == "ru":
    #     price_value = get_price_rub(int(selected_credit_option))
    #     token_provider = YOOMONEY
    #     price_value = price_value
    #     payment_currency = "rub"
    #     label = "Пополнение кредитов"
    #     tax_label = "НДС"
    #     description = f"Покупка {int(selected_credit_option)} кредитов"
    #     title = f"Счет на оплату кредитов {selected_credit_option} шт."
    # else:
    price_value = get_price_usd(int(selected_credit_option))
    token_provider = STRIPE
    payment_currency = "usd"
    label = "Credit purchase"
    tax_label = "VAT"
    description = f"Purchase {int(selected_credit_option)} credits"
    title = f"Invoice for {int(selected_credit_option)} credits"
    #print(price_value)

    

    PRICE = {
        "label": label,  # Invoice label (e.g., "Credit purchase")
        "amount": int(price_value * 100),  # Convert price to cents for Stripe (assuming Stripe)
    }
    
    TAX = {
        "label": tax_label,
        "amount": int(price_value * 0.22 * 100),
    }
    #print(PRICE["amount"])

    image_link = await get_image_link(int(selected_credit_option))

    chat_id = query.message.chat.id  # Extracting chat ID from the message
    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=query.data,
        provider_token=token_provider,
        currency=payment_currency,
        photo_url=image_link,
        photo_height=512,
        photo_width=512,
        photo_size=4000,
        is_flexible=False,
        prices=[PRICE] + [TAX],
    )


@router_payment.pre_checkout_query(lambda query: True)
async def pre_checkout_query_handler(pre_checkout_q: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router_payment.message(lambda message: message.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def message_handler(message: types.Message):
    try:
        #print("Успешный платеж!")
        payment_info = {
            "total_amount": message.successful_payment.total_amount,
            "currency": message.successful_payment.currency,
        }

        user_id = message.chat.id
        
        # Получаем пользователя из базы данных
        user = await User.get(id=user_id)  # Assuming you have the user's ID

        selected_credit_option = message.successful_payment.invoice_payload.split('_')[0]

        user.credits += int(selected_credit_option)
        await user.save()
        user_id = user.pk
        
        # Создаем транзакцию
        transaction = Transaction(
            user_id=user_id,
            amount=int(selected_credit_option),
            currency=payment_info["currency"],
            status="SUCCESS",
            price=payment_info["total_amount"] / 100,
        )
        await transaction.save()
        
        # if user.language == "ru":
        #     await message.answer(f"Платеж успешно проведен! \nВам начислено {int(selected_credit_option)} кредитов. \nВаш баланс составляет {user.credits} кредитов")
        # else:
        await message.answer(f"Payment successful! \nYou have been credited with {int(selected_credit_option)} credits. \nYour balance is {user.credits} credits")

    except Exception as e:
        # Обработка ошибки
        print(f"Ошибка при обработке платежа: {e}")
        await message.answer("An error occurred while processing the payment. Please try again later.")
        transaction = Transaction(
            user_id=user_id,
            amount=int(selected_credit_option),
            currency=payment_info["currency"],
            status="FAILED",
            price=payment_info["total_amount"] / 100,
        )
        await transaction.save()


