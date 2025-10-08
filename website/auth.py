from flask import Blueprint, request, render_template, flash, redirect, url_for
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import db #DB importado do arquivo init
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.senha, senha):
                login_user(usuario)
                flash('Logged in successfully!', category='success')
                
                if usuario.nivel_usuario not in ['A', 'B', 'C']:
                    return redirect(url_for('views.nivelamento'))
                else: 
                    return redirect(url_for('views.conteudo'))
            else: 
                flash('Incorrect password. Please try again!', category='error')
        else: 
            flash('Email not registered.', category='error')

    return render_template("login.html", usuario = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/cadastro-usuario', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha1')
        senha2 = request.form.get('senha2')
        nivel_usuario = request.form.get('nivel_usuario')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            flash('Email already registered!', category='error' )
        elif len(email) < 4: 
            flash('Email must be longer than 3 characters.', category='error')
        elif len(nome) < 3: 
            flash('Name must be longer than 2 characters.', category='error')
        elif senha != senha2:
            flash('Passwords do not match.', category='error')
        elif len(senha) < 6:
            flash('The password must be at least 5 characters long.', category='error')
        else:
            novo_usuario = Usuario(nome=nome, email=email, senha=generate_password_hash(senha, method='scrypt'), nivel_usuario=nivel_usuario)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Account created successfully!', category='success') 
            return redirect(url_for('auth.login'))


    return render_template("cadastro_usuario.html")

@auth.route('/password-recover', methods=['GET', 'POST'])
def password_recover():

    return render_template("password_recover.html")