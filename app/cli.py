from flask_apidoc.commands import GenerateApiDoc  # Lädt das Werkzeug zur Generierung der API-Doku.


def register(app):
    @app.cli.group()  # Definiert die Befehlsgruppe für entsprechende commands
    def docs():
        """API documentation commands.""" #Da dies eine Befehlsgruppe ist, ist diese Leer und mit einem PLatzhalter versehen
        pass
    @docs.command()
    # Dies sind die Befehle für apidoc, in diesem falle der erstellungsbefehl welcher die Dokumentatiosseite erstellt
    def generate():
        """Compile apidoc"""
        GenerateApiDoc("./app", "app/static/docs").run()
