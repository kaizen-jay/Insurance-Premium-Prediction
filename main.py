from fastapi import FastAPI
from fastapi.responses import JSONResponse

import pickle 
import pandas as pd

from schema.user_input import UserInput

from config.city_tier import tier_1_cities, tier_2_cities

#importing the ml model
with open('model/model.pkl', 'rb') as f: #means we are opening the file in read binary mode
    model = pickle.load(f)
    # iss step me hamne model import kar liya hai

#Now we should also add a model version so that the aws services do know that which model we are working on 

MODEL_VERSION = '1.0.0' #ye hamne abhi manually khud se banaya hai but generally ye version ek mlflow jaise software se aata hai... to mujhe ye info bhi aage ke step me apne health check me pass karunga.

#now we will create a fast api app object

app = FastAPI()




'''now we will make a pydantic model to validate the incoming data:'''



'''Pydantic model to ban gaya
Now we will create our predict endpoint'''
#but isse pehle hame 2 endpoint aur chahiye i.e the home endpoint and the health_check endpoint for aws services.

@app.get('/') #this one is human readable but we also want services to read it so we created the second endpoint health.
def home():
    return {'message': 'Insurance Premium Prediction API'}

@app.get('/health') #this is machine readable... because like aws ki services i.e kubernetese etc, ye services iss end point pe hit karti hai and if unhe ye message ok milta hai then hamari api aws pe sahi se deploy hoti hai.
def health_check():
    return {'status': 'ok', 'version': MODEL_VERSION, 'model_loaded': model is True}



#Sabse pehle ham ek route create karnge i.e the predict route:
@app.post('/predict')
def predict_premium(data: UserInput): #yaha pe ek function create kiya by the name of predict_premium... isko input me user ka data milega by the name 'data'... aur ye 'data' kis type ka hoga? ye hamare UserInput type ka object hoga jo hamara pydantic model hai. 
#To hame request body se data aayega, vo seedha chala jayega hamare pydantic model ke paas i.e UserInput. Hamara pydantic model then usko validate karega, computed fields nikalega AUR FIR vo palat ke hame 'data' ke form me mil jayega.

    '''now that hamara model load ho chuka hai, ab hame ek proper input format create karna hai... aur hame ek row ka data pass karna hai hamarae model me... aur ye input pandas dataframe ke format me bheja jayega kyuki jo ML model hai jo rando forest model hai vo panda dataframe object ke oopar train hua hai  '''

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }]) #now we will create a panda dataframe jisme ki ham bas ek row rakhenge and usme ham ek dictionary pass karenge... in sakbo ek variable me store kar lenge by the name input_df.
    #ye ban gaya hamara input jo ham apne ml model ke paas bhejenge.

    #ab hame predicton karna hai toh:

    prediction = model.predict(input_df)[0]#oopar hamne jo model import kiya hai uske predict function ko call karenge...fir usme ham pass kar denge 'input_df'... fir isse palat ke hame list me ek output milega... aur hame uss list ka 0th item chahiye hoga... aur yahi hoga hamara 'prediction'... aur isi prediction ko hame json ke format me return karna hai... for this we will use fastapi.responses se jsonresponse

    return JSONResponse(status_code= 200, content={'predicted_category': prediction})

'''THAT'S IT, THIS IS OUR ML MODEL '''
