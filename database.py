import pandas as pd
#import pymongo
from uk_covid19 import Cov19API
from pymongo import MongoClient

#Client
client = MongoClient("mongodb+srv://matt:fjTrmxLnqiSqKi70@cluster0.llzxg.mongodb.net/covid_data?retryWrites=true&w=majority")
#Database
db = client["covid_data"]
#Collection
collection = db["vacc"]

#Define metric structures
#Metrics for main
metrics = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByPublishDate": "cumDeathsByPublishDate",
        "cumAdmissions" : "cumAdmissions"
    }

#Metrics for vacc
secondary_metrics = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "cumPeopleVaccinatedFirstDoseByPublishDate": "cumPeopleVaccinatedFirstDoseByPublishDate",
        "cumPeopleVaccinatedSecondDoseByPublishDate": "cumPeopleVaccinatedSecondDoseByPublishDate",
        "cumPeopleVaccinatedCompleteByPublishDate": "cumPeopleVaccinatedCompleteByPublishDate"
    }

def data_loading(this_area, this_metric):
    area_type = [this_area]
    api = Cov19API(filters=area_type, structure= this_metric)
    data = api.get_json()
    #data['date'] = pd.to_datetime(data['date'])
    #data.sort_values('date', ascending = True, inplace = True, ignore_index = True)
    return data

data_init = data_loading('areaType=', )
collection.insert_many(data_init['data'])





