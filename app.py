import random
import requests
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, login_manager, User
from flask_login import login_user, logout_user, current_user


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    # Inject common template variables
    @app.context_processor
    def inject_common():
        return dict(current_user=current_user)

    # Home page - trending and featured products
    @app.route("/", methods=["GET"])
    def index():
        try:
            response = requests.get("https://dummyjson.com/products")
            products = response.json().get("products", [])
        except Exception as e:
            print("Error fetching products:", e)
            products = []

        trending = random.sample(products, 12) if len(
            products) >= 12 else products
        featured = random.sample(products, 6) if len(
            products) >= 6 else products

        # Extract unique categories dynamically
        categories = sorted({p["category"] for p in products})

        return render_template(
            "index.html",
            trending=trending,
            featured=featured,
            categories=categories,
            query=request.args.get("q", "")
        )

    # Shop page
    @app.route("/shop")
    def shop():
        q = request.args.get("q", "")
        category = request.args.get("category", "")
        try:
            response = requests.get("https://dummyjson.com/products")
            products = response.json().get("products", [])
        except Exception as e:
            print("Error fetching products:", e)
            products = []

        # Filter by search query
        if q:
            products = [p for p in products if q.lower() in p["title"].lower()]

        # Filter by category
        if category:
            products = [p for p in products if category.lower()
                        in p["category"].lower()]

        return render_template("shop.html", products=products, query=q, category=category)

    # Product detail page
    @app.route("/product/<int:product_id>")
    def product_detail(product_id):
        try:
            response = requests.get(
                f"https://dummyjson.com/products/{product_id}")
            product = response.json()
        except Exception as e:
            print("Error fetching product:", e)
            product = None

        if not product or "id" not in product:
            return "Product not found", 404

        return render_template("product_detail.html", product=product)

    # Search redirects to shop
    @app.route("/search", methods=["GET", "POST"])
    def search_route():
        query = request.values.get("q", "")
        return redirect(url_for("shop", q=query))

    # Simple demo login/logout
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(
                username=username, password=password).first()
            if user:
                login_user(user)
                return redirect(request.args.get("next") or url_for("index"))
            else:
                return render_template("login.html", error="Invalid credentials")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    return app
