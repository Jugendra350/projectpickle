    # ...existing code...


import os
from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from models.user import UserModel
from utils.auth import AppUser
from flask_mail import Mail, Message
from dotenv import load_dotenv

    # ...existing code...

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devsecret')

# Flask-Mail config (example, update for production)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your@email.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'password')

mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # user_id is email in this demo
    user = UserModel.find_user(user_id)
    if user:
        return AppUser(user['email'], user['email'])
    return None

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if UserModel.validate_user(email, password):
            user = AppUser(email, email)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if UserModel.find_user(email):
            flash('Email already registered.', 'danger')
        else:
            UserModel.add_user(email, password)
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Dummy order confirmation
        flash('Order placed successfully!', 'success')
        return redirect(url_for('confirmation'))
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/snacks')
def snacks():
    return render_template('snacks.html')


@app.route('/veg-pickles', methods=['GET'])
def veg_pickles():
    return render_template('veg_pickles.html')

# Add to cart route
@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.form.get('image')
    # Here you would call your add_to_cart logic, e.g. DynamoDB or session
    # For now, just flash a message
    flash(f'Added {name} to cart!', 'success')
    return redirect(request.referrer or url_for('veg_pickles'))

@app.route('/non-veg-pickles')
def non_veg_pickles():
    return render_template('non_veg_pickles.html')


    # ...existing code...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
