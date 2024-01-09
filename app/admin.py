from flask_admin import Admin
from flask import Flask, redirect, url_for, request
from app import db, flightapp
from app.models import Airport, Route, Flight, Transit, Flight_Transit, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField
from wtforms.validators import DataRequired
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user


"""*===AUTHENTICATE===*"""
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


"""*===FLIGHT===*"""
class FlightView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_list = ['id', 'name', 'numberOfClassFirstSeat', 'numberOfClassSecondSeat', 'departure_time', 'destination_time', 'availableClassFirstSeat',
                   'availableClassSecondSeat', 'flights.name', 'unitPriceOfClassFirstSeat', 'unitPriceOfClassSecondSeat']
    form_columns = ['name', 'numberOfClassFirstSeat', 'numberOfClassSecondSeat', 'departure_time', 'destination_time',
                   'route_id', 'unitPriceOfClassFirstSeat', 'unitPriceOfClassSecondSeat']
    column_labels = {
        'id': 'Mã chuyến bay',
        'name': 'Tên chuyến bay',
        'numberOfClassFirstSeat': 'Số lượng ghế hạng 1',
        'numberOfClassSecondSeat': 'Số lượng ghế hạng 2',
        'availableClassFirstSeat': 'Số ghế hạng 1 còn trống',
        'availableClassSecondSeat': 'Số ghế hạng 2 còn trống',
        'departure_time': 'Ngày giờ khởi hành',
        'destination_time': 'Ngày giờ đến',
        'flights.name': 'Tên tuyến bay',
        'unitPriceOfClassFirstSeat': 'Đơn giá ghế hạng 1',
        'unitPriceOfClassSecondSeat': 'Đơn giá ghế hạng 2',
    }

class FormSearchFlight(FlaskForm):
    with flightapp.app_context():
        start = SelectField('Start', choices=[(Airport.id, Airport.name) for Airport in Airport.query.all()],
                             validators=[DataRequired()])
        destination = SelectField('Destination', choices=[(Airport.id, Airport.name) for Airport in Airport.query.all()],
                             validators=[DataRequired()])
        departure_date = DateField('Departure date', format='%Y-%m-%d', validators=[DataRequired()])



"""
class TransitForm(FlaskForm):
    stopTime = StringField("Thời gian chờ", validators=[DataRequired()])
    airportName = SelectField("Tên sân bay", validators=[DataRequired()], coerce=int)

    def __init__(self, *args, **kwargs):
        super(TransitForm, self).__init__(*args, **kwargs)
        self.airportName.choices = [(airport.id, airport.name) for airport in Airport.query.all()]
"""

"""*===TRANSIT===*"""
class TransitView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    #column_searchable_list = ['name']
    #column_filters = ['name']
    column_list = ['id', 'stopTime', 'airportfk.id', 'airportfk.name']
    form_columns = ['stopTime', 'airport_id']
    #form = TransitForm

    """
    def edit_form(self, obj):
        form = super(TransitView, self).edit_form(obj=obj)
        form.stopTime.default = obj.stopTime
        form.airportName.default = obj.airportfk.id
        form.process()
        return form
    """
    column_labels = {
        'id': 'Mã sân bay trung gian',
        'stopTime': 'Thời gian dừng',
        'airportfk.id': 'Mã sân bay',
        'airportfk.name': 'Tên sân bay',
    }

"""*===ROUTE===*"""
"""
class RouteForm(FlaskForm):
    name = StringField("Tên tuyến bay", validators=[DataRequired()])
    routefk1 = SelectField("Sân bay khởi hành", query_factory=lambda: Airport.query.all(), get_label='name', validators=[DataRequired()])
    routefk2 = SelectField("Sân bay đích đến", query_factory=lambda: Airport.query.all(), get_label='name',
                               validators=[DataRequired()])
"""


class RouteView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_list = ['id', 'name', 'routefk1.name', 'routefk2.name']
    form_columns = ['name', 'departure_id', 'destination_id']
    column_labels = {
        'id': 'Mã tuyến bay',
        'name': 'Tên tuyến bay',
        'routefk1.name': 'Sân bay khởi hành',
        'routefk2.name': 'Sân bay đích đến'
    }
    #page_size = 50

    #form = RouteForm


"""*===AIRPORT===*"""
class AirportView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_list = ['id', 'code', 'name', 'address']
    form_columns = ['code', 'name', 'address']
    column_labels = {
        'code': 'Mã sân bay',
        'name': 'Tên sân bay',
        'address': 'Địa chỉ'
    }

"""*===LOGOUT===*"""
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated



"""*===ADMIN===*"""
class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    #redirect den trang login neu nguoi dung khong dang nhap
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))




admin = Admin(app=flightapp, name='HỆ THỐNG QUẢN LÝ CHUYẾN BAY', template_mode='bootstrap4', index_view='')
admin.add_view(AirportView(Airport, db.session, name="Sân bay"))
admin.add_view(TransitView(Transit, db.session, name="Sân bay trung gian"))
admin.add_view(RouteView(Route, db.session, name="Tuyến bay"))
admin.add_view(FlightView(Flight, db.session, name="Chuyến bay"))
admin.add_view(LogoutView(name='Đăng xuất'))
