"""
Programming Fundamentals (Computation in Biophysics) Final Project

Goal: Produce a histogram of all the PDB entries by date. 2 Y-axes: Average
        MW and number of structures

Authors: Andrew Alamban and Ben Orr
"""

import os
import numpy as np
import matplotlib.pyplot as plt


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


def get_MW(mmcif_dict):
    #mmcif_dict = MMCIF2Dict(filename) #get a dict for non-struct info
    #date = mmcif_dict["_pdbx_database_status.recvd_initial_deposition_date"]
    #print(date)
    mass = mmcif_dict["_entity.formula_weight"]
    print(mass)
    weight = 0
    for unit in mass:
        weight += float(unit)
    print(weight)
    return weight

def get_date(mmcif_dict):
    date = mmcif_dict["_pdbx_database_status.recvd_initial_deposition_date"]
    print(date)
    return date



def plot_data(): #array_of_tuples):

    #Create some mock data
    t = np.arange(0.01, 10.0, 0.01)
    data1 = np.exp(t)
    data2 = np.sin(2 * np.pi * t)

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('exp', color=color)
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
    #for cif in list_of_cifs , say. Or, we could feed the cifs into the
    #program one-by-one
    #get_filename - return .cif file

    #mmcif_dict = MMCIF2Dict("6yyt.cif") #get a dict for non-struct info
    #tuple = (get_date(mmcif_dict), get_MW(mmcif_dict))

    directory = '/databases/mol/mmCIF'
    array_of_tuples = []
    dict = {}

    #for directory2 in os.listdir(directory)
    for filename in os.listdir(directory): #(directory2)
        if filename.endswith(".cif"):

            mmcif_dict = MMCIF2Dict(filename)

            name = filename.rstrip(".cif")
            mw = get_MW(mmcif_dict)
            date = get_date(mmcif_dict)

            """
            if date in dict{}:
                add the new info to the existing index
            else:
                create a new index with info
            """

            continue
        else:
            continue

    for date in dict:



#main()
plot_data()
