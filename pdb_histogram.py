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


def plot_data(dict, num_deposits_array):

    #Create some mock data
    t = np.arange(0.01, 10.0, 0.01)
    data1 = np.exp(t)
    data2 = np.sin(2 * np.pi * t)

    """
    #Plot #1: Average MW
    average_mw_array = []
    date_array = []
    for date in dict.keys():
        date_array.append(date)
        ave_mw = sum(dict[date])/len(dict[date])
        #ave_mw = np.average(dict[date])
        average_mw_array.append(ave_mw)
    """

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Average MW', color=color)
    #in example, ax1.plot takes np arrays as data. Do python arrays work here?

    #ax1.plot(date_array, average_mw_array, color=color)
    ax1.plot(t, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()



def main():

    directory = '/databases/mol/mmCIF'

    #defaultdict allows for a dictionary full of key:lists
    dict = defaultdict(list)

    #test size
    i = 0


    #print(os.listdir(directory)) #out of interest
    for subdirectory in os.listdir(directory):
        #print(subdirectory) #also out of interest

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

    """
    num_deposits_array = []

    for date in dict:
        num_deposits_array.append(len(dict[date]))


    #print(num_deposits_array)
    dates, weights = create_list(dict)
    num_deposits_array = np.array(num_deposits_array)
   # print(num_deposits_array)
   # print(dates)
   # print(weights)
   # print(type(dates))
    data = {"Dates":dates, "Number of Structures":num_deposits_array, "Weights":weights}
    df = pd.DataFrame(data)
    print(df)
    plot_data(dict, num_deposits_array)

    print(num_deposits_array)
    """

    #plot_data(sorted_dict)


main()


#works!!
def test_dir():
    directory = '/databases/mol/mmCIF'
    for dir2 in os.listdir(directory):
        for filename in os.listdir(directory+'/'+dir2):
            print(filename)

#test_dir()
