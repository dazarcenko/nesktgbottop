import asyncio
import os

from aiogram import Bot, F, Dispatcher
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

bot = Bot(
    token=TOKEN,
    session=AiohttpSession()
)

router = Router()

# Активные чаты:
# ADMIN_ID -> user_id
active_chats = {}


# =========================================================
# ТОВАРЫ
# =========================================================

categories = {

    # =====================================================
    # ЖИЖА
    # =====================================================

    "phones": {
        "name": "🧪 Жижа",

        "brands": {

            # =================================================
            # PODONKI
            # =================================================

            "podonki": {
                "name": "🧪 PODONKI",

                "variants": {

                    # -------------------------------------------------
                    # PODONKI & BLOOD
                    # -------------------------------------------------

                    "podonki_blood": {
                        "name": "🧪 & BLOOD",

                        "products": {

                            "podonki_1": {
                                "name": "PODONKI & BLOOD 60мг — Лесные ягоды",
                                "price": 10,
                                "description": ""
                            },
                            "podonki_blood_2": {
                                "name": "PODONKI & BLOOD 60мг — Малиновый лимонад",
                                "price": 10,
                                "description": ""
                            }
                        }
                    },

                    # -------------------------------------------------
                    # PODONKI MALASIAN ARCADE
                    # -------------------------------------------------

                    "podonki_malasian_arcade": {
                        "name": "🧪 MALASIAN ARCADE",

                        "products": {
                            "pma_2": {
                                "name": "PODONKI MALASIAN ARCADE 50мг — Вишневый энергетик",
                                "price": 15,
                                "description": ""
                            },

                            "pma_4": {
                                "name": "PODONKI MALASIAN ARCADE 50мг — Малина черника",
                                "price": 15,
                                "description": ""
                            },

                            "pma_5": {
                                "name": "PODONKI MALASIAN ARCADE 50мг — Лимонад голубика",
                                "price": 15,
                                "description": ""
                            },

                            "pma_6": {
                                "name": "PODONKI MALASIAN ARCADE 50мг — Маунти дью яблоко",
                                "price": 15,
                                "description": ""
                            },

                            "pma_7": {
                                "name": "PODONKI MALASIAN ARCADE 50мг — Цитрусовый микс",
                                "price": 15,
                                "description": ""
                            },

                            "pma_8": {
                                "name": "PODONKI MALASIAN ARCADE 50мг — Явболо вишня",
                                "price": 15,
                                "description": ""
                            }
                        }
                    },

                    # -------------------------------------------------
                    # PODONKI MALASIAN NEW
                    # -------------------------------------------------

                    "podonki_malasian_new": {
                        "name": "🧪 MALASIAN NEW",

                        "products": {

                            "pmn_1": {
                                "name": "PODONKI MALASIAN NEW 50мг — Киви яблоко",
                                "price": 15,
                                "description": ""
                            },

                            "pmn_2": {
                                "name": "PODONKI MALASIAN NEW 50мг — Розовый лимонад",
                                "price": 15,
                                "description": ""
                            },

                            "pmn_3": {
                                "name": "PODONKI MALASIAN NEW 50мг — Черника смородина анис",
                                "price": 15,
                                "description": ""
                            }
                        }
                    },

                    # -------------------------------------------------
                    # PODONKI & ALFA VAPE
                    # -------------------------------------------------

                    "podonki_alfa_vape": {
                        "name": "🧪 & ALFA VAPE",

                        "products": {

                            "podonki_4": {
                                "name": "PODONKI & ALFA VAPE 50мг — Дыня",
                                "price": 15,
                                "description": ""
                            }
                        }
                    },

                    # -------------------------------------------------
                    # PODONKI ALFA ICE — из ОСТАТКОВ
                    # -------------------------------------------------

                    "podonki_alfa_ice": {
                        "name": "🧪 ALFA ICE",

                        "products": {

                            "podonki_alfa_ice_1": {
                                "name": "PODONKI ALFA ICE 50мг — Садовые ягоды",
                                "price": 15,
                                "description": ""
                            }
                        }
                    }
                }
            },

            # =================================================
            # RICK & MORTY
            # =================================================

            "rick_and_morty": {
                "name": "🧪 RICK & MORTY",

                "variants": {

                    "bad_trip": {
                        "name": "🧪 BAD TRIP",

                        "products": {

                            "rm_1": {
                                "name": "R&M BAD TRIP 50мг — Клубника земляника",
                                "price": 16,
                                "description": ""
                            },

                            "rm_2": {
                                "name": "R&M BAD TRIP 50мг — Садовые ягоды",
                                "price": 16,
                                "description": ""
                            },

                            "rm_3": {
                                "name": "RICK & MORTY bad trip 50 — Дыня",
                                "price": 16,
                                "description": ""
                            }
                        }
                    }
                }
            },

            # =================================================
            # OGGO
            # =================================================

            "oggo": {
                "name": "🧪 OGGO",

                "variants": {

                    "oggo_max": {
                        "name": "🧪 MAX",

                        "products": {

                            "oggo_max_1": {
                                "name": "OGGO MAX 50мг — Ананасовый сок",
                                "price": 17,
                                "description": ""
                            },

                            "oggo_max_2": {
                                "name": "OGGO MAX 50мг — Манго банан",
                                "price": 17,
                                "description": ""
                            },

                            "oggo_max_3": {
                                "name": "OGGO MAX 50мг — Сладкий грейпфрут",
                                "price": 17,
                                "description": ""
                            },

                            "oggo_max_4": {
                                "name": "OGGO MAX 50мг — Сладкое киви",
                                "price": 17,
                                "description": ""
                            },

                            "oggo_max_5": {
                                "name": "OGGO MAX 50мг — Энергетик с малиной",
                                "price": 17,
                                "description": ""
                            },

                            "oggo_max_6": {
                                "name": "OGGO MAX 50мг — Ягодный мармелад",
                                "price": 17,
                                "description": ""
                            },

                            "oggo_max_7": {
                                "name": "OGGO MAX 50мг — Сладкая маракуя",
                                "price": 17,
                                "description": ""
                            }
                        }
                    },

                    "oggo_cherry": {
                        "name": "🧪 CHERRY",

                        "products": {

                            "oggo_cherry_1": {
                                "name": "OGGO CHERRY 50мг — Вишня виноград",
                                "price": 18,
                                "description": ""
                            },

                            "oggo_cherry_2": {
                                "name": "OGGO CHERRY 50мг — Кислый вишневый лимонад",
                                "price": 18,
                                "description": ""
                            },

                            "oggo_cherry_3": {
                                "name": "OGGO CHERRY 50мг — Вишневый мармелад",
                                "price": 18,
                                "description": ""
                            }
                        }
                    }
                }
            },

            # =================================================
            # DOGSWILL
            # =================================================

            "dogswill": {
                "name": "🧪 DogSwill",

                "variants": {

                    "dogswill": {
                        "name": "🧪 DogSwill",

                        "products": {

                            "dogswill_1": {
                                "name": "DogSwill 70мг — Персиковый лимонад",
                                "price": 17,
                                "description": ""
                            },

                            "dogswill_2": {
                                "name": "DogSwill 70мг — Малиновый лимонад",
                                "price": 17,
                                "description": ""
                            },

                            "dogswill_3": {
                                "name": "DogSwill 70мг — Земляничный фреш",
                                "price": 17,
                                "description": ""
                            },

                            "dogswill_4": {
                                "name": "DogSwill 70мг — Черника голубика",
                                "price": 17,
                                "description": ""
                            },

                            "dogswill_5": {
                                "name": "DogSwill 70мг — Ягодный редбулл",
                                "price": 17,
                                "description": ""
                            }
                        }
                    }
                }
            }
        }
    },

    # =====================================================
    # ПОД-СИСТЕМЫ
    # =====================================================

    "headphones": {
        "name": "⚡ Под-Системы",

        "brands": {

            "VAPORESSO": {
                "name": "🟩 VAPORESSO",

                "products": {
                    
                    "headphones_2": {
                        "name": "XROS 5 NANO (Orange Leatherette)",
                        "price": 70,
                        "description": ""
                    }
                }
            }
        }
    },


    # =====================================================
    # ИСПАРИТЕЛИ
    # =====================================================

    "other": {
        "name": "⚙️ Испарители",

        "brands": {

            "VAPORESSO": {
                "name": "⚙️ VAPORESSO",

                "products": {

                    "xros_corex_3": {
                        "name": "Xros Corex 3.0, 0.4 ОМ",
                        "price": 15,
                        "description": ""
                    }
                }
            },

            "GEEKVAPE": {
                "name": "⚙️ GEEKVAPE",

                "products": {

                    "aegis_coil_boost": {
                        "name": "Aegis Сoil 0.2 ОМ 50-58 Ватт",
                        "price": 13,
                        "description": ""
                    }
                }
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
# ГЛАВНАЯ КЛАВИАТУРА
# =========================================================

def main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="🛒 Заказать",
        callback_data="catalog"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


# =========================================================
# START
# =========================================================

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        🛍 Добро пожаловать в наш магазин!

Мы рады приветствовать вас! Здесь вы найдете огромное множество разновидностей товаров на любой вкус — мы постарались собрать для вас всё самое лучшее. 🔥

Желаем приятных покупок! 🛒
👇 Используйте кнопки меню ниже, чтобы открыть каталог и сделать заказ.
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
# КАТЕГОРИЯ
# =========================================================

@router.callback_query(F.data.startswith("category:"))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data.split(":", 1)[1]
    category = categories.get(category_id)

    if not category:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    keyboard = InlineKeyboardBuilder()

    if "brands" in category:
        for brand_id, brand in category["brands"].items():
            keyboard.button(
                text=brand["name"],
                callback_data=f"brand:{category_id}:{brand_id}"
            )
    elif "products" in category:
        for product_id, product in category["products"].items():
            keyboard.button(
                text=f"{product['name']} — {product['price']}Р",
                callback_data=f"product:{category_id}:{product_id}"
            )

    keyboard.button(
        text="Назад",
        callback_data="catalog"
    )
    keyboard.adjust(1)

    if "brands" in category:
        text = f"{category['name']}\n\nВыбери производителя:"
    else:
        text = f"{category['name']}\n\nВыбери товар:"

    await callback.message.edit_text(text, reply_markup=keyboard.as_markup())
    await callback.answer()


# =========================================================
# БРЕНД
# =========================================================

@router.callback_query(F.data.startswith("brand:"))
async def brand_selected(callback: CallbackQuery):
    _, category_id, brand_id = callback.data.split(":")

    category = categories.get(category_id)
    if not category:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    brand = category.get("brands", {}).get(brand_id)
    if not brand:
        await callback.answer("Производитель не найден", show_alert=True)
        return

    keyboard = InlineKeyboardBuilder()

    # Новая структура: производитель -> разновидность -> вкус
    if "variants" in brand:
        for variant_id, variant in brand["variants"].items():
            keyboard.button(
                text=variant["name"],
                callback_data=f"variant:{category_id}:{brand_id}:{variant_id}"
            )

        keyboard.button(
            text="Назад",
            callback_data=f"category:{category_id}"
        )
        keyboard.adjust(1)

        await callback.message.edit_text(
            f"{brand['name']}\n\nВыбери разновидность:",
            reply_markup=keyboard.as_markup()
        )
        await callback.answer()
        return

    # Старая структура: производитель -> товар
    for product_id, product in brand.get("products", {}).items():
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
        f"{brand['name']}\n\nВыбери вкус:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# РАЗНОВИДНОСТЬ ТОВАРА
# =========================================================

@router.callback_query(F.data.startswith("variant:"))
async def variant_selected(callback: CallbackQuery):
    _, category_id, brand_id, variant_id = callback.data.split(":")

    category = categories.get(category_id)
    if not category:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    brand = category.get("brands", {}).get(brand_id)
    if not brand:
        await callback.answer("Производитель не найден", show_alert=True)
        return

    variant = brand.get("variants", {}).get(variant_id)
    if not variant:
        await callback.answer("Разновидность не найдена", show_alert=True)
        return

    keyboard = InlineKeyboardBuilder()

    for product_id, product in variant.get("products", {}).items():
        product_name = product["name"]
        if "—" in product_name:
            flavor = product_name.split("—", 1)[1].strip()
        else:
            flavor = product_name

        keyboard.button(
            text=f"{flavor} — {product['price']}Р",
            callback_data=f"product:{category_id}:{brand_id}:{variant_id}:{product_id}"
        )

    keyboard.button(
        text="Назад",
        callback_data=f"brand:{category_id}:{brand_id}"
    )
    keyboard.adjust(1)

    await callback.message.edit_text(
        f"{variant['name']}\n\nВыбери вкус:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# ПОЛУЧЕНИЕ ТОВАРА
# =========================================================

def get_product(category_id, product_id, brand_id=None, variant_id=None):
    category = categories.get(category_id)
    if not category:
        return None

    if brand_id:
        brand = category.get("brands", {}).get(brand_id)
        if not brand:
            return None

        if variant_id:
            variant = brand.get("variants", {}).get(variant_id)
            if not variant:
                return None
            return variant.get("products", {}).get(product_id)

        return brand.get("products", {}).get(product_id)

    return category.get("products", {}).get(product_id)


# =========================================================
# ТОВАР — КАРТОЧКА
# =========================================================

@router.callback_query(F.data.startswith("product:"))
async def product_selected(callback: CallbackQuery):
    parts = callback.data.split(":")

    # Новая структура: product:category:brand:variant:product
    if len(parts) == 5:
        _, category_id, brand_id, variant_id, product_id = parts
    # Старая структура: product:category:brand:product
    elif len(parts) == 4:
        _, category_id, brand_id, product_id = parts
        variant_id = None
    # Старая структура без бренда
    else:
        _, category_id, product_id = parts
        brand_id = None
        variant_id = None

    product = get_product(category_id, product_id, brand_id, variant_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    keyboard = InlineKeyboardBuilder()

    if brand_id and variant_id:
        select_callback = f"select:{category_id}:{brand_id}:{variant_id}:{product_id}"
        back_callback = f"variant:{category_id}:{brand_id}:{variant_id}"
    elif brand_id:
        select_callback = f"select:{category_id}:{brand_id}:{product_id}"
        back_callback = f"brand:{category_id}:{brand_id}"
    else:
        select_callback = f"select:{category_id}:{product_id}"
        back_callback = f"category:{category_id}"

    keyboard.button(text="Выбрать", callback_data=select_callback)
    keyboard.button(text="Назад", callback_data=back_callback)
    keyboard.adjust(1)

    description = product.get("description", "")

    await callback.message.edit_text(
        f"{product['name']}\n\n"
        f"Цена: {product['price']}Р\n\n"
        f"{description}",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# ВЫБОР ТОВАРА
# =========================================================

@router.callback_query(F.data.startswith("select:"))
async def select_product(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")

    if len(parts) == 5:
        _, category_id, brand_id, variant_id, product_id = parts
    elif len(parts) == 4:
        _, category_id, brand_id, product_id = parts
        variant_id = None
    else:
        _, category_id, product_id = parts
        brand_id = None
        variant_id = None

    product = get_product(category_id, product_id, brand_id, variant_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    await state.update_data(
        category_id=category_id,
        brand_id=brand_id,
        variant_id=variant_id,
        product_id=product_id
    )
    await state.set_state(OrderState.choosing_time)

    keyboard = InlineKeyboardBuilder()

    for time in times:
        keyboard.button(text=time, callback_data=f"time:{time}")

    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(2)

    await callback.message.edit_text(
        f"{product['name']}\n"
        f"{product['price']}Р\n\n"
        "Выбери время:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# ВЫБОР ВРЕМЕНИ
# =========================================================

@router.callback_query(OrderState.choosing_time, F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split(":", 1)[1]
    await state.update_data(time=time)
    await state.set_state(OrderState.choosing_delivery)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Самовывоз", callback_data="pickup")
    keyboard.button(text="Доставка (+3Р)", callback_data="delivery")
    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(1)

    await callback.message.edit_text(
        f"Время: {time}\n\nВыбери способ получения:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# САМОВЫВОЗ
# =========================================================

@router.callback_query(OrderState.choosing_delivery, F.data == "pickup")
async def pickup_selected(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()

    for index, place in enumerate(pickup_places):
        keyboard.button(text=place, callback_data=f"pickup_place:{index}")

    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(1)

    await callback.message.edit_text(
        "Выбери место самовывоза:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# ПОЛУЧЕНИЕ ТОВАРА ИЗ STATE
# =========================================================

def get_product_from_state(data):
    return get_product(
        data["category_id"],
        data["product_id"],
        data.get("brand_id"),
        data.get("variant_id")
    )


# =========================================================
# ВЫБОР ТОЧКИ
# =========================================================

@router.callback_query(OrderState.choosing_delivery, F.data.startswith("pickup_place:"))
async def pickup_place_selected(callback: CallbackQuery, state: FSMContext):
    try:
        index = int(callback.data.split(":")[1])
    except (ValueError, IndexError):
        await callback.answer("Ошибка выбора места", show_alert=True)
        return

    if index >= len(pickup_places):
        await callback.answer("Место не найдено", show_alert=True)
        return

    place = pickup_places[index]

    await state.update_data(
        delivery=False,
        delivery_price=0,
        address=place
    )

    data = await state.get_data()
    product = get_product_from_state(data)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    total_price = product["price"]

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Подтвердить", callback_data="confirm_order")
    keyboard.button(text="Отмена", callback_data="cancel")
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

@router.callback_query(OrderState.choosing_delivery, F.data == "delivery")
async def delivery_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery=True, delivery_price=3)
    await state.set_state(OrderState.entering_address)

    await callback.message.edit_text(
        "🚚 Доставка\n\n"
        "Напиши адрес доставки одним сообщением.\n\n"
        "Например:\n"
        "ул. Ленина, 10, кв. 25"
    )
    await callback.answer()


# =========================================================
# АДРЕС
# =========================================================

@router.message(OrderState.entering_address)
async def address_received(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправь адрес текстом.")
        return

    address = message.text.strip()
    if not address:
        await message.answer("Адрес не может быть пустым.")
        return

    await state.update_data(address=address)

    data = await state.get_data()
    product = get_product_from_state(data)

    if not product:
        await message.answer("Ошибка: товар не найден.")
        return

    delivery_price = data.get("delivery_price", 3)
    total_price = product["price"] + delivery_price

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Подтвердить", callback_data="confirm_order")
    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(2)

    await message.answer(
        "Проверь заказ:\n\n"
        f"Товар: {product['name']}\n"
        f"Цена товара: {product['price']}Р\n"
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
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        await callback.answer("Заказ не найден.", show_alert=True)
        return

    product = get_product_from_state(data)
    if not product:
        await callback.answer("Товар не найден.", show_alert=True)
        return

    delivery_price = data.get("delivery_price", 0)
    total_price = product["price"] + delivery_price
    address = data.get("address", "Не указан")

    user = callback.from_user
    username = f"@{user.username}" if user.username else "нет username"

    admin_message = (
        "🛍 НОВЫЙ ЗАКАЗ\n\n"
        f"👤 Пользователь: {user.full_name}\n"
        f"📱 Username: {username}\n"
        f"🆔 ID: {user.id}\n\n"
        f"📦 Товар: {product['name']}\n"
        f"💰 Цена товара: {product['price']}Р\n"
        f"🚚 Доставка: {delivery_price}Р\n"
        f"💵 ИТОГО: {total_price}Р\n"
        f"🕐 Время: {data['time']}\n"
        f"📍 Место/адрес: {address}"
    )

    chat_keyboard = InlineKeyboardBuilder()
    chat_keyboard.button(text="💬 Написать покупателю", callback_data=f"chat:{user.id}")

    await bot.send_message(
        ADMIN_ID,
        admin_message,
        reply_markup=chat_keyboard.as_markup()
    )

    await state.clear()
    await callback.message.edit_text(
        "✅ Заказ принят!\n\n"
        f"📦 Товар: {product['name']}\n"
        f"💵 Итого: {total_price}Р\n"
        f"🕐 Время: {data['time']}\n"
        f"📍 {address}\n\n"
        "Информация отправлена администратору."
    )
    await callback.answer()


# =========================================================
# АДМИН — ОТКРЫТЬ ЧАТ
# =========================================================

@router.callback_query(F.data.startswith("chat:"))
async def start_admin_chat(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    try:
        user_id = int(callback.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await callback.answer("Ошибка ID пользователя", show_alert=True)
        return

    active_chats[ADMIN_ID] = user_id

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ Завершить диалог", callback_data="chat_stop")

    await callback.message.answer(
        f"💬 Чат с покупателем {user_id} активирован.\n\n"
        "Пиши сюда сообщения — они будут отправляться покупателю.\n"
        "Ответы покупателя будут приходить сюда.\n\n"
        "Когда закончишь, нажми «❌ Завершить диалог».",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer("Чат открыт")


# =========================================================
# ЗАКРЫТЬ ЧАТ
# =========================================================

@router.callback_query(F.data == "chat_stop")
async def stop_admin_chat(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    active_chats.pop(ADMIN_ID, None)
    await callback.message.edit_text("❌ Диалог завершён.")
    await callback.answer("Чат завершён")


# =========================================================
# АДМИН → ПОКУПАТЕЛЬ
# =========================================================

@router.message(F.from_user.id == ADMIN_ID, F.text)
async def admin_message_to_customer(message: Message):
    user_id = active_chats.get(ADMIN_ID)
    if not user_id:
        return

    try:
        await bot.send_message(
            user_id,
            "💬 Сообщение от администратора:\n\n"
            f"{message.text}"
        )
        await message.answer("✅ Сообщение отправлено.")
    except Exception as error:
        print("Ошибка отправки покупателю:", error)
        await message.answer(
            "❌ Не удалось отправить сообщение.\n"
            "Возможно, покупатель заблокировал бота."
        )


# =========================================================
# ПОКУПАТЕЛЬ → АДМИН
# =========================================================

@router.message(F.from_user.id != ADMIN_ID, F.text)
async def customer_message_to_admin(message: Message):
    user_id = active_chats.get(ADMIN_ID)
    if user_id != message.from_user.id:
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"

    await bot.send_message(
        ADMIN_ID,
        "💬 Сообщение от покупателя\n\n"
        f"Имя: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: {user.id}\n\n"
        f"{message.text}"
    )


# =========================================================
# ОТМЕНА
# =========================================================

@router.callback_query(F.data == "cancel")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ Заказ отменён.\n\nМожешь начать заново.",
        reply_markup=main_keyboard()
    )
    await callback.answer()


# =========================================================
# ГЛАВНОЕ МЕНЮ
# =========================================================

@router.callback_query(F.data == "home")
async def home(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🏠 Главное меню\n\nВыбери действие:",
        reply_markup=main_keyboard()
    )
    await callback.answer()


# =========================================================
# ЗАПУСК
# =========================================================

async def main():
    print("🚀 Бот запущен!")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")
