from flask import Blueprint, request, flash, redirect, render_template, url_for

import auth
import forms
from service.employee_service import EmployeeService
from service.role_service import RoleService

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/manage')
@auth.login_required
@auth.roles_required('Manažer')
def view_manage_employees_page():
    employees = EmployeeService.get_all()
    return render_template("employee/manage/page.jinja", employees=employees)


@employee_bp.route('/add', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer')
def view_add_employee_page():
    roles = RoleService.get_employee_roles()
    form = forms.AddEmployeeForm(request.form, roles)

    if request.method == 'POST':
        EmployeeService.add_employee(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            role=request.form['role'],
            password=request.form['password']
        )
        flash('Zaměstnanec byl úspěšne přidán.', 'success')
        return redirect(url_for('employee.view_manage_employees_page'))
    return render_template('employee/add/page.jinja', form=form)


@employee_bp.route('/edit/<employee_id>', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer')
def view_edit_employee_page(employee_id):
    roles = RoleService.get_employee_roles()
    employee = EmployeeService.get_by_id(employee_id)
    form = forms.EditEmployeeForm(request.form, roles)
    form.fill_with_employee(employee)

    if request.method == 'POST':
        EmployeeService.edit_employee(
            employee_id=employee_id,
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            role_id=request.form['role'],
        )
        flash('Profil zaměstnance byl úspěšně upraven.', 'success')
        return redirect(url_for('employee.view_manage_employees_page'))

    return render_template('employee/edit/page.jinja', form=form, employee=employee)