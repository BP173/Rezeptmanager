from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product, Recipe, RecipeIngredient, Menu, MenuRecipe
from . import db

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    products = Product.query.all()
    recipes = Recipe.query.all()
    menus = Menu.query.all()

    return render_template(
        "index.html",
        products=products,
        recipes=recipes,
        menus=menus
    )


@bp.route("/add_product", methods=["POST"])
def add_product():
    name = request.form.get("name")
    unit = request.form.get("unit")
    price = request.form.get("price")

    product = Product(
        name=name,
        unit=unit,
        price=float(price) if price else 0
    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for("main.home"))

@bp.route("/add_recipe", methods=["POST"])
def add_recipe():
    name = request.form.get("name")

    recipe = Recipe(name=name)
    db.session.add(recipe)
    db.session.commit()

    return redirect(url_for("main.home"))

@bp.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    recipe_id = request.form.get("recipe_id")
    product_id = request.form.get("product_id")
    amount = request.form.get("amount")

    ingredient = RecipeIngredient(
        recipe_id=int(recipe_id),
        product_id=int(product_id),
        amount=float(amount)
    )

    db.session.add(ingredient)
    db.session.commit()

    return redirect(url_for("main.home"))

@bp.route("/add_menu", methods=["POST"])
def add_menu():
    name = request.form.get("name")

    menu = Menu(name=name)
    db.session.add(menu)
    db.session.commit()

    return redirect(url_for("main.home"))

@bp.route("/add_menu_recipe", methods=["POST"])
def add_menu_recipe():
    menu_id = request.form.get("menu_id")
    recipe_id = request.form.get("recipe_id")
    portions = request.form.get("portions")

    mr = MenuRecipe(
        menu_id=int(menu_id),
        recipe_id=int(recipe_id),
        portions=int(portions)
    )

    db.session.add(mr)
    db.session.commit()

    return redirect(url_for("main.home"))

@bp.route("/calculate/<int:menu_id>")
def calculate(menu_id):
    menu = Menu.query.get(menu_id)

    result = {}

    for mr in menu.recipes:
        for ing in mr.recipe.ingredients:
            total_amount = ing.amount * mr.portions
            product = ing.product

            key = product.id

            if key not in result:
                result[key] = {
                    "name": product.name,
                    "unit": product.unit,
                    "amount": total_amount,
                    "price": product.price,
                    "total_price": total_amount * product.price
                }
            else:
                result[key]["amount"] += total_amount
                result[key]["total_price"] += total_amount * product.price

    total_cost = sum(item["total_price"] for item in result.values())

    return render_template(
        "result.html",
        result=result,
        menu=menu,
        total_cost=total_cost
    )