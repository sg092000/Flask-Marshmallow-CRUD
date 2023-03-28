from flask import Flask , request , redirect , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:admin1234@localhost:5432/Hospital_CRUD'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Patient(db.Model):
    PatientId = db.Column(db.Integer, primary_key=True)
    PatientFirstName = db.Column(db.String(45), nullable=False)
    PatientLastName = db.Column(db.String(45), nullable=False)
    SufferingFrom = db.Column(db.String(45), nullable=False)
    DoctorAssigned = db.Column(db.String(45), nullable=False)
    PhoneNumber = db.Column(db.String(10), nullable=False)
    AdmitDate = db.Column(db.Date(),nullable = False)
    Address = db.Column(db.String(100), nullable=False)
    WardNo = db.Column(db.Integer)
    BedNo = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Patient(PatientId={self.PatientId}, PatientFirstName='{self.PatientFirstName}', PatientLastName='{self.PatientLastName}')"

with app.app_context():
    db.create_all()

class PatientSchema(ma.Schema):
    class Meta:
        fields = ("PatientId", "PatientFirstName", "PatientLastName", "SufferingFrom", "DoctorAssigned", "PhoneNumber", "AdmitDate", "Address", "WardNo", "BedNo")

Patient_Schema = PatientSchema()
Patients_Schema = PatientSchema(many=True)

class PatientList(Resource):
    def get(self):
        try:
            patients = Patient.query.all()
            result = Patients_Schema.dump(patients)
            return jsonify(result)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
    
    def post(self):
        try:
            NewPatient = Patient (
                PatientId = request.json["PatientId"],
                PatientFirstName = request.json["PatientFirstName"],
                PatientLastName = request.json["PatientLastName"],
                SufferingFrom = request.json["SufferingFrom"],
                DoctorAssigned = request.json["DoctorAssigned"],
                PhoneNumber = request.json["PhoneNumber"],
                AdmitDate = request.json["AdmitDate"],
                Address = request.json["Address"],
                WardNo = request.json["WardNo"],
                BedNo = request.json["BedNo"]
            )
            db.session.add(NewPatient)
            db.session.commit()
            Patient_Schema.dump(NewPatient)
            return {"Message" : "Successfully Added your record."},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
class PatientResource(Resource):
    def get(self, PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            Result = Patient_Schema.dump(patient)
            return jsonify(Result)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
    def patch(self, PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            user_data = Patient_Schema.load(request.get_json(), partial=True)

            """if "PatientId" in request.json:
                patient.PatientId = request.json["PatientId"]
            if "PatientFirstName" in request.json:
                patient.PatientFirstName = request.json["PatientFirstName"]
            if "PatientLastName" in request.json:
                patient.PatientLastName = request.json["PatientLastName"]
            if "SufferingFrom" in request.json:
                patient.SufferingFrom = request.json["SufferingFrom"]
            if "DoctorAssigned" in request.json:
                patient.DoctorAssigned = request.json["DoctorAssigned"]
            if "PhoneNumber" in request.json:
                patient.PhoneNumber = request.json["PhoneNumber"]
            if "AdmitDate" in request.json:
                patient.AdmitDate = request.json["AdmitDate"]
            if "Address" in request.json:
                patient.Address = request.json["Address"]
            if "WardNo" in request.json:
                patient.WardNo = request.json["WardNo"]
            if "BedNo" in request.json:
                patient.BedNo = request.json["BedNo"]"""
            db.session.commit()
            return Patient_Schema.dump(user_data)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
    
    def put(self,PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            updated_patient = Patient_Schema.load(request.json)
            db.session.commit()
            return Patient_Schema.dump(updated_patient)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
    def delete(self, PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                    return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            db.session.delete(patient)
            db.session.commit()
            return {"Message" : "Successfully Deleted your record."},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
    
    
api.add_resource(PatientList, "/AllPatients/")
api.add_resource(PatientResource, "/Patients/<int:PatientId>/")

if __name__ == "__main__":
    app.run(debug=True)