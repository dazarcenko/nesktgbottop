from flask import Flask, request, redirect, url_for, render_template_string

from database import (
    init_db,
    get_categories,
    add_category,
    delete_category,
    get_brands,
    add_brand,
    get_products,
    add_product,
    delete_product,
    toggle_product,
)


app = Flask(__name__)

init_db()


HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Админ-панель</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1100px;
            margin: 30px auto;
            padding: 0 15px;
            background: #f4f4f4;
        }

        h1 {
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
        }

        input, select, textarea {
            width: 100%;
            box-sizing: border-box;
            padding: 10px;
            margin: 6px 0 12px;
        }

        button {
            padding: 10px 15px;
            border: 0;
            border-radius: 8px;
            cursor: pointer;
        }

        .add {
            background: #222;
            color: white;
        }

        .delete {
            background: #d33;
            color: white;
        }

        .toggle {
            background: #ddd;
        }

        .product {
            border-top: 1px solid #ddd;
            padding: 15px 0;
        }

        .available {
            color: green;
        }

        .hidden {
            color: red;
        }
    </style>
</head>

<body>

<h1>🛠 Админ-панель каталога</h1>


<div class="card">

<h2>➕ Добавить категорию</h2>

<form method="POST"
      action="/category/add">

    <input
        name="name"
        placeholder="Название категории"
        required
    >

    <button class="add">
        Добавить
    </button>

</form>

</div>


<div class="card">

<h2>📂 Категории</h2>

{% for category in categories %}

<div>

    <b>{{ category["name"] }}</b>

    <form
        method="POST"
        action="/category/delete"
        style="display:inline"
    >

        <input
            type="hidden"
            name="id"
            value="{{ category['id'] }}"
        >

        <button class="delete">
            Удалить
        </button>

    </form>

</div>

{% endfor %}

</div>


<div class="card">

<h2>🏷 Добавить бренд</h2>

<form method="POST"
      action="/brand/add">

    <select name="category_id" required>

        {% for category in categories %}

        <option value="{{ category['id'] }}">
            {{ category["name"] }}
        </option>

        {% endfor %}

    </select>

    <input
        name="name"
        placeholder="Название бренда"
        required
    >

    <button class="add">
        Добавить бренд
    </button>

</form>

</div>


<div class="card">

<h2>➕ Добавить товар</h2>

<form method="POST"
      action="/product/add">

    <label>Категория</label>

    <select name="category_id" required>

        {% for category in categories %}

        <option value="{{ category['id'] }}">
            {{ category["name"] }}
        </option>

        {% endfor %}

    </select>


    <label>Бренд</label>

    <select name="brand_id">

        <option value="">
            Без бренда
        </option>

        {% for category in categories %}

            {% for brand in brands_by_category[category["id"]] %}

            <option value="{{ brand['id'] }}">

                {{ category["name"] }}
                →
                {{ brand["name"] }}

            </option>

            {% endfor %}

        {% endfor %}

    </select>


    <input
        name="name"
        placeholder="Название товара"
        required
    >


    <input
        name="price"
        type="number"
        step="0.01"
        placeholder="Цена"
        required
    >


    <textarea
        name="description"
        placeholder="Описание"
    ></textarea>


    <button class="add">
        Добавить товар
    </button>

</form>

</div>


<div class="card">

<h2>📦 Товары</h2>

{% for product in products %}

<div class="product">

    <h3>
        {{ product["name"] }}
    </h3>

    <div>
        Категория:
        {{ product["category_name"] }}
    </div>

    {% if product["brand_name"] %}

    <div>
        Бренд:
        {{ product["brand_name"] }}
    </div>

    {% endif %}

    <div>
        Цена:
        <b>{{ product["price"] }}</b>
    </div>

    <div>

        {% if product["available"] %}

        <span class="available">
            🟢 В наличии
        </span>

        {% else %}

        <span class="hidden">
            🔴 Скрыт
        </span>

        {% endif %}

    </div>


    <form
        method="POST"
        action="/product/toggle"
        style="display:inline"
    >

        <input
            type="hidden"
            name="id"
            value="{{ product['id'] }}"
        >

        <button class="toggle">
            Вкл / Выкл
        </button>

    </form>


    <form
        method="POST"
        action="/product/delete"
        style="display:inline"
    >

        <input
            type="hidden"
            name="id"
            value="{{ product['id'] }}"
        >

        <button class="delete">
            Удалить
        </button>

    </form>

</div>

{% endfor %}

</div>

</body>
</html>
"""


def prepare_data():
    categories = get_categories()

    brands_by_category = {}

    for category in categories:
        brands_by_category[category["id"]] = (
            get_brands(category["id"])
        )

    products = get_products()

    return categories, brands_by_category, products


@app.route("/")
def index():

    categories, brands_by_category, products = (
        prepare_data()
    )

    return render_template_string(
        HTML,
        categories=categories,
        brands_by_category=brands_by_category,
        products=products,
    )


@app.post("/category/add")
def category_add():

    name = request.form["name"].strip()

    if name:
        add_category(name)

    return redirect(url_for("index"))


@app.post("/category/delete")
def category_delete():

    category_id = int(request.form["id"])

    delete_category(category_id)

    return redirect(url_for("index"))


@app.post("/brand/add")
def brand_add():

    category_id = int(
        request.form["category_id"]
    )

    name = request.form["name"].strip()

    if name:
        add_brand(category_id, name)

    return redirect(url_for("index"))


@app.post("/product/add")
def product_add():

    category_id = int(
        request.form["category_id"]
    )

    brand_id = request.form.get("brand_id")

    if brand_id:
        brand_id = int(brand_id)
    else:
        brand_id = None

    name = request.form["name"].strip()

    price = float(
        request.form["price"]
    )

    description = request.form.get(
        "description",
        ""
    ).strip()

    add_product(
        category_id,
        brand_id,
        name,
        price,
        description
    )

    return redirect(url_for("index"))


@app.post("/product/delete")
def product_delete():

    product_id = int(
        request.form["id"]
    )

    delete_product(product_id)

    return redirect(url_for("index"))


@app.post("/product/toggle")
def product_toggle():

    product_id = int(
        request.form["id"]
    )

    toggle_product(product_id)

    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )