from aiogram import Router, types
from bot.handlers.keyboards import get_keyboard, get_credits



from db.models import User
router = Router()


async def get_user_language(user_id: int) -> str:
    try:
        user = await User.get(id=user_id)
        return user.language
    except User.DoesNotExist:  # Handle missing user case
        return "en"  # Default to English if user not found


# def ru_caption(user_credit):
#     return f"<b>Добро пожаловать в PS2 AI!</b> \n\n<i>Выберите действие для обработки изображения 🎮✨</i> \n\n<u>Доступные команды:</u> \n/start \n/credits \n\n<i>Ваш баланс:</i> {user_credit} <i>кредитов</i>"

def en_caption(user_credit):
    return f"<b>Welcome to PS2 AI!</b> \n\n<i>Choose an action to process the image 🎮✨</i> \n\n<u>Available commands:</u> \n/start \n/credits \n\n<i>Your balance:</i> {user_credit} <i>credits</i>"

@router.callback_query(lambda c: c.data.startswith('language:'))
async def handle_language_selection(query: types.CallbackQuery):
    user_id = query.from_user.id
    language_code = query.data.split(':')[1]

    await User.filter(id=user_id).update(language=language_code)  # Update database
    new_keyboard = get_keyboard(language_code)  # Directly retrieve keyboard based on language
    user = await User.get(id=user_id)
    user_credit = user.credits
    
    # if language_code == "ru":
    #     await query.message.edit_caption(caption=ru_caption(user_credit), reply_markup=new_keyboard, parse_mode="HTML")
    # else:
    await query.message.edit_caption(caption=en_caption(user_credit), reply_markup=new_keyboard, parse_mode="HTML")

    await query.answer()



# def get_credits_caption_ru(user_credits):
#     return f"<b>Кредиты в нашем Telegram-боте:</b>\n\n" \
#            f"<i>Чем больше у вас кредитов, тем больше творческих возможностей вы получаете!</i>\n\n" \
#            f"<i>1 кредит = 1 изображение</i>\n\n" \
#            f"<i>Ваш баланс:</i> <b>{user_credits}</b> <i>кредитов</i>\n\n" \
   
def get_credits_caption_en(user_credits):
    return f"<b>Credits in our Telegram bot:</b>\n\n" \
           f"<i>The more credits you have, the more creative possibilities you get!</i>\n\n" \
           f"<i>1 credit = 1 image</i>\n\n" \
           f"<i>Your balance:</i> <b>{user_credits}</b> <i>credits</i>"  # Ensure closing tag for "<b>"


@router.callback_query(lambda c: c.data in ["generate", "credits", "back"])
async def handle_common_actions(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)

    # # Language-specific responses and keyboard handling
    # if user_language == "ru":
    #     # Process actions in Russian
    #     if query.data == "generate":
    #         await query.message.answer("Для обработки фотографии ее нужно скинуть в чат и написать промпт если вы этого хотите или оставьте его пустым!")
    #     elif query.data == "credits":
    #         keyboard = get_credits(user_language)  # Get keyboard directly
    #         # Get user credits from the database
    #         user = await User.get(id=user_id)
    #         user_credit = user.credits
    #         inviter_id = user.id
    #         await query.message.edit_caption(caption=get_credits_caption_ru(user_credit), reply_markup=keyboard, parse_mode='HTML')  # Update caption and keyboard
    #     elif query.data == "back":
    #         user = await User.get(id=user_id)
    #         user_credit = user.credits
    #         await query.message.edit_caption(caption=ru_caption(user_credit), reply_markup=get_keyboard(user_language), parse_mode='HTML')
    # else:
        # Process actions in English
    if query.data == "generate":
        await query.message.answer("To process the photo, you need to send it to the chat and write prompt if you want or leave it empty!")
    elif query.data == "credits":
        keyboard = get_credits(user_language)  # Get keyboard directly
        user = await User.get(id=user_id)
        user_credit = user.credits
        await query.message.edit_caption(caption=get_credits_caption_en(user_credit), reply_markup=keyboard, parse_mode='HTML')  # Update caption and keyboard
    elif query.data == "back":
        user = await User.get(id=user_id)
        user_credit = user.credits
        await query.message.edit_caption(caption=en_caption(user_credit), reply_markup=get_keyboard(user_language), parse_mode='HTML')

    await query.answer()

