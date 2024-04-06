import pyodbc
from flask import Flask, render_template, request
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

def connection():
    server = 'badalpatel.database.windows.net'
    database = 'badalpatel'
    username = 'badalpatel'
    password = 'Badal1302@'
    driver = '{ODBC Driver 18 for SQL Server}'
    con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return con


@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        con = connection()
        cursor = con.cursor()
        return render_template('index.html')
    except Exception as e:
        return render_template('index.html', error=e)

class First(FlaskForm):
    mag = StringField(label='Enter Magnitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/first', methods=['GET', 'POST'])
def first():
    try:
        con = connection()
        cursor = con.cursor()
        count = 0

        cursor.execute('SELECT count(*) as "Magnitude below 1.0" from earthquake where mag < 1')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result = {columns[0]: row[0]}
            count += row[0]

        cursor.execute('SELECT count(*) as "Magnitude between 1.0 to 2.0" from earthquake where mag >= 1.0 and  mag <2.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            count += row[0]

        cursor.execute('SELECT count(*) as "Magnitude between 2.0 to 3.0" from earthquake where mag >= 2.0 and mag < 3.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            count += row[0]

        cursor.execute('SELECT count(*) as "Magnitude between 3.0 to 4.0" from earthquake where mag >= 3.0 and mag < 4.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            count += row[0]

        cursor.execute('SELECT count(*) as "Magnitude between 4.0 to 5.0" from earthquake where mag >= 4.0 and mag < 5.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            count += row[0]

        cursor.execute('SELECT count(*) as "Magnitude grater than 5.0" from earthquake where mag >= 5.0')
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result[columns[0]] = row[0]
            count += row[0]

        return render_template('first.html', result=result, count=count, data=1)
    except Exception as e:
        print(e)
        return render_template('first.html', error='Error')

class Second(FlaskForm):
    data1 = StringField(label='Lower Range of Depth: ', validators=[DataRequired()])
    data2 = StringField(label='Upper Range of Depth: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/second', methods=['GET', 'POST'])
def second():
    form = Second()
    count = 0
    if form.validate_on_submit():
        try:
            con = connection()
            cursor = con.cursor()
            data1 = float(form.data1.data)
            data2 = float(form.data2.data)

            if data1 > data2:
                return render_template('second.html', form=form, error='Error')

            cursor.execute('SELECT count(*) as "Magnitude below 1.0" from earthquake where mag < 1 and depth between ? and ?', data1, data2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = {columns[0]: row[0]}
                count += row[0]

            cursor.execute('SELECT count(*) as "Magnitude between 1.0 to 2.0" from earthquake where mag >= 1.0 and  mag <2.0 and depth between ? and ?', data1, data2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Magnitude between 2.0 to 3.0" from earthquake where mag >= 2.0 and mag < 3.0 and depth between ? and ?', data1, data2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Magnitude between 3.0 to 4.0" from earthquake where mag >= 3.0 and mag < 4.0 and depth between ? and ?', data1, data2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Magnitude between 4.0 to 5.0" from earthquake where mag >= 4.0 and mag < 5.0 and depth between ? and ?', data1, data2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Magnitude above 5.0" from earthquake where mag >= 5.0 and depth between ? and ?', data1, data2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            return render_template('second.html', result=result, form=form, count=count, data1=data1, data2=data2, data=1)
        except Exception as e:
            print(e)
            return render_template('second.html', form=form, error='Error')
    return render_template('second.html', form=form)

class Third(FlaskForm):
    mag1 = StringField(label='Enter Lower Magnitude: ', validators=[DataRequired()])
    mag2 = StringField(label='EnterUpper Magnitude: ', validators=[DataRequired()])
    data1 = StringField(label='Enter Lower Depth: ', validators=[DataRequired()])
    data2 = StringField(label='Enter Upper Depth: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/third', methods=['GET', 'POST'])
def third():
    form = Third()
    count = 0
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            mag1 = float(form.mag1.data)
            mag2 = float(form.mag2.data)
            data1 = float(form.data1.data)
            data2 = float(form.data2.data)

            if data1 > data2 or mag1 > mag2:
                return render_template('third.html', form=form, error='Error')

            result = dict()

            cursor.execute('select mag,depth from earthquake where mag BETWEEN ? and ? and depth BETWEEN ? and ? order by mag,depth', mag1, mag2, data1, data2)
            for row in cursor.fetchall():
                for i in row:
                    result.setdefault(count, []).append(i)
                count += 1

            return render_template('third.html', result=result, data1=data1, data2=data2, mag1=mag1, mag2=mag2, count=count, form=form, data=1)
        except Exception as e:
            print(e)
            return render_template('third.html', form=form, error='Error')
    return render_template('third.html', form=form)

@app.route('/fourth', methods=['GET', 'POST'])
def fourth():
    count = 0
    if request.method == "POST":
        try:
            con = connection()
            cursor = con.cursor()
            clust = request.form['type']

            cursor.execute('SELECT count(*) as "Magnitude below than 1.0" from earthquake where mag < 1 and type = ?', clust)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = {columns[0]: row[0]}
                count += row[0]

            cursor.execute('SELECT count(*) as "Magnitude between 1.0 to 2.0" from earthquake where mag >= 1.0 and  mag <2.0 and type = ?', clust)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 2.0 to 3.0" from earthquake where mag >= 2.0 and mag < 3.0 and type = ?', clust)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 3.0 to 4.0" from earthquake where mag >= 3.0 and mag < 4.0 and type = ?', clust)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 4.0 to 5.0" from earthquake where mag >= 4.0 and mag < 5.0 and type = ?', clust)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            cursor.execute('SELECT count(*) as "Mag. grater than 5.0" from earthquake where mag >= 5.0 and type = ?', clust)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                count += row[0]

            return render_template('fourth.html', result=result, type=clust, count=count, data=1)
        except Exception as e:
            print(e)
            return render_template('fourth.html', error=e)
    return render_template('fourth.html')

if __name__ == "__main__":
    app.run(debug=True)