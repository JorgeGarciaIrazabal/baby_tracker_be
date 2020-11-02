from flask import Flask
from flask_assistant import Assistant, ask, tell

app = Flask(__name__)
assist = Assistant(app, route='/')


@assist.action('greeting')
def greet_and_start():
    speech = "Hey! Are you male or female?"
    return ask(speech)


@assist.action('JorgeTest')
def greet_and_start():
    speech = "Hey! Are you male or female?"
    return tell(speech)


@assist.action('FEED')
def greet_and_start():
    speech = "Hey! Are you male or female?"
    return tell(speech)



if __name__ == '__main__':
    app.run(debug=True)