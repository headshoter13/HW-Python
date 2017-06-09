from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from collections import Counter
import json
import requests
import re

m = Mystem()
app = Flask(__name__)

def all_verbs(text):
    analyzed = m.analyze(text)
    verbs_total = [i['analysis'][0]['lex'] for i in analyzed if i['text'].strip() \
                           and 'analysis' in i and i['analysis'] and i['analysis'][0]['gr'].split('=')[0].split(',')[0] == 'V']
    prop_verbs = len(verbs_total) / len(text.split())

    perfect = [i for i in analyzed if i['text'].strip() \
                           and 'analysis' in i and i['analysis'] and 'V,сов' in i['analysis'][0]['gr']]


    imperfect = [i for i in analyzed if i['text'].strip() \
                           and 'analysis' in i and i['analysis'] and 'V,несов' in i['analysis'][0]['gr']]

    freq_verbs = Counter(verbs_total).most_common()


    return len(verbs_total), prop_verbs, len(perfect), len(imperfect), freq_verbs  


@app.route('/verb_page', methods=['get', 'post'])

def verb_page():
    if request.form:
        text = request.form['text']
        verbs_all, prop_verbs, perfect, imperfect, freq_verbs = all_verbs(text)
        return render_template('verb_page.html', input=text, text = text,
                               verbs_all = verbs_all , prop_verbs = prop_verbs, perfect = perfect, imperfect = imperfect, freq_verbs = freq_verbs)
    return render_template('verb_page.html')


def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def checking(group):
    err = 'error'
    params = {'count':1, 'domain':group}
    result = vk_api('wall.get',**params)
    if err in result:
        print(result)
        return [('error',result['error']['error_msg'])]
    else:
        return 1

def get_words(group):
    params = {'count':1,'domain':group}
    result = vk_api('wall.get',**params)['response'][0]
    posts = min(1000,result)
    i = 0
    words = []
    while i <= posts + 100:
        params = {'count':100,'domain':group,'offset':min(i,posts),'fields':['text']}
        words += vk_api('wall.get',**params)['response'][1:]
        i += 100

    text = ''
    words = [x['text'] for x in words]
    for z in words:
        text += z + ' '
    return text

    
def hundred_words(group):
    if checking(group) == 1:
        text = get_words(group)
        text = re.sub('<.*?>', '', text)
        words = text.split()
        words = [i.lower().strip('.,!?:- ()–#') for i in words]
        number = Counter(words)
        return number.most_common(100), True
    else:
        return checking(group), False



@app.route('/vk_info', methods=['get', 'post'])
def vk():
    if request.method == 'POST':
        group = request.form['group']
        most_common, found = hundred_words(group)
        return render_template('vk_info.html',data = most_common,found = found)
    return render_template('vk_info.html',data = [])


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5009, debug=True)
    app.run(debug=True)

