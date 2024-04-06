import pyodbc
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from datetime import datetime as dt
from datetime import date
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import timedelta
from geopy.distance import geodesic
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

#connection with database

def connection():    
    server = 'badalpatel.database.windows.net'
    database = 'badalpatel'
    username = 'badalpatel'
    password = 'Badal1302@'
    driver = '{ODBC Driver 18 for SQL Server}'
    connect = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return connect

@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        connect = connection()
        cursor = connect.cursor()
        return render_template('index.html')
    except Exception as e:
        return render_template('index.html', error=e)
    
#que-1 find magnitude >5.0:    

class First(FlaskForm):
    magnitude = StringField(label='Enter Magnitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/first', methods=['GET', 'POST'])
def first():
    form1 = First()
    cnt = 0
    if form1.validate_on_submit():
        try:
            connect = connection()
            cursor = connect.cursor()
            magnitude = float(form1.magnitude.data)
            if magnitude <= 5.0:
                return render_template('first.html', form=form1, error="Magnitude must be > 5.0", data=0)
            cursor.execute("SELECT * FROM earthquake where mag >?", magnitude)
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                result.append(row)
                cnt += 1
            return render_template('first.html', result=result, cnt=cnt, magnitude=magnitude, form=form1, data=1)
        except Exception as e:
            print(e)
            return render_template('first.html', form=form1, error="Wrong input.", data=0)
    return render_template('first.html', form=form1)

#find records in bewteen two mag range with specified days:

class Second(FlaskForm):
    range1 = StringField(label='Enter Magnitude for Range 1: ', validators=[DataRequired()])
    range2 = StringField(label='Enter Magnitude for Range 2: ', validators=[DataRequired()])
    days = StringField(label='Enter Specific Days: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/second', methods=['GET', 'POST'])
def second():
    form = Second()
    if form.validate_on_submit():
        try:
            connect = connection()
            cursor = connect.cursor()
            range1 = float(form.range1.data)
            range2 = float(form.range2.data)
            days = int(form.days.data)
            cnt = 0
            if days > 30 or range1 > range2:
                raise Exception()
            today = date.today()
            days_ago = today - timedelta(days=days)
            print(days_ago)
            cursor.execute("SELECT * FROM earthquake where time > ? AND mag BETWEEN ? AND ?", days_ago, range1, range2)
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                result.append(row)
                cnt += 1
            return render_template('second.html', result=result, cnt=cnt, range1=range1, range2=range2, days=days, form=form, data=1)

        except Exception as e:
            print(e)
            return render_template('second.html', form=form, error="Range 1 and Range 2 must be numeric, Range 1 > Range 2 and Days must be integer and less then 31.", data=0)
    return render_template('second.html', form=form, data=0)

#search record by latitude,logitude with specific km(distance():

class Third(FlaskForm):
    latitude = StringField(label='Enter Latitude: ', validators=[DataRequired()])
    longitude = StringField(label='Enter Longitude: ', validators=[DataRequired()])
    km = StringField(label='Enter Kilometers: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/third', methods=['GET', 'POST'])
def third():
    form = Third()
    if form.validate_on_submit():
        try:
            connect = connection()
            cursor = connect.cursor()
            latitude = float(form.latitude.data)
            longitude = float(form.longitude.data)
            km = float(form.km.data)
            cnt = 0
            cursor.execute("SELECT time, latitude, longitude, mag, id, place, type FROM earthquake")
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                if geodesic((float(row[1]), float(row[2])), (latitude, longitude)).km <= km:
                    result.append(row)
                    cnt += 1
            return render_template('third.html', result=result, cnt=cnt, latitude=latitude, longitude=longitude, km=km, form=form, data=1)

        except Exception as e:
            print(e)
            return render_template('third.html', form=form, error="Latitude must be in the [-90; 90] range, Latitude must be in [-180; 180] and all input must be numaric.")
    return render_template('third.html', form=form, data=0)

#retrive records by cluster type:
 
@app.route('/fourth', methods=['GET', 'POST'])
def fourth():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            cluster = request.form['cluster']
            cnt = 0
            cursor.execute("SELECT * FROM earthquake where type = ?", cluster)
            result = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                result.append(row)
                cnt += 1
            return render_template('fourth.html', result=result, cnt=cnt, cluster=cluster, data=1)

        except Exception as e:
            print(e)
            return render_template('fourth.html', error="Error", data=0)

    return render_template('fourth.html', data=0)

#find that large mag occure more in night:

@app.route('/fifth', methods=['GET', 'POST'])
def fifth():
    cnt = 0
    tot_cnt = 0
    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('select * from earthquake where mag > 4.0')
        result = []
        while True:
            row = cursor.fetchone()
            if not row:
                break
            hour = dt.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ').hour
            if hour > 18 or hour < 7:
                result.append(row)
                cnt += 1
            tot_cnt += 1
        return render_template('fifth.html', result=result, cnt=cnt, tot_cnt=tot_cnt, data=1)

    except Exception as e:
        print(e)
        return render_template('fifth.html', error="Error", data=0)


if __name__ == "__main__":
    app.run(debug=True)