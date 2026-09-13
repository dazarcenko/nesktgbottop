import asyncio
import os
import sqlite3

from aiohttp import web
from aiogram import Bot, F, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


TOKEN = os.environ.get("TOKEN", "").strip()
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "").strip()

if not TOKEN:
    raise RuntimeError("TOKEN не найден в Variables")

bot = Bot(token=TOKEN, session=AiohttpSession())
router = Router()

DB = "catalog.db"


# =========================================================
# DATABASE
# =========================================================

def db():
    return sqlite3.connect(DB)


def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            brand_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT DEFAULT '',
            active INTEGER DEFAULT 1
        )
    """)

    con.commit()

    # Демо-данные только при пустой базе
    cur.execute("SELECT COUNT(*) FROM categories")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute(
            "INSERT INTO categories (name) VALUES (?)",
            ("📱 Электроника",)
        )
        category_id = cur.lastrowid

        cur.execute(
            "INSERT INTO brands (category_id, name) VALUES (?, ?)",
            (category_id, "Apple")
        )
        brand_id = cur.lastrowid

        cur.execute("""
            INSERT INTO products
            (category_id, brand_id, name, price, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            category_id,
            brand_id,
            "Пример товара",
            100,
            "Описание товара"
        ))

        con.commit()

    con.close()


# =========================================================
# TELEGRAM
# =========================================================

def main_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="🛒 Каталог",
        callback_data="catalog"
    )

    kb.adjust(1)
    return kb.as_markup()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🛍 Добро пожаловать!\n\n"
        "Выбери действие:",
        reply_markup=main_keyboard()
    )


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    con = db()
    cur = con.cursor()

    cur.execute("""
        SELECT id, name
        FROM categories
        ORDER BY id
    """)

    categories = cur.fetchall()
    con.close()

    kb = InlineKeyboardBuilder()

    for category_id, name in categories:
        kb.button(
            text=name,
            callback_data=f"cat:{category_id}"
        )

    kb.adjust(1)

    await callback.message.edit_text(
        "📂 Выбери категорию:",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("cat:"))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])

    con = db()
    cur = con.cursor()

    cur.execute(
        "SELECT name FROM categories WHERE id=?",
        (category_id,)
    )
    category_name = cur.fetchone()

    cur.execute("""
        SELECT id, name
        FROM brands
        WHERE category_id=?
        ORDER BY id
    """, (category_id,))

    brands = cur.fetchall()

    cur.execute("""
        SELECT id, name, price
        FROM products
        WHERE category_id=?
          AND brand_id IS NULL
          AND active=1
        ORDER BY id
    """, (category_id,))

    products = cur.fetchall()

    con.close()

    if not category_name:
        await callback.answer(
            "Категория не найдена",
            show_alert=True
        )
        return

    kb = InlineKeyboardBuilder()

    for brand_id, name in brands:
        kb.button(
            text=name,
            callback_data=f"brand:{brand_id}"
        )

    for product_id, name, price in products:
        kb.button(
            text=f"{name} — {price:g} ₽",
            callback_data=f"product:{product_id}"
        )

    kb.button(
        text="⬅️ Назад",
        callback_data="catalog"
    )

    kb.adjust(1)

    await callback.message.edit_text(
        f"{category_name[0]}\n\nВыбери товар:",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("brand:"))
async def brand(callback: CallbackQuery):
    brand_id = int(callback.data.split(":")[1])

    con = db()
    cur = con.cursor()

    cur.execute(
        "SELECT name FROM brands WHERE id=?",
        (brand_id,)
    )
    brand_name = cur.fetchone()

    cur.execute("""
        SELECT id, name, price
        FROM products
        WHERE brand_id=?
          AND active=1
        ORDER BY id
    """, (brand_id,))

    products = cur.fetchall()

    cur.execute(
        "SELECT category_id FROM brands WHERE id=?",
        (brand_id,)
    )
    category_id = cur.fetchone()

    con.close()

    if not brand_name or not category_id:
        await callback.answer(
            "Бренд не найден",
            show_alert=True
        )
        return

    kb = InlineKeyboardBuilder()

    for product_id, name, price in products:
        kb.button(
            text=f"{name} — {price:g} ₽",
            callback_data=f"product:{product_id}"
        )

    kb.button(
        text="⬅️ Назад",
        callback_data=f"cat:{category_id[0]}"
    )

    kb.adjust(1)

    await callback.message.edit_text(
        f"{brand_name[0]}\n\nВыбери товар:",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])

    con = db()
    cur = con.cursor()

    cur.execute("""
        SELECT name, price, description
        FROM products
        WHERE id=? AND active=1
    """, (product_id,))

    product_data = cur.fetchone()
    con.close()

    if not product_data:
        await callback.answer(
            "Товар не найден",
            show_alert=True
        )
        return

    name, price, description = product_data

    kb = InlineKeyboardBuilder()

    kb.button(
        text="⬅️ Назад",
        callback_data="catalog"
    )

    await callback.message.edit_text(
        f"🛍 {name}\n\n"
        f"Цена: {price:g} ₽\n\n"
        f"{description}",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


# =========================================================
# WEB ADMIN
# =========================================================

async def admin_page(request):
    password = request.query.get("password", "")

    if password != ADMIN_PASSWORD:
        return web.Response(
            text="Неверный пароль",
            status=403
        )

    con = db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            products.id,
            categories.name,
            COALESCE(brands.name, ''),
            products.name,
            products.price,
            products.active
        FROM products
        JOIN categories
            ON categories.id = products.category_id
        LEFT JOIN brands
            ON brands.id = products.brand_id
        ORDER BY products.id DESC
    """)

    products = cur.fetchall()
    con.close()

    rows = ""

    for item in products:
        product_id, category, brand, name, price, active = item

        rows += f"""
        <tr>
            <td>{product_id}</td>
            <td>{category}</td>
            <td>{brand}</td>
            <td>{name}</td>
            <td>{price:g}</td>
            <td>{"Включён" if active else "Скрыт"}</td>
            <td>
                <a href="/admin/delete/{product_id}?password={password}">
                    🗑 Удалить
                </a>
            </td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Админка</title>
        <style>
            body {{
                font-family: Arial;
                max-width: 1100px;
                margin: 40px auto;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
            }}

            th {{
                background: #eee;
            }}

            input {{
                padding: 8px;
                margin: 4px;
            }}

            button {{
                padding: 8px 14px;
            }}
        </style>
    </head>

    <body>

    <h1>🛠 Админка</h1>

    <h2>➕ Добавить товар</h2>

    <form method="POST"
          action="/admin/add?password={password}">

        <input name="category"
               placeholder="Категория"
               required>

        <input name="brand"
               placeholder="Бренд">

        <input name="name"
               placeholder="Название товара"
               required>

        <input name="price"
               type="number"
               step="0.01"
               placeholder="Цена"
               required>

        <input name="description"
               placeholder="Описание">

        <button type="submit">
            Добавить
        </button>

    </form>

    <h2>📦 Товары</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Категория</th>
            <th>Бренд</th>
            <th>Название</th>
            <th>Цена</th>
            <th>Статус</th>
            <th></th>
        </tr>

        {rows}

    </table>

    </body>
    </html>
    """

    return web.Response(
        text=html,
        content_type="text/html"
    )


async def admin_add(request):
    password = request.query.get("password", "")

    if password != ADMIN_PASSWORD:
        return web.Response(
            text="Неверный пароль",
            status=403
        )

    data = await request.post()

    category_name = data.get("category", "").strip()
    brand_name = data.get("brand", "").strip()
    product_name = data.get("name", "").strip()
    description = data.get("description", "").strip()
    price = float(data.get("price", 0))

    con = db()
    cur = con.cursor()

    cur.execute(
        "SELECT id FROM categories WHERE name=?",
        (category_name,)
    )

    category = cur.fetchone()

    if category:
        category_id = category[0]
    else:
        cur.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category_name,)
        )
        category_id = cur.lastrowid

    brand_id = None

    if brand_name:
        cur.execute("""
            SELECT id
            FROM brands
            WHERE category_id=? AND name=?
        """, (category_id, brand_name))

        brand = cur.fetchone()

        if brand:
            brand_id = brand[0]
        else:
            cur.execute("""
                INSERT INTO brands
                (category_id, name)
                VALUES (?, ?)
            """, (category_id, brand_name))

            brand_id = cur.lastrowid

    cur.execute("""
        INSERT INTO products
        (category_id, brand_id, name, price, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        category_id,
        brand_id,
        product_name,
        price,
        description
    ))

    con.commit()
    con.close()

    raise web.HTTPFound(
        f"/admin?password={password}"
    )


async def admin_delete(request):
    password = request.query.get("password", "")

    if password != ADMIN_PASSWORD:
        return web.Response(
            text="Неверный пароль",
            status=403
        )

    product_id = int(request.match_info["product_id"])

    con = db()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )

    con.commit()
    con.close()

    raise web.HTTPFound(
        f"/admin?password={password}"
    )


# =========================================================
# WEB SERVER
# =========================================================

async def start_web():
    app = web.Application()

    app.router.add_get(
        "/admin",
        admin_page
    )

    app.router.add_post(
        "/admin/add",
        admin_add
    )

    app.router.add_get(
        "/admin/delete/{product_id}",
        admin_delete
    )

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", "8080"))

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(f"Админка запущена на порту {port}")

    return runner


# =========================================================
# START
# =========================================================

async def main():
    init_db()

    dp = Dispatcher()
    dp.include_router(router)

    await start_web()

    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
