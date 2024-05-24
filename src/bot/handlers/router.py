from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import FSInputFile
from db.models import User
from bot.handlers.keyboards import get_keyboard
from bot.handlers.callback import get_credits_caption_en, en_caption


photo = FSInputFile('/home/ubuntu/ReplicateBotAI/src/banner_test.png')

import bot.handlers.keyboards as kb



router = Router()


@router.message(CommandStart())
async def start_command(message: Message):

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
            user_credit = user.credits
            keyboard = get_keyboard('en')
            caption = en_caption(user_credit)
            await message.answer_photo(
            photo,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
            )
        else:
            user = await User.get(id=message.from_user.id)
            user_credit = user.credits
            keyboard = get_keyboard('en')
            caption = en_caption(user_credit)
            await message.answer_photo(
            photo,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
            )

    else:
        user = existing_user
        user = await User.get(id=user_id)
        user_language = user.language
        user_credit = user.credits
        # if user_language == "ru":
        #     keyboard = get_keyboard(user_language)
        #     caption = ru_caption(user_credit)
    
        keyboard = get_keyboard('en')
        caption = en_caption(user_credit)

        await message.answer_photo(
            photo,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

#pay command
@router.message(Command("credits"))
async def pay_command(message: Message):
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
            keyboard = kb.get_credits("en")
            caption = get_credits_caption_en(user_credit)
        keyboard = kb.get_credits("en")
        caption = get_credits_caption_en(user_credit)

        await message.answer_photo(
            photo,
            caption,
            reply_markup=keyboard
        )
    else:
        user = await User.get(id=user_id)
        user_language = user.language
        user_credit = user.credits
        # if user_language == "ru":
        #     keyboard = kb.get_credits(user_language)
        #     caption = get_credits_caption_ru(user_credit)
        # elif user_language == "en":
        keyboard = kb.get_credits('en')
        caption = get_credits_caption_en(user_credit)

        await message.answer_photo(
            photo,
            caption,
            reply_markup=keyboard
        )
