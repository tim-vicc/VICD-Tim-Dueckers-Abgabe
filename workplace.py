from app import create_app, cli
# Erstellt Flask APP und registriert CLI-Commands
app = create_app()
cli.register(app)
