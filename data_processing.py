import pandas as pd
import numpy as np
import pymongo
import random
from pymongo import MongoClient
from database import metrics, secondary_metrics

#Re-establish database connection
client = MongoClient("mongodb+srv://matt:fjTrmxLnqiSqKi70@cluster0.llzxg.mongodb.net/covid_data?retryWrites=true&w=majority")
db = client["covid_data"]
main_coll = db["main1"]
other_coll = db["other1"]

#List of all metrics
all_metrics = {
        "newCasesByPublishDate",
        "cumCasesBySpecimenDate",
        "newDeathsByDeathDate",
        "cumDeathsByPublishDate",
        "cumPeopleVaccinatedFirstDoseByPublishDate",
        "cumPeopleVaccinatedSecondDoseByPublishDate",
        "cumPeopleVaccinatedCompleteByPublishDate",
        "cumVirusTests"
    }

#Prompting and validating metric input
def metric_select():
    print("Metrics available for visualisation: \n"
          "newCasesByPublishDate \n"
          "cumCasesBySpecimenDate \n"
          "newDeathsByDeathDate \n"
          "cumDeathsByPublishDate \n"
          "cumPeopleVaccinatedFirstDoseByPublishDate \n"
          "cumPeopleVaccinatedSecondDoseByPublishDate \n"
          "cumPeopleVaccinatedCompleteByPublishDate \n"
          "cumVirusTests \n"
          )
    
    chosen_metric = input("Please enter one of the above metrics: \n")

    if chosen_metric in all_metrics:
        print("\n" + chosen_metric + " selected")
    else:
        print("\n===========================================\n"
              "Error - The metric you entered is not valid\n"
              "===========================================")
        
    return chosen_metric

#Prompting and validation timestep input
def get_timestep():
    
    timestep = input("Please enter the timestep for visualisation (in days): \n")
    
    err_out = ("\n===========================================\n"
              "Error - The metric you entered is not valid\n"
              "===========================================")
    
    if timestep.isdigit() == False:
        print(err_out)
    elif timestep == 0:
        print(err_out)
    else:
        return int(timestep)

#Retrieve correct data from collection based on metric
def get_data(chosen_metric):
    
    if chosen_metric in metrics:
        access_coll = main_coll
    elif chosen_metric in secondary_metrics:
        access_coll = other_coll
    
    data = pd.DataFrame(list(access_coll.find({}).sort('date', pymongo.ASCENDING)))
    data['date'] = pd.to_datetime(data['date'])
    
    return data

#Get maximum y-value of metric for y-axis scaling
def get_y_max(data, chosen_metric):
    
    max_range = np.nanmax(data[chosen_metric])
    
    return max_range

#Random colour generation for region
def colour_mapping(area_denoms,  min, max):
    
    colour_map = dict()
    
    for area in area_denoms.unique():
        red = random.randint(min, max)
        green = random.randint(min, max)
        blue = random.randint(min, max)
        rgb = 'rgb({}, {}, {})'.format(red, green, blue)
    
        colour_map[area] = rgb
        
    return colour_map

#Map colours to regions in dataframe
def insert_colours(data):
    mapped_colours = colour_mapping(data.areaName, 0, 255)
    
    data['colour'] = data['areaName'].map(mapped_colours)
    
#Check if given date has matching event w/ event date-title dictionary    
def get_event(this_date): 
    
    event_dates = ['2020-03-23', 
                   '2020-06-01', 
                   '2020-09-01', 
                   '2020-11-05', 
                   '2020-12-01', 
                   '2020-12-08', 
                   '2021-01-05', 
                   '2021-04-12']
                
    events = {
        '2020-03-23': ' First national lockdown ',
        '2020-06-01': ' First lockdown eases ',
        '2020-09-01': ' Schools return ',
        '2020-11-05': ' Second national lockdown ',
        '2020-12-01': ' Second lockdown eases ',
        '2020-12-08': ' Vaccination program begins ',
        '2021-01-05': ' Third national lockdown ',
        '2021-04-12': ' Third lockdown eases '
        }
  
    if pd.to_datetime(this_date) >= pd.to_datetime(event_dates[7]):
        return events[event_dates[7]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[6]):
        return events[event_dates[6]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[5]):
        return events[event_dates[5]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[4]):
        return events[event_dates[4]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[3]):
        return events[event_dates[3]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[2]):
        return events[event_dates[2]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[1]):
        return events[event_dates[1]]
    elif pd.to_datetime(this_date) >= pd.to_datetime(event_dates[0]):
        return events[event_dates[0]]
    else: 
        return ' '
    
    
#Retreieve initial values for plotting
def get_init_val(chosen_metric, data, start):
    
    if chosen_metric == "newCasesByPublishDate":
        init_val = data[data['date'] == start].newCasesByPublishDate
    elif chosen_metric == "cumCasesBySpecimenDate":
        init_val = data[data['date'] == start].cumCasesBySpecimenDate
    elif chosen_metric == "newDeathsByDeathDate":
        init_val = data[data['date'] == start].newDeathsByDeathDate
    elif chosen_metric == "cumDeathsByPublishDate":
        init_val = data[data['date'] == start].cumDeathsByPublishDate
    elif chosen_metric == "cumPeopleVaccinatedFirstDoseByPublishDate":
        init_val = data[data['date'] == start].cumPeopleVaccinatedFirstDoseByPublishDate
    elif chosen_metric == "cumPeopleVaccinatedSecondDoseByPublishDate":
        init_val = data[data['date'] == start].cumPeopleVaccinatedSecondDoseByPublishDate
    elif chosen_metric == "cumPeopleVaccinatedCompleteByPublishDate":
        init_val = data[data['date'] == start].cumPeopleVaccinatedCompleteByPublishDate
    elif chosen_metric == "cumVirusTests":
        init_val = data[data['date'] == start].cumVirusTests
    return init_val

