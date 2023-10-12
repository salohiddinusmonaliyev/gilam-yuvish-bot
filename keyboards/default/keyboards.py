from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from loader import db, dp
import logging

async def services_keyboard():
    menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    services = await db.get_services()
    for i in services:
        menu.insert(
            InlineKeyboardButton(text=f"{i['name']} - {i['price']}", callback_data=i['id'])
        )
    return menu

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
invoice = KeyboardButton("🆔 Nakladnoy raqami orqali ma'lumot olish")
order = KeyboardButton("🛍 Buyurtma Berish")
history = KeyboardButton("🗓 Buyurtmalar Tarixi")
about_button = KeyboardButton("ℹ️ Biz haqimizda")
services = KeyboardButton("📃 Xizmat turlari")
main_menu.add(invoice)
main_menu.add(order, history)
main_menu.add(services, about_button)


admin_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
invoice = KeyboardButton("🆔 Nakladnoy raqami orqali ma'lumot olish")
setprice = KeyboardButton("💲 Narx belgilash")
image = KeyboardButton("Nakladnoyni yuklash")
history = KeyboardButton("🗓 Buyurtmalar")
completed = KeyboardButton("✔️ Buyurtma tugatildi")
update = KeyboardButton("❌ Nakladnoyni o'chirish")
mode = KeyboardButton("↔️ Mijoz rejimiga o'tish")
admin_main_menu.add(invoice)
admin_main_menu.add(setprice, completed)
admin_main_menu.add(history)
admin_main_menu.add(image, update)

driver_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
receive_goods = KeyboardButton("✔️ Buyurtmmalarni qabul qildim")
delivered = KeyboardButton("✅ Buyurtma yetkazib berildi")
driver_main_menu.add(delivered, receive_goods)

yes_no = ReplyKeyboardMarkup(resize_keyboard=True)
yes = KeyboardButton("Ha, yetkazib berildi")
no = KeyboardButton("Yo'q, kelmadi")
yes_no.add(yes, no)

address_key = ReplyKeyboardMarkup(resize_keyboard=True)
location = KeyboardButton("Manzilni ulashish", request_location=True)
# back_btn = KeyboardButton("🔙 Ortga")
address_key.add(location)
# address_key.add(back_btn)


add_second_order = ReplyKeyboardMarkup(resize_keyboard=True)
button4 = KeyboardButton("➕ Buyurtma qo'shish")
button5 = KeyboardButton("🔚 Buyurtmani yakunlash")
add_second_order.add(button4, button5)


def generate_pagination_keyboard(page, total_pages):
    keyboard = []
    row = []
    if page > 1:
        row.append(InlineKeyboardButton('⬅️', callback_data=f'prev_page:{page}'))
    if page < total_pages:
        row.append(InlineKeyboardButton('➡️', callback_data=f'next_page:{page}'))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

phone_number_key = ReplyKeyboardMarkup(resize_keyboard=True)
phone_number = KeyboardButton("📤 Telefon raqamni ulashish", request_contact=True)
phone_number_key.add(phone_number)
# phone_number_key.add(back_btn)

back = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("🔙 Ortga")]
    ]
)

