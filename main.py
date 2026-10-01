from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle 
import pandas as pd

from schema.user_input import UserInput

from config.city_tier import tier_1_cities, tier_2_cities

from model.predict import predict_output,model, MODEL_VERSION



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

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    } #now we will create a panda dataframe jisme ki ham bas ek row rakhenge and usme ham ek dictionary pass karenge... in sakbo ek variable me store kar lenge by the name input_df.
    #ye ban gaya hamara input jo ham apne ml model ke paas bhejenge.

    #ab hame predicton karna hai toh:

    try: #yaha pe agar koi code fat-ta hai toh---
        prediction = predict_output(user_input) #oopar hamne jo model import kiya hai uske predict function ko call karenge...fir usme ham pass kar denge 'input_df'... fir isse palat ke hame list me ek output milega... aur hame uss list ka 0th item chahiye hoga... aur yahi hoga hamara 'prediction'... aur isi prediction ko hame json ke format me return karna hai... for this we will use fastapi.responses se jsonresponse
        '''try catch scenario''' # Ye jo prediction hai ye ek external file (predict.py) ki working pe depend kar raha hai Toh kabhi bhi aise scenario me hame try catch / try accept (in python) me likhna chahiye 


        return JSONResponse(status_code= 200, content={'predicted_category': prediction})

    except Exception as e: #--- ham use gracefully handle kar payenge iss tarah se.
        return JSONResponse(status_code=500, content=str(e))

'''THAT'S IT, THIS IS OUR ML MODEL'''
'''THIS IS SOME CRAZY MING OF OPENING THE MAC AND EDITING ANYTHING JUST FOR THE SAKE OF SOME GREEN DOTS 😭"
