# Storefront Shopping Cart API

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.x-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **Django REST Framework (DRF)** project implementing a **Shopping Cart API**.
Currently supports **Products** and **Collections** endpoints. More endpoints (Reviews, Orders, Cart) will be added in the future.

**Repository:** [Storefront Shopping Cart API](https://github.com/Abduraheem-H/Storefront_Shoping_cart_API)

---

## 🚀 Features

### Products

* Create, list, update, delete products
* Filter products by collection
* Custom delete protection (cannot delete if linked to orders)

### Collections

* Create, list, update, delete product collections
* Annotated product count per collection
* Delete protection if collection contains products

### Planned Features (Coming Soon)

* **Reviews:** Add, list, update, delete reviews for each product
* **Shopping Cart:** Add/remove products, manage quantities, automatic price calculations
* **Orders:** Checkout, order history, order management

---

## 🛠️ Tech Stack

* **Backend:** Django 5.x
* **API Framework:** Django REST Framework (DRF)
* **Environment:** Pipenv
* **Database:** SQLite (default, can be replaced with PostgreSQL/MySQL)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Abduraheem-H/Storefront_Shoping_cart_API.git
cd Storefront_Shoping_cart_API
```

### 2. Install dependencies

```bash
pipenv install
pipenv shell
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Run the development server

```bash
python manage.py runserver
```

---

## 📌 Usage

API Root: `http://127.0.0.1:8000/store/`

**Products**

* `GET /products/` → List all products
* `POST /products/` → Create a product
* `GET /products/?collection_id=2` → Filter products by collection

**Collections**

* `GET /collections/` → List all collections
* `POST /collections/` → Create a collection

**Future Endpoints**

* `GET /products/{id}/reviews/` → List reviews for a product
* `POST /cart/` → Add items to shopping cart
* And more…

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License

This project is licensed under the MIT License.
