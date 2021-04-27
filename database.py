from uk_covid19 import Cov19API
from pymongo import MongoClient

#Client
client = MongoClient("mongodb+srv://matt:fjTrmxLnqiSqKi70@cluster0.llzxg.mongodb.net/covid_data?retryWrites=true&w=majority")
#Database
db = client["covid_data"]
#Collection
collection = db["main"]

#Define metric structures
#Metrics for main - Cases/Deaths
metrics = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesBySpecimenDate": "cumCasesBySpecimenDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByPublishDate": "cumDeathsByPublishDate"
        
    }

#Metrics for other - Vaccinations/Tests
secondary_metrics = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "cumPeopleVaccinatedFirstDoseByPublishDate": "cumPeopleVaccinatedFirstDoseByPublishDate",
        "cumPeopleVaccinatedSecondDoseByPublishDate": "cumPeopleVaccinatedSecondDoseByPublishDate",
        "cumPeopleVaccinatedCompleteByPublishDate": "cumPeopleVaccinatedCompleteByPublishDate",
        "cumVirusTests": "cumVirusTests"
        #"hospitalCases": "hospitalCases"
    }

def data_loading(this_area, this_metric):
    area_type = [this_area]
    api = Cov19API(filters = area_type, structure = this_metric)
    data = api.get_json()
    return data

if __name__ == "__main__":
    data_init = data_loading('areaType=region', metrics)
    collection.insert_many(data_init['data'])

