# Class 2 Thabo Setsubi
# Backend for the final Projects
from flask import Flask, request, redirect
from flask_mail import Mail, Message
from flask_cors import CORS
from datetime import datetime
import sqlite3
import re


# Creating Database
# Initialising admin table
def init_admin_table():
    conn = sqlite3.connect('dentists.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "first_name TEXT NOT NULL,"
                 "last_name TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("admin table created successfully")
    conn.close()


# Initialising patients table
def init_patients_table():
    with sqlite3.connect("dentists.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS patients (patient_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "first_name TEXT NOT NULL,"
                     "last_name TEXT NOT NULL,"
                     "address TEXT NOT NULL,"
                     "email TEXT NOT NULL,"
                     "birth_date DATE,"
                     "gender TEXT NOT NULL,"
                     "phone_num INTEGER NOT NULL,"
                     "id_num INTEGER NOT NULL,"
                     "start_date DATE)")
        print("patients table created successfully")
    conn.close()


def init_illness_table():
    with sqlite3.connect("dentists.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS illness ("
                     "name NOT NULL,"
                     "type NOT NULL,"
                     "description NOT NULL,"
                     "patient_id INTEGER,"
                     "CONSTRAINT fk_patients FOREIGN KEY (patient_id) REFERENCES patients(patient_id))")
        print("illness table created successfully")
    conn.close()


init_admin_table()
init_patients_table()
init_illness_table()


app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def welcome():
    return "Welcome To The Dentist Registry"


@app.route('/patient', methods=['POST'])
def patient_registration():
    global phone_num, id_num
    response = {}
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    try:
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            email = request.form['email']
            birth_date = request.form['birth_date']
            gender = request.form['gender']
            phone_num = request.form['phone_num']
            id_num = request.form['id_num']
            start_date = datetime.now()
            if re.search(ex, email):
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO patients("
                                   "first_name,"
                                   "last_name,"
                                   "address,"
                                   "email,"
                                   "birth_date,"
                                   "gender,"
                                   "phone_num,"
                                   "id_num,"
                                   "start_date) VALUES(?,?,?,?,?,?,?,?,?)",
                                   (first_name, last_name, address, email, birth_date,
                                    gender, int(phone_num), int(id_num), start_date))
                    conn.commit()
                    response['message'] = "Registered patient successfully"
                    response['data'] = {
                        "first name": first_name,
                        "last_name": last_name,
                        "address": address,
                        "email": email,
                        "birth date": birth_date,
                        "gender": gender,
                        "phone number": phone_num,
                        "id number": id_num,
                        "start date": start_date
                    }
                    response['status_code'] = 201
                return response
        else:
            if request.method != "POST":
                response['error'] = "Wrong method, it must be a POST"
    except ValueError:
        if phone_num != int or id_num != int:
            response['error_message'] = "Values or not in a number"
            response['status_code'] = 400
        return response
    except ConnectionError:
        response['message'] = "No Connection"
        return response


@app.route('/view-patient/<int:patient_id>', methods=["GET"])
def view_patient(patient_id):
    response = {}
    with sqlite3.connect("dentists.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id=" + str(patient_id))
        patient = cursor.fetchone()
        response['data'] = patient
        response['message'] = "Fetched the patient successfully"
        response['status_code'] = 200
    return response


@app.route('/view-patient/', methods=['GET'])
def fetch_patients():
    response = {}
    with sqlite3.connect("dentists.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")

        response['status_code'] = 200
        response['message'] = "Fetched all patients"
        response['data'] = cursor.fetchall()
    return response


if __name__ == "__main__":
    app.run()
