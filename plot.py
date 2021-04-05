import plotly.express as px
import plotly.io as pio
import pandas as pd
#INTERACTIVE DISPLAY IN BROWSER
pio.renderers.default='browser'

#DISPLAY IN SPYDER
#pio.renderers.default='svg'

#def set_metrics():
    
def test_out():
    this_data = get_data('areaType=region')
    print(this_data)  
    
    test_bar = px.bar(
                data_frame = this_data, 
                x = 'areaName', 
                y = 'cumDeathsByPublishDate', 
                color = 'areaName', 
                animation_frame = 'date', 
                animation_group = 'areaName',
                range_y = [0, 24000]
                )
    
    test_bar.show()
    
test_out()   