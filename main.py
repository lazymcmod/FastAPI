from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'rb') as f:
        data = json.load(f)
    return data

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