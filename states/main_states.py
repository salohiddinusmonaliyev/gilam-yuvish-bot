from aiogram.dispatcher.filters.state import State, StatesGroup


class Order(StatesGroup):
    user = State()
    address = State()
    # service = State()
    phone_number_state = State()
    delivery_date = State()
    is_completed = State()

class Complete(StatesGroup):
    id = State()

class Delivered(StatesGroup):
    id = State()

class Invoice(StatesGroup):
    id = State()


class SetPrice(StatesGroup):
    id = State()
    price = State()

class Image(StatesGroup):
    id = State()
    image = State()