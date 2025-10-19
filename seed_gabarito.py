from website import create_app, db
from website.models import Testegabarito

app = create_app()

with app.app_context():
    nome_teste = "Teste_Proficiencia"

    gabarito_existente = Testegabarito.query.filter_by(name_test=nome_teste).first()
    if gabarito_existente:
        print("⚠️ Gabarito já existe no banco!")
    else:
        gabarito = Testegabarito(
            name_test=nome_teste,
            question_1='A',
            question_2='B',
            question_3='C',
            question_4='A',
            question_5='D',
            question_6='B',
            question_7='C',
            question_8='A',
            question_9='D',
            question_10='B'
        )
        db.session.add(gabarito)
        db.session.commit()
        print("✅ Gabarito inserido com sucesso!")
