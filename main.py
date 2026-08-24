from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
import json

app = FastAPI()

class Patient(BaseModel):

   id: Annotated[str, Field(..., description='ID of the Patient', examples=['P001'])]
   name: Annotated[str, Field(..., description='Name of the Patient', examples=['Rahul'])]
   city: Annotated[str, Field(..., description='City of the Patient', examples=['Mumbai'])]
   age: Annotated[int, Field(..., gt=0,lt=120,description='Age of the Patient')]
   gender: Annotated[str, Literal['Male', 'Female', 'others'], Field(..., description='Gender of the Patient male,female,others', examples=['male'])]
   height: Annotated[float, Field(...,gt=0, description='Height of the Patient in mtrs')]
   weight: Annotated[float, Field(..., gt=0, description='Weight of the Patient in kgs')]

   @computed_field
   @property
   def bmi(self) -> float:
       bmi = round(self.weight/(self.height**2),2)
       return bmi
   
   @computed_field
   @property
   def verdict(self) -> str:
       
       if self.bmi < 18.5:
           return 'underweight'
       elif self.bmi < 24.9:
           return 'normal'
       elif self.bmi < 29.9:
           return 'overweight'
       else:
           return 'obese'
       
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female']],Field(default=None)]
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated[Optional[float],Field(default=None,gt=0)]
def load_data():
    with open('patients.json', 'rb') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message': 'Patients Management System API'}

@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your Patients record'}


@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patients/{patient_id}')
def view_patients(patient_id: str = Path(..., description= 'ID of the patients in the DB', example='P001')):
    #load all patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patients not found')

@app.get('/sort')
def sort(sort_by: str = Query(..., description='sort on the basic of height,weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid fields select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid orders select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patinet already exists')

    #now add the patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient added sucessfully'})


@app.put('/edit{patient_id}')
def update_patients(patient_id: str, patients_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patinet not found')
    
    existing_Patients_data = data[patient_id]

    update_patients_info = patients_update.model_dump(exclude_unset=True)

    for key, value in update_patients_info.items():
        existing_Patients_data[key] = value

    existing_Patients_data['id'] = patient_id
    patinet_pydantic_obj = Patient(**existing_Patients_data)
    existing_Patients_data = patinet_pydantic_obj.model_dump(exclude='id')

    #add this dict to the data
    data[patient_id] = existing_Patients_data

    #save data
    save_data(data)

    return JSONResponse(status_code=200,content={'message': 'patients update sucessfully'})

@app.delete('/delete{patients_id}')
def delete_patients(patients_id: str):

    #load data
    data = load_data()

    if patients_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')
    
    del data[patients_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient delete sucessfully'})