from flask import Flask, render_template, request

class WebApp:
    def __init__(self, assistant=None):
        self.app = Flask(__name__)
        self._setup_routes()
        self.assistant = assistant

    def _setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            user_input = None
            response = None
            if request.method == "POST":
                user_input = request.form.get("user_input")
                if self.assistant:
                    response = self.assistant.mainLoop(inputTxt=user_input, webApp=True)

                print("Received input:", user_input)
            return render_template("index.html", messages=response)

    def run(self, host="0.0.0.0", port=4200):
        self.app.run(host=host, port=port, debug=True)
