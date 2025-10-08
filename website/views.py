from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Usuario, ConteudoTeste, Testerespostas, Testeresultado
from . import db #DB importado do arquivo init

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@views.route('/contactus')
def contactus():
    return render_template("contactus.html")

@views.route('/conteudo')
@login_required
def conteudo():

    nivel_conteudo = current_user.nivel_usuario

    if nivel_conteudo not in ['A', 'B', 'C']:
        flash('Please take the English Tests Level to unlock the course content.', category= 'error')

    conteudos = ConteudoTeste.query.filter_by(nivel_conteudo=nivel_conteudo).all()
    
    return render_template("conteudo.html", usuario=current_user, conteudos=conteudos)

@views.route('/nivelamento', methods=['GET', 'POST'])
@login_required
def nivelamento():

    if request.method == 'POST':

        # Inserir o teste de nivelamento na tabela Testesrespostas
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        q5 = request.form.get('q5')
        q6 = request.form.get('q6')
        q7 = request.form.get('q7')
        q8 = request.form.get('q8')
        q9 = request.form.get('q9')
        q10= request.form.get('q10')

        user_id = current_user.user_id
        name_test = 'Teste_Proficiencia'

        novo_teste = Testerespostas(user_id = user_id, name_test = name_test, question_1 = q1, question_2 = q2,
                                    question_3 = q3, question_4 = q4, question_5 = q5, question_6 = q6, question_7 = q7,
                                    question_8 = q8, question_9 = q9, question_10 = q10)
        
        db.session.add(novo_teste)
        db.session.commit()
        flash('Test answered successfully.', category='success')

        #Pegar o resultado do teste na view testeresultado

        resultado = Testeresultado.query.filter_by(user_id= user_id).order_by(Testeresultado.insert_at.desc()).first()

        #Lógica de porcentagem para letra e inserção do nível na tabela Usuario

        usuario = Usuario.query.get(user_id)

        if usuario: 

            if resultado.percet_result <= 0.35: 
                usuario.nivel_usuario = 'A'
                db.session.commit()
                flash('You have been placed at the beginner level.', category='success')
            elif resultado.percet_result > 0.35 and resultado.percet_result <= 0.65:
                usuario.nivel_usuario = 'B'
                db.session.commit()
                flash('You have been placed at the intermediate level.', category= 'success')
            else:
                usuario.nivel_usuario = 'C'
                db.session.commit()
                flash('You have been placed at the advanced level.', category='success')

        else: 
            flash('We had a problem. Please try again.', category='error')


        return redirect((url_for('views.conteudo')))


    return render_template("nivelamento.html", usuario=current_user)

@views.route('/conteudo-post', methods=['POST'])
def conteudo_postagem():

    titulo = request.form.get('titulo')
    descricao = request.form.get('titulo')
    url = request.form.get('url')
    nivel_conteudo = request.form.get('nivel_conteudo')

    novo_conteudo = ConteudoTeste(titulo = titulo, descricao = descricao, url = url, nivel_conteudo = nivel_conteudo)
    db.session.add(novo_conteudo)
    db.session.commit()
    return 'Novo conteúdo postado!'
