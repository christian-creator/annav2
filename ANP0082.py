import pandas as pd
import numpy as np
import os
import sys
import datetime
from boundaries import room_classes

def create_ANPP082_table(data_fixed,dates):
    rooms = sorted([file[:-4] for file in os.listdir("data/ANP0082/raw")])
    dates = np.array(dates)
    header = np.array(["date"] + sorted([room + "_{}".format(i+1) for i in range(2) for room in rooms]))
    matrix = np.zeros((len(dates),len(rooms)*2))
    # print(matrix)
    for i,date in enumerate(dates):
        for j,room in enumerate(data_fixed.keys()):
            index_j = j*2
            try:
                matrix[i,index_j] = str(data_fixed[room][date]["Point 1"])
                matrix[i,index_j+1] = str(data_fixed[room][date]["Point 2"])
            except KeyError:
                matrix[i,index_j] = "nan"
                matrix[i,index_j+1] = "nan"
    dates = np.reshape(dates,(len(dates),1))
    header = np.reshape(header,(1,len(header)))
    matrix = np.concatenate((dates,matrix),axis=1)
    matrix = np.concatenate((header,matrix),axis=0)
    matrix = pd.DataFrame(matrix)
    matrix.to_excel('settleplates.xlsx',header=None,index=None)



def get_ANP0082_data():
    path_to_files = "data/ANP0082/raw"
    data_fixed = dict()
    dates = []
    for file in os.listdir(path_to_files):
        room = file[:-4]
        data_fixed[room] = dict()
        data = pd.read_csv(path_to_files +"/"+ file, header=None).to_numpy()[:,:4]
        data = np.delete(data,[2],1)
        point = 1
        for i,row in enumerate(data):
            date = [int(x) for x in row[1].split("-")]
            if len(date) < 3:
                print(room,"Date is missing in ANP0082")
                break
            date = datetime.date(*date)
            if date not in dates:
                dates.append(date)


            if date not in data_fixed[room].keys():
                data_fixed[room][date] = {"Point {}".format(point):row[2]}


            else:
                 data_fixed[room][date]["Point {}".format(point)] = row[2]
            if str(row[0]) != "nan":
                point += 1
    dates = sorted(dates)
    create_ANPP082_table(data_fixed,dates)


if __name__ == "__main__":
    get_ANP0082_data()