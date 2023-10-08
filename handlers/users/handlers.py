from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from geopy import Nominatim

from data import config
from data.config import ADMINS
from keyboards.default.keyboards import services_keyboard, main_menu, address_key, add_second_order, phone_number_key, \
    admin_main_menu, back
from loader import dp, db, bot
from states.main_states import Order


def get_location_from_coordinates(latitude, longitude):
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="myGeocoder")

    # Create a string with the coordinates
    location_str = f"{latitude}, {longitude}"

    try:
        # Perform the reverse geocoding
        location = geolocator.reverse(location_str, exactly_one=True)
        return location.address
    except Exception as e:
        return str(e)


@dp.message_handler(text="ℹ️ Biz haqimizda")
async def about(message: types.Message):
    # if message.from_user.id == ADMINS[0]:
    #     main_menu = admin_main_menu
    latitude = 40.39127277952883
    longitude = 71.78640595125687

    # Create a location object
    location = types.Location(latitude=latitude, longitude=longitude)

    # Send the location
    # await bot.send_location(message.chat.id, location.latitude, location.longitude)
    # order = await db.add_order(user_id=message.from_user.id, is_completed=False, delivery_date=datetime.today().date(),)
    text = ("""Nafis chistka hizmat turlar va narx navo turlari\n\n
Gilam olib ketish💰 12 000 so'mdan 💰14 000 so'mgacha \n
️Joyda tozalash (ya'ni uyingizni o'zida) 💰15 000 so'mdan\n
️Mebel mestasi 💰 60 000 so'mdan \n
️Ugalok mestasi 💰50 000 so'mdan \n
️Stular 💰20 000 so'mdan💰 35 000 so'mgacha\n
Parda 💰18 000 so'mdan \n
️Burschatka 💰13 000 so'mdan\n 
️Kafel💰 15 000 so'mdan\n
️Sokl 💰20 000 so'mdan \n
Matras 1 kishilik 💰180 000 so'm 2 kishilik 💰220 000 so'mgacha"""
            "\n\n<b>Murojat uchun:</b>"
            "\n\n📞 +998919942525"
            "\n📞 +998339922525"
            "\n📞 +998339552525")
    await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text="🛍 Buyurtma Berish")
async def order(message: types.Message):
    # order = await db.add_order(user_id=message.from_user.id, is_completed=False, delivery_date=datetime.today().date(),)
    # await message.answer("Buyurtma berish uchun ba'zi ma'lumotlar kerak bo'ladi.", reply_markup=back)
    text = "Buyurtma berish uchun manzilni kiriting:"
    await message.answer(text, reply_markup=address_key)
    await Order.address.set()


@dp.message_handler(state=Order.address, content_types=types.ContentType.LOCATION)
async def get_address(message: types.Message, state: FSMContext):
    global address
    address = (message.location)
    address = get_location_from_coordinates(address.latitude, address.longitude)
    # print(addressss)
    user = await db.select_user(telegram_id=message.from_user.id)
    await Order.service.set()
    markup = await services_keyboard()
    # await message.answer("Manzil kiritildi.", reply_markup=back)
    await message.answer("Xizmat turini tanlang:\n(narx 1kv.m uchun so'mda)", reply_markup=markup)


@dp.callback_query_handler(state=Order.service)
async def get_service(callback: CallbackQuery, state: FSMContext):
    global service
    global user
    service = await db.get_service(callback.data)
    await callback.message.edit_text(f"{service[0]['name']} yuvish ximatini tanladizgiz\n{service[0]['description']}")
    # await callback.message.answer("Yana buyurtma qo'shasizmi?", reply_markup=add_second_order)
    await callback.message.answer("Telefon raqamingizni kiriting:", reply_markup=phone_number_key)
    user = await db.select_user(telegram_id=callback.from_user.id)
    await Order.next()


@dp.message_handler(state=Order.phone_number_state,content_types=types.ContentType.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.contact and message.contact.phone_number:
        global phone_number
        phone_number = message.contact.phone_number
        await message.answer(f"Telefon raqam qabul qilindi")
        await message.answer("Yana buyurtma qo'shasizmi?", reply_markup=add_second_order)
        await state.finish()

@dp.message_handler(text="🔚 Buyurtmani yakunlash")
async def end_order(message: types.Message, state: FSMContext):
    # if message.from_user.id == ADMINS[0]:
        # main_menu = admin_main_menu
    global service
    global address
    global user
    global phone_number
    text = "Buyurtma yakunlandi tez orada siz bilan operator bo'glanadi"
    await message.answer(text, reply_markup=main_menu)
    order = await db.add_order(user_id=int(user['id']), address=address, service_id=int(service[0]['id']),
                               phone_number=str(phone_number),
                               is_completed=False, price=0, delivered=False, supplier_id=None)
    await db.update_count(int(user['id']))
    service_id = int(order['service_id'])
    service_id = await db.get_service(service_id)
    user = await db.select_user(id=int(order['user_id']))

    await bot.send_message(chat_id=config.ADMINS[0], text=f"<b>Yangi buyurtma</b>\n\nId: {order['id']} \n"
                         f"<b>Manzil:</b> {order['address']} \n"
                         f"<b>Xizmat turi:</b> {service_id[0]['name']}\n"
                         f"<b>Buyurtmachi telefon raqami:</b> {order['phone_number']}\n"
                            )
    await state.finish()

@dp.message_handler(text="➕ Buyurtma qo'shish")
async def second_order(message: types.Message, state: FSMContext):
    global service
    global address
    global user
    global phone_number

    text = "Manzilni kirirting: "
    await message.answer(text, reply_markup=address_key)
    order = await db.add_order(user_id=user['id'], address=address, service_id=int(service[0]['id']), phone_number=phone_number,
                               is_completed=False, price=0, delivered=False)
    await db.update_count(int(user['id']))
    service_id = int(order['service_id'])
    service_id = await db.get_service(service_id)
    user = await db.select_user(id=int(order['user_id']))
    await bot.send_message(chat_id=config.ADMINS[0], text=f"<b>Buyurtma raqami:</b> {order['id']} \n"
                                                          f"<b>Manzil:</b> {order['address']} \n"
                                                          f"<b>Xizmat turi:</b> {service_id[0]['name']}\n"
                                                          f"<b>Buyurtmachi telefon raqami:</b> {order['phone_number']}\n"
                                                          )
    await Order.address.set()

@dp.message_handler(text="📃 Xizmat turlari")
async def services(message: types.Message, state: FSMContext):
    await message.answer("""Nafis chistka hizmat turlar va narx navo turlari (narx 1 kv.m uchun)\n\n
Gilam olib ketish: 12 000 so'mdan-14 000 so'mgacha \n
️Joyda tozalash (ya'ni uyingizni o'zida): 15 000 so'mdan\n
️Mebel mestasi: 60 000 so'mdan \n
️Ugalok mestasi: 50 000 so'mdan \n
️Stular: 20 000 so'mdan 35 000 so'mgacha\n
Parda: 18 000 so'mdan \n
️Burschatka: 13 000 so'mdan\n 
️Kafel: 15 000 so'mdan\n
️Sokl: 20 000 so'mdan \n
Matras 1 kishilik: 180 000 so'm, 2 kishilik: 220 000 so'mgacha\n
Ko'rpacha: 70 000 so'mdan""", reply_markup=main_menu)