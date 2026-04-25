import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/lashmaster')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    appointments = db.relationship('Appointment', backref='client', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    client_name = db.Column(db.String(100))  # Для быстрой записи без регистрации клиента
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))
    is_busy = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Формы
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ClientForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email')
    submit = SubmitField('Сохранить')

class AppointmentForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()], format='%Y-%m-%d')
    time = SelectField('Время', choices=[], validators=[DataRequired()])
    client_name = StringField('Имя клиента')
    phone = StringField('Телефон')
    service = SelectField('Услуга', choices=[
        ('Классическое наращивание', 'Классическое наращивание'),
        ('Объем 2D', 'Объем 2D'),
        ('Объем 3D', 'Объем 3D'),
        ('Голливудский объем', 'Голливудский объем'),
        ('Снятие ресниц', 'Снятие ресниц'),
        ('Ламинирование', 'Ламинирование')
    ])
    notes = StringField('Комментарий')
    submit = SubmitField('Забронировать')

# Маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schedule/<int:year>/<int:month>')
@login_required
def get_schedule(year, month):
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    appointments = Appointment.query.filter(
        Appointment.date >= first_day.date(),
        Appointment.date <= last_day.date()
    ).all()
    
    schedule = {}
    for app in appointments:
        date_str = app.date.strftime('%Y-%m-%d')
        if date_str not in schedule:
            schedule[date_str] = []
        schedule[date_str].append({
            'id': app.id,
            'time': app.time,
            'is_busy': app.is_busy,
            'client_name': app.client_name or (app.client.name if app.client else ''),
            'service': app.service,
            'notes': app.notes
        })
    
    return jsonify(schedule)

@app.route('/api/appointment', methods=['POST'])
@login_required
def create_appointment():
    data = request.json
    appointment = Appointment(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time=data['time'],
        client_name=data.get('client_name'),
        phone=data.get('phone'),
        service=data.get('service'),
        is_busy=True,
        notes=data.get('notes', '')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'success': True, 'id': appointment.id})

@app.route('/api/appointment/<int:id>', methods=['DELETE'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Неверный логин или пароль')
    return render_template('login.html', form=form)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/clients')
@login_required
def manage_clients():
    # Статистика по клиентам и записям
    from sqlalchemy import func
    
    # Общее количество клиентов
    total_clients = Client.query.count()
    
    # Общее количество записей
    total_appointments = Appointment.query.count()
    
    # Записи за текущий месяц
    now = datetime.now()
    first_day_of_month = now.replace(day=1)
    appointments_this_month = Appointment.query.filter(
        Appointment.date >= first_day_of_month.date()
    ).count()
    
    # Записи за сегодня
    today_appointments = Appointment.query.filter(
        Appointment.date == now.date()
    ).count()
    
    # Популярные услуги
    services_stats = db.session.query(
        Appointment.service, 
        func.count(Appointment.id).label('count')
    ).group_by(Appointment.service).order_by(func.count(Appointment.id).desc()).limit(5).all()
    
    # Записи по дням недели (для текущей недели)
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekly_stats = db.session.query(
        func.strftime('%w', Appointment.date).label('day'),
        func.count(Appointment.id).label('count')
    ).filter(
        Appointment.date >= start_of_week.date(),
        Appointment.date <= end_of_week.date()
    ).group_by(func.strftime('%w', Appointment.date)).all()
    
    # Последние клиенты
    recent_clients = Client.query.order_by(Client.id.desc()).limit(5).all()
    
    return render_template('clients.html', 
                         total_clients=total_clients,
                         total_appointments=total_appointments,
                         appointments_this_month=appointments_this_month,
                         today_appointments=today_appointments,
                         services_stats=services_stats,
                         weekly_stats=weekly_stats,
                         recent_clients=recent_clients)

@app.route('/init-db')
def init_db():
    db.create_all()
    # Создаем администратора по умолчанию
    if not User.query.filter_by(username='master').first():
        admin = User(
            username='master',
            password_hash=generate_password_hash('Master123')
        )
        db.session.add(admin)
        db.session.commit()
        return 'База данных инициализирована. Логин: master, Пароль: Master123'
    return 'База данных уже инициализирована'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
