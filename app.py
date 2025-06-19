from flask import Flask

from database import database

from views.employee import employee_bp
from views.home_page import home_page_bp
from views.order import order_bp
from views.repair import repair_bp
from views.stats import stats_bp
from views.stock import stock_bp
from views.user import user_bp
from views.client import client_bp
from views.vehicle import vehicle_bp

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

app.register_blueprint(home_page_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(client_bp, url_prefix='/client')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(stats_bp, url_prefix='/stats')
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(vehicle_bp, url_prefix='/vehicle')
app.register_blueprint(repair_bp, url_prefix='/repair')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
