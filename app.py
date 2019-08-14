from flask import Flask
import math
import time

app = Flask(__name__)

@app.route("/")
def home():
  return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=False, port=8080, host='0.0.0.0')
