from datetime import datetime
from tokenize import String

from wtforms import validators
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import IntegerField, DecimalField
from wtforms.fields.simple import StringField, PasswordField, EmailField, MultipleFileField
from wtforms.form import Form
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, ValidationError


def no_space(form, field):
    if " " in field.data:
        raise ValidationError("Mezery nejsou povoleny.")

class SignInForm(Form):
    login = EmailField(label='E-mail', validators=[InputRequired(), Email(), Length(min=3, max=40)])
    password = PasswordField(label='Heslo', validators=[InputRequired(), Length(min=3, max=40)])

class RegisterForm(Form):
    first_name = StringField(label='Jméno', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField(label='Příjmení', validators=[InputRequired(), Length(min=1, max=50)])
    login = EmailField(label='E-mail', validators=[InputRequired(), Email(), Length(min=3, max=40)])
    password = PasswordField(label='Heslo', validators=[InputRequired(), Length(min=6, max=40)])
    confirm_password = PasswordField(label='Potvrzení hesla', validators=[InputRequired(), Length(min=6, max=40)])

class AddEmployeeForm(Form):
    def __init__(self, data, roles):
        super(AddEmployeeForm, self).__init__(data)
        self.role.choices = [(role['id_role'], role['nazev']) for role in roles]
    first_name = StringField(label='Jméno', validators=[InputRequired()])
    last_name = StringField(label='Příjmení', validators=[InputRequired()])
    email = EmailField(label='E-mail', validators=[InputRequired(), Email()])
    role = SelectField(label='Pozice', choices=[], validators=[InputRequired()])
    password = PasswordField(label='Heslo', validators=[InputRequired(), Length(min=3, max=40)])

class EditEmployeeForm(Form):
    def __init__(self, data, roles):
        super(EditEmployeeForm, self).__init__(data)
        self.role.choices = [(role['id_role'], role['nazev']) for role in roles]

    def fill_with_employee(self, employee):
        self.first_name.data = employee['jmeno']
        self.last_name.data = employee['prijmeni']
        self.email.data = employee['email']
        self.role.data = str(employee['role_id_role'])

    first_name = StringField(label='Jméno', validators=[InputRequired()])
    last_name = StringField(label='Příjmení', validators=[InputRequired()])
    email = EmailField(label='E-mail', validators=[InputRequired(), Email()])
    role = SelectField(label='Pozice', choices=[], validators=[InputRequired()])
    password = PasswordField(label='Heslo', validators=[InputRequired(), Length(min=3, max=40)])


class AddClientForm(Form):
    first_name = StringField(label='Jméno', validators=[InputRequired()])
    last_name = StringField(label='Příjmení', validators=[InputRequired()])
    email = EmailField(label='Email', validators=[InputRequired(), Email()])
    password = PasswordField(label='Heslo', validators=[InputRequired(), Length(min=3, max=40)])

class EditClientForm(Form):
    def __init__(self, data):
        super(EditClientForm, self).__init__(data)

    def fill_with_client(self, client):
        self.first_name.data = client['jmeno']
        self.last_name.data = client['prijmeni']
        self.email.data = client['email']

    first_name = StringField(label='Jméno', validators=[InputRequired()])
    last_name = StringField(label='Příjmení', validators=[InputRequired()])
    email = EmailField(label='E-mail', validators=[InputRequired(), Email()])

class AddItemForm(Form):
    name = StringField(label='Název', validators=[InputRequired()])
    maker = StringField(label='Výrobce', validators=[InputRequired()])
    amount = IntegerField(label='Množství', validators=[InputRequired(), NumberRange(min=1)])
    purchase_price = DecimalField(label='Kupní cena', validators=[InputRequired()])
    selling_price = DecimalField(label='Prodejní cena', validators=[InputRequired()])
    min_amount = IntegerField(label='Min. množství', validators=[InputRequired()])
    description = StringField(label='Poznámka', validators=[InputRequired()])

class EditItemForm(Form):
    def __init__(self, data):
        super(EditItemForm, self).__init__(data)

    def fill_with_item(self, item):
        self.name.data = item['nazev']
        self.maker.data = item['vyrobce']
        self.amount.data = item['pocet_kusu']
        self.purchase_price.data = item['nakupni_cena']
        self.selling_price.data = item['prodejni_cena']
        self.min_amount.data = item['minimalni_pocet_kusu']
        self.description.data = item['poznamka']

    name = StringField(label='Název', validators=[InputRequired()])
    maker = StringField(label='Výrobce', validators=[InputRequired()])
    amount = IntegerField(label='Množství', validators=[InputRequired()])
    purchase_price = DecimalField(label='Kupní cena', validators=[InputRequired()])
    selling_price = DecimalField(label='Prodejní cena', validators=[InputRequired()])
    min_amount = IntegerField(label='Min. množství', validators=[InputRequired()])
    description = StringField(label='Poznámka', validators=[InputRequired()])

class AddVehicleForm(Form):
    brand = StringField(label='Značka vozidla (výrobce)', render_kw={'placeholder': 'Mercedes-Benz'}, validators=[InputRequired(), Length(min=1, max=30)])
    license_plate = StringField(label='SPZ', render_kw={'placeholder': '8B81234'}, validators=[InputRequired(), Length(min=3, max=12)])
    type = SelectField(label='Typ vozidla', choices=[
        ('Osobní automobil', 'Osobní automobil'),
        ('Motocykl', 'Motocykl'),
        ('Dodávka', 'Dodávka'),
        ('Tahač', 'Tahač')
    ], validators=[InputRequired()])


class EditOrderForm(Form):
    def __init__(self, data):
        super(EditOrderForm, self).__init__(data)

    def fill_with_order(self, order):
        self.status.data = order['stav']
        self.note.data = order['poznamka']

    status = SelectField(label='Stav objednávky', choices=[
        ('čekající', 'čekající'),
        ('v procesu', 'v procesu'),
        ('dokončeno', 'dokončeno')
    ], validators=[InputRequired()])
    note = StringField(label='Přidat poznámku', validators=[])

class CreateOrderForm(Form):
    def __init__(self, data, vehicles, service_types):
        super(CreateOrderForm, self).__init__(data)
        self.vehicle.choices = [(vehicle['id_vozidla'], vehicle['spz'] + ' - ' + vehicle['znacka_vozidla']) for vehicle in vehicles]
        self.service_type.choices = [(service_type['id_opravy'], service_type['nazev']) for service_type in service_types]

    def validate_date_older_than_now(form, field):
        today = datetime.now().date()
        if field.data < today:
            raise ValidationError('Preferovaný termín musí být dnešní nebo pozdější.')

    service_type = SelectField(label='Typ služby', choices=[], validators=[InputRequired()])
    description = StringField(label='Popis', validators=[InputRequired()])
    vehicle = SelectField(label='Vozidlo', choices=[], validators=[InputRequired()])
    preferred_date = DateField(label='Preferovaný termín', format='%Y-%m-%d', validators=[InputRequired(), validate_date_older_than_now] )

class StatsOrderForm(Form):
    start_date = DateField(label='Od', validators=[InputRequired()])
    end_date = DateField(label='Do', validators=[InputRequired()])

class RepairForm(Form):
    def validate_date_range(form, field):
        start_date = form.start_date.data
        end_date = field.data
        if start_date > end_date:
            raise ValidationError('Datum zahájení musí být dříve nebo ve stejný den jako datum ukončení.')

    description = StringField('Popis opravy', validators=[InputRequired()])
    time = DecimalField('Čas opravy (v hodinách)', validators=[InputRequired()])
    start_date = DateField('Datum zahájení', format='%Y-%m-%d', validators=[InputRequired()])
    end_date = DateField('Datum ukončení', format='%Y-%m-%d', validators=[InputRequired(), validate_date_range])
    order = SelectField('Objednávka', choices=[])
    selected_items = MultipleFileField('selected_items', default=[])
