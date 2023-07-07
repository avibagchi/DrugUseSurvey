import random
import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def GPT (prompt):
    message = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message,
        temperature=0.2,
        max_tokens=1000,
        frequency_penalty=0.0
    )
    return response


df = pd.DataFrame(columns=["Age", "Gender", "Race", "Education"])
count = 1
while count <= 100:
    demographic_arr = []
    age_arr = ["18-24", "25-34", "35-44", "45-54", "55 or above"]
    gender_arr = ["Male", "Female", "Non-binary/third gender", "Transgender Male", "Transgender Female"]
    race_arr = ["American Indian/Alaska Native", "Asian", "Black",
                "Native Hawaiian/other Pacific Islander", "White"]
    education_arr = ["High School or below", "Associate's degree", "Bachelor's degree", "Master's degree", "PhD"]
    age = age_arr[random.randint(0, 4)]
    gender = gender_arr[random.randint(0, 4)]
    race = race_arr[random.randint(0, 4)]
    education = education_arr[random.randint(0, 4)]
    demographic_arr.append(age)
    demographic_arr.append(gender)
    demographic_arr.append(race)
    demographic_arr.append(education)
    df.loc[len(df)] = demographic_arr
    count += 1
    prompt = "You are " + age + " years old." + " You are a " + race + " " + gender + "."

    res = GPT(prompt + "Have you ever used recreational drugs")
