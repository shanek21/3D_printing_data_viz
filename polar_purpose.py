"""Plots polar plot with purposes as the directions, number of prints in the category as magnitude, and average print time in the category as intensity (color)
"""

import plotly.plotly as py
import plotly.graph_objs as go
import get_sheet_data

def reformat_data():
    """Gets data from Google Sheets as list of lists and returns dictionary with data relevant to a polar purpose plot.
    parameters: none
    returns: dictionary of lists --> dict[purpose] = [print times]
    """
    data_dict = dict() #create data dictionary we'll be returning
    data_list = get_sheet_data.get_data()

    for row in data_list:
        if len(row) > 8: #filter out partially empty rows
            purpose = str(row[3]) #the str() gets rid of u in u'blah' 
            time = str(row[7])
            if purpose in data_dict: #if there's already a dictionary entry, get it so we can update it
                current_data = data_dict[purpose]
                current_data.append(time)
                data_dict[purpose] = current_data
            else: #no dictionary entry yet for this purpose, make empty list to add to
                data_dict[purpose] = [time]
    
    print (data_dict)


if __name__ == '__main__':
    reformat_data()