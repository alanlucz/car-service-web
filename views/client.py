from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint

import auth
import forms
from service.client_service import ClientService
from service.order_service import OrderService

client_bp = Blueprint('client', __name__)

@client_bp.route('/manage')
@auth.login_required
@auth.roles_required('Manažer', 'Administrativní pracovník')
def view_manage_clients_page():
    clients = ClientService.get_all()
    return render_template("client/manage/page.jinja", clients=clients)


@client_bp.route('/add', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer', 'Administrativní pracovník')
def view_add_client_page():
    form = forms.AddClientForm(request.form)

    if request.method == 'POST':
        ClientService.add_client(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            password=request.form['password']
        )
        flash('Zákazník byl úspěšně přidán.', 'success')
        return redirect(url_for('client.view_manage_clients_page'))
    return render_template('client/add/page.jinja', form=form)


@client_bp.route('/edit/<client_id>', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer', 'Administrativní pracovník')
def view_edit_client_page(client_id):
    client = ClientService.get_by_id(client_id)
    form = forms.EditClientForm(request.form)
    form.fill_with_client(client)

    if request.method == 'POST':
        ClientService.edit_client(
            client_id=client_id,
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
        )
        flash('Profil zákazníka byl úspěšně upraven.', 'success')
        return redirect(url_for('client.view_manage_clients_page'))

    return render_template('client/edit/page.jinja', form=form, client=client)

@client_bp.route('/history/<client_id>', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer', 'Administrativní pracovník')
def view_client_history_page(client_id):
    client = ClientService.get_by_id(client_id)
    orders = OrderService.get_by_client_id(client_id)
    return render_template('client/history/page.jinja', client=client, orders=orders)
