import asyncio
import random
import os
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command

from aiogram.types import Message
from config import TOKEN, WEATHER_TOKEN



bot = Bot(TOKEN)
dp = Dispatcher()


# Функция для получения данных о погоде
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_TOKEN,
        "units": "metric",
        "lang": "ru"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["cod"] != 200:
            return f"Ошибка: {data['message']}"
        weather_description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Погода в городе <b>{city}</b>:\n"
            f"🌡️ Температура: {temperature}°C\n"
            f"🤗 Ощущается как: {feels_like}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬️ Ветер: {wind_speed} м/с\n"
            f"☁️ Описание: {weather_description}"
        )
    except Exception as e:
        return f"Ошибка при получении данных: {str(e)}"


@dp.message(Command('weather'))
async def weather_command(message: types.Message):
    command = message.text.strip()
    parts = command.split(" ", 1)

    if len(parts) < 2:
        await message.reply(
            "Пожалуйста, укажите город. Пример: /weather Москва"
        )
        return

    city = parts[1].strip()
    weather_info = get_weather(city)
    await message.reply(weather_info, parse_mode='HTML')


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://cs6.livemaster.ru/storage/47/1f/e6c1defa8ea4fc9293081373656a.jpg', 'https://cs6.livemaster.ru/storage/51/8d/e9304e78c01418b5ea956d3be36a.jpg!','https://cs6.livemaster.ru/storage/f1/a7/378d36a85b8e6cab15c48e25026a.jpg','https://cs3.livemaster.ru/zhurnalfoto/d/a/1/150404091759.jpeg']
    rand_photo = random.choice(list)
    await message.answer_photo(rand_photo, caption='Это супер кот')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого!', 'Cool!','Фу бяка','Кака бяка бее']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(F.text=='Что такое ИИ')
async def aitext(message: Message):
    await message.answer('ИИ - это дох и больше текста ааа')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды \n /start  \n /help \n /photo \n /weather \n Что такое ИИ')


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

async def main(dispatcher):
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(dp))