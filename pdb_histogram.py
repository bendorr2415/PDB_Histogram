"""
Programming Fundamentals (Computation in Biophysics) Final Project

Goal: Produce a histogram of all the PDB entries by date. 2 Y-axes: Average
        MW and number of structures

Authors: Andrew Alamban and Ben Orr
"""
#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict #for multidict structure
from Bio.PDB.MMCIF2Dict import MMCIF2Dict


#Uses Biopython MMCIF2Dict to extract MW data
def get_MW(mmcif_dict):
    mass = mmcif_dict["_entity.formula_weight"]
    weight = 0
    for unit in mass:
        try: #in case a unit in mass is a '?'
            weight += float(unit)
        except:
            continue
    return weight

#Uses Biopython MMCIF2Dict to extract deposition date data
def get_date(mmcif_dict):
    date = mmcif_dict["_pdbx_database_status.recvd_initial_deposition_date"]
    return date


def create_list(dict):
    """ Create some arrays so that we can use it to turn into a pandas dataframe
    for some easy organization of our data. """
    dates = dict.keys()
    weights = []
    new_dates = []
    for date in dates:
        weights.append(dict[date][0])
        new_dates.append(date)
    weights = np.array(weights)
    new_dates = np.array(new_dates)
    return new_dates, weights

#Takes the unsorted dictionary (key = date, value = list of MWs) and
#   returns an array of tuples, each containing the dictionary's information
#   plus the number of structures deposited on that date, sorted by date
def sort_dict(dict):
    """Takes the unsorted dictionary, sorts this dictionary by date, and
    returns the sorted dictionary"""

    final_data = {}
    sorted_dict = sorted(dict.keys()) #To have chronological order dict.
    for key in sorted_dict:
        date = key
        final_data[date] = dict[key] 
    return final_data

def create_histogram(dataframe):
    """ Taking a pd dataframe as an input, create a plot that has two y-axes:
    1) avg. molecular weight of files deposited that day
    2) number of files deposited that day
    Output will result in a .png file """

    df = dataframe
    fig = plt.figure() #create matplotlib figure    
    
    ax = fig.add_subplot(111) #create some axes
    ax2 = ax.twinx() # create second axis for scaling

    df['Avg. MW'].plot(kind='bar',color='red',ax=ax,position=1,legend=True)
    df['# of Struc.'].plot(kind='bar',color='blue',ax=ax2,position=0,legend=True)

    ax.set_ylabel('Avg. MW (Da)')
    ax2.set_ylabel('# of Structures')
    
    #plt.show() #will need to do a 'save to png' function for the final product
    fig.savefig('/wynton/home/rotation/aalamban/comp_course/fig_1.png')


#Iterates through directories and mmCIF files, converts each file to a dictionary, and extracts
#MW and date data from these dictionaries and loads these data into a new dictionary and
#returns this dictionary
def read_in_data():
    directory = '/databases/mol/mmCIF'

    #defaultdict allows for a dictionary full of key:lists
    dict = defaultdict(list)

    #test size
    #i = 0

    for subdirectory in os.listdir(directory):
        #test size
        #if(i<500):

        for filename in os.listdir(directory+'/'+subdirectory):
            print(filename)
            if filename.endswith(".cif"):

                #test size
                #i+=1

                mmcif_dict = MMCIF2Dict(directory+'/'+subdirectory+'/'+filename)

                #Error: sometimes get_MW returns a '?' - handled in get_MW
                mw = float(get_MW(mmcif_dict))
                date = get_date(mmcif_dict)[0]

               # print((date,mw))

                if date in dict.keys():
                    dict[date].append(mw)
                else:
                    dict[date] = [mw] #make a new list
                #continue
            else:
                continue
    return dict


#Loads the date, num deposits, and ave mw data into numpy arrays and returns these arrays
def create_np_arrays(sorted_dict):
    num_deposits_array = [] 
    ave_mw_array = []    

    for date in sorted_dict:
        num_deposits_array.append(len(sorted_dict[date])) #To count # of deposited structures per date
        ave_mw_array.append(sum(sorted_dict[date])/len(sorted_dict[date])) #Calculate average mw for each day, and put these values into an array
    
    #Create np arrays for use in pandas
    dates, weights = create_list(sorted_dict)
    ave_mw_array = np.array(ave_mw_array)
    num_deposits_array = np.array(num_deposits_array)

    return dates, num_deposit_array, ave_mw_array

                
def main():

    dict = read_in_data()

    sorted_dict = sort_dict(dict) #To sort data in chronological order, by date

    dates, num_deposit_array, ave_mw_array = create_np_arrays(sorted_dict)
    
    data = {"Dates":dates, "# of Struc.":num_deposits_array, "Avg. MW":ave_mw_array}
    df = pd.DataFrame(data) #will use this data to plot histogram
    df = df.set_index('Dates')
    
    create_histogram(df)

main()
