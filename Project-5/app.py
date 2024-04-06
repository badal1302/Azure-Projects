import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.corpus import stopwords
from wtforms.validators import DataRequired
from nltk.stem import PorterStemmer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

def cleanfile():
    filesclean = []
    for i in os.listdir('static'):
        if i.endswith('.txt'):
            filesclean.append(i)

    port = PorterStemmer()
    token = RegexpTokenizer(r'\w+')

    for i in filesclean:
        path = f'static/{i}'
        with open(path, encoding='utf8') as file:
            x = file.read()
            x = x.replace("\n", "q1")
            token1 = token.tokenize(x)
            filter = [w for w in token1 if not w in stopwords.words('english')]
            x = " ".join(filter)
            temp = word_tokenize(x)
            arr = []
            for j in temp:
                arr.append(port.stem(j))
            a1 = " ".join(arr)
            x = a1.replace("q1", "\n")
        path = f'static/clean_files/{i}'
        with open(path, 'w', encoding='utf8') as out:
            out.writelines(x)
            
@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        count = 0
        if count == 0:
            count = 1
        form = First()  # Create an instance of the First class
        return render_template('index.html', form=form)  # Pass the form variable to the template
    except Exception as e:
        return render_template('index.html', error=e)

class First(FlaskForm):
    y = StringField(label='Enter Word: ', validators=[DataRequired()])
    submit = SubmitField(label='Search')

@app.route('/first', methods=['GET', 'POST'])
def first():
    form = First()
    if form.validate_on_submit():
        try:
            find_word = form.y.data
            find_file = []
            find_line_num = []
            find_line = []
            clean_files = []
            final_count = 0
            final = []

            for i in os.listdir('static/'):
                if i.endswith('.txt'):
                    clean_files.append(i)

            for i in clean_files:
                path = f'static/{i}'
                total_count = 0
                with open(path, encoding='utf8') as file:
                    lines = file.readlines()
                    for j in lines:
                        total_count += 1
                        if find_word in j:
                            if i not in find_file:
                                find_file.append(i)
                                final.append(final_count)
                            final_count += 1
                            find_line_num.append(total_count)
                            find_line.append(j.strip())
            find_results = zip(find_line, find_line_num)
            return render_template('first.html',find_results=find_results,find_file=find_file,form=form, find_word=find_word,data=1)

        except Exception as error:
            print(error)
            return render_template('first.html', form=form, error=error)
    return render_template('first.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5000)