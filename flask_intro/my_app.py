from flask import Flask
from flask import render_template, request, redirect
from collections import Counter

app = Flask(__name__)

@app.route('/')
def quiz():
    if request.args:
        arg = request.args
        f = open('stats.txt','w',encoding='utf-8')
        f.write(arg['name']+'-'+arg['choice']+'\n')
        f.close()
        return redirect('/result')
    return render_template('quiz.html')

@app.route('/result')
def results():
    try:
        f = open('stats.txt','r',encoding='utf-8')
        lines = f.readlines()
        names = [elem.split('-')[0].strip() for elem in lines]
        choices = [elem.split('-')[1].strip() for elem in lines]
        numb_names = dict(Counter(names))
        numb_choice = dict(Counter(choices))
        return render_template('result.html',n_n = numb_names, n_c = numb_choice)
    except:
        return ('Nothing')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5008, debug=True)
