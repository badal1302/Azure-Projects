import pyodbc
from flask import Flask, render_template, request
import time
import redis
import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

def connection():    
    server = 'badalpatel.database.windows.net'
    database = 'badalpatel'
    username = 'badalpatel'
    password = 'Badal1302@'
    driver = '{ODBC Driver 18 for SQL Server}'
    conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return conn

def redisconn():
    try:
        rconn = redis.StrictRedis(host='badalpatel.redis.cache.windows.net', port=6380, password='5W6xB650wbnrwcBIgU4UAG7ibFvctUTPEAzCaF2WcsE=', ssl=True)
        return rconn
    except Exception as e:
        print(e)


@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        conn = connection()
        cursor = conn.cursor()
        rconn = redisconn()
        return render_template('index.html')
    except Exception as e:
        return render_template('index.html', error=e)


class First(FlaskForm):
    number = StringField(label='Enter number of Query Execution: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/first', methods=['GET', 'POST'])
def first():
    try:
        form = First()
        if form.validate_on_submit():
            time1 = time.time()
            conn = connection()
            cursor = conn.cursor()
            rconn = redisconn()
            number = int(form.number.data)

            if number < 1 or number > 1000:
                return render_template('first.html', form=form, error='Number must be between 1 and 1000')

            query = 'SELECT latitude from earthquake'
            key = hashlib.sha224(query.encode()).hexdigest()

            if rconn.llen(key) == 0:
                cursor.execute(query)
                rows = cursor.fetchall()
                rconn.rpush(key, str(rows))

            time1 = time.time()
            for i in range(0, number):
                cursor.execute(query)
                rows = cursor.fetchall()
            different1 = time.time() - time1

            time1 = time.time()
            for i in range(0, number):
                temp = []
                for j in range(0, rconn.llen(key)):
                    temp.append(rconn.lindex(key, j))
            different2 = time.time() - time1

            return render_template('first.html', form=form, number=number, different1=different1, different2=different2,
                                   data=1)

        return render_template('first.html', form=form)

    except Exception as e:
        print(e)
        return render_template('first.html', form=form, error='Wrong input')


class Second(FlaskForm):
    number = StringField(label='Enter Number of Query Execution: ', validators=[DataRequired()])
    magnitude1 = StringField(label='Enter Lower Magnitude Range: ', validators=[DataRequired()])
    magnitude2 = StringField(label='Enter Upper Magnitude Range: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/second', methods=['GET', 'POST'])
def second():
    try:
        form = Second()
        if form.validate_on_submit():
            time2 = time.time()
            conn = connection()
            cursor = conn.cursor()
            rconn = redisconn()
            number = int(form.number.data)
            magnitude1 = float(form.magnitude1.data)
            magnitude2 = float(form.magnitude2.data)

            if number < 1 or number > 1000:
                return render_template('second.html', form=form, error='Number must be between 1 and 1000')

            if magnitude1 > magnitude2:
                return render_template('second.html', form=form, error='Wrong input')

            rconn.flushall()
            query = f'SELECT time from earthquake where mag between {magnitude1} and {magnitude2}'
            key = hashlib.sha224(query.encode()).hexdigest()

            cursor.execute(query)
            rows = cursor.fetchall()
            rconn.rpush(key, str(rows))

            time2 = time.time()
            for i in range(0, number):
                cursor.execute(query)
                rows = cursor.fetchall()
            different1 = time.time() - time2

            time2 = time.time()
            for i in range(0, number):
                temp = []
                for j in range(0, rconn.llen(key)):
                    temp.append(rconn.lindex(key, j))
            different2 = time.time() - time2

            return render_template('second.html', form=form, number=number, magnitude1=magnitude1, magnitude2=magnitude2, different1=different1, different2=different2, data=1)

        return render_template('second.html', form=form)

    except Exception as e:
        print(e)
        return render_template('second.html', form=form, error='Wrong input')


if __name__ == '__main__':
    app.run(debug=True)
