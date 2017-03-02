"""Plots stacked area chart with cumalative values with prints over time for each purpose as the different layers/areas.
"""

import plotly.plotly as py
import plotly.graph_objs as go
import get_sheet_data
import datetime

def reformat_data():
    """Gets data from Google Sheets as list of lists and returns filtered dictionary with data relevant to a area purpose chart.
    parameters: none
    returns: dictionary of lists --> dict[print date] = [purpose]
    """
    all_data_dict = dict() #we'll filter entries later, put all raw purpose data here
    data_dict = dict() #create data dictionary we'll be returning
    data_list = get_sheet_data.get_data()
    purpose_dict = dict()

    #put purpose data from Google Sheets into dictionary
    for row in data_list:
        if len(row) > 8: #filter out partially empty rows
            purpose = str(row[3]) #the str() gets rid of u in u'blah' 
            date = datetime.datetime.strptime(str(row[0]), '%m/%d/%Y %H:%M:%S').strftime('%m/%d/%Y') #create datetime object, round to days
            if date in all_data_dict: #if there's already a dictionary entry, get it so we can update it
                current_data = all_data_dict[date]
                current_data.append(purpose)
                all_data_dict[date] = current_data
            else: #no dictionary entry yet for this purpose, make empty list to add to
                all_data_dict[date] = [purpose]
            if purpose in purpose_dict:
                purpose_dict[purpose] += 1
            else:
                purpose_dict[purpose] = 1

    return [purpose_dict, all_data_dict]

def process_data():
    """Converts raw purpose data to a list of lists that are ready to be plotted.
    parameters: none
    returns: list of lists -- [day1 counts for purpose, day2 counts...dayn counts]
    """
    raw_data = reformat_data()
    purpose_dict = raw_data[0]
    data_dict = raw_data[1]
    purposes = [] #use for trace labels
    purpose_count_dict = [] #temporary dict to keep track of daily counts
    dates = [] #list of all of the dates in the dictionary
    prints_day_purpose = dict() #hold daily sums for each purpose for each date
    
    # ***TODO*** correct for days without prints by adding empty days to list
    
    #filter purposes so only the important ones (at least 20 prints) are graphed
    for purpose in purpose_dict:
        if purpose_dict[purpose] > 20: 
            purposes.append(purpose)
            purpose_count_dict = 0
            prints_day_purpose[purpose] = []
    
    #LEFT OFF HERE!!!! PROBLEMS IN LOOP BELOW; RUN TO SEE THEM

    #go day-by-day and add daily counts to each of the purpose lists in purpose dict
    for date in data_dict:
        dates.append(date)
        for print_entries in data_dict[date]:
            print (print_entries)
            purpose =  data_dict[date]
            if purpose in purposes:
                purpose_count_dict[purpose] += 1

        for purpose in purposes:
            prints_day_purpose[purpose].append(sum(purpose_count_dict[purpose]))
            purpose_count_dict[purpose] = 0

    return [purposes, dates, prints_day_purpose]

def plot_data():
    """Plots purpose data as cumalative area plot.
    parameters: none
    returns: none (updates on plotly)
    """

    data_lists = process_data()
    purposes = data_lists[0]
    dates = data_lists[1]
    prints_day_purpose = data_lists[2]
    traces = []

    #create a trace for every purpose

    # ***TODO*** change color values for each new trace; create list of colors vals, update index each iteration
    for purpose in purposes:
        trace = go.Scatter(
            x= dates,
            y= prints_day_purpose[purpose],
            mode='lines',
            line=dict(width=0.5,
                      color='rgb(184, 247, 212)'),
            fill='tonexty'
        )
        traces.append[trace]

    data = traces
    layout = go.Layout(
        showlegend=True,
        xaxis=dict(
            type='category',
        ),
        yaxis=dict(
            type='linear',
            range=[1, 100],
            dtick=20,
            ticksuffix='%'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='stacked-area-plot')

if __name__ == '__main__':
    process_data()