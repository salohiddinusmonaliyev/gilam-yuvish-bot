from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.keyboards import back, admin_main_menu, main_menu
from loader import dp, db, bot
from states.main_states import *


@dp.message_handler(text="🆔 Nakladnoy raqami orqali ma'lumot olish")
async def invoice(message: types.Message, state: FSMContext):
    await message.answer("Nakladnoy raqamini kiriting: ", reply_markup=back)
    await Invoice.id.set()


@dp.message_handler(state=Invoice.id)
async def give_info(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            info = await db.get_invoice(id=int(message.text))
            if message.from_user.id == int(ADMINS[0]):
                menu = admin_main_menu
            else:
                menu = main_menu
        
            input_file = types.InputFile(f"/home/gilamyu2/tm.gilamyuvishxizmati.uz/gilam_yuvish_bot/gilamyuvish_bot/media/{info['invoice']}.jpg")
            await message.answer_photo(input_file, reply_markup=menu)
        
            await state.finish()
            
        else:
            await message.answer("Nakladnoy raqamini kiriting! \n\nSiz raqam kiritmadingiz!")
    except TypeError:
        await message.answer("Bunday raqamli buyurtma yo'q\nTekshirib qaytadan kiriting:", reply_markup=back)
    if message.text == "🔙 Ortga":
        if message.from_user.id == int(ADMINS[0]):
            await message.answer("Ortga qaytildi.", reply_markup=admin_main_menu)
            await state.finish()

        else:
            await message.answer("Ortga qaytildi.", reply_markup=main_menu)
            await state.finish()

    



#
@dp.message_handler(text="Nakladnoyni yuklash")
async def invoice(message: types.Message):
    await message.answer("Nakladnoy raqamini kiriting.")
    await Image.id.set()


@dp.message_handler(state=Image.id)
async def get_id(message: types.Message):
    try:
        global order_number
        order_number = int(message.text)
        await message.answer("Rasmni yuboring")
        await Image.image.set()
    except:
        await message.answer("Xatolik. Qaytadan kiriting.")



@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=Image.image)
async def image(message: types.Message, state: FSMContext):
    global order_number
    file_id = message.photo[-1].file_id
    local_file_path = f'/home/gilamyu2/tm.gilamyuvishxizmati.uz/gilam_yuvish_bot/gilamyuvish_bot/media/{file_id}.jpg'
    try:
        await db.add_invoice(order_number=order_number, invoice=file_id)
    except:
        await message.answer("Bunday raqamli nakladnoy bor. Agar nakladnoyni yangilamoqchi bo'lsangiz bosh menyudan Nakladnoyni yangilashni bosing.", reply_markup=admin_main_menu)
        await state.finish()
    file_path = await bot.download_file_by_id(file_id, destination=local_file_path)
    print(file_path)
    await message.answer("Fayl qabul qilindi", reply_markup=admin_main_menu)
    await state.finish()
    
    
@dp.message_handler(text="ðŸ”„ Nakladnoyni yangilash")
async def invoice(message: types.Message):
    await message.answer("Nakladnoy raqamini kiriting.")
    
    await Update.id.set()


@dp.message_handler(state=Update.id)
async def get_id(message: types.Message):
    try:
        global order_number
        order_number = int(message.text)
        await message.answer("Rasmni yuboring")
        await Update.image.set()
    except:
        await message.answer("Xatolik. Qaytadan kiriting.")
    


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=Update.image)
async def image(message: types.Message, state: FSMContext):
    global order_number
    file_id = message.photo[-1].file_id
    
    local_file_path = f'/home/gilamyu2/tm.gilamyuvishxizmati.uz/gilam_yuvish_bot/gilamyuvish_bot/media/{file_id}.jpg'
    try:
        file_path = await bot.download_file_by_id(file_id, destination=local_file_path)
        await db.update_invoice(file_id=file_id, id=order_number)
    except:
        await message.answer("Bunday raqamli nakladnoy bor. Agar nakladnoyni yangilamoqchi bo'lsangiz bosh menyudan Nakladnoyni yangilashni bosing.", reply_markup=admin_main_menu)
        await state.finish()
    
    # print(file_path)
    await message.answer("Fayl qabul qilindi", reply_markup=admin_main_menu)
    await state.finish()
    


    
@dp.message_handler(text="❌ Nakladnoyni o'chirish")
async def invoice(message: types.Message):
    await message.answer("O'chirish uchun nakladnoy raqamini kiriting.")
    await Delete.id.set()
    
@dp.message_handler(state=Delete.id)
async def get_id(message: types.Message, state: FSMContext):
    # try:
    global order_numbers
    order_numbers = int(message.text)
    await db.delete_invoice(id=order_numbers)
    await message.answer("Nakladnoy o'chirib yuborildi.")
    await state.finish()
    # except:
        # await message.answer("Xatolik. Qaytadan kiriting.")
    
    
    
    