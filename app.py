# Class 2 Thabo Setsubi
# Backend for the final Projects
from flask import Flask, request
from flask_mail import Mail, Message
from flask_cors import CORS
from datetime import datetime
import sqlite3
import re


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("dentists.db")
        self.cursor = self.conn.cursor()
        self.init_admin_table()
        self.init_patients_table()
        self.init_illness_table()
        self.init_appointments_table()

    # Creating Database
    # Initialising admin table
    def init_admin_table(self):
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
        return self.init_admin_table

    # Initialising patients table
    def init_patients_table(self):
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
        return self.init_patients_table

    # initialising illness table with a foreign table linking to the patients
    def init_illness_table(self):
        with sqlite3.connect("dentists.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS illness ("
                         "name TEXT NOT NULL,"
                         "type TEXT NOT NULL,"
                         "description TEXT NOT NULL,"
                         "patient_id INTEGER,"
                         "CONSTRAINT fk_patients FOREIGN KEY (patient_id) REFERENCES patients(patient_id))")
            print("illness table created successfully")
        conn.close()
        return self.init_illness_table

    # initialising appointments table with a foreign key linking to the patients
    def init_appointments_table(self):
        with sqlite3.connect("dentists.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS appointments ("
                         "first_name TEXT NOT NULL,"
                         "last_name TEXT NOT NULL,"
                         "email TEXT NOT NULL,"
                         "phone_num INTEGER NOT NULL,"
                         "type TEXT NOT NULL,"
                         "booking_date DATE,"
                         "date_made DATE,"
                         "patient_id INTEGER,"
                         "CONSTRAINT fk_patients FOREIGN KEY (patient_id) REFERENCES patients(patient_id))")
            print("appointments table created successfully")
        conn.close()
        return self.init_appointments_table


Database()


# to make the data into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


app = Flask(__name__)
app.debug = True
# This is to help with the frontend
CORS(app)
# Setting up the flask mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lifechoiceslotto147@gmail.com'
app.config['MAIL_PASSWORD'] = 'lifechoices2021'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=['GET'])
def welcome():
    response = {}
    if request.method == "GET":
        response['message'] = "Welcome"
    return response


@app.route('/admin/', methods=["POST"])
def admin_registration():
    # route to register admin registration
    response = {}
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    username = request.json["username"]
    password = request.json["password"]
    # to check if email is valid
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    try:
        if request.method == "POST":
            if re.search(ex, email):
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO admin("
                                   "first_name,"
                                   "last_name,"
                                   "email,"
                                   "username,"
                                   "password) VALUES(?, ?, ?, ?, ?)",
                                   (first_name, last_name, email, username, password))
                    conn.commit()
                    response['message'] = "admin registered successfully"
                    response['status_code'] = 201
                    response['data'] = {
                        "first name": first_name,
                        "last name": last_name,
                        "email": email,
                        "username": username,
                        "password": password
                    }
                return response
        else:
            if request.method != "POST":
                response['message'] = "Incorrect method"
                response['status_code'] = 400
                return response
    except ValueError:
        response['message'] = "Incorrect values"
        response['status_code'] = 400
        return response
    except ConnectionError:
        response['message'] = "Connection Failed"
        response['status_code'] = 500
        return response
    except TimeoutError:
        response['message'] = "Connection Timeout"
        response['status_code'] = 500
        return response


@app.route('/login', methods=["PATCH"])
def login():
    response = {}
    # Login using patch method
    if request.method == "PATCH":
        username = request.json["username"]
        password = request.json["password"]

        with sqlite3.connect("dentists.db") as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
            admin = cursor.fetchone()

        response['status_code'] = 200
        response['data'] = admin
        return response
    else:
        if request.method != "PATCH":
            response['message'] = "Incorrect Method"
            response['status_code'] = 400
            return response


@app.route('/patient', methods=['POST'])
def patient_registration():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    address = request.json['address']
    email = request.json['email']
    birth_date = request.json['birth_date']
    gender = request.json['gender']
    phone_num = request.json['phone_num']
    id_num = request.json['id_num']
    start_date = datetime.now()
    response = {}
    # to check if email is valid
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    x = "Welcome to Setsubi Dentist Registry"
    try:
        if request.method == "POST":
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
                    msg = Message("Registered Successfully", sender="lifechoiceslotto147@gmail.com", recipients=[email])
                    msg.body = x
                    mail.send(msg)
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


@app.route('/appointment/<int:patient_id>', methods=["POST"])
def appointment(patient_id):
    response = {}
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone_num = request.json['phone_num']
    a_type = request.json['type']
    booking_date = request.json['booking_date']
    date_made = datetime.now()
    patient_id = patient_id
    # to check if email is valid
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if request.method == "POST":
        if re.search(ex, email):
            with sqlite3.connect("dentists.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO appointments ("
                               "first_name,"
                               "last_name,"
                               "email,"
                               "phone_num,"
                               "type,"
                               "booking_date,"
                               "date_made,"
                               "patient_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                               (first_name, last_name, email, phone_num, a_type, booking_date, date_made, patient_id))
                conn.commit()
                msg = Message("Appointment", sender="lifechoiceslotto147@gmail.com", recipients=[email])
                msg.body = "Appointment was made for:" + str(first_name) + "for the date of " + str(booking_date)
                mail.send(msg)
                response['message'] = "appointment made successfully"
                response['status_code'] = 200
                response['data'] = {
                    "first name": first_name,
                    "last_name": last_name,
                    "phone_num": phone_num,
                    "email": email,
                    "type": a_type,
                    "booking_date": booking_date,
                    "date_made": date_made,
                    "patient_id": patient_id
                }
            return response


@app.route('/view-patient/<int:patient_id>', methods=["GET"])
def view_patient(patient_id):
    response = {}
    # a route to check one patient
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
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
    # a route to check all the patients
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")

        response['status_code'] = 200
        response['message'] = "Fetched all patients"
        response['data'] = cursor.fetchall()
    return response


@app.route('/view-appointment/<int:patient_id>', methods=['GET'])
def fetch_appointment(patient_id):
    response = {}
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE patient_id=" + str(patient_id))
        date_check = cursor.fetchone()

        response['status_code'] = 200
        response['message'] = "Fetch one appointment"
        response['data'] = date_check
    return response


@app.route('/view-appointment/', methods=['GET'])
def view_appointments():
    response = {}
    # route to check all appointments
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")

        response['status_code'] = 200
        response['message'] = "Displaying appointments"
        response['data'] = cursor.fetchall()
    return response


@app.route('/illness/<int:patient_id>', methods=['POST'])
def illness(patient_id):
    response = {}
    # a route to register a patients illness
    name = request.json['name']
    ill_type = request.json['type']
    description = request.json['description']
    patient_id = patient_id
    if request.method == "POST":
        with sqlite3.connect("dentists.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO illness("
                           "name, "
                           "type, "
                           "description,"
                           "patient_id) VALUES(?, ?, ?, ?)", (name, ill_type, description, patient_id))
            conn.commit()
            response['message'] = "success"
            response['status_code'] = 200
            response['data'] = {
                "name": name,
                "type": ill_type,
                "description": description,
            }
        return response


@app.route('/view-illness/', methods=["GET"])
def view_illness():
    response = {}
    if request.method == "GET":
        with sqlite3.connect("dentists.db") as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM illness")
            ill = cursor.fetchall()
            response['data'] = ill
            response['message'] = "Success"
            response['status_code'] = 200
        return response
    else:
        if request.method != "GET":
            response['error'] = "Wrong method"
            response['status_code'] = 400
            return response


@app.route('/view-illness/<int:patient_id>')
def fetch_illness(patient_id):
    response = {}
    # a route to view a patients illness
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM illness WHERE patient_id = ?", str(patient_id))
        ill = cursor.fetchone()
        response['data'] = ill
        response['message'] = "Success"
        response['status_code'] = 200
    return response


@app.route('/delete-patient/<int:patient_id>', methods=["DELETE"])
def delete_patient(patient_id):
    response = {}
    if request.method == "DELETE":
        with sqlite3.connect("dentists.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_id=" + str(patient_id))
            conn.commit()

            response['status_code'] = 200
            response['message'] = "Patient deleted successfully"
        return response
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
            response['message'] = "Wrong Method"
            return response


@app.route("/delete-illness/<int:patient_id>", methods=["DELETE"])
def delete_illness(patient_id):
    response = {}
    if request.method == "DELETE":
        with sqlite3.connect("dentists.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM illness WHERE patient_id=" + str(patient_id))
            conn.commit()

            response['status_code'] = 200
            response['message'] = "Record deleted successfully"
        return response
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
            response['message'] = "Wrong Method"
            return response


@app.route('/delete-appointment/<int:patient_id>', methods=["DELETE"])
def delete_appointment(patient_id):
    response = {}
    if request.method == "DELETE":
        with sqlite3.connect("dentists.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE patient_id=" + str(patient_id))
            conn.commit()

            response['status_code'] = 200
            response['message'] = "Appointment deleted successfully"
        return response
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
            response['message'] = "Wrong Method"
            return response


@app.route('/edit-patient/<int:patient_id>', methods=['PUT'])
def edit_patient(patient_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect("dentists.db") as conn:
            incoming_data = dict(request.json)
            conn.row_factory = dict_factory
            put_data = {}

            if incoming_data.get("email") is not None:
                put_data['email'] = incoming_data.get("email")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE patients SET email=? WHERE patient_id=?", (put_data["email"], patient_id))
                    conn.commit()
                    response['message'] = "Updated email was successfully"
                    response['status_code'] = 200
                return response
            if incoming_data.get("address") is not None:
                put_data['address'] = incoming_data.get("address")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE patients SET address=? WHERE patient_id=?",
                                   (put_data["address"], patient_id))
                    conn.commit()
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
            if incoming_data.get("phone_num") is not None:
                put_data['phone_num'] = incoming_data.get("phone_num")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE patients SET phone_num=? WHERE patient_id=?",
                                   (put_data["phone_num"], patient_id))
                    conn.commit()
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
    else:
        if request.method != "PUT":
            response['message'] = "Wrong method"
            response['status_code'] = 400


@app.route('/edit-illness/<int:patient_id>', methods=["PUT"])
def edit_illness(patient_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect("dentists.db") as conn:
            incoming_data = dict(request.json)
            conn.row_factory = dict_factory
            put_data = {}
            if incoming_data.get("name") is not None:
                put_data["name"] = incoming_data.get("name")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE illness SET name=? WHERE patient_id=?",
                                   (put_data["name"], patient_id))
                    conn.commit()
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
            if incoming_data.get("type") is not None:
                put_data["type"] = incoming_data.get("type")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE illness SET type=? WHERE patient_id=?",
                                   (put_data["type"], patient_id))
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
            if incoming_data.get("description") is not None:
                put_data["description"] = incoming_data.get("description")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE illness SET description=? WHERE patient_id=?",
                                   (put_data["description"], patient_id))
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
    else:
        if request.method != "PUT":
            response['message'] = "Wrong method"
            response['status_code'] = 400


@app.route('/edit-appointment/<int:patient_id>', methods=["PUT"])
def edit_appointment(patient_id):
    response = {}
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if request.method == "PUT":
        with sqlite3.connect("dentists.db") as conn:
            incoming_data = dict(request.json)
            conn.row_factory = dict_factory
            put_data = {}
            if incoming_data.get("email") is not None:
                put_data["email"] = incoming_data.get("email")
                if re.search(ex, put_data["email"]):
                    with sqlite3.connect("dentists.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE appointments SET email=? WHERE patient_id=?",
                                       (put_data["email"], patient_id))
                        response['message'] = "Update successfully"
                        response['status_code'] = 200
                    return response
            if incoming_data.get("phone_num") is not None:
                put_data["phone_num"] = incoming_data.get("phone_num")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE appointments SET phone_num=? WHERE patient_id=?",
                                   (put_data["phone_num"], patient_id))
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
            if incoming_data.get("booking_date") is not None:
                put_data["booking_date"] = incoming_data.get("booking_date")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE appointments SET booking_date=? WHERE patient_id=?",
                                   (put_data["booking_date"], patient_id))
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
            if incoming_data.get("type") is not None:
                put_data["type"] = incoming_data.get("type")
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE appointments SET type=? WHERE patient_id=?",
                                   (put_data["type"], patient_id))
                    response['message'] = "Update successfully"
                    response['status_code'] = 200
                return response
    else:
        if request.method != "PUT":
            response['message'] = "Wrong method"
            response['status_code'] = 400


if __name__ == "__main__":
    app.run()
