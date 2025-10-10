from website.__init__ import create_app

# O ambiente local está como padrão,
# Caso queira utilizar o ambiente remoto, basta subistituir por:
# app = create_app("remoto") ou app = create_app(ambiente="remoto")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

