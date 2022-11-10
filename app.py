from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
# load python-dotenv
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

GCP_MYSQL_HOSTNAME = os.getenv('GCP_MYSQL_HOSTNAME')
GCP_MYSQL_USER = os.getenv('GCP_MYSQL_USER')
GCP_MYSQL_PASSWORD = os.getenv('GCP_MYSQL_PASSWORD')
GCP_MYSQL_DATABASE = os.getenv('GCP_MYSQL_DATABASE')

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + GCP_MYSQL_USER+ ':' + GCP_MYSQL_PASSWORD + '@' + GCP_MYSQL_HOSTNAME + ':3306/patient_portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '87378742'

db.init_app(app)




###Models

class Patients(db.Model):
    __tablename__ = 'production_patients'
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    dob = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    contact_mobile = db.Column(db.String(255))
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, mrn, first_name, last_name):
        self.mrn = mrn
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.contact_mobile = contact_mobile
    # this second function is for the API endpoints to return JSON 
    def to_json(self):
        return {
            'id': self.id,
            'mrn': self.mrn,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.dob,
            'gender': self.gender,
            'contact_mobile': self.contact_mobile
        }



class Conditions_patient(db.Model):
    __tablename__ = 'patient_conditions'
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(255), db.ForeignKey('production_patients.mrn'))
    icd10_code = db.Column(db.String(255), db.ForeignKey('conditions.icd10_code')) ###make sure this line is correct
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, mrn, icd10_code):
        self.mrn = mrn
        self.icd10_code = icd10_code
    # this second function is for the API endpoints to return JSON
    def to_json(self):
        return {
            'id': self.id,
            'mrn': self.mrn,
            'icd10_code': self.icd10_code
        }

class Conditions(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    icd10_code = db.Column(db.String(255))
    icd10_description = db.Column(db.String(255))
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, icd10_code, icd10_description):
        self.icd10_code = icd10_code
        self.icd10_description = icd10_description
    # this second function is for the API endpoints to return JSON
    def to_json(self):
        return {
            'id': self.id,
            'icd10_code': self.icd10_code,
            'icd10_description': self.icd10_description
        }




class Medications_patient(db.Model):
    __tablename__ = 'patient_medications'
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(255), db.ForeignKey('production_patients.mrn'))
    med_ndc = db.Column(db.String(255), db.ForeignKey('medications.med_ndc'))
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, mrn, med_ndc):
        self.mrn = mrn
        self.med_ndc = med_ndc
    # this second function is for the API endpoints to return JSON
    def to_json(self):
        return {
            'id': self.id,
            'mrn': self.mrn,
            'med_ndc': self.med_ndc
        }
    
class Medications(db.Model):
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True)
    med_ndc = db.Column(db.String(255))
    med_human_name = db.Column(db.String(255))
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, med_ndc, med_human_name):
        self.med_ndc = med_ndc
        self.med_human_name = med_human_name
    # this second function is for the API endpoints to return JSON
    def to_json(self):
        return {
            'id': self.id,
            'med_ndc': self.med_ndc,
            'med_human_name': self.med_human_name
        }




class Patient_treatment_procedures(db.Model):
    __tablename__ = 'patient_treatment_procedures'
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(255), db.ForeignKey('production_patients.mrn'))
    cpt_code = db.Column(db.String(255), db.ForeignKey('treatment_procedures.cpt_code'))
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, mrn, cpt_code):
        self.mrn = mrn
        self.cpt_code = cpt_code
    # this second function is for the API endpoints to return JSON
    def to_json(self):
        return {
            'id': self.id,
            'mrn': self.mrn,
            'cpt_code': self.cpt_code
        }


class Treatment_procedures(db.Model):
    __tablename__ = 'treatment_procedures'
    id = db.Column(db.Integer, primary_key=True)
    cpt_code = db.Column(db.String(255))
    cpt_description = db.Column(db.String(255))
    # this first function __init__ is to establish the class for python GUI
    def __init__(self, cpt_code, cpt_description):
        self.cpt_code = cpt_code
        self.cpt_description = cpt_description
    # this second function is for the API endpoints to return JSON
    def to_json(self):
        return {
            'id': self.id,
            'cpt_code': self.cpt_code,
            'cpt_description': self.cpt_description
        }



#### BASIC ROUTES WITHOUT DATA PULSL FOR NOW ####
@app.route('/')
def index():
    return render_template('landing.html') ##change templates

@app.route('/signin')
def signin():
    return render_template('/signin.html') ##change templates




##### CREATE BASIC GUI FOR CRUD #####
@app.route('/patients', methods=['GET'])
def get_gui_patients():
    returned_Patients = Patients.query.all() # documentation for .query exists: https://docs.sqlalchemy.org/en/14/orm/query.html
    return render_template("patient_all.html", patients = returned_Patients)

# this endpoint is for inserting in a new patient
@app.route('/insert', methods = ['POST'])
def insert(): # note this function needs to match name in html form action 
    if request.method == 'POST':
        mrn = request.form['mrn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        contact_mobile = request.form['contact_mobile']
        new_patient = Patients(mrn, first_name, last_name, gender, contact_mobile)
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient Inserted Successfully")
        return redirect(url_for('get_gui_patients'))
    else:
        flash("Something went wrong")
        return redirect(url_for('get_gui_patients'))

# this endpoint is for updating our patients basic info 
@app.route('/update', methods = ['GET', 'POST'])
def update(): # note this function needs to match name in html form action
    if request.method == 'POST':
        ## get mrn from form
        form_mrn = request.form.get('mrn')
        patient = Patients.query.filter_by(mrn=form_mrn).first()
        patient.first_name = request.form.get('first_name')
        patient.last_name = request.form.get('last_name')
        patient.gender = request.form.get('gender')
        patient.contact_mobile = request.form.get('contact_mobile')
        db.session.commit()
        flash("Patient Updated Successfully")
        return redirect(url_for('get_gui_patients'))

#This route is for deleting our patients
@app.route('/delete/<string:mrn>', methods = ['GET', 'POST'])
def delete(mrn): # note this function needs to match name in html form action
    patient = Patients.query.filter_by(mrn=mrn).first()
    print('Found patient: ', patient)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient Deleted Successfully")
    return redirect(url_for('get_gui_patients'))


#This route is for getting patient details
@app.route('/details/<string:mrn>', methods = ['GET'])
def get_patient_details(mrn):
    patient_details = Patients.query.filter_by(mrn=mrn).first()
    patient_conditions = Conditions_patient.query.filter_by(mrn=mrn).all()
    patient_medications = Medications_patient.query.filter_by(mrn=mrn).all()
    db_conditions = Conditions.query.all()
    db_medications = Medications.query.all()
    return render_template("patient_details.html", patient_details = patient_details, 
        patient_conditions = patient_conditions, patient_medications = patient_medications,
        db_conditions = db_conditions, db_medications = db_medications)


# this endpoint is for updating ONE patient condition
@app.route('/update_conditions', methods = ['GET', 'POST'])
def update_conditions(): # note this function needs to match name in html form action
    if request.method == 'POST':
        ## get mrn from form
        form_id = request.form.get('id')
        print('form_id', form_id)
        form_icd10_code = request.form.get('icd10_code')
        print('form_icd10_code', form_icd10_code)
        patient_condition = Conditions_patient.query.filter_by(id=form_id).first()
        print('patient_condition', patient_condition)
        patient_condition.icd10_code = request.form.get('icd10_code')
        db.session.commit()
        flash("Patient Condition Updated Successfully")
        ## then return to patient details page
        return redirect(url_for('get_patient_details', mrn=patient_condition.mrn))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)