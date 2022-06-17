# from data import *
import re


def convert_locations(recruiter):
    locations=[]
    for key, value in recruiter.items():
        if key.startswith("L-") and (value == "x" or value=='X'):
            locations.append(key[2:])
    return locations

def convert_skills(recruiter):
    skills=[]
    for key, value in recruiter.items():
        if key.startswith("S-") and (value == "x" or value=='X'):
            skills.append(key[2:])
    return skills

def convert_hours(recruiter):
    hours=[]
    for key, value in recruiter.items():
        if re.search("^[0-2][0-3]:[0-5][0-9]", key) is not None:
            if recruiter[key]=='x' or recruiter[key]=='X':
                hours.append(key)
    return hours

def get_recruiter_list(recruiters):
    recruiter_list=[]
    for recruiter in recruiters:
        locations=convert_locations(recruiter)
        skills=convert_skills(recruiter)
        hours=convert_hours(recruiter)
        to_add={
            "EMPRESA": recruiter['EMPRESA'],
            "NOMBRE DEL RECRUITER": recruiter['NOMBRE DEL RECRUITER'],
            "EMAIL": recruiter["EMAIL"],
            "CARGO": recruiter["CARGO"],
            "LINKEDIN": recruiter["LINKEDIN"],
            "LOCATIONS":locations,
            "SKILLS":skills,
            "HOURS_DISP":hours
        }
        recruiter_list.append(to_add)
    print(recruiter_list)
    return recruiter_list


