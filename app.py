import flask
import json
import os

# EDIT THE FOLLOWING LINE
DefaultTitle="Work in progress"

# Don't touch the code below unless you really mean to.

# Templates
hello = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>""" + DefaultTitle + """</title>
  </head>
  <body>
    <h1> {{ greeting }}  </h1>
    {% if kitten != "" %}
    <img src="/static/{{ kitten }}"/ alt="An image of a kitten should be here.">
    {% endif %}
  </body>
</html>"""

# Default configuration
defaults = { "pwd": "defaultPassword", "port": 8080, "host": '0.0.0.0', "debug": "False", "greeting": "defaultHello"}

# Flask app object
app = flask.Flask(__name__,
    static_url_path='/static',
    static_folder='static')

# Routes
@app.route("/", methods=['GET'])
def home():
  return "Hello, world!"

@app.route("/kitten", methods=['GET'])
def kitten():
  config = app.config['custom']
  return flask.render_template_string(
      hello, 
      kitten='kitten.jpg', 
      greeting = config['greeting'])

@app.route("/secret-kitten/<string:pwd>", methods=['GET'])
def secretKitten(pwd):
  config = app.config['custom']
  if pwd == config['pwd']:
    return flask.render_template_string(hello, kitten='kitten.jpg', greeting = config['greeting'] + ', and welcome to the Secret section...')
  return flask.render_template_string(hello, kitten='', greeting = 'Ah but you must know the correct password!'), 403

# Helper function
def mergeDefaultConfig(config):
  for key in defaults:
    if not key in config:
      config[key] = defaults[key]

# Entry function
def main():
  try:
    with open('config/custom.json') as custom_config_file:
      app.config['custom'] = json.load(custom_config_file)
  except FileNotFoundError:
    pass

  pwd = os.getenv("PASSWORD")
  if not pwd == None:
    app.config['custom']['pwd'] = pwd.strip()
  
  app.config['custom'] = {}
  mergeDefaultConfig(app.config['custom'])
  if not "pwd" in app.config['custom']:
    app.config['custom']

  print('Custom configuration:')
  print(json.dumps(app.config['custom']))

  app.run(debug=app.config['custom']["debug"]=="True",
      port=app.config['custom']["port"], 
      host=app.config['custom']["host"])

if __name__ == "__main__":
  main()
