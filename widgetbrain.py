import requests
import json
import os
from collections import namedtuple
from flask import Flask, render_template, session

app = Flask(__name__)

Joke = namedtuple('Joke', 'id,joke,categories')

@app.before_request
def random():
    response = requests.get("http://api.icndb.com/jokes/random?exclude=[explicit]").json()
    session['random'] = response['value']['joke']

@app.route('/')
def index():
    data = requests.get("http://api.icndb.com/jokes?exclude=[explicit]").json()
    datalist = [Joke(**k) for k in data["value"]]
    jokes = [x[1] for x in datalist]
    jokes = json.dumps(jokes[:10])
    session['jokes'] = jokes
    return render_template('index.html', value=session['random'])

@app.route('/getJokes/')
def getJokes():
    try:
        if session['jokes']:
            my_object = session['jokes']
            my_object= my_object.replace('["','').replace('"]', '').split('", "')
            return render_template('index.html', mylist=my_object,value=session['random'],title='Get Jokes From Session')
    except:
        return render_template('index.html', value=session['random'], ext='Session is not loaded. Please Press \'Reload Homepage\' Button')


@app.route('/flushJokes/')
def flushJokes():
    session.clear()
    return render_template('index.html', value='cleared')

@app.route('/getNewJokes/')
def getNewJokes():
    data = requests.get("http://api.icndb.com/jokes?exclude=[explicit]").json()
    data = data['value']
    results = []
    for i in data:
        results.append(i['joke'])
    jokes  = json.dumps(results[11:21]).replace('["','').replace('"]', '').split('", "')
    return render_template('index.html', mylist=jokes, value=session['random'], title='Get New Jokes')

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
