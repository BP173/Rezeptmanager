from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    price = db.Column(db.Float)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    ingredients = db.relationship("RecipeIngredient", backref="recipe", lazy=True)


class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    amount = db.Column(db.Float)

    product = db.relationship("Product")

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    recipes = db.relationship("MenuRecipe", backref="menu", lazy=True)


class MenuRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    portions = db.Column(db.Integer)

    recipe = db.relationship("Recipe")