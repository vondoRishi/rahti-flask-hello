import flask
import json

app = flask.Flask(__name__,
    static_url_path='/static',
    static_folder='static')

hello = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Hello</title>
  </head>
  <body>
    <h1> {{ greeting }}  </h1>
    {% if kitten != "" %}
    <img src="/static/{{ kitten }}"/ alt="An image of a kitten should be here.">
    {% endif %}
  </body>
</html>
"""


@app.route("/", methods=['GET'])
def home():
  return "Hello, world!"

@app.route("/kitten", methods=['GET'])
def kitten():
  return flask.render_template_string(hello, kitten='kitten.jpg', greeting = 'Hello')

@app.route("/secret-kitten/<string:pwd>", methods=['GET'])
def secretKitten(pwd):
  if pwd == app.config['custom']['pwd']:
    return flask.render_template_string(hello, kitten='kitten.jpg', greeting = 'Hello, and welcome to the Secret section...')
  return flask.render_template_string(hello, kitten='', greeting = 'Ah but you must know the correct password!'), 403

if __name__ == "__main__":
  try:
    with  open('config/custom.json') as custom_config_file:
      app.config['custom'] = json.load(custom_config_file)
  except FileNotFoundError:
    app.config['custom'] = {"pwd": "defaultPassword"}

  print('Custom configuration:')
  print(json.dumps(app.config['custom']))
  app.run(debug=True, port=8080, host='0.0.0.0')
