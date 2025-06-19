from datetime import date

from flask import Blueprint, request, flash, redirect, render_template, url_for

import auth
import forms
from service.stats_service import StatsService

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/')
@auth.login_required
@auth.roles_required('Manažer')
def view_stats_page():
    return redirect(url_for('stats.view_stats_repairs'))

@stats_bp.route('/repairs', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('Manažer')
def view_stats_repairs():
    today = date.today().strftime('%Y-%m-%d')

    start_date = request.form.get('start_date', today)
    end_date = request.form.get('end_date', today)
    form = forms.StatsOrderForm(request.form)

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

    repairs = StatsService.get_repair_stats(start_date, end_date)

    return render_template('stats/repair/page.jinja', repairs=repairs, start_date=start_date, end_date=end_date, parent_active='stats', form=form)

@stats_bp.route('/vehicles')
@auth.login_required
@auth.roles_required('Manažer')
def view_stats_vehicles():
    leaderboard = StatsService.get_vehicle_leaderboard()
    return render_template('stats/vehicle/page.jinja', leaderboard=leaderboard, parent_active='stats')

@stats_bp.route('/employees')
@auth.login_required
@auth.roles_required('Manažer')
def view_stats_employees():
    employees = StatsService.get_employee_stats()
    return render_template('stats/employee/page.jinja', employees=employees, parent_active='stats')

@stats_bp.route('/income')
@auth.login_required
@auth.roles_required('Manažer')
def view_stats_income():
    income = StatsService.get_income_stats()
    return render_template('stats/income/page.jinja', income=income, parent_active='stats')

@stats_bp.route('/services')
@auth.login_required
@auth.roles_required('Manažer')
def view_stats_services():
    services = StatsService.get_services_stats()
    return render_template('stats/service/page.jinja', services=services, parent_active='stats')
