from flask import Blueprint, request, flash, redirect, render_template, url_for, session

import auth
import forms
from service.order_service import OrderService
from service.repair_service import RepairService
from service.stock_service import StockService

repair_bp = Blueprint('repair', __name__)


@repair_bp.route('/manage')
@auth.login_required
@auth.roles_required('Technik')
def view_manage_repairs_page():
    repairs = RepairService.get_all()
    return render_template('repair/manage/page.jinja', repairs=repairs)


@repair_bp.route('/add', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Technik')
def view_add_repair_page():
    form = forms.RepairForm(request.form)
    orders = OrderService.get_all_unfinished()
    form.order.choices = [(order['id_objednavky'], f'Objednávka č. {order['id_objednavky']} - {order['popis']}') for order in orders]
    items = StockService.get_all()

    if request.method == 'POST':
        selected_items = {}

        print(request.form)
        if form.validate():
            for item_id in request.form.getlist('selected_items'):
                amount = request.form.get(f'amount[{item_id}]', 0)
                selected_items[item_id] = int(amount)
            RepairService.add_repair(
                description=request.form['description'],
                time=request.form['time'],
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                order=request.form['order'],
                employee_id=session['user_id'],
                selected_items=selected_items,
            )
            flash('Oprava byla úspěšně zaznamenána.', 'success')
            return redirect(url_for('repair.view_manage_repairs_page'))

    return render_template('repair/add/page.jinja', form=form, items=items)



