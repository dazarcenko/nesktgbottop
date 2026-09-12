import asyncio
import os
from aiogram import Bot, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


# =========================================================
# НАСТРОЙКИ
# =========================================================



TOKEN = os.environ.get("TOKEN", "").strip()

if not TOKEN:
    raise RuntimeError("TOKEN не найден в Variables")
ADMIN_ID = 1067205524

bot = Bot(token=TOKEN, session=AiohttpSession())
router = Router()


# =========================================================
# ТОВАРЫ
# =========================================================

categories = {
    "phones": {
        "name": "🧪 Жижа",
        "brands": {
            "podonki": {
                "name": "🧪 PODONKI",
                "products": {
                    "podonki_1": {
                        "name": "PODONKI & BLOOD 60мг — лесные ягоды",
                        "price": 15,
                        "description": ""
                    },
                    "podonki_2": {
                        "name": "PODONKI & BLOOD 60мг — малиновый лимонад",
                        "price": 15,
                        "description": ""
                    },
                    "podonki_3": {
                        "name": "PODONKI & BLOOD 60мг — черника и малина",
                        "price": 15,
                        "description": ""
                    },
                    "podonki_4": {
                        "name": "PODONKI & BLOOD 60мг — чёрная смородина",
                        "price": 15,
                        "description": ""
                    },
                    "podonki_5": {
                        "name": "PODONKI & BLOOD 60мг — ягодный энергетик",
                        "price": 15,
                        "description": ""
                    },
                    "podonki_6": {
                        "name": "PODONKI PODGON 50мг — малина хвоя",
                        "price": 15,
                        "description": ""
                    },
                    "podonki_7": {
                        "name": "PODONKI & ALFA VAPE 50мг — дыня",
                        "price": 15,
                        "description": ""
                    }
                }
            },
            "rick_and_morty": {
                "name": "🧪 RICK & MORTY",
                "products": {
                    "rm_1": {
                        "name": "R&M BAD DRIP 50мг — клубника земляника",
                        "price": 16,
                        "description": ""
                    },
                    "rm_2": {
                        "name": "R&M BAD DRIP 50мг — садовые ягоды",
                        "price": 16,
                        "description": ""
                    }
                }
            }
        }
    },

    "headphones": {
        "name": "⚡ Под-Системы",
        "products": {
            "headphones_1": {
                "name": "VAPORESSO XROS 5 NANO orange leatherette",
                "price": 95,
                "description": ""
            },
            "headphones_2": {
                "name": "VAPORESSO XROS 6 MINI titanium black",
                "price": 60,
                "description": ""
            }
        }
    },

    "other": {
        "name": "📦 Другое",
        "products": {
            "other_1": {
                "name": "тут пока ничего нет...",
                "price": 0,
                "description": ""
            }
        }
    }
}


# =========================================================
# ВРЕМЯ
# =========================================================

times = [
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
]


# =========================================================
# ТОЧКИ САМОВЫВОЗА
# =========================================================

pickup_places = [
    "📍 Московский 64А",
]


# =========================================================
# СОСТОЯНИЯ
# =========================================================

class OrderState(StatesGroup):
    choosing_time = State()
    choosing_delivery = State()
    entering_address = State()


# =========================================================
# КЛАВИАТУРА ГЛАВНОГО МЕНЮ
# =========================================================

def main_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="🛒 Заказать",
        callback_data="catalog"
    )

    return keyboard.as_markup()


# =========================================================
# START
# =========================================================

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🛍 Добро пожаловать в магазин!\n\n"
        "Выбери действие:",
        reply_markup=main_keyboard()
    )


# =========================================================
# КАТАЛОГ
# =========================================================

@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    for category_id, category in categories.items():
        keyboard.button(
            text=category["name"],
            callback_data=f"category:{category_id}"
        )

    keyboard.button(
        text="🏠 Главное меню",
        callback_data="home"
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        "📂 Выбери категорию:",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# КАТЕГОРИЯ — ТОВАРЫ
# =========================================================

@router.callback_query(F.data.startswith("category:"))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data.split(":")[1]

    category = categories.get(category_id)

    if not category:
        await callback.answer(
            "Категория не найдена",
            show_alert=True
        )
        return

    keyboard = InlineKeyboardBuilder()

    # Для жижи сначала показываем бренды,
    # а уже после выбора бренда — вкусы.
    if "brands" in category:
        for brand_id, brand in category["brands"].items():
            keyboard.button(
                text=brand["name"],
                callback_data=f"brand:{category_id}:{brand_id}"
            )

    # Для обычных категорий оставляем старое поведение.
    elif "products" in category:
        for product_id, product in category["products"].items():
            keyboard.button(
                text=f"{product['name']} {product['price']}Р",
                callback_data=f"product:{category_id}:{product_id}"
            )

    keyboard.button(
        text="Назад",
        callback_data="catalog"
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        f"{category['name']}\n\n"
        + ("Выбери производителя:" if "brands" in category else "Выбери товар:"),
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# БРЕНД ЖИЖИ — ВЫБОР ВКУСА
# =========================================================

@router.callback_query(F.data.startswith("brand:"))
async def brand_selected(callback: CallbackQuery):
    _, category_id, brand_id = callback.data.split(":")

    category = categories.get(category_id)

    if not category or "brands" not in category:
        await callback.answer(
            "Категория не найдена",
            show_alert=True
        )
        return

    brand = category["brands"].get(brand_id)

    if not brand:
        await callback.answer(
            "Производитель не найден",
            show_alert=True
        )
        return

    keyboard = InlineKeyboardBuilder()

    for product_id, product in brand["products"].items():
        # На этой странице показываем именно вкус,
        # без повторения названия бренда.
        product_name = product["name"]
        if "—" in product_name:
            flavor = product_name.split("—", 1)[1].strip()
        else:
            flavor = product_name

        keyboard.button(
            text=f"{flavor} — {product['price']}Р",
            callback_data=f"product:{category_id}:{brand_id}:{product_id}"
        )

    keyboard.button(
        text="Назад",
        callback_data=f"category:{category_id}"
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        f"{brand['name']}\n\n"
        "Выбери вкус:",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# ТОВАР — КАРТОЧКА
# =========================================================

@router.callback_query(F.data.startswith("product:"))
async def product_selected(callback: CallbackQuery):
    parts = callback.data.split(":")

    if len(parts) == 4:
        _, category_id, brand_id, product_id = parts
    else:
        _, category_id, product_id = parts
        brand_id = None

    category = categories.get(category_id)

    if not category:
        await callback.answer(
            "Категория не найдена",
            show_alert=True
        )
        return

    if brand_id:
        brand = category.get("brands", {}).get(brand_id)
        if not brand:
            await callback.answer(
                "Производитель не найден",
                show_alert=True
            )
            return
        product = brand["products"].get(product_id)
    else:
        product = category.get("products", {}).get(product_id)

    if not product:
        await callback.answer(
            "Товар не найден",
            show_alert=True
        )
        return

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="Выбрать",
        callback_data=(
            f"select:{category_id}:{brand_id}:{product_id}"
            if brand_id
            else f"select:{category_id}:{product_id}"
        )
    )

    keyboard.button(
        text="Назад",
        callback_data=(
            f"brand:{category_id}:{brand_id}"
            if brand_id
            else f"category:{category_id}"
        )
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        f"{product['name']}\n\n"
        f"Цена: {product['price']}Р\n\n"
        f"{product['description']}",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# ВЫБРАЛИ ТОВАР — ВЫБОР ВРЕМЕНИ
# =========================================================

@router.callback_query(F.data.startswith("select:"))
async def select_product(
    callback: CallbackQuery,
    state: FSMContext
):
    parts = callback.data.split(":")

    if len(parts) == 4:
        _, category_id, brand_id, product_id = parts
    else:
        _, category_id, product_id = parts
        brand_id = None

    category = categories.get(category_id)

    if not category:
        await callback.answer(
            "Категория не найдена",
            show_alert=True
        )
        return

    if brand_id:
        brand = category.get("brands", {}).get(brand_id)
        if not brand:
            await callback.answer(
                "Производитель не найден",
                show_alert=True
            )
            return
        product = brand["products"].get(product_id)
    else:
        product = category.get("products", {}).get(product_id)

    if not product:
        await callback.answer(
            "Товар не найден",
            show_alert=True
        )
        return

    await state.update_data(
        category_id=category_id,
        brand_id=brand_id,
        product_id=product_id
    )

    await state.set_state(OrderState.choosing_time)

    keyboard = InlineKeyboardBuilder()

    for time in times:
        keyboard.button(
            text=time,
            callback_data=f"time:{time}"
        )

    keyboard.button(
        text="Отмена",
        callback_data="cancel"
    )

    keyboard.adjust(2)

    await callback.message.edit_text(
        f"{product['name']}\n"
        f"{product['price']}Р\n\n"
        "Выбери время:",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# ВЫБРАЛИ ВРЕМЯ — ДОСТАВКА ИЛИ САМОВЫВОЗ
# =========================================================

@router.callback_query(
    OrderState.choosing_time,
    F.data.startswith("time:")
)
async def choose_time(
    callback: CallbackQuery,
    state: FSMContext
):
    time = callback.data.split(":", 1)[1]

    await state.update_data(time=time)

    await state.set_state(OrderState.choosing_delivery)

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="Самовывоз",
        callback_data="pickup"
    )

    keyboard.button(
        text="Доставка (+3Р)",
        callback_data="delivery"
    )

    keyboard.button(
        text="Отмена",
        callback_data="cancel"
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        f"Время: {time}\n\n"
        "Выбери способ получения:",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# САМОВЫВОЗ — ВЫБОР ТОЧКИ
# =========================================================

@router.callback_query(
    OrderState.choosing_delivery,
    F.data == "pickup"
)
async def pickup_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    keyboard = InlineKeyboardBuilder()

    for index, place in enumerate(pickup_places):
        keyboard.button(
            text=place,
            callback_data=f"pickup_place:{index}"
        )

    keyboard.button(
        text="Отмена",
        callback_data="cancel"
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        "Выбери место самовывоза:",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# ВЫБРАЛИ ТОЧКУ САМОВЫВОЗА
# =========================================================

def get_product_from_state(data):
    category = categories[data["category_id"]]
    brand_id = data.get("brand_id")

    if brand_id:
        brand = category["brands"][brand_id]
        return brand["products"][data["product_id"]]

    return category["products"][data["product_id"]]


@router.callback_query(
    OrderState.choosing_delivery,
    F.data.startswith("pickup_place:")
)
async def pickup_place_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    index = int(callback.data.split(":")[1])

    if index >= len(pickup_places):
        await callback.answer(
            "Место не найдено",
            show_alert=True
        )
        return

    place = pickup_places[index]

    await state.update_data(
        delivery=False,
        delivery_price=0,
        address=place
    )

    data = await state.get_data()

    product = get_product_from_state(data)

    total_price = product["price"]

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="Подтвердить",
        callback_data="confirm_order"
    )

    keyboard.button(
        text="Отмена",
        callback_data="cancel"
    )

    keyboard.adjust(2)

    await callback.message.edit_text(
        "Проверь заказ:\n\n"
        f"Товар: {product['name']}\n"
        f"Цена: {total_price}Р\n"
        f"Время: {data['time']}\n"
        f"Самовывоз: {place}\n\n"
        "Всё верно?",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()


# =========================================================
# ДОСТАВКА
# =========================================================

@router.callback_query(
    OrderState.choosing_delivery,
    F.data == "delivery"
)
async def delivery_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.update_data(
        delivery=True,
        delivery_price=3
    )

    await state.set_state(OrderState.entering_address)

    await callback.message.edit_text(
        "Доставка\n\n"
        "Напиши адрес доставки одним сообщением.\n\n"
        "Например:\n"
        "ул. Ленина, 10, кв. 25"
    )

    await callback.answer()


# =========================================================
# ПОЛУЧИЛИ АДРЕС
# =========================================================

@router.message(OrderState.entering_address)
async def address_received(
    message: Message,
    state: FSMContext
):
    if not message.text:
        await message.answer(
            "Пожалуйста, отправь адрес текстом."
        )
        return

    address = message.text.strip()

    await state.update_data(
        address=address
    )

    data = await state.get_data()

    product = get_product_from_state(data)

    delivery_price = 3
    total_price = product["price"] + delivery_price

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="Подтвердить",
        callback_data="confirm_order"
    )

    keyboard.button(
        text="Отмена",
        callback_data="cancel"
    )

    keyboard.adjust(2)

    await message.answer(
        "Проверь заказ:\n\n"
        f"Товар: {product['name']}\n"
        f"Товар: {product['price']}Р\n"
        f"Доставка: +{delivery_price}Р\n"
        f"Итого: {total_price}Р\n"
        f"Время: {data['time']}\n"
        f"Адрес: {address}\n\n"
        "Всё верно?",
        reply_markup=keyboard.as_markup()
    )


# =========================================================
# ПОДТВЕРЖДЕНИЕ ЗАКАЗА
# =========================================================

@router.callback_query(F.data == "confirm_order")
async def confirm_order(
    callback: CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()

    if not data:
        await callback.answer(
            "Заказ не найден.",
            show_alert=True
        )
        return

    product = get_product_from_state(data)

    delivery_price = data.get("delivery_price", 0)
    total_price = product["price"] + delivery_price
    address = data.get("address", "Не указан")

    user = callback.from_user

    username = (
        f"@{user.username}"
        if user.username
        else "нет username"
    )

    admin_message = (
        "НОВЫЙ ЗАКАЗ\n\n"
        f"Пользователь: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: {user.id}\n\n"
        f"Товар: {product['name']}\n"
        f"Цена товара: {product['price']}Р\n"
        f"Доставка: {delivery_price}Р\n"
        f"ИТОГО: {total_price}Р\n"
        f"Время: {data['time']}\n"
        f"Место/адрес: {address}"
    )

    await bot.send_message(
        ADMIN_ID,
        admin_message
    )

    await state.clear()

    await callback.message.edit_text(
        "Заказ принят!\n\n"
        f"Товар: {product['name']}\n"
        f"Итого: {total_price}Р\n"
        f"Время: {data['time']}\n"
        f"{address}\n\n"
        "Информация отправлена администратору."
    )

    await callback.answer()


# =========================================================
# ОТМЕНА
# =========================================================

@router.callback_query(F.data == "cancel")
async def cancel_order(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "Заказ отменён.\n\n"
        "Можешь начать заново.",
        reply_markup=main_keyboard()
    )

    await callback.answer()


# =========================================================
# ГЛАВНОЕ МЕНЮ
# =========================================================

@router.callback_query(F.data == "home")
async def home(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "Главное меню\n\n"
        "Выбери действие:",
        reply_markup=main_keyboard()
    )

    await callback.answer()


# =========================================================
# ЗАПУСК
# =========================================================

async def main():
    print("Бот запущен!")

    from aiogram import Dispatcher

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
