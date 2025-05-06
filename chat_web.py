from flask import Flask, render_template, request, jsonify
from chat_for_gui import get_response

app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("chatbot.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # check for validity of text

    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
