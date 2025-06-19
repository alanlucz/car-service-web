from flask import Blueprint, request, flash, redirect, render_template, url_for

import auth
import forms
from service.stock_service import StockService

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/manage')
@auth.login_required
@auth.roles_required('Administrativní pracovník')
def view_manage_stock_page():
    items = StockService.get_all()
    return render_template("stock/manage/page.jinja", items=items)

@stock_bp.route('/add_item', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Administrativní pracovník')
def view_add_item_page():
    form = forms.AddItemForm(request.form)

    if request.method == 'POST':
        StockService.add_item(
            name=request.form['name'],
            maker=request.form['maker'],
            amount=request.form['amount'],
            purchase_price=request.form['purchase_price'],
            selling_price=request.form['selling_price'],
            min_amount=request.form['min_amount'],
            description=request.form['description'],
        )
        flash('Položka byla úspěšně přidána.', 'success')
        return redirect(url_for('stock.view_manage_stock_page'))
    return render_template('stock/add_item/page.jinja', form=form)

@stock_bp.route('/edit_item/<item_id>', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Administrativní pracovník')
def view_edit_item_page(item_id):
    item = StockService.get_by_id(item_id)
    form = forms.EditItemForm(request.form)
    form.fill_with_item(item)

    if request.method == 'POST':
        StockService.edit_item(
            item_id=item_id,
            name=request.form['name'],
            maker=request.form['maker'],
            amount=request.form['amount'],
            purchase_price=request.form['purchase_price'],
            selling_price=request.form['selling_price'],
            min_amount=request.form['min_amount'],
            description=request.form['description'],
        )
        flash('Položka byla úspěšně aktualizována.', 'success')
        return redirect(url_for('stock.view_manage_stock_page'))

    return render_template('stock/edit_item/page.jinja', form=form, item=item)