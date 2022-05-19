import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from FSM.states import Spam
from keyboard.inline import btn_cmd_start, btn_state_users
from loader import dp
from user.user_bot import client


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await dp.bot.send_message(message.from_user.id, "Панель управления 🤖", reply_markup=btn_cmd_start)


@dp.callback_query_handler(text="mailing")
async def mailing(call: types.CallbackQuery):
    await call.bot.send_message(call.from_user.id, "Напишите текст для рассылки")
    await Spam.text.set()

    await call.bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(state=Spam.text)
async def text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    ans = """Напишите юзернеймы пользователей, которые должны получить сообщение
<em>Пример ввода:</em>
<b>user_1
user_2
и т.д</b>"""
    await message.answer(text=ans)
    await Spam.next()


@dp.message_handler(state=Spam.users)
async def users(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['users'] = message.text
    await message.answer(f"Сообщение:\n{data.get('text')}\n\nПользователи:\n{data.get('users')}",
                         reply_markup=btn_state_users)
    await Spam.next()


@dp.callback_query_handler(text="confirm", state=Spam.confirmation)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(callback_query_id=call.id)

    async with state.proxy() as data:
        u = data["users"].split("\n")
        m = data["text"]

    for index, user in enumerate(u):
        if await state.get_state() == "Spam:confirmation":
            try:
                await client.send_message(entity=user, message=m)
                await call.bot.send_message(call.from_user.id,
                                            f"<b>Сообщение отправлено {'@' + user if user[0] != '@' else user}</b> [{index + 1}/{len(u)}]")
            except Exception as e:
                await call.bot.send_message(call.from_user.id,
                                            f"<b>Не удалось отправить сообщение {'@' + user if user[0] != '@' else user}</b> [{index + 1}/{len(u)}] ({e})")
            finally:
                await asyncio.sleep(30)
        else:
            await state.finish()

    await call.bot.send_message(call.from_user.id, "<b>Рассылка успешно завершена ✅</b>")
    await state.finish()


@dp.callback_query_handler(text="cancel", state="*")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.bot.send_message(call.from_user.id, "<em>Рассылка успешно отменена!</em>")

    await call.bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text="userbot_info")
async def userbot_info(call: types.CallbackQuery):
    data = await client.get_me()
    ans = f"""<b>ID:</b> {data.id}
<b>name:</b> {data.first_name + ' ' + (data.last_name if data.last_name else '')}
<b>username:</b> {data.username if data.username else 'Отсутствует'}"""
    await call.bot.send_message(call.from_user.id, ans)

    await call.bot.answer_callback_query(callback_query_id=call.id)
