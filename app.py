from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import MODEL_VERSION,predict_output


app = FastAPI()


        
@app.get('/')
def home():
    return {'message':'welcome to prediction'} 

@app.get('/health')
def health_check():
    return {'status':'ok',
            'version':MODEL_VERSION} 

@app.post('/predict')
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    try:
        
        prediction =  predict_output(user_input )

        return JSONResponse(status_code=200, content={'predicted_category': prediction})

    except Exception as r:
        return JSONResponse(status_code=500,content=str(r))


