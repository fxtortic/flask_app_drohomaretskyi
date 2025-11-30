from flask import render_template, jsonify

from app.products import products_bp
from app.products.models import Product


@products_bp.route("/")
def list_products():
    products = Product.query.all()
    return render_template("products/list.html", products=products)


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("products/detail.html", product=product)


@products_bp.route("/api/<int:product_id>")
def product_api(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
    )
