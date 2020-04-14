from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/post", methods=["POST"])
def post():
    content=request.get_json(force=True)
    print type(content), content["url"]
    return content

if __name__ == "__main__":
    app.run()
