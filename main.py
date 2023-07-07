import random
import pandas as pd
import openai
import os
from dotenv import load_dotenv
import re
from fuzzywuzzy import process
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt(prompt):
    role = "Your job is to fill out a drug use survey."

    messages = [{"role": "system", "content": role},
              {"role": "user", "content": prompt}]

    output = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )
    return output["choices"][0]["message"]["content"]

# def regex (exp, text):
#     matches = re.findall(exp, text)
#     if matches:
#         return matches[0]
#     else:
#         return "None"

def fuzzyMatch(choices, text):
    processed_choices = [re.sub(r'\W+', '', choice.lower()) for choice in choices]
    processed_text = re.sub(r'\W+', '', text.lower())
    best_match = process.extractOne(processed_text, processed_choices)
    choice = choices[processed_choices.index(best_match[0])]
    return choice


df = pd.DataFrame(columns=["Age", "Gender", "Race", "Education", "Drugs?", "Type of Drug", "Frequency",
                           "Reason", "Risk", "Learning More"])

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

    count += 1
    prompt = "You are " + age + " years old." + " You are a " + race + " " + gender + "."

    new_prompt = prompt + " Have you ever used recreational drugs? Only respond Yes or No"
    res = gpt(new_prompt)
    ex = fuzzyMatch(["Yes", "No"], res)
    demographic_arr.append(fuzzyMatch(["Yes", "No"], res))


    new_prompt = prompt + " What types of recreational drugs have you used out of the following choices: " \
                          "Marijuana, Cocaine, LSD, Ecstasy, Methamphetamine, Non-medical Prescription Drugs. " \
                          "Only pick one choice."
    res = gpt(new_prompt)
    choices = [
        "Marijuana",
        "Cocaine",
        "LSD",
        "Ecstasy",
        "Methamphetamine",
        "Non-medical Prescription Drugs"
    ]
    demographic_arr.append(fuzzyMatch(choices, res))

    new_prompt = prompt + " How frequently do you currently use recreational drugs out of the following choices: " \
                          "Daily, Weekly, Monthly, Less than monthly" \
                          "Only pick one choice."
    res = gpt(new_prompt)
    choices = [
        "Daily",
        "Weekly",
        "Monthly",
        "Ecstasy",
        "Less than monthly",
    ]
    demographic_arr.append(fuzzyMatch(choices, res))

    new_prompt = prompt + " What is your primary reason for using recreational drugs?" \
                          "Recreation, Curiosity, Socializing, Stress coping, Peer pressure" \
                          "Only pick one choice."
    res = gpt(new_prompt)
    choices = [
        "Recreation",
        "Curiosity",
        "Socializing",
        "Stress coping",
        "Peer pressure",
    ]
    demographic_arr.append(fuzzyMatch(choices, res))

    new_prompt = prompt + " Are you aware of the potential risks and health consequences associated with drug use?" \
                          " Only respond Yes or No."
    res = gpt(new_prompt)
    demographic_arr.append(fuzzyMatch(["Yes", "No"], res))

    new_prompt = prompt + " Would you be interested in learning more about the risks and health consequences of drug use?" \
                          " Only respond Yes or No."
    res = gpt(new_prompt)
    demographic_arr.append(fuzzyMatch(["Yes", "No"], res))
    df.loc[len(df)] = demographic_arr

df.to_csv("output.csv")

