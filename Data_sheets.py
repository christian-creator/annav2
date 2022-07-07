import os
import sys
import pandas as pd
import numpy as np
import openpyxl as xl
import datetime
from openpyxl import Workbook



def get_ANP0019_data(path_to_file,room):
    # Read data from CSV files
    df = pd.read_csv(path_to_file, header=None)
    data = df.to_numpy()
    # Delete useless columns
    data = np.delete(data, [2, 3, 5], axis=1)
    data_fixed = dict()
    # Extract data from the numpy array using dict()
    point = 1
    for row in data:
        date = [int(x) for x in row[1].split("-")]
        if len(date) < 3:
            # print(room,"Date is missing in ANP0019")
            continue
        date = datetime.date(*date)
        if date not in data_fixed.keys():
            data_fixed[date] = {"Point {}".format(point): row[2]}
        else:
            if point not in data_fixed[date].keys():
                data_fixed[date]["Point {}".format(point)] = row[2]
            else:
                # Der er 2 datoer som er ens og har samme punkter
                print("Der er 2 datoer som er ens in: ", room)
                # Uncomment to run the continue the program and comment that there is a mistake.
                sys.exit(1)
        if str(row[0]) != "nan":
            point += 1
    
    data_fixed = pd.DataFrame.from_dict(data_fixed).T
    N,M = data_fixed.shape
    ANP0019_dates = np.array(data_fixed.index.values.tolist()).reshape(N,1)
    ANP0019_header = np.array(["dates"] + data_fixed.columns.values.tolist()).reshape(1,M+1)
    data_fixed = data_fixed.to_numpy()
    data_fixed = np.concatenate((ANP0019_dates,data_fixed),axis=1)
    data_fixed = np.concatenate((ANP0019_header,data_fixed),axis=0)
    return data_fixed


def get_ANP0020_data(path_to_file,room):
    # Read data from CSV files
    df = pd.read_csv(path_to_file, header=None)
    data = df.to_numpy()
    # Delete useless columns
    data = np.delete(data, [2], axis=1)
    data_fixed = dict()
    # Extract data from the numpy array using dict()
    point = 1
    for row in data:
        date = [int(x) for x in row[1].split("-")]
        if len(date) < 3:
            # print(room,"Date is missing in ANP0020")
            continue
        date = datetime.date(*date)
        if date not in data_fixed.keys():
            data_fixed[date] = {"0.5_Point {}".format(
                point): row[2], "5.0_Point {}".format(point): row[3]}
        else:
            if point not in data_fixed[date].keys():
                data_fixed[date]["0.5_Point {}".format(point)] = row[2]
                data_fixed[date]["5.0_Point {}".format(point)] = row[3]
            else:
                # Der er 2 datoer som er ens og har samme punkter
                # print("Der er 2 datoer som er ens in: ", room)
                # Uncomment to run the continue the program and comment that there is a mistake.
                sys.exit(1)
        if str(row[0]) != "nan":
            point += 1
    data_fixed = pd.DataFrame.from_dict(data_fixed).T
    data_fixed = data_fixed.reindex(sorted(data_fixed.columns), axis=1)
    N,M = data_fixed.shape
    ANP0020_dates = np.array(data_fixed.index.values.tolist()).reshape(N,1)
    ANP0020_header = np.array(["dates"] + data_fixed.columns.values.tolist()).reshape(1,M+1)
    data_fixed = data_fixed.to_numpy()
    data_fixed = np.concatenate((ANP0020_dates,data_fixed),axis=1)
    data_fixed = np.concatenate((ANP0020_header,data_fixed),axis=0)
    return data_fixed
    

def create_datasheets():
    count = 0
    wb = Workbook()
    for file in os.listdir("data/ANP0019/raw"):
        room = file[:-4]
        if os.path.isfile("data/ANP0019/raw/"+ file) and os.path.isfile("data/ANP0020/raw/"+ file):
            pass
        else:
            continue
        ANP0019_data = get_ANP0019_data("data/ANP0019/raw/"+ file,room)
        ANP0020_data = get_ANP0020_data("data/ANP0020/raw/"+ file,room)
        if ANP0019_data.shape[0] == ANP0020_data.shape[0]:
            All_data = np.concatenate((ANP0019_data,ANP0020_data),axis=1)
            All_data = All_data.tolist()
            ws = wb.create_sheet(title=room)
            for row in All_data:
                ws.append(row)
            
        else:
            print("ANP0019 and ANP0020 does not have the same shape in {}".format(room))
            continue
    wb._sheets.sort(key=lambda ws: ws.title)
    wb.save(filename = "data_sheets.xlsx")




if __name__ == "__main__":
    create_datasheets()