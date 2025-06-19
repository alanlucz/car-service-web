from flask import Blueprint, render_template

home_page_bp = Blueprint('home_page', __name__)


@home_page_bp.route("/")
def page():
    return render_template("home_page/page.jinja", footer=True)
