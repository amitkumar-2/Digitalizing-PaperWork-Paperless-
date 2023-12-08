from flask import Blueprint, render_template

batsman1 = Blueprint('batsman', __name__)

@batsman1.route("/batsman")
def batsman():
    return "<h1>This is batsman page</h1>"

@batsman1.route("/batsmans")
def batsmans():
    return "<h1>This is batsmans pages</h1>"