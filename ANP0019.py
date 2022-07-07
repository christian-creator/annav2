import pandas as pd
import numpy as np
import os
import sys
import datetime
from boundaries import room_classes
from excel_plot import write_and_plot_excel_ANP0019,write_and_plot_excel_ANP0020


def get_ANP0019_data(slut_dato):
    # Make folder wheret the data should be saved
    for file in os.listdir("data/ANP0019/raw/"):
        # Read data from CSV files
        room = file[:-4]
        df = pd.read_csv("data/ANP0019/raw/"+file, header=None)
        data = df.to_numpy()
        # Delete useless columns
        data = np.delete(data, [2, 3, 5], axis=1)
        data_fixed = dict()
        # Extract data from the numpy array using dict()
        point = 1
        for row in data:
            date = [int(x) for x in row[1].split("-")]
            if len(date) < 3:
                print(room,"Date is missing in ANP0019")
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

        if room in room_classes.keys():
            data_fixed['alert'] = [
                int(room_classes[room]["ANP0019_alert"]) for i in range(len(data_fixed))]
            # data_fixed.to_excel("data/ANP0019/filtered/{}.xlsx".format(room))
            write_and_plot_excel_ANP0019(data_fixed, room, slut_dato)
        else:
            pass
            # print(room,"does not have boundary")
