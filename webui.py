# Should produce a flask hosted webapp to be able
# to interact with the assistant via a webapp input


from flask import Flask, render_template, request

class WebApp:
    def __init__(self, assistant):
        self.app = Flask(__name__)
        self._setup_routes()
        self.assistant = assistant

    def _setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            if request.method == "POST":
                user_input = request.form.get("user_input")
                return f"You entered: {user_input}"
            return render_template("index.html")

    def run(self, host="0.0.0.0", port=4200):
        self.app.run(host=host, port=port)

