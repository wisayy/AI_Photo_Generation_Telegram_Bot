import os
from httpx import RequestError
import replicate
from aiogram.types import Message
from config_reader import config
from aiogram import Router, F
from aiogram.methods.get_file import GetFile
from db.models import User, Image, Order
import datetime
from tortoise.transactions import in_transaction
from asyncio import Lock



os.environ['REPLICATE_API_TOKEN'] = config.REPLICATE_API_TOKEN.get_secret_value()

TOKEN = config.BOT_TOKEN.get_secret_value()

whitelisted_users = [425425686, 603972219]

router1 = Router()



async def process_image(image_url, prompt, message: Message):  
    try:
        output = replicate.run(
            "fofr/face-to-many:35cea9c3164d9fb7fbd48b51503eabdb39c9d04fdaef9a68f368bed8087ec5f9",
            input={
                "image": image_url,
                "style": "Video game",
                "prompt": prompt,
                "lora_scale": 1,
                "negative_prompt": "boring",
                "prompt_strength": 4.5,
                "denoising_strength": 0.65,
                "instant_id_strength": 0.8,
                "control_depth_strength": 0.8
            }
        )
        return output[0]  # Возвращаем только первый URL из списка
    except Exception as e:
        print("Ошибка при обработке фотографии:", e)
        await message.reply("An error occurred while processing the image. Please try again later.")
        return None
    

async def image_processing(user, message: Message, user_id):
    largest_photo = message.photo[-1]
    file_id = largest_photo.file_id
    file_info: GetFile = await message.bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"


    #print(f"File URL: {file_url}")
    
    order = await Order.create(status="Processing", user_id=user_id)
    order_id = order.id

    prompt = message.caption if message.caption else "ps2, video game, aesthetic, old video game, playstation 2"
    user_credit = user.credits
    try:
        # if user_language == "ru":
        #     await message.reply(f"Ваша фотография обрабатывается. Пожалуйста, подождите. \n\n🕐 Это может занять некоторое время.\n\n Осталось: {user_credit} кредитов")
        # else:
        await message.reply(f"Your photo is being processed. Please wait. \n\n🕐 This may take some time.\n\n Credits left: {user_credit} credits")
        output = await process_image(file_url, prompt, message)
        if output:
            response = await message.reply_photo(output)
            file_id = response.photo[-1].file_id
            file_info: GetFile = await message.bot.get_file(file_id)
            processed_at = datetime.datetime.utcnow()
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

            image = await Image.create(url=file_url, prompt=prompt, credits=1)
            image_id = image.id
            

            order = await Order.get(id=order_id)
            order.status = "Processed"
            order.processed_at = processed_at
            order.image_id = image_id
            await order.save()
            #print(f"Image processed and saved for user {user_id}")
        else:
            await handle_processing_error(user, order, message)
            #print(f"Error processing image for user {user_id}")
        
    except RequestError as e:
        #print("Ошибка при обработке фотографии:", e)
        await handle_processing_error(user, order, message)
        #print(f"Error processing image for user {user_id}")




async def check_user_credit(user_id, message: Message):
    user = await User.get(id=user_id)
    user_credit = user.credits
    if user_credit < 1:
        await message.reply("You don't have enough credits to process the image. Please top up your balance.")
        return



    

processing_queues = {}

credit_lock = Lock()


@router1.message(F.photo)
async def handle_photo(message: Message):
    #print(f"Received photos from user {message.from_user.id}")
    
        user_id = message.from_user.id
        existing_user = await User.filter(id=message.from_user.id).first()
        if not existing_user:
            user = await User.get_or_create(id=message.from_user.id, username=message.from_user.username)
            all_data = await User.all()
            user_index = len(all_data)
            #print(user_index)
            if user_index < 1000:
                user = await User.get(id=message.from_user.id)
                user.credits += 1
                await user.save()

                async with credit_lock:
                    user = await User.get(id=user_id)
                    user_credits = user.credits

                    # Проверяем наличие кредитов у пользователя
                    if user_credits < 1:
                        await message.answer("You don't have enough credits to process the image. Please top up your balance.")
                        return
                                # Уменьшаем количество кредитов у пользователя
                    user.credits -= 1
                    await user.save()

                await image_processing(user, message, user_id)
        else:
            async with credit_lock:
                user = await User.get(id=user_id)
                user_credits = user.credits

                # Проверяем наличие кредитов у пользователя
                if user_credits < 1:
                    await message.answer("You don't have enough credits to process the image. Please top up your balance.")
                    return
                            # Уменьшаем количество кредитов у пользователя
                user.credits -= 1
                await user.save()

            await image_processing(user, message, user_id)


async def handle_processing_error(user, order, message: Message):
    user.credits += 1
    await user.save()

    order.status = "Error"
    await order.save()

    user_credit = user.credits

    await message.reply(f"An error occurred while processing the image. Your credits have been refunded. \n\n Credits left: {user_credit} credits")

