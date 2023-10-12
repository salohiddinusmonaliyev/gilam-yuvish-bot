
from aiogram import types
from aiogram.types import ParseMode

from keyboards.default.keyboards import generate_pagination_keyboard
from loader import dp, db, bot

items_per_page = 3

# @dp.message_handler(text="🗓 Buyurtmalar Tarixi")
# async def history(message: types.Message):
#     global orders
#     items = await db.get_orders(user_id=message.from_user.id)
#     print(len(items))
#     orders = []
#     for i in items:
#         if i["is_completed"]:
#             status = "Topshirildi"
#         else:
#             status = "Topshirilmadi"
#         orders.append(
#             f"Id: {i['id']}, \n"
#             f"Manzil: {i['address']}, \n"
#             f"Buyurtma holati: {status}\n"
#             f"Yetkazib beriladigan sana: {i['delivery_date']}\n\n"
#         )
#     await message.answer(orders)
#


# Command to start pagination
@dp.message_handler(text="🗓 Buyurtmalar Tarixi")
async def start_pagination(message: types.Message):
    global orders
    items = await db.get_orders(user_id=message.from_user.id)
    orders = []
    for i in items:
        if i["is_completed"]:
            status = "Topshirildi ✅"
        else:
            status = "Topshirilmadi ❌"
        orders.append(
            f"Buyurtma raqami: {i['id']} \n"
            f"Manzil: {i['address']} \n"
            f"Buyurtmachi telefon raqami: {i['phone_number']}\n"
        )
    current_page = 1
    total_pages = (len(orders)) // items_per_page
    try:
        await send_page(message.chat.id, current_page, total_pages)
    except:
        await message.answer("Sizning buyurtmalaringiz mavjud emas! Siz bu bot orqali faqat botdan buyurtma bergan buyurtmalaringizni ko'ra olasiz.")


@dp.message_handler(text="🗓 Buyurtmalar")
async def start_pagination(message: types.Message):
    global orders
    items = await db.get_all_orders()
    orders = []
    for i in items:
        service_id = int(i['service_id'])
        service = await db.get_service(service_id)
        orders.append(
            f"Buyurtma raqami: {i['id']} \n"
            f"Manzil: {i['address']} \n"
            f"Buyurtmachi telefon raqami: {i['phone_number']}\n"
        )
    current_page = 1
    total_pages = (len(orders)) // items_per_page
    try:
        await send_page(message.chat.id, current_page, total_pages)
    except:
        await message.answer("Buyurtmalar mavjud emas!")


# Function to send a page of items
async def send_page(chat_id, page, total_pages, message_id=None):
    start_idx = (page - 1) * items_per_page
    end_idx = min(page * items_per_page, len(orders))

    page_items = orders[start_idx:end_idx]

    message_text = "\n".join(page_items)
    markup = generate_pagination_keyboard(page, total_pages)

    if message_id:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=markup,
                                    parse_mode=ParseMode.MARKDOWN)
    else:
        message = await bot.send_message(chat_id, message_text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        return message.message_id


# Callback handler for pagination buttons
@dp.callback_query_handler(lambda c: c.data.startswith('next_page') or c.data.startswith('prev_page'))
async def process_pagination(callback_query: types.CallbackQuery):
    action, current_page = callback_query.data.split(':')
    current_page = int(current_page)

    total_pages = (len(orders) + items_per_page - 1) // items_per_page

    if action == 'next_page':
        current_page += 1
    elif action == 'prev_page':
        current_page -= 1

    await send_page(callback_query.message.chat.id, current_page, total_pages, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)