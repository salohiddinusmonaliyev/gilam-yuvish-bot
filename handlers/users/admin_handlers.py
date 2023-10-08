from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.keyboards import main_menu, back, admin_main_menu
from loader import dp, db, bot
from states.main_states import Complete, SetPrice


@dp.message_handler(text="↔️ Mijoz rejimiga o'tish")
async def switch_mode(message: types.Message):
    await message.answer("Mijoz rejimiga o'tildi.\n<b>Agar admin sahifasiga qaytmochi bo'lsangiz /start ni bosing</b>", reply_markup=main_menu)

@dp.message_handler(commands=["set_completed"])
@dp.message_handler(text="✔️ Buyurtma tugatildi")
async def get_id(message: types.Message):
    await message.answer("Buyurtma raqamini kiriting: ", reply_markup=back)
    await Complete.id.set()

@dp.message_handler(state=Complete.id)
async def completed(message: types.Message, state=FSMContext):
    try:
        if message.text.isdigit():
            await message.answer(f"Siz kiritdingiz: {message.text}", reply_markup=main_menu)
            order_record = await db.get_order(id=int(message.text))
            order_id = order_record['id']  # Extract the id from the record
            await db.completed(id=order_id)  # Pass the id to the completed method
            service_id = int(order_record['service_id'])
            service = await db.get_service(service_id)
            user = await db.select_user(id=int(order_record['user_id']))
            await message.answer(f"Id: {order_record['id']} \n"
                    f"Manzil: {order_record['address']} \n"
                    f"Buyurtma holati: Topshirildi\n"
                    f"Xizmat turi: {service[0]['name']}\n"
                    f"Buyurtmachi telefon raqami: {order_record['phone_number']}\n"
                                 "\n<b>Buyurtma yakunlandi!</b>")
            await bot.send_message(int(user['telegram_id']), f"{order_record['id']} raqamli buyurtmangiz yakunlandi! Tez orada yetkazib beriladi")
            await state.finish()
        elif message.text == "🔙 Ortga":
            await state.finish()
            if message.from_user.id == int(ADMINS[0]):
                await message.answer("Ortga qaytildi.", reply_markup=admin_main_menu)
            else:
                await message.answer("Ortga qaytildi.", reply_markup=main_menu)
    except:
        await message.answer("Bu raqamga tegishli buyurtma yo'q\nTekshirib qaytadan kiriting: ")


def send_completed(chat_id):
    # Your existing code...

    # Assuming order_record is your Order model instance
    if order_record.is_completed:
        bot.message.answer(chat_id=chat_id, message=f"Completed\n"
                                                      f"Id: {order_record.id}\n"
                                                      f"Manzil: {order_record.address}\n"
                                                      f"Xizmat turi: {order_record.service.name}\n"
                                                      f"Buyurtmachi telefon raqami: {order_record.phone_number}\n"
                                                      f"\n<b>Buyurtma yakunlandi!</b>")



@dp.message_handler(commands=["set_price"])
@dp.message_handler(text="💲 Narx belgilash")
async def get_id(message: types.Message, state: FSMContext):
    await message.answer("Buyurtma raqamini kiriting: ", reply_markup=back)
    await SetPrice.id.set()


@dp.message_handler(state=SetPrice.id)
async def get_price(message: types.Message, state=FSMContext):
    global order_record
    if message.text.isdigit():
        await message.answer(f"Buyurtma umumiy narxini kiriting:")
        order_record = await db.get_order(id=int(message.text))
        await SetPrice.price.set()
    elif message.text == "🔙 Ortga":
        await state.finish()
        if message.from_user.id == int(ADMINS[0]):
            await message.answer("Ortga qaytildi.", reply_markup=admin_main_menu)
        else:
            await message.answer("Ortga qaytildi.", reply_markup=main_menu)

    else:
        await message.answer("Nakladnoy raqamini kiriting! \n\nSiz raqam kiritmadingiz!", reply_markup=back)




@dp.message_handler(state=SetPrice.price)
async def get_price(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        order = order_record['id']
        update = await db.update_price(id=int(order), price=int(message.text))
        await state.finish()
        await message.answer("Buyurtmaga narx belgilandi", reply_markup=admin_main_menu)
    elif message.text == "🔙 Ortga":
        await state.finish()
        if message.from_user.id == int(ADMINS[0]):
            await message.answer("Ortga qaytildi.", reply_markup=admin_main_menu)
        else:
            await message.answer("Ortga qaytildi.", reply_markup=main_menu)
    else:
        await message.answer("Son kiriting:")

#
# @dp.message_handler(text="🗓 Buyurtmalar")
# async def history(message: types.Message):
#     await message.answer()