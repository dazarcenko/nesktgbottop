import sqlite3

DB_NAME = "catalog.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            brand_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 0,
            description TEXT DEFAULT '',
            available INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (brand_id) REFERENCES brands(id)
        )
    """)

    conn.commit()
    conn.close()


def get_categories():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM categories ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def add_category(name):
    conn = get_connection()
    conn.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()


def delete_category(category_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM products WHERE category_id = ?",
        (category_id,)
    )

    conn.execute(
        "DELETE FROM brands WHERE category_id = ?",
        (category_id,)
    )

    conn.execute(
        "DELETE FROM categories WHERE id = ?",
        (category_id,)
    )

    conn.commit()
    conn.close()


def get_brands(category_id):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM brands
        WHERE category_id = ?
        ORDER BY id DESC
        """,
        (category_id,)
    ).fetchall()

    conn.close()
    return rows


def add_brand(category_id, name):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO brands (category_id, name)
        VALUES (?, ?)
        """,
        (category_id, name)
    )

    conn.commit()
    conn.close()


def get_products(category_id=None):
    conn = get_connection()

    if category_id:
        rows = conn.execute(
            """
            SELECT
                products.*,
                categories.name AS category_name,
                brands.name AS brand_name
            FROM products
            LEFT JOIN categories
                ON products.category_id = categories.id
            LEFT JOIN brands
                ON products.brand_id = brands.id
            WHERE products.category_id = ?
            ORDER BY products.id DESC
            """,
            (category_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT
                products.*,
                categories.name AS category_name,
                brands.name AS brand_name
            FROM products
            LEFT JOIN categories
                ON products.category_id = categories.id
            LEFT JOIN brands
                ON products.brand_id = brands.id
            ORDER BY products.id DESC
            """
        ).fetchall()

    conn.close()
    return rows


def add_product(
    category_id,
    brand_id,
    name,
    price,
    description=""
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO products
        (category_id, brand_id, name, price, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            category_id,
            brand_id,
            name,
            price,
            description
        )
    )

    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()


def toggle_product(product_id):
    conn = get_connection()

    conn.execute(
        """
        UPDATE products
        SET available = CASE
            WHEN available = 1 THEN 0
            ELSE 1
        END
        WHERE id = ?
        """,
        (product_id,)
    )

    conn.commit()
    conn.close()