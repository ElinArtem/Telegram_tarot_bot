import telebot
import final.config as config
from telebot import types
from final.layout import create_layout
from final.chat_gpt import deciphering































class TarotBot(telebot.TeleBot):
    def __init__(self, api: str) -> None:
        super().__init__(api)

bot = TarotBot(api=config.settings["TOKEN"])

# Handler for the /start command
@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/create_layout")
    btn2 = types.KeyboardButton("/info")
    markup.add(btn1, btn2)

    welcome_message = (
        f"Приветствую вас, <b>{message.from_user.first_name}</b>!\n"
        "Мы рады видеть вас в Боте для расклада таро!"
    )
    bot.send_message(message.chat.id, welcome_message, parse_mode="html", reply_markup=markup)

# Handler for the /create_layout command
@bot.message_handler(commands=["create_layout"])
def create_layout_handler(message: types.Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1")
    btn2 = types.KeyboardButton("2")
    btn3 = types.KeyboardButton("3")
    btn4 = types.KeyboardButton("5")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Выберите количество карт:", reply_markup=markup)
    bot.register_next_step_handler(message, get_card_count)

def get_card_count(message: types.Message) -> None:
    try:
        count = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Польное описание вместе с описанием карт")
        btn2 = types.KeyboardButton("Только трактовку расклада")
        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, "Выберите тип расклада:", reply_markup=markup)
        bot.register_next_step_handler(message, choose_type, count)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_card_count)

def choose_type(message: types.Message, count: int) -> None:
    if message.text in ["Польное описание вместе с описанием карт", "Только трактовку расклада"]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Будущее")
        btn2 = types.KeyboardButton("Профессиональная деятельность")
        btn3 = types.KeyboardButton("Семья")
        btn4 = types.KeyboardButton("Здоровье")
        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        markup.row(btn4)

        bot.send_message(message.chat.id, "На какую тему вы хотите расклад?", reply_markup=markup)
        bot.register_next_step_handler(message, fun_layout, count, message.text)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите тип расклада.")
        bot.register_next_step_handler(message, choose_type, count)

def fun_layout(message: types.Message, count: int, layout_type: str) -> None:
    if message.text in [
        "Будущее",
        "Профессиональная деятельность",
        "Семья",
        "Здоровье"
    ]:
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/create_layout")
            btn2 = types.KeyboardButton("/info")
            markup.add(btn1, btn2)
            layout = create_layout(count)

            for item in layout[0]:
                rotation = "прямое" if item["rotation"] == "straight" else "перевернутое"
                bot.send_message(message.chat.id, f'Карта: {item["name"]}, {rotation} положение')
                bot.send_photo(message.chat.id, item["image"])

            bot.send_message(message.chat.id, "Мы создаем для вас трактовку расклада. Нужно немного подождать.")
            
            info = deciphering(layout[1], message.text, layout_type)

            bot.send_message(message.chat.id, info, reply_markup=markup)
        except Exception as e:
            bot.send_message(
                message.chat.id,
                f"Возникли проблемы в работе сервиса. Подождите некоторое время. Ошибка: {e}",
                reply_markup=markup
            )
    else:
        bot.send_message(message.chat.id, "Выберите тему для запроса из представленного списка!")
        bot.register_next_step_handler(message, fun_layout, count, layout_type)

# Handler for the /info command
@bot.message_handler(commands=["info"])
def info_handler(message: types.Message) -> None:
    info_message = "Информация о боте и раскладах."
    bot.send_message(message.chat.id, info_message)

bot.polling(non_stop=True)
