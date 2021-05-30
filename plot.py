import plotly.io as pio
import plotly.graph_objects as go
import datetime
from data_processing import (get_data, metric_select, get_event, insert_colours, 
                             get_y_max, get_init_val, all_metrics, get_timestep)

#INTERACTIVE DISPLAY IN BROWSER
pio.renderers.default='browser'

#Create individual frames for visualisation
def bar_frames(data, chosen_metric):
    
    all_frames = []
    start = min(data['date'])
    end = max(data['date'])
    
    timestep = datetime.timedelta(days = time_step)
    i = start
   
    while i <= end: 
        this_event = get_event(i)
        frame_data = data[data['date'] == i]
        all_frames.append(go.Frame(data = [go.Bar(
                                            x = frame_data['areaName'],
                                            y = frame_data[chosen_metric],
                                            marker_color = frame_data['colour'])],
                                    layout = go.Layout(
                                            xaxis_title = "Regions",
                                            yaxis_title = chosen_metric,
                                            plot_bgcolor = '#FFFFFF',
                                            bargap = 0.15,
                                            title = str(i) + this_event)))
        
        i += timestep
        
    return all_frames 

#Combine frames to create figure (animated visualisation)
def bar_plot(chosen_metric):
    
    data = get_data(chosen_metric)
    
    insert_colours(data)
    
    y_range = get_y_max(data, chosen_metric)
    frames0 = bar_frames(data, chosen_metric)
    start = min(data['date'])
    this_event = get_event(start)
    
    initial_name = data[data['date'] == start].areaName
    initial_val = get_init_val(chosen_metric, data, start)
    initial_col = data[data['date'] == start].colour
    
    
    bar_out = go.Figure(data=[go.Bar(x = initial_name,
                                     y = initial_val,
                                     marker_color = initial_col)],
                        layout = go.Layout(plot_bgcolor = '#FFFFFF',
                                           xaxis = {},
                                           yaxis = {'range' : (0, y_range)},
                                           xaxis_title = "Regions",
                                           yaxis_title = chosen_metric,
                                           bargap = 0.15,
                                           title = str(start) + this_event,
                                           updatemenus=[dict(type="buttons",
                                                             buttons=[dict(label="Play",
                                                                           method="animate",
                                                                           args=[None,{"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]),
                                                                      dict(label="Stop",
                                                                           method="animate",
                                                                           args=[[None],{"frame": {"duration": 0, "redraw": False}, "mode": "immediate","transition": {"duration": 0}}])])]),
                        frames = list(frames0))
    
    return bar_out

#Main loop - Execute visualisation and output to browser
#Input validation constraints 
while True:
    chosen_metric = metric_select()
    time_step = get_timestep()
    if (chosen_metric in all_metrics) and (type(time_step) == int):
        fig = bar_plot(chosen_metric)
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'})
        fig.show()
        break
    