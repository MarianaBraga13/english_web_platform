from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Usuario, ConteudoTeste, Testerespostas, Testeresultado, Testegabarito
from . import db  # DB importado do arquivo __init__

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
        flash('Please take the English Tests Level to unlock the course content.', category='error')

    # Conteúdos já existentes do banco
    conteudos = ConteudoTeste.query.filter_by(nivel_conteudo=nivel_conteudo).all()

    # --- Vídeos de teste (somente para mostrar) ---
    videos_teste = [
        {"titulo": "Vídeo Teste 1", "url": "https://www.youtube.com/watch?v=JxHiuCI2Xro"},
        {"titulo": "Vídeo Teste 2", "url": "https://www.youtube.com/watch?v=euIqptZpe5Q"},
        {"titulo": "Vídeo Teste 3", "url": "https://youtu.be/VyCgJdRzAvA?si=kgyCuuKM6w-bPks_"},
        {"titulo": "Vídeo Teste 3", "url": "https://youtu.be/OQ0GMdX3daE?si=0D8ZPToM9WU3jFVW"}
        
    ]

    # Transformando os vídeos em objetos compatíveis com o template
    class VideoFake:
        def __init__(self, titulo, url):
            self.titulo = titulo
            self.url = url

    for video in videos_teste:
        conteudos.append(VideoFake(video["titulo"], video["url"]))

    return render_template("conteudo.html", usuario=current_user, conteudos=conteudos)

@views.route('/nivelamento', methods=['GET', 'POST'])
@login_required
def nivelamento():
    if request.method == 'POST':
        # --- Captura das respostas do formulário ---
        respostas = {f'q{i}': request.form.get(f'q{i}') for i in range(1, 11)}
        user_id = current_user.user_id
        name_test = 'Teste_Proficiencia'

        teste_existente = Testerespostas.query.filter_by(user_id=user_id, name_test=name_test).first()
        if teste_existente:
            flash('You have already submitted this test.', category='error')
            return redirect(url_for('views.conteudo'))

        # --- Cria e salva as respostas do usuário ---
        novo_teste = Testerespostas(
            user_id=user_id,
            name_test=name_test,
            **{f'question_{i}': respostas[f"q{i}"] for i in range(1, 11)}
        )
        db.session.add(novo_teste)
        db.session.commit()
        flash('Test answered successfully.', category='success')

        print(f">>> Novo teste salvo! ID: {novo_teste.test_id}, User: {novo_teste.user_id}")
        for i in range(1, 11):
            print(f"user answer q{i}: {getattr(novo_teste, f'question_{i}', None)}")

        # --- Busca o gabarito ---
        gabarito = Testegabarito.query.filter_by(name_test=name_test).first()
        print(">>> Gabarito encontrado?", bool(gabarito))

        if not gabarito:
            flash('Answer key not found in database.', category='error')
            return redirect(url_for('views.nivelamento'))

        # --- Corrige o teste ---
        total_perguntas = 10
        acertos = 0

        for i in range(1, total_perguntas + 1):
            resposta_user = getattr(novo_teste, f"question_{i}", None)
            resposta_correta = getattr(gabarito, f"question_{i}", None)
            print(f"[DEBUG] Q{i}: user={resposta_user}, correta={resposta_correta}")
            if resposta_user == resposta_correta:
                acertos += 1

        percet_result = acertos / total_perguntas
        print(f">>> Resultado: {acertos}/{total_perguntas} ({percet_result:.2%})")

        # --- Salva o resultado ---
        novo_resultado = Testeresultado(
            user_id=user_id,
            name_test=name_test,
            percet_result=percet_result,
            **{f"question_{i}": getattr(novo_teste, f"question_{i}") for i in range(1, total_perguntas + 1)}
        )
        db.session.add(novo_resultado)
        db.session.commit()

        # --- Busca o último resultado e define o nível ---
        resultado = Testeresultado.query.filter_by(user_id=user_id).order_by(Testeresultado.insert_at.desc()).first()
        usuario = Usuario.query.get(user_id)

        if usuario and resultado:
            if resultado.percet_result <= 0.35:
                usuario.nivel_usuario = 'A'
                flash('You have been placed at the beginner level.', category='success')
            elif resultado.percet_result <= 0.65:
                usuario.nivel_usuario = 'B'
                flash('You have been placed at the intermediate level.', category='success')
            else:
                usuario.nivel_usuario = 'C'
                flash('You have been placed at the advanced level.', category='success')

            db.session.commit()
        else:
            flash('We had a problem. Please try again.', category='error')

        return redirect(url_for('views.conteudo'))

    # GET → Exibe a página do teste
    return render_template("nivelamento.html", usuario=current_user)

@views.route('/conteudo-post', methods=['POST'])
def conteudo_postagem():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    url = request.form.get('url')
    nivel_conteudo = request.form.get('nivel_conteudo')

    novo_conteudo = ConteudoTeste(
        titulo=titulo,
        descricao=descricao,
        url=url,
        nivel_conteudo=nivel_conteudo
    )
    db.session.add(novo_conteudo)
    db.session.commit()
    return 'Novo conteúdo postado!'