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

# Активные чаты (ADMIN_ID -> user_id)
active_chats = {}

# КОРЗИНЫ ПОЛЬЗОВАТЕЛЕЙ
# Формат: {user_id: {"product_id_str": {"name": "...", "price": X, "qty": Y}}}
carts = {}

# =========================================================
# ТОВАРЫ (Оставил без изменений)
# =========================================================

categories = {
    "phones": {
        "name": "🧪 Жижа",
        "brands": {
            "podonki": {
                "name": "🧪 PODONKI",
                "variants": {
                    "podonki_blood": {
                        "name": "🧪 & BLOOD",
                        "products": {
                            "podonki_1": {"name": "PODONKI & BLOOD 60мг — Лесные ягоды", "price": 10, "description": ""},
                            "podonki_blood_2": {"name": "PODONKI & BLOOD 60мг — Малиновый лимонад", "price": 10, "description": ""}
                        }
                    },
                    "podonki_malasian_arcade": {
                        "name": "🧪 MALASIAN ARCADE",
                        "products": {
                            "pma_2": {"name": "PODONKI MALASIAN ARCADE 50мг — Вишневый энергетик", "price": 15, "description": ""},
                            "pma_4": {"name": "PODONKI MALASIAN ARCADE 50мг — Малина черника", "price": 15, "description": ""},
                            "pma_5": {"name": "PODONKI MALASIAN ARCADE 50мг — Лимонад голубика", "price": 15, "description": ""},
                            "pma_6": {"name": "PODONKI MALASIAN ARCADE 50мг — Маунти дью яблоко", "price": 15, "description": ""},
                            "pma_7": {"name": "PODONKI MALASIAN ARCADE 50мг — Цитрусовый микс", "price": 15, "description": ""},
                            "pma_8": {"name": "PODONKI MALASIAN ARCADE 50мг — Явболо вишня", "price": 15, "description": ""}
                        }
                    },
                    "podonki_malasian_new": {
                        "name": "🧪 MALASIAN NEW",
                        "products": {
                            "pmn_1": {"name": "PODONKI MALASIAN NEW 50мг — Киви яблоко", "price": 15, "description": ""},
                            "pmn_2": {"name": "PODONKI MALASIAN NEW 50мг — Розовый лимонад", "price": 15, "description": ""},
                            "pmn_3": {"name": "PODONKI MALASIAN NEW 50мг — Черника смородина анис", "price": 15, "description": ""}
                        }
                    },
                    "podonki_alfa_vape": {
                        "name": "🧪 & ALFA VAPE",
                        "products": {
                            "podonki_4": {"name": "PODONKI & ALFA VAPE 50мг — Дыня", "price": 15, "description": ""}
                        }
                    },
                    "podonki_alfa_ice": {
                        "name": "🧪 ALFA ICE",
                        "products": {
                            "podonki_alfa_ice_1": {"name": "PODONKI ALFA ICE 50мг — Садовые ягоды", "price": 15, "description": ""}
                        }
                    }
                }
            },
            "rick_and_morty": {
                "name": "🧪 RICK & MORTY",
                "variants": {
                    "bad_trip": {
                        "name": "🧪 BAD TRIP",
                        "products": {
                            "rm_1": {"name": "R&M BAD TRIP 50мг — Клубника земляника", "price": 16, "description": ""},
                            "rm_2": {"name": "R&M BAD TRIP 50мг — Садовые ягоды", "price": 16, "description": ""},
                            "rm_3": {"name": "RICK & MORTY bad trip 50 — Дыня", "price": 16, "description": ""}
                        }
                    }
                }
            },
            "oggo": {
                "name": "🧪 OGGO",
                "variants": {
                    "oggo_max": {
                        "name": "🧪 MAX",
                        "products": {
                            "oggo_max_1": {"name": "OGGO MAX 50мг — Ананасовый сок", "price": 17, "description": ""},
                            "oggo_max_2": {"name": "OGGO MAX 50мг — Манго банан", "price": 17, "description": ""},
                            "oggo_max_3": {"name": "OGGO MAX 50мг — Сладкий грейпфрут", "price": 17, "description": ""},
                            "oggo_max_4": {"name": "OGGO MAX 50мг — Сладкое киви", "price": 17, "description": ""},
                            "oggo_max_5": {"name": "OGGO MAX 50мг — Энергетик с малиной", "price": 17, "description": ""},
                            "oggo_max_6": {"name": "OGGO MAX 50мг — Ягодный мармелад", "price": 17, "description": ""},
                            "oggo_max_7": {"name": "OGGO MAX 50мг — Сладкая маракуя", "price": 17, "description": ""}
                        }
                    },
                    "oggo_cherry": {
                        "name": "🧪 CHERRY",
                        "products": {
                            "oggo_cherry_1": {"name": "OGGO CHERRY 50мг — Вишня виноград", "price": 18, "description": ""},
                            "oggo_cherry_3": {"name": "OGGO CHERRY 50мг — Вишневый мармелад", "price": 18, "description": ""}
                        }
                    }
                }
            },
            "dogswill": {
                "name": "🧪 DogSwill",
                "variants": {
                    "dogswill": {
                        "name": "🧪 DogSwill",
                        "products": {
                            "dogswill_1": {"name": "DogSwill 70мг — Персиковый лимонад", "price": 17, "description": ""},
                            "dogswill_2": {"name": "DogSwill 70мг — Малиновый лимонад", "price": 17, "description": ""},
                            "dogswill_3": {"name": "DogSwill 70мг — Земляничный фреш", "price": 17, "description": ""},
                            "dogswill_4": {"name": "DogSwill 70мг — Черника голубика", "price": 17, "description": ""},
                            "dogswill_5": {"name": "DogSwill 70мг — Ягодный редбулл", "price": 17, "description": ""}
                        }
                    }
                }
            }
        }
    },
    "headphones": {
        "name": "⚡ Под-Системы",
        "brands": {
            "VAPORESSO": {
                "name": "🟩 VAPORESSO",
                "products": {
                    "headphones_2": {"name": "XROS 5 NANO (Orange Leatherette)", "price": 70, "description": ""}
                }
            }
        }
    },
    "other": {
        "name": "⚙️ Испарители",
        "brands": {
            "VAPORESSO": {
                "name": "⚙️ VAPORESSO",
                "products": {
                    "xros_corex_3": {"name": "Xros Corex 3.0, 0.4 ОМ", "price": 12, "description": ""}
                }
            },
            "GEEKVAPE": {
                "name": "⚙️ GEEKVAPE",
                "products": {
                    "aegis_coil_boost": {"name": "Aegis Сoil 0.2 ОМ 50-58 Ватт", "price": 13, "description": ""}
                }
            }
        }
    }
}


# =========================================================
# ВРЕМЯ И ТОЧКИ САМОВЫВОЗА
# =========================================================

times = ["13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
pickup_places = ["📍 Московский 64А"]


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
    keyboard.button(text="🛍 Каталог", callback_data="catalog")
    keyboard.button(text="🛒 Корзина", callback_data="cart")
    keyboard.adjust(1)
    return keyboard.as_markup()


# =========================================================
# START
# =========================================================

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛍 Добро пожаловать в наш магазин!\n\n"
        "Мы рады приветствовать вас! Здесь вы найдете огромное множество "
        "разновидностей товаров на любой вкус.\n\n"
        "Желаем приятных покупок! 🛒\n"
        "👇 Используйте кнопки ниже.",
        reply_markup=main_keyboard()
    )


# =========================================================
# КАТАЛОГ И КАТЕГОРИИ
# =========================================================

@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    for category_id, category in categories.items():
        keyboard.button(text=category["name"], callback_data=f"category:{category_id}")
    keyboard.button(text="🛒 Корзина", callback_data="cart")
    keyboard.button(text="🏠 Главное меню", callback_data="home")
    keyboard.adjust(1)

    await callback.message.edit_text("📂 Выбери категорию:", reply_markup=keyboard.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("category:"))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data.split(":", 1)[1]
    category = categories.get(category_id)
    if not category:
        return await callback.answer("Категория не найдена", show_alert=True)

    keyboard = InlineKeyboardBuilder()
    if "brands" in category:
        for brand_id, brand in category["brands"].items():
            keyboard.button(text=brand["name"], callback_data=f"brand:{category_id}:{brand_id}")
    elif "products" in category:
        for product_id, product in category["products"].items():
            keyboard.button(text=f"{product['name']} — {product['price']}Р", callback_data=f"product:{category_id}:{product_id}")

    keyboard.button(text="Назад", callback_data="catalog")
    keyboard.adjust(1)

    text = f"{category['name']}\n\nВыбери производителя:" if "brands" in category else f"{category['name']}\n\nВыбери товар:"
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("brand:"))
async def brand_selected(callback: CallbackQuery):
    _, category_id, brand_id = callback.data.split(":")
    category = categories.get(category_id)
    brand = category.get("brands", {}).get(brand_id)
    if not brand:
        return await callback.answer("Производитель не найден", show_alert=True)

    keyboard = InlineKeyboardBuilder()
    if "variants" in brand:
        for variant_id, variant in brand["variants"].items():
            keyboard.button(text=variant["name"], callback_data=f"variant:{category_id}:{brand_id}:{variant_id}")
        keyboard.button(text="Назад", callback_data=f"category:{category_id}")
        keyboard.adjust(1)
        await callback.message.edit_text(f"{brand['name']}\n\nВыбери разновидность:", reply_markup=keyboard.as_markup())
        return

    for product_id, product in brand.get("products", {}).items():
        flavor = product["name"].split("—", 1)[1].strip() if "—" in product["name"] else product["name"]
        keyboard.button(text=f"{flavor} — {product['price']}Р", callback_data=f"product:{category_id}:{brand_id}:{product_id}")

    keyboard.button(text="Назад", callback_data=f"category:{category_id}")
    keyboard.adjust(1)
    await callback.message.edit_text(f"{brand['name']}\n\nВыбери вкус:", reply_markup=keyboard.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("variant:"))
async def variant_selected(callback: CallbackQuery):
    _, category_id, brand_id, variant_id = callback.data.split(":")
    variant = categories.get(category_id, {}).get("brands", {}).get(brand_id, {}).get("variants", {}).get(variant_id)
    if not variant:
        return await callback.answer("Разновидность не найдена", show_alert=True)

    keyboard = InlineKeyboardBuilder()
    for product_id, product in variant.get("products", {}).items():
        flavor = product["name"].split("—", 1)[1].strip() if "—" in product["name"] else product["name"]
        keyboard.button(text=f"{flavor} — {product['price']}Р", callback_data=f"product:{category_id}:{brand_id}:{variant_id}:{product_id}")

    keyboard.button(text="Назад", callback_data=f"brand:{category_id}:{brand_id}")
    keyboard.adjust(1)
    await callback.message.edit_text(f"{variant['name']}\n\nВыбери вкус:", reply_markup=keyboard.as_markup())
    await callback.answer()


def get_product(category_id, product_id, brand_id=None, variant_id=None):
    category = categories.get(category_id)
    if not category: return None
    if brand_id:
        brand = category.get("brands", {}).get(brand_id)
        if not brand: return None
        if variant_id:
            return brand.get("variants", {}).get(variant_id, {}).get("products", {}).get(product_id)
        return brand.get("products", {}).get(product_id)
    return category.get("products", {}).get(product_id)


# =========================================================
# КАРТОЧКА ТОВАРА
# =========================================================

@router.callback_query(F.data.startswith("product:"))
async def product_selected(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) == 5: _, category_id, brand_id, variant_id, product_id = parts
    elif len(parts) == 4:
        _, category_id, brand_id, product_id = parts
        variant_id = None
    else:
        _, category_id, product_id = parts
        brand_id, variant_id = None, None

    product = get_product(category_id, product_id, brand_id, variant_id)
    if not product:
        return await callback.answer("Товар не найден", show_alert=True)

    # Меняем префикс для добавления в корзину
    add_cart_cb = callback.data.replace("product:", "add_cart:")
    
    if brand_id and variant_id: back_cb = f"variant:{category_id}:{brand_id}:{variant_id}"
    elif brand_id: back_cb = f"brand:{category_id}:{brand_id}"
    else: back_cb = f"category:{category_id}"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="➕ В корзину", callback_data=add_cart_cb)
    keyboard.button(text="🛒 Перейти в корзину", callback_data="cart")
    keyboard.button(text="Назад", callback_data=back_cb)
    keyboard.adjust(1)

    description = product.get("description", "")
    await callback.message.edit_text(
        f"🏷 {product['name']}\n\n"
        f"💰 Цена: {product['price']}Р\n\n{description}",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


# =========================================================
# КОРЗИНА: ДОБАВЛЕНИЕ И ПРОСМОТР
# =========================================================

@router.callback_query(F.data.startswith("add_cart:"))
async def add_to_cart(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) == 5: _, category_id, brand_id, variant_id, product_id = parts
    elif len(parts) == 4:
        _, category_id, brand_id, product_id = parts
        variant_id = None
    else:
        _, category_id, product_id = parts
        brand_id, variant_id = None, None

    product = get_product(category_id, product_id, brand_id, variant_id)
    if not product:
        return await callback.answer("Ошибка при добавлении", show_alert=True)

    user_id = callback.from_user.id
    if user_id not in carts:
        carts[user_id] = {}

    # Уникальный ключ товара (просто объединяем id из callback)
    prod_key = ":".join(parts[1:])
    
    if prod_key in carts[user_id]:
        carts[user_id][prod_key]['qty'] += 1
    else:
        carts[user_id][prod_key] = {
            'name': product['name'],
            'price': product['price'],
            'qty': 1
        }

    await callback.answer(f"✅ Добавлено: {product['name']}", show_alert=False)


@router.callback_query(F.data == "cart")
async def view_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_cart = carts.get(user_id, {})

    if not user_cart:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="🛍 В каталог", callback_data="catalog")
        await callback.message.edit_text("🛒 Ваша корзина пуста.", reply_markup=keyboard.as_markup())
        return

    text = "🛒 Ваша корзина:\n\n"
    total = 0
    for i, (key, item) in enumerate(user_cart.items(), 1):
        cost = item['price'] * item['qty']
        total += cost
        text += f"{i}. {item['name']} (x{item['qty']}) — {cost}Р\n"

    text += f"\n💰 Итого к оплате: {total}Р"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Оформить заказ", callback_data="checkout")
    keyboard.button(text="🗑 Очистить корзину", callback_data="clear_cart")
    keyboard.button(text="🛍 Вернуться в каталог", callback_data="catalog")
    keyboard.adjust(1)

    await callback.message.edit_text(text, reply_markup=keyboard.as_markup())
    await callback.answer()


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    carts.pop(callback.from_user.id, None)
    await callback.answer("🗑 Корзина очищена!")
    await view_cart(callback)


# =========================================================
# ОФОРМЛЕНИЕ ЗАКАЗА (ПО ВСЕЙ КОРЗИНЕ)
# =========================================================

@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not carts.get(user_id):
        return await callback.answer("Корзина пуста!", show_alert=True)

    await state.set_state(OrderState.choosing_time)

    keyboard = InlineKeyboardBuilder()
    for time in times:
        keyboard.button(text=time, callback_data=f"time:{time}")
    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(2)

    await callback.message.edit_text("🕐 Выбери желаемое время получения:", reply_markup=keyboard.as_markup())
    await callback.answer()


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

    await callback.message.edit_text(f"Время: {time}\n\nВыбери способ получения:", reply_markup=keyboard.as_markup())
    await callback.answer()


# =========================================================
# САМОВЫВОЗ
# =========================================================

@router.callback_query(OrderState.choosing_delivery, F.data == "pickup")
async def pickup_selected(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    for index, place in enumerate(pickup_places):
        keyboard.button(text=place, callback_data=f"pickup_place:{index}")
    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(1)

    await callback.message.edit_text("📍 Выбери место самовывоза:", reply_markup=keyboard.as_markup())
    await callback.answer()


@router.callback_query(OrderState.choosing_delivery, F.data.startswith("pickup_place:"))
async def pickup_place_selected(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    place = pickup_places[index]

    await state.update_data(delivery=False, delivery_price=0, address=place)
    
    user_id = callback.from_user.id
    user_cart = carts.get(user_id, {})
    
    items_total = sum(item['price'] * item['qty'] for item in user_cart.values())
    cart_text = "\n".join([f"- {v['name']} (x{v['qty']})" for v in user_cart.values()])
    
    data = await state.get_data()

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Подтвердить заказ", callback_data="confirm_order")
    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(1)

    await callback.message.edit_text(
        "📝 Проверь заказ:\n\n"
        f"📦 Товары:\n{cart_text}\n\n"
        f"💰 К оплате: {items_total}Р\n"
        f"🕐 Время: {data['time']}\n"
        f"📍 Самовывоз: {place}\n\n"
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
        "Напиши адрес доставки одним сообщением.\n"
        "Например: ул. Ленина, 10, кв. 25"
    )
    await callback.answer()


@router.message(OrderState.entering_address)
async def address_received(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("Пожалуйста, отправь адрес текстом.")

    await state.update_data(address=message.text.strip())
    data = await state.get_data()
    
    user_id = message.from_user.id
    user_cart = carts.get(user_id, {})
    if not user_cart:
        return await message.answer("Корзина пуста.")

    items_total = sum(item['price'] * item['qty'] for item in user_cart.values())
    delivery_price = data.get("delivery_price", 3)
    total_price = items_total + delivery_price
    cart_text = "\n".join([f"- {v['name']} (x{v['qty']})" for v in user_cart.values()])

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Подтвердить заказ", callback_data="confirm_order")
    keyboard.button(text="Отмена", callback_data="cancel")
    keyboard.adjust(1)

    await message.answer(
        "📝 Проверь заказ:\n\n"
        f"📦 Товары:\n{cart_text}\n\n"
        f"💰 Цена товаров: {items_total}Р\n"
        f"🚚 Доставка: +{delivery_price}Р\n"
        f"💵 ИТОГО: {total_price}Р\n"
        f"🕐 Время: {data['time']}\n"
        f"📍 Адрес: {data['address']}\n\n"
        "Всё верно?",
        reply_markup=keyboard.as_markup()
    )


# =========================================================
# ПОДТВЕРЖДЕНИЕ ЗАКАЗА
# =========================================================

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = callback.from_user
    user_cart = carts.get(user.id, {})

    if not user_cart:
        return await callback.answer("Корзина пуста.", show_alert=True)

    items_total = sum(item['price'] * item['qty'] for item in user_cart.values())
    delivery_price = data.get("delivery_price", 0)
    total_price = items_total + delivery_price
    address = data.get("address", "Не указан")
    
    cart_text = "\n".join([f"➖ {v['name']} (x{v['qty']}) — {v['price'] * v['qty']}Р" for v in user_cart.values()])
    username = f"@{user.username}" if user.username else "нет username"

    admin_message = (
        "🛍 НОВЫЙ ЗАКАЗ\n\n"
        f"👤 Пользователь: {user.full_name}\n"
        f"📱 Username: {username}\n"
        f"🆔 ID: {user.id}\n\n"
        f"📦 ТОВАРЫ:\n{cart_text}\n\n"
        f"💰 Сумма товаров: {items_total}Р\n"
        f"🚚 Доставка: {delivery_price}Р\n"
        f"💵 ИТОГО: {total_price}Р\n"
        f"🕐 Время: {data['time']}\n"
        f"📍 Место/адрес: {address}"
    )

    chat_keyboard = InlineKeyboardBuilder()
    chat_keyboard.button(text="💬 Написать покупателю", callback_data=f"chat:{user.id}")

    await bot.send_message(ADMIN_ID, admin_message, reply_markup=chat_keyboard.as_markup())

    # Очищаем корзину и состояние после успешного оформления
    carts.pop(user.id, None)
    await state.clear()

    await callback.message.edit_text(
        "✅ Ваш заказ успешно принят!\n\n"
        "Ожидайте, администратор свяжется с вами или соберёт заказ к указанному времени.\n"
        "Спасибо за покупку!",
        reply_markup=main_keyboard()
    )
    await callback.answer()


# =========================================================
# АДМИН И ЧАТ (Оставил без изменений)
# =========================================================

@router.callback_query(F.data.startswith("chat:"))
async def start_admin_chat(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return await callback.answer("Нет доступа", show_alert=True)
    user_id = int(callback.data.split(":", 1)[1])
    active_chats[ADMIN_ID] = user_id

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ Завершить диалог", callback_data="chat_stop")
    await callback.message.answer(
        f"💬 Чат с покупателем {user_id} активирован.\n"
        "Пиши сюда сообщения — они будут отправляться покупателю.",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer("Чат открыт")


@router.callback_query(F.data == "chat_stop")
async def stop_admin_chat(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return await callback.answer("Нет доступа", show_alert=True)
    active_chats.pop(ADMIN_ID, None)
    await callback.message.edit_text("❌ Диалог завершён.")
    await callback.answer()


@router.message(F.from_user.id == ADMIN_ID, F.text)
async def admin_message_to_customer(message: Message):
    user_id = active_chats.get(ADMIN_ID)
    if not user_id: return
    try:
        await bot.send_message(user_id, f"💬 Сообщение от магазина:\n\n{message.text}")
        await message.answer("✅ Отправлено.")
    except Exception:
        await message.answer("❌ Ошибка отправки.")


@router.message(F.from_user.id != ADMIN_ID, F.text)
async def customer_message_to_admin(message: Message):
    if active_chats.get(ADMIN_ID) != message.from_user.id: return
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"
    await bot.send_message(
        ADMIN_ID,
        f"💬 От покупателя (ID: {user.id}, {username}):\n\n{message.text}"
    )


# =========================================================
# ОТМЕНА И ГЛАВНОЕ МЕНЮ
# =========================================================

@router.callback_query(F.data == "cancel")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Оформление отменено.\nМожешь вернуться в корзину или в меню.", reply_markup=main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "home")
async def home(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("🏠 Главное меню\n\nВыбери действие:", reply_markup=main_keyboard())
    await callback.answer()


# =========================================================
# ЗАПУСК
# =========================================================

async def main():
    print("🚀 Бот запущен!")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")
