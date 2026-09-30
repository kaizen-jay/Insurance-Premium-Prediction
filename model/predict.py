import pickle
import pandas as pd

#importing the ml model
with open('model/model.pkl', 'rb') as f: #means we are opening the file in read binary mode
    model = pickle.load(f)
    # iss step me hamne model import kar liya hai

#Now we should also add a model version so that the aws services do know that which model we are working on 

MODEL_VERSION = '1.0.0' #ye hamne abhi manually khud se banaya hai but generally ye version ek mlflow jaise software se aata hai... to mujhe ye info bhi aage ke step me apne health check me pass karunga.

#Get class labels from model (imp for matching probabilities to class names)
class_labels = model.classes_.tolist()

#now ham ek naya function banayenge by the name predict_output

def predict_output(user_input: dict): #means predict_output ko apna kaam karne ke liye ek user_input dictionary milegi.
#sabse pehle hame is dictionary ko dataframe me convert karna hai:
    df = pd.DataFrame([user_input]) #iss dataframe ko hamne ek variable me store kar liya.. aur hamne user input ko as a list diya hai kyuki daraframe input ko as a row lera hai.

    #predict the class
    predicted_class = model.predict(df)[0]

    #get probabilities for all classes 
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    #create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return{
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }
    