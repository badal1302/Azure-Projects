from flask import Flask, render_template, request
import csv
import os
import ctypes  # An included library with Python install.  

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/add", methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route("/data", methods=['GET', 'POST'])
def data():

    if request.method == 'POST':
        data1 = []
        csv_data = request.files['csvfile']
        csv_file_path = os.path.join('static','people.csv')
        csv_data.save(csv_file_path)
        with open(csv_file_path) as file:
            csv_data = csv.DictReader(file)
            for r in csv_data:
                data1.append(r)
        return render_template('data.html', data=data1)


@app.route("/findpic", methods=['GET', 'POST'])
def findpic():
    return render_template('findpic.html')

@app.route("/find", methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        name1 = request.form['name']
        print(name1);
        csv_reader1 = csv.DictReader(open('static/people.csv'))
        print(csv_reader1)
        temp_pathhh = ''
        for r in csv_reader1:
            print(r)
            if name1 == r['Name']:
                temp_pathhh = '../static/' + r['Picture']
        if temp_pathhh != '':
            return render_template('findpic.html', image_path=temp_pathhh, message="found")
        else:
            return render_template('findpic.html', error="Picture not found")

@app.route("/searchpicbysal", methods=['GET', 'POST'])
def searchpicbysal():
    csv_reader1 = csv.DictReader(open('static/people.csv'))
    temp_pathhh = []
    for r in csv_reader1:
        if r['Salary'] == '' or r['Salary'] == ' ':
            r['Salary'] = 99000;
        if int(float(r['Salary'])) < 99000:
            if r['Picture'] != ' ':
                temp_pathhh.append('static/' + r['Picture'])
                print(temp_pathhh)
                print(int(float(r['Salary'])))

    print(len(temp_pathhh))
    if temp_pathhh != '':
        return render_template('searchpicbysal.html', image_path=temp_pathhh,  message="found")

    else:
        return render_template('searchpicbysal.html', error="Picture not found")
    
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')

@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails():
    if request.method == 'POST':
        name1 = request.form['name']
        csv_reader1 = csv.DictReader(open('static/people.csv'))
        temp_name = ''
        for r in csv_reader1:
            if name1 == r['Name']:
                temp_name = name1
        if temp_name != '':
            return render_template('display.html', name1=temp_name)
        else:
            return render_template('display.html', error="No Record Found!")

@app.route("/updatedetails", methods=['GET', 'POST'])
def updatedetails():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        file = request.files['picture']
        file.save('static/'+file.filename)
        keyword = request.form['keyword']
        cnt = 0

        temp = [name, state, salary, grade, room, file.filename, keyword]
        line = list()
        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    line.append(temp)
                else:
                    line.append(r)
                cnt += 1

            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

            if cnt!= 0:
                return render_template('display.html', update="Record Updated.")
            else:
                return render_template('display.html', error="No Record Found!")


@app.route("/remove", methods=['GET', 'POST'])
def remove():
    return render_template('remove.html')

@app.route("/removedetails", methods=['GET', 'POST'])
def removedetails():
    if request.method == 'POST':
        name = request.form['name']
        cntt = 0
        line = list()
        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                line.append(r)
                if name == r[0]:
                    line.remove(r)
                    cntt+=1

            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

        if cntt != 0:
            return render_template('removedetails.html', message="Record Removed")
        else:
            return render_template('removedetails.html', error="Record Not Found.")

@app.route("/uploadpic", methods=['GET', 'POST'])
def remove1():
    return render_template('uploadpic.html')

@app.route("/uploadnew", methods=['GET', 'POST'])
def uploadnew():
    if request.method == 'POST':
        name = request.form['name']
        csv_file_path = os.path.join('static', 'people.csv')
        temp_path = ''
        
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if name == row['Name']:
                    temp_path = '../static/' + row['Picture']
                    break
        
        if temp_path != '':
            file = request.files['img']
            filename = file.filename  # Get the filename directly
            
            file.save('static/' + filename)
            
            # Update the CSV file with the new image file name
            with open(csv_file_path, 'r') as file:
                rows = list(csv.reader(file))
                for row in rows:
                    if row[0] == name:
                        row[6] = filename
            
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            
            return render_template('uploadpic.html', msg="Image uploaded successfully.")
        else:
            return render_template('uploadpic.html', error="No record found for the given name.")

if __name__ == "__main__":

    app.run(debug=True)