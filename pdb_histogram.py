"""
Programming Fundamentals (Computation in Biophysics) Final Project

Goal: Produce a histogram of all the PDB entries by date. 2 Y-axes: Average
        MW and number of structures

Author: Ben Orr (Adapted from Andrew Alamban)
"""
import os
from Bio.PDB import MMCIFParser
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

parser = MMCIFParser()

def go_through_database(data):
    """ This section is supposed to iterate through all the files of the
    database and then begin to organize the dictionary that will help us
    manipulate the data that we will plot later. The input is the initial
    empty dictionary. """
    directory = os.getcwd()
    for subdir, dirs, files in os.walk(directory): #walks through directories
            for file in files:
                if file.endswith('.cif'):
                    location = os.path.join(file)
                    organize_data(location, data)
    #I am having issues of accessing the last file in a directory. I think that
    #the 'cursor' is moving on to the next directory without opening the last
    #file.
    return data

def get_MW(mmcif_dict):
    mass = mmcif_dict["_entity.formula_weight"]
    """print(mass)
    weight = 0
    for unit in mass:
        weight += float(unit)
    print(weight)"""
    return mass

def get_date(mmcif_dict):
    date = mmcif_dict["_pdbx_database_status.recvd_initial_deposition_date"]
    #print(date)
    return date

def data_for_plot(dictionary):
    """ Takes the initial dictionary created as an input and, using that, create
    a tuple of the information that's necessary for plotting in the following
    format: (deposit date, # of structures, average MW) """

    final_data = []
    sorted_dict = sorted(dictionary.keys()) #To have chronological order dict.
    for key in sorted_dict:
        date = key
        total_structures = len(dictionary[key])
        avg_mw = sum(dictionary[key])/total_structures
        data = final_data.append((date, total_structures, avg_mw))
    return final_data

def organize_data(file, data):
    """ Create a dictionary which contains the date and molecular weights of
    the .cif files specified """
    mmcif_dict = MMCIF2Dict(file) #get a dict for non-struct
    #print(get_date(mmcif_dict)[0])
    data[get_date(mmcif_dict)[0]] = [float(i) for i in get_MW(mmcif_dict)]
    return data

def main():
    #for cif in list_of_cifs , say. Or, we could feed the cifs into the
    #program one-by-one
    files = ["6yyt.cif", "1axc.cif"] #Might need to change this to a
                                          #directory
    data = dict()
    #I need to figure out a way to iterate through files in a directory
    data = go_through_database(data)
    #print(data)
    new_data = sorted(data.keys())
    #print(new_data)
    plot_this = data_for_plot(data)
    #print(plot_this)


main()
