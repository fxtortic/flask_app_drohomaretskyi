from flask import render_template, request, redirect, url_for

from app.products import products_bp

# Простий список продуктів
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 699.99},
    {"id": 3, "name": "Book", "price": 19.99},
]

@products_bp.route("/")
def list_products():
    """Список продуктів"""
    return render_template("products/list.html", products=products)

@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    """Деталі продукту"""
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template("products/detail.html", product=product)

@products_bp.route("/api/<int:product_id>")
def product_api(product_id):
    """API для продукту"""
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}, 404
    return product
