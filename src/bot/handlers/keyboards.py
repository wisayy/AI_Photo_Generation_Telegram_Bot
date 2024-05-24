from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_keyboard(language):
  text = {
    # "ru": {
    #   "language_ru": "🇷🇺 Русский",
    #   "language_en": "🇬🇧 English",
    #   "technical_support": "🆘 Техническая поддержка",
    #   "buy_credits": "Купить кредиты",
    #   "generate": "️ Сгенерировать"
    # },
    "en": {
      # "language_ru": "🇷🇺 Russian",
      # "language_en": "🇬🇧 English",
      "technical_support": "🆘 Technical Support",
      "buy_credits": "Buy credits",
      "generate": "️ Generate"
    }
  }

  buttons = [
    # [
    #   InlineKeyboardButton(text=text[language]["language_ru"], callback_data="language:ru"),
    #   InlineKeyboardButton(text=text[language]["language_en"], callback_data="language:en")
    # ],
    [
      InlineKeyboardButton(text=text[language]["technical_support"], callback_data="technical_support", url="https://t.me/Technical_Support_AI_bot")
    ],
    [InlineKeyboardButton(text=text[language]["buy_credits"], callback_data="credits")],
    [InlineKeyboardButton(text=text[language]["generate"], callback_data="generate")]
  ]
  return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_price_usd(credits_usd):
  return credits_usd * 0.01 * 15 # в долларах

def get_price_rub(credits_rub):
  return credits_rub * 0.01 * 15 * 92 # в рублях

def price_rub_vat(credits_rub):
  return get_price_rub(credits_rub) + (get_price_rub(credits_rub) * 0.20)

def price_usd_vat(credits_usd):
  return get_price_usd(credits_usd) + (get_price_usd(credits_usd) * 0.22)

def format_price(price):
  if price.is_integer():  # Проверяем, является ли число целым
    return str(int(price))  # Если целое, преобразуем в строку без дробной части
  else:
    return str(price)  # Если дробное, просто преобразуем в строку


def get_credits(language):
  text = {
    # "ru": {
    #   "10_credits": f"Купить 10 кредитов - {format_price(price_rub_vat(10))} ₽",
    #   "20_credits": f"Купить 20 кредитов - {format_price(price_rub_vat(20))} ₽",
    #   "50_credits": f"Купить 50 кредитов - {format_price(price_rub_vat(50))} ₽",
    #   "100_credits": f"Купить 100 кредитов - {format_price(price_rub_vat(100))} ₽",
    #   "500_credits": f"Купить 500 кредитов - {format_price(price_rub_vat(500))} ₽",
    #   "1000_credits": f"Купить 1000 кредитов - {format_price(price_rub_vat(1000))} ₽",
    #   "3000_credits": f"Купить 3000 кредитов - {format_price(price_rub_vat(3000))} ₽",
    #   "back": "Назад"
    # },
    "en": {
      "10_credits": f"Buy 10 credits - {format_price(price_usd_vat(10))} $",
      "20_credits": f"Buy 20 credits - {format_price(price_usd_vat(20))} $",
      "50_credits": f"Buy 50 credits - {format_price(price_usd_vat(50))} $",
      "100_credits": f"Buy 100 credits - {format_price(price_usd_vat(100))} $",
      "500_credits": f"Buy 500 credits - {format_price(price_usd_vat(500))} $",
      "1000_credits": f"Buy 1000 credits - {format_price(price_usd_vat(1000))} $",
      "3000_credits": f"Buy 3000 credits - {format_price(price_usd_vat(3000))} $",
      "back": "Back"
    }
  }

  buttons = [
    [
      InlineKeyboardButton(text=text[language]["10_credits"], callback_data="10_credits"),
    ],
    [
      InlineKeyboardButton(text=text[language]["20_credits"], callback_data="20_credits")
    ],
    [
      InlineKeyboardButton(text=text[language]["50_credits"], callback_data="50_credits")
    ],
    [
      InlineKeyboardButton(text=text[language]["100_credits"], callback_data="100_credits")
    ],
    [
      InlineKeyboardButton(text=text[language]["500_credits"], callback_data="500_credits")
    ],
    [
      InlineKeyboardButton(text=text[language]["1000_credits"], callback_data="1000_credits")
    ],
    [
      InlineKeyboardButton(text=text[language]["3000_credits"], callback_data="3000_credits")
    ],
    [
      InlineKeyboardButton(text=text[language]["back"], callback_data="back")
    ]
  ]
  return InlineKeyboardMarkup(inline_keyboard=buttons)
