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


#currently don't use this f(x), instead copied this code in main()
def get_filename():
    directory = '/databases/mol/mmCIF'

    #for directory2 in os.listdir(directory)
    for filename in os.listdir(directory): #(directory2)
        if filename.endswith(".cif"):
          #do smth
          continue
        else:
            continue

#Uses Biopython MMCIF2Dict to extract MW data
def get_MW(mmcif_dict):
    mass = mmcif_dict["_entity.formula_weight"]
    weight = 0
    for unit in mass:
        weight += float(unit)
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
    """ Takes the initial dictionary created as an input and, using that, create
    a tuple of the information that's necessary for plotting in the following
    format: (deposit date, # of structures, average MW). Also sorts the
    dictionary by date, and returns all this information in an array of tuples. """

    final_data = []
    sorted_dict = sorted(dict.keys()) #To have chronological order dict.
    for key in sorted_dict:
        date = key
        total_structures = len(dict[key])
        avg_mw = sum(dict[key])/total_structures
        data = final_data.append((date, total_structures, avg_mw))
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

    df['Weights'].plot(kind='bar',color='red',ax=ax,width=0.4,position=1)
    df['Number of Structures'].plot(kind='bar',color='blue',ax=ax2,width=0.4,position=0)

    ax.set_ylabel('Avg. MW (Da)')
    ax2.set_ylabel('# of Structures')
    
    #plt.show() #will need to do a 'save to png' function for the final product
    fig.savefig('/wynton/home/rotation/aalamban/comp_course/fig_1.png')

def main():

    directory = '/databases/mol/mmCIF'

    #defaultdict allows for a dictionary full of key:lists
    dict = defaultdict(list)

    #test size
    i = 0

    for subdirectory in os.listdir(directory):
        #test size
        if(i<50):

            for filename in os.listdir(directory+'/'+subdirectory):
               # print(filename)
                if filename.endswith(".cif"):

                    #test size
                    i+=1

                    mmcif_dict = MMCIF2Dict(directory+'/'+subdirectory+'/'+filename)

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

    sorted_dict = sort_dict(dict)

    num_deposits_array = []

    for date in dict:
        num_deposits_array.append(len(dict[date]))
    dates, weights = create_list(dict)
    num_deposits_array = np.array(num_deposits_array)
    data = {"Dates":dates, "Number of Structures":num_deposits_array, "Weights":weights}
    df = pd.DataFrame(data) #will use this data to plot histogram
    df = df.set_index('Dates')
    create_histogram(df)

main()
