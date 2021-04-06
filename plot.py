import plotly.express as px
import plotly.io as pio
import pandas as pd
from database import client, metrics, secondary_metrics

#INTERACTIVE DISPLAY IN BROWSER
pio.renderers.default='browser'

#DISPLAY IN SPYDER
#pio.renderers.default='svg'

db = client["covid_data"]
main_coll = db["main"]
other_coll = db["other"]

#test_FIND = main_coll.find({"areaName":"London"})
#for test in test_FIND:  
    #print(test)
    


all_metrics = {
        "newCasesByPublishDate",
        "cumCasesByPublishDate",
        "newDeathsByDeathDate",
        "cumDeathsByPublishDate",
        "cumAdmissions",
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
          "cumAdmissions \n"
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
        
    
def test_out():
    #this_data = get_data('areaType=region')
    #print(this_data)  
    
    chosen_metric = metric_select()
    
    if chosen_metric in metrics:
        access_coll = main_coll
    elif chosen_metric in secondary_metrics:
        access_coll = other_coll
    
    data = pd.DataFrame(list(access_coll.find({})))
    #data['date'] = pd.to_datetime(data['date'])
    #data.sort_values('date', ascending = True, inplace = True, ignore_index = True)
    
    test_bar = px.bar(
                data_frame = data, 
                x = 'areaName', 
                y = chosen_metric, 
                color = 'areaName', 
                animation_frame = 'date', 
                animation_group = 'areaName',
                range_y = [0, 11124000]
                )
    
    test_bar.show()
    
test_out()   