"""
Programming Fundamentals (Computation in Biophysics) Final Project

Goal: Produce a histogram of all the PDB entries by date. 2 Y-axes: Average
        MW and number of structures

Author: Ben Orr (Adapted from Andrew Alamban)
"""

from Bio.PDB import MMCIFParser
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

parser = MMCIFParser()


def get_MW(mmcif_dict):
    date = mmcif_dict["_pdbx_database_status.recvd_initial_deposition_date"]
    print(date)
    mass = mmcif_dict["_entity.formula_weight"]
    print(mass)
    weight = 0
    for unit in mass:
        weight += float(unit)
    print(weight)


def main():
    #for cif in list_of_cifs , say. Or, we could feed the cifs into the
    #program one-by-one
    mmcif_dict = MMCIF2Dict("6yyt.cif") #get a dict for non-struct info
    tuple = (get_date(mmcif_dict), get_MW(mmcif_dict))







main()
