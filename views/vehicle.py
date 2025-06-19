from flask import Blueprint, request, flash, redirect, render_template, url_for, session

import auth
import forms
from service.stock_service import StockService
from service.vehicle_service import VehicleService

vehicle_bp = Blueprint('vehicle', __name__)


@vehicle_bp.route('/manage', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Zákazník')
def view_manage_vehicles_page():
    client_id = session['user_id']
    vehicles = VehicleService.get_by_client_id(client_id)
    return render_template("vehicle/manage/page.jinja", vehicles=vehicles)

@vehicle_bp.route('/add', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Zákazník')
def view_add_vehicle_page():
    form = forms.AddVehicleForm(request.form)

    if request.method == 'POST':
        VehicleService.add_vehicle(
            owner_id=session['user_id'],
            brand=request.form['brand'],
            license_plate=request.form['license_plate'],
            type=request.form['type'],
        )
        flash('Auto bylo úspěšně přidáno do garáže.', 'success')
        return redirect(url_for('vehicle.view_manage_vehicles_page'))
    return render_template('vehicle/add/page.jinja', form=form)


