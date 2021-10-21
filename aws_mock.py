from flask import Flask, request

app = Flask(__name__)


@app.route("/create_instances", methods=["POST"])
def create_instances():
    args = request.get_json()


if __name__ == "__main__":
    app.run(debug=True)