from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint

import auth
import forms
from service.order_service import OrderService
from service.repair_service import RepairService
from service.vehicle_service import VehicleService

order_bp = Blueprint('order', __name__)



@order_bp.route('/manage')
@auth.login_required
@auth.roles_required('Manažer', 'Administrativní pracovník', 'Technik')
def view_manage_orders_page():
    orders = OrderService.get_all()
    return render_template('order/manage/page.jinja', orders=orders)

@order_bp.route('/create', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Zákazník')
def view_create_order_page():
    client_id = session['user_id']
    vehicles = VehicleService.get_by_client_id(client_id)
    service_types = RepairService.get_all_services()
    form = forms.CreateOrderForm(request.form, vehicles, service_types)

    if request.method == 'POST':
        if form.validate():
            OrderService.create_order(
                description=request.form['description'],
                preferred_date=request.form['preferred_date'],
                service_type=request.form['service_type'],
                vehicle_id=request.form['vehicle'],
            )
            flash('Objednávka byla úspěšně vytvořena.', 'success')
            return redirect(url_for('vehicle.view_manage_vehicles_page'))

    return render_template('order/create/page.jinja', form=form)


@order_bp.route('/edit/<order_id>', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer', 'Administrativní pracovník', 'Technik')
def view_edit_order_page(order_id):
    order = OrderService.get_by_id(order_id)
    form = forms.EditOrderForm(request.form)
    form.fill_with_order(order)

    if request.method == 'POST':
        OrderService.edit_order(
            order_id=order_id,
            status=request.form['status'],
            note=request.form['note']
        )
        flash('Objednávka byla úspěšně aktualizována.', 'success')
        return redirect(url_for('order.view_manage_orders_page'))

    return render_template('order/edit/page.jinja', form=form, order=order)
