import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pymongo
import datetime
import random
from pymongo import MongoClient
from database import metrics, secondary_metrics

#INTERACTIVE DISPLAY IN BROWSER
pio.renderers.default='browser'

#DISPLAY IN SPYDER
#pio.renderers.default='svg'

client = MongoClient("mongodb+srv://matt:fjTrmxLnqiSqKi70@cluster0.llzxg.mongodb.net/covid_data?retryWrites=true&w=majority")
db = client["covid_data"]
main_coll = db["main1"]
other_coll = db["other1"]

#test_FIND = main_coll.find({"areaName":"London"})
#for test in test_FIND:  
    #print(test)

all_metrics = {
        "newCasesByPublishDate",
        "cumCasesByPublishDate",
        "newDeathsByDeathDate",
        "cumDeathsByPublishDate",
        "hospitalCases",
        "cumPeopleVaccinatedFirstDoseByPublishDate",
        "cumPeopleVaccinatedSecondDoseByPublishDate",
        "cumPeopleVaccinatedCompleteByPublishDate",
        "cumVirusTests"
    }


def metric_select():
    print("Metrics available for visualisation: \n"
          "newCasesByPublishDate \n"
          "cumCasesByPublishDate \n"
          "newDeathsByDeathDate \n"
          "cumDeathsByPublishDate \n"
          "hospitalCases \n"
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
        metric_select()
        
    return chosen_metric

def get_data(chosen_metric):
    
    if chosen_metric in metrics:
        access_coll = main_coll
    elif chosen_metric in secondary_metrics:
        access_coll = other_coll
    
    data = pd.DataFrame(list(access_coll.find({}).sort('date', pymongo.ASCENDING)))
    data['date'] = pd.to_datetime(data['date'])
    
    return data

def get_y_max(data, chosen_metric):
    
    max_range = np.nanmax(data[chosen_metric])
    #print(max_range)
    
    return max_range

def colour_mapping(area_denoms,  min, max):
    
    colour_map = dict()
    
    for area in area_denoms.unique():
        red = random.randint(min, max)
        green = random.randint(min, max)
        blue = random.randint(min, max)
        rgb = 'rgb({}, {}, {})'.format(red, green, blue)
    
        colour_map[area] = rgb
        
    return colour_map

def insert_colours(data):
    mapped_colours = colour_mapping(data.areaName, 0, 255)
    
    data['colour'] = data['areaName'].map(mapped_colours)


def bar_frames(data, chosen_metric):
    
    all_frames = []
    start = min(data['date'])
    end = max(data['date'])
    
    timestep = datetime.timedelta(days = 7)
    i = start
    
    while i <= end:
        frame_data = data[data['date'] == i]
        all_frames.append(go.Frame(data = [go.Bar(
                                            x = frame_data['areaName'],
                                            y = frame_data[chosen_metric],
                                            marker_color = frame_data['colour'])],
                                    layout = go.Layout(
                                            plot_bgcolor = '#FFFFFF',
                                            bargap = 0.15,
                                            title = str(i))))
        i += timestep
        
    return all_frames 

def get_init_val(chosen_metric, data, start):
    
    if chosen_metric == "newCasesByPublishDate":
        init_val = data[data['date'] == start].newCasesByPublishDate
    elif chosen_metric == "cumCasesByPublishDate":
        init_val = data[data['date'] == start].cumCasesByPublishDate
    elif chosen_metric == "newDeathsByDeathDate":
        init_val = data[data['date'] == start].newDeathsByDeathDate
    elif chosen_metric == "cumDeathsByPublishDate":
        init_val = data[data['date'] == start].cumDeathsByPublishDate
    elif chosen_metric == "hospitalCases":
        init_val = data[data['date'] == start].hospitalCases
    elif chosen_metric == "cumPeopleVaccinatedFirstDoseByPublishDate":
        init_val = data[data['date'] == start].cumPeopleVaccinatedFirstDoseByPublishDate
    elif chosen_metric == "cumPeopleVaccinatedSecondDoseByPublishDate":
        init_val = data[data['date'] == start].cumPeopleVaccinatedSecondDoseByPublishDate
    elif chosen_metric == "cumPeopleVaccinatedCompleteByPublishDate":
        init_val = data[data['date'] == start].cumPeopleVaccinatedCompleteByPublishDate
    elif chosen_metric == "cumVirusTests":
        init_val = data[data['date'] == start].cumVirusTests
    return init_val

def bar_plot():
    chosen_metric = metric_select()
    #data.sort_values('date', ascending = True, inplace = True, ignore_index = True)
    
    data = get_data(chosen_metric)
    
    insert_colours(data)
    
    y_range = get_y_max(data, chosen_metric)
    frames0 = bar_frames(data, chosen_metric)
    start = min(data['date'])
    #range_max = data[chosen_metric].max()
    
    initial_name = data[data['date'] == start].areaName
    initial_val = get_init_val(chosen_metric, data, start)
    #data[data['date'] == start].chosen_metric 
    initial_col = data[data['date'] == start].colour
    
    
    bar_out = go.Figure(data=[go.Bar(x = initial_name,
                                     y = initial_val,
                                     marker_color = initial_col)],
                        layout = go.Layout(plot_bgcolor = '#FFFFFF',
                                           xaxis = {},
                                           yaxis = {'range' : (0, y_range)},
                                           bargap = 0.15,
                                           title = str(start),
                                           updatemenus=[dict(type="buttons",
                                                             buttons=[dict(label="Play",
                                                                           method="animate",
                                                                           args=[None,{"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]),
                                                                      dict(label="Stop",
                                                                           method="animate",
                                                                           args=[[None],{"frame": {"duration": 0, "redraw": False}, "mode": "immediate","transition": {"duration": 0}}])])]),
                        frames = list(frames0))
    
    return bar_out
    
    """
    bar_out = px.bar(
                data_frame = data, 
                x = 'areaName', 
                y = chosen_metric, 
                color = 'areaName', 
                animation_frame = 'date', 
                animation_group = 'areaName',
                range_y = [0, 24000]
                )
    
    bar_out.show()
    """
    
fig = bar_plot()
fig.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'})
fig.show()   