import pandas as pd
import numpy as np
import os
import sys
import datetime
from boundaries import room_classes
from ANP0019 import get_ANP0019_data
from ANP0020 import get_ANP0020_data
from ANP0082 import get_ANP0082_data
from ANP0230 import get_ANP0230_data
from count_samples import count_ANP0019,count_ANP0020,count_ANP0230
from Data_sheets import create_datasheets

def dataFiltration(filename):
    infile = open(filename, "r")
    outfile = open(filename[:-4] + "_filtered.txt", "w+")
    flag_list = ['Plant:', 'Suite/System:', 'Date', 'Sampling', 'Feller',
                 'Ave.', 'CFU/plate', 'Printed', 'End', 'Test/Specification']
    for line in infile:
        line = line.split()
        if len(line) >= 1 and line[0] not in flag_list:
            print("\t".join(line), file=outfile)


def sort_dataframe(data, ANP, room):
    # Extract the data in the correct format
    df = pd.DataFrame(data)
    
    if room == "1_G13" and ANP == "ANP0230":
        pokemon_og_games = df.loc[df.iloc[:,0].str.contains("PERS", case=False)]
        if pokemon_og_games.shape[0] > 0:
            return None

    for index, row in df.iterrows():
        if df.iloc[index, -1] is None:
            df.iloc[index, :] = df.iloc[index, :].shift(1)
    # Print to CSV.files
    if not os.path.exists('data/{}'.format(ANP)):
        os.makedirs('data/{}'.format(ANP))
        os.makedirs('data/{}/raw'.format(ANP))
    df.to_csv("data/{}/raw/{}.csv".format(ANP, room),
              header=False, index=False, na_rep="NaN")


def read_file(file_name):
    lims_file = open(file_name[:-4] + "_filtered.txt", "r")
    data = []
    ANP = None
    for line in lims_file:
        line = line.split()
        # If i read a Category and the len of the data is above one print and reset the room number
        if line[0] == "Category:":
            if len(data) >= 1:
                sort_dataframe(data, ANP, room)
                data = []
            room = line[1]
        # If you read ANP and the data is above one reset and print using the ANP and room
        elif "ANP" in line[0]:
            if len(data) >= 1:
                sort_dataframe(data, ANP, room)
                data = []
            ANP = line[0]
        
        elif ANP is not None:
            data.append(line)


if __name__ == "__main__":
    os.system("./clean.sh")
    # fil_navn = "data/lims_data/Q1_jan_mar_2020.txt"
    fil_navn = "data/lims_data/Q2_(Apr-Jun)_2020_rigtig.txt"
    slut_dato = "2020-07-01"
    dataFiltration(fil_navn)
    read_file(fil_navn)
    get_ANP0019_data(slut_dato)
    get_ANP0020_data(slut_dato)
    # get_ANP0082_data()
    get_ANP0230_data(slut_dato)
    # count_ANP0019()
    # count_ANP0020()
    # count_ANP0230()
    # create_datasheets()
