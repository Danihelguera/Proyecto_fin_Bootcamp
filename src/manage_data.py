import pandas as pd

def cargadataframe():
    data = pd.read_pickle("data/All_joined.pkl")
    return data


def monthdf(year):
    data = cargadataframe()
    return data[(data["year"] == year)].groupby("month").agg({"mean_time_m":'mean'}).reset_index(drop=True) 

def years():
    data = cargadataframe()
    return list(data.year.unique())

def origin():
    data = cargadataframe()
    sss = list(data.origin.unique())
    sss.sort()
    return sss 

def destiny():
    data = cargadataframe()
    sss = list(data.destiny.unique())
    sss.sort()
    return sss
