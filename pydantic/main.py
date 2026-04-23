from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel, Field,computed_field
from typing import Annotated,Literal, Optional
from fastapi.responses import JSONResponse
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    
    name:Annotated[str,Field(...,description='name of the patient')]
    
    city:Annotated[str,Field(...,description='city where pt is living')]
    age:Annotated[int,Field(...,gt=0,lt=50,description='age of the patient')]
    gender:Annotated[Literal['male','femal','others'],Field(...,description='gender of the pt')]
    height:Annotated[float,Field(...,gt=0,description='height of the patient in m')]
    weight:Annotated[float,Field(...,gt=0,description='height of the patient in kg')]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/self.height**2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi<18.5:
            return 'under 18'
        elif self.bmi<25:
            return 'normal'
        else:
            return 'obesase'
 
class PatientUpdate(BaseModel):
        name:Annotated[Optional[str],Field(default=None)]
        city:Annotated[Optional[str],Field(default=None)]
        age:Annotated[Optional[int],Field(default=None,gt=0)]
        gender:Annotated[Optional[Literal['male','female']],Field(default=None)]
        height:Annotated[Optional[float],Field(default=None,gt=0)]
        weight:Annotated[Optional[float],Field(default=None,gt=0)]
        
def load_data():
        with open('patients.json','r')as f:
            data=json.load(f)
        return data
    
def save_data(data):
    with open('patients.json','w')as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {".":"management system"}


@app.post("/create")
def create_patient(patient:Patient):
    #loadPatient. existing data
    data=load_data()
    #check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='pt already exist')
    #new patient add to database
    data[patient.id]=patient.model_dump(exclude=['id'])
    #save the data
    save_data(data)
    return JSONResponse(status_code=201, content="successfully")


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='detail not found')
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value
    # existing_patient_info -> pydantic object -> bmi + verdict 
    existing_patient_info['id']=patient_id
    patient_pydantic_obj=Patient(**existing_patient_info)
    
    # -> pydantic object -> dict
    existing_patient_info= patient_pydantic_obj.model_dump(exclude='id')
    
    data[patient_id]=existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200,content='updtaed')


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content='ok')