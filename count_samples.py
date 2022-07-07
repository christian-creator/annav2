import pandas as pd
import numpy as np
import os
import sys
import datetime
import openpyxl as xl


Months = ["Jan","Feb","Mar","Apr","Maj","Juni","Juli","Aug","Sep","Okt","Nov","Dec"]

def count_ANP0019():
    counts = dict()
    for file in os.listdir("data/ANP0019/raw"):
        df = pd.read_csv("data/ANP0019/raw/" + file,header=None)
        data = df.to_numpy()
        # Delete useless columns
        data = np.delete(data, [2, 3], axis=1)
        room = file[:-4]
        counts[room+"_count"] = dict()
        counts[room+"_mold"] = dict()
        for row in data:
            date = [int(x) for x in row[1].split("-")]
            if len(date) < 3:
                # print(room,"Date is missing in ANP0020")
                continue
            month = Months[date[1]-1]
            mold = row[-1]
            if month not in counts[room+"_count"].keys():
                if mold > 0:
                    counts[room+"_count"][month] = 1
                    counts[room+"_mold"][month] = 1

                else:
                    counts[room+"_count"][month] = 1
                    counts[room+"_mold"][month] = 0
            else:
                if mold > 0:
                    counts[room+"_count"][month] += 1
                    counts[room+"_mold"][month] += 1
                else:
                    counts[room+"_count"][month] += 1
    df = pd.DataFrame.from_dict(counts)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.fillna(0)
    df.to_excel("ANP0019_count.xlsx")

def count_ANP0020():
    counts = dict()
    for file in os.listdir("data/ANP0020/raw"):
        df = pd.read_csv("data/ANP0020/raw/" + file,header=None)
        data = df.to_numpy()
        # Delete useless columns
        data = np.delete(data, [2], axis=1)
        room = file[:-4]
        counts[room] = dict()
        for row in data:
            date = [int(x) for x in row[1].split("-")]
            if len(date) < 3:
                # print(room,"Date is missing in ANP0020")
                continue
            month = Months[date[1]-1]
            if month not in counts[room].keys():
                counts[room][month] = 2
            else:
                counts[room][month] += 2
    df = pd.DataFrame.from_dict(counts)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.fillna(0)
    df.to_excel("ANP0020_count.xlsx")

def count_ANP0082():
    pass

def count_ANP0230():
    counts = dict()
    for file in os.listdir("data/ANP0230/raw"):
        df = pd.read_csv("data/ANP0230/raw/" + file,header=None)
        data = df.to_numpy()
        # Delete useless columns
        data = np.delete(data, [2,4,6], axis=1)
        room = file[:-4]
        counts[room+"_count"] = dict()
        counts[room+"_mold"] = dict()
        for row in data:
            date = [int(x) for x in row[1].split("-")]
            if len(date) < 3:
                # print(room,"Date is missing in ANP0020")
                continue
            month = Months[date[1]-1]
            mold = row[-1]
            if month not in counts[room+"_count"].keys():
                if mold > 0:
                    counts[room+"_count"][month] = 1
                    counts[room+"_mold"][month] = 1

                else:
                    counts[room+"_count"][month] = 1
                    counts[room+"_mold"][month] = 0
            else:
                if mold > 0:
                    counts[room+"_count"][month] += 1
                    counts[room+"_mold"][month] += 1
                else:
                    counts[room+"_count"][month] += 1
    df = pd.DataFrame.from_dict(counts)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.fillna(0)
    df.to_excel("ANP0230_count.xlsx")

if __name__ == "__main__":
    count_ANP0019()
    count_ANP0020()
    count_ANP0230()
