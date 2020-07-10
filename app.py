from flask import Flask, escape

app = Flask(__name__)

@app.route('/')
def index():
	return "Bem vindo"

@app.route('/<name>')
def hello(name):
	return f'hello {escape(name)}!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)