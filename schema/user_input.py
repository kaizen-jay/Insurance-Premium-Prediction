'''Pydantic model ka jo poora code hai main file me use mai yaha cut and paste karunga '''

from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated

tier_1_cities = ["Mumbai", "Delhi", "Banglore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = ["Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodra", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijaywada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]


#step 1: we will create a class 'UserInput' jo ki BaseModel se inherit karegi.:
class UserInput(BaseModel): #now isme total 7 fields hongi.... fir hame isme thode discription and validation add karne hai jo ki ham typing modele ke annotated se karenge 
    age: Annotated[int, Field(..., gt=0, lt=120, description= 'Age of the user')] #this will be an integer... and field function ko call karke ham required (...) kar denge for the input... and fir validation add kar denge of gt=0, lt=120... then we can also add description just like i did.
    weight:Annotated[float, Field(..., gt=0, description= 'Weight of the user')]
    height:Annotated[float, Field(..., gt=0, lt=2.5, description= 'Height of the user')]
    income_lpa:Annotated[float, Field(..., gt=0, description= 'Annual Salary of the user in lpa')]
    smoker:Annotated[bool, Field(..., description= 'Is user a smoker')]
    city:Annotated[str, Field(..., description= 'Residing City of the user')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description= 'Occupation of the user')] #Literal is used when we want to add options to choose from

    @field_validator('city') #field validators are used to maintain consistency. ab maan lo kisi ne small letter se city ka naam likh diya to ham use khud se capitalize karke push kar sakte hai
    @classmethod
    def normalize_city(cls, v:str) -> str:
        v = v.strip().title()
        return v
    #means hame jaise hi city mil raha hai hamare client se ham use strip kar rahe hai (means city ke pehle ya baad me koi white space hai to ham use hata rahe hai uske baad city ka jo naam aa rha hai use title case me convert kar rahe hai and then use return kar de rahe hai)

    #now mujhe above features se new features banane hai i.e for eg. height and weight se mujhe bmi banana hai to mai use karunga computed fields ka just like:
    @computed_field
    @property
    #now we will create a new function by the name of bmi:
    def bmi(self) -> float: #isme hame ek self object mil raha hai and jo palat ke mil raha hai i.e a float, and ye function mujhe return kar raha hai:
        return self.weight/(self.height**2)
    #Ye ban gayi hamari first computed field.

    #now we will create another computed field by the name lifestyle risk:
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    #Ye ban gayi hamari lifestyle risk computed field

    #Now we will create another computed field by the name age group:
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age <25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
    #ye ban gayi hamari age group ki computed field.

    #Now we will create another computed field named city tier:
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in 'tier_1_cities':
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

    #Computed fields can be said as features that we add, and this as a whole is called feature engineering.