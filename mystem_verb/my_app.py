from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from collections import Counter

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


@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form['text']
        verbs_all, prop_verbs, perfect, imperfect, freq_verbs = all_verbs(text)#.replace('\n', '<br>')
        return render_template('index_page.html', input=text, text = text,
                               verbs_all = verbs_all , prop_verbs = prop_verbs, perfect = perfect, imperfect = imperfect, freq_verbs = freq_verbs)
    return render_template('index_page.html')


if __name__ == '__main__':
    app.run(debug=True)

