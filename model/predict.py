import pickle
import pandas as pd
# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)   
MODEL_VERSION='1.0.0'

# def predict_output(user_input:dict):
#     input_df=pd.DataFrame([user_input])
#     output=model.predict(input_df)[0]
#     return output
     
class_labels=model.classes_.tolist()

def predict_output(user_input:dict):
    
def make_prediction(data:dict)->dict:
    df=pd.DataFrame([user_input])
    
    #predict the class
    
    predicted_class=model.predict(df)[0]
    #get  probablities for all classes
    
    probablities=model.predict_proba(df)[0]
    confidence=max(probablities)
    
    #create mapping : {class name probablities}
    class_probs=dict(zip(class_labels,map(lambda p: round(p,4),probablities)))
    
    return {
        "predicted_category":predicted_class,
        "confidence":round(confidence,4),
        "class_probablities":class_probs
    }