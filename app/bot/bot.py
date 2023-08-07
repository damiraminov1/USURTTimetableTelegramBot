import io
import json

import aiohttp
from aiogram import Bot, Dispatcher, types
import redis

from config import TelegramBotConfig, ParserConfig, RedisConfig
from app.parser.parser import Parser

parser = Parser()

button_timetable_text = "Выбрать расписание"
bot = Bot(TelegramBotConfig.TOKEN)
dp = Dispatcher(bot=bot)
redis_instance = redis.Redis(host=RedisConfig.REDIS_HOST, port=6379)


@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Main Keyboard-menu
    button_timetable = types.KeyboardButton(button_timetable_text)
    markup.add(button_timetable)
    await message.reply("Привет! Это бот-расписание УрГУПС", reply_markup=markup)


@dp.message_handler(content_types=["text"])
async def main(message: types.Message):
    if message.text == button_timetable_text:
        markup = await get_timetable_list_buttons(ParserConfig.URL)
        await message.reply(
            "Хорошо, посмотрим расписание. Нажми на кнопку для выбора",
            reply_markup=markup,
        )


@dp.callback_query_handler()
async def callback_dict(call):
    if call.message:
        data = json.loads(call.data)
        raw_link = redis_instance.get(name=data["link_id"])
        if not raw_link:
            return await call.message.reply(
                "Ссылка устарела :( Очень жаль, но придется выбрать расписание заново",
                reply_markup=await get_timetable_list_buttons(ParserConfig.URL),
            )
        link: str = raw_link.decode(encoding="utf-8")
        if data["format"] in ParserConfig.FILE_FORMATS:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    if response.ok:
                        file = types.InputFile(
                            io.BytesIO(await response.read()),
                            filename=response.real_url.name,
                        )
            await call.message.answer_document(document=file)
            await main(message=call.message)
        elif data["format"] == "directory":
            markup = await get_timetable_list_buttons(link)
            await call.message.reply("Хорошо. Выбери дальше:", reply_markup=markup)


async def get_timetable_list_buttons(url):
    parser_data = await parser.get_content(url)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for button in parser_data:
        button_name = hash(button["link"])
        redis_instance.set(name=button_name, value=button["link"], ex=2592000)
        timetable_markup_keyboard_button = types.InlineKeyboardButton(
            button["name"],
            callback_data=json.dumps(
                {
                    "link_id": button_name,
                    "format": button["format"],
                }
            ),
        )
        markup.add(timetable_markup_keyboard_button)
    return markup
