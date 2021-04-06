import plotly.express as px
import plotly.io as pio
import pandas as pd
from database import client

#INTERACTIVE DISPLAY IN BROWSER
pio.renderers.default='browser'

#DISPLAY IN SPYDER
#pio.renderers.default='svg'

db = client["covid_data"]
main_coll = db["main"]
other_coll = db["other"]

test_FIND = main_coll.find({"areaName":"London"})
for test in test_FIND:  
    print(test)
    
data = pd.DataFrame(list(main_coll.find({})))
data['date'] = pd.to_datetime(data['date'])
data.sort_values('date', ascending = True, inplace = True, ignore_index = True)

#def set_metrics():    
def test_out():
    #this_data = get_data('areaType=region')
    #print(this_data)  
    
    test_bar = px.bar(
                data_frame = data, 
                x = 'areaName', 
                y = 'cumDeathsByPublishDate', 
                color = 'areaName', 
                animation_frame = 'date', 
                animation_group = 'areaName',
                range_y = [0, 24000]
                )
    
    test_bar.show()
    
test_out()   