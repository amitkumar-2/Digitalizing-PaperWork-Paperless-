from flask import Blueprint, render_template

bowler1 = Blueprint('bowler', __name__)

@bowler1.route("/bowler")
def bowler():
    return "<h1>This is bowler page</h1>"