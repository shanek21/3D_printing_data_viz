"""Plots polar plot with purposes as the directions, number of prints in the category as magnitude, and average print time in the category as intensity (color)
"""

import plotly.plotly as py
import plotly.graph_objs as go
import get_sheet_data

def reformat_data():
    """Gets data from Google Sheets as list of lists and returns filtered dictionary with data relevant to a polar purpose plot.
    parameters: none
    returns: dictionary of lists --> dict[purpose] = [print times]
    """
    all_data_dict = dict() #we'll filter entries later, put all raw purpose data here
    data_dict = dict() #create data dictionary we'll be returning
    data_list = get_sheet_data.get_data()

    #put purpose data from Google Sheets into dictionary
    for row in data_list:
        if len(row) > 8: #filter out partially empty rows
            purpose = str(row[3]) #the str() gets rid of u in u'blah' 
            time = str(row[7])
            if purpose in all_data_dict: #if there's already a dictionary entry, get it so we can update it
                current_data = all_data_dict[purpose]
                current_data.append(time)
                all_data_dict[purpose] = current_data
            else: #no dictionary entry yet for this purpose, make empty list to add to
                all_data_dict[purpose] = [time]

    #filter out fringe purposes (one or two time purposes)
    for purpose in all_data_dict:
        if len(all_data_dict[purpose]) > 20: #we're only keeping entries with 20+ list items
            data_dict[purpose] = all_data_dict[purpose]

    return data_dict

def process_data():
    """Converts raw purpose data to a list of lists that are ready to be plotted.
    parameters: none
    returns: list of lists -- [keys, two hour count, four hour count, four hour plus count]
    """
    data_dict = reformat_data()

    keys = [] #dictionary entries that will be the plot's labels
    # counts = [] #the number of prints per purpose
    two_hours_less_counts = [] #number of prints per purpose that were < 2 hours
    four_hours_less_counts = [] #num prints per purpose < 4 hours
    four_hours_plus_counts = [] #num prints per purpose >= 4 hours

    for purpose in data_dict:
        keys.append(purpose)
        two_count = 0 #count of prints that are < 2 hours
        four_count = 0 #prints < 4 hours
        four_plus_count = 0 #prints >= 4 hours

        #categorize the print time (<2, <4, or >=4?)
        for entry in data_dict[purpose]:
            hours = int(entry.split(':')[0]) #convert from H:M:S to rounded down hours
            if hours < 2: 
                two_count += 1
            elif hours < 4:
                four_count += 1
            else:
                four_plus_count += 1
        #add counts for purpose to list of counts
        #plotly overlaps traces, so we'll add the hour counts before each one to whichever one we're on now --> makes the plot looks better
        two_hours_less_counts.append(two_count)
        four_hours_less_counts.append(two_count + four_count)
        four_hours_plus_counts.append(two_count + four_count + four_plus_count)

    return [keys, two_hours_less_counts, four_hours_less_counts, four_hours_plus_counts]

def plot_data():
    """Plots purpose data as wind rose plot.
    parameters: none
    returns: none (updates on plotly)
    """
    data_lists = process_data()
    keys = data_lists[0]
    two_hours = data_lists[1]
    four_hours = data_lists[2]
    four_plus_hours = data_lists[3]

    #create traces (directions + magnitude in that direction)
    trace1 = go.Area(
        r= four_plus_hours,
        t= keys,
        name='>= 4 Hours',
        marker=dict(
            color='rgb(159,226,191)' #"sea green"
        )
    )
    trace2 = go.Area(
        r= four_hours,
        t= keys,
        name='< 4 Hours',
        marker=dict(
            color='rgb(59,176,143)' #"jungle green"
        )
    )
    trace3 = go.Area(
        r= two_hours,
        t= keys,
        name='< 2 Hours',
        marker=dict(
            color='rgb(23,128,109)' #"tropical rain forest"
        )
    )

    #plot traces -- plotly graph will be online with filename specified below
    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title='Why Are Oliners 3D Printing?',
        font=dict(
            size=16
        ),
        legend=dict(
            font=dict(
                size=16
            )
        ),
        radialaxis=dict(
            ticksuffix=' prints'
        ),
        orientation=270,
    )
    fig = go.Figure(data=data, layout=layout) #categoryorder --> "category descending"
    py.iplot(fig, filename='test')

if __name__ == '__main__':
    plot_data()