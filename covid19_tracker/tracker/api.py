import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import os

class API:
    
    def __init__(self):    
        self.dirpath = os.getcwd()


    def get_current_number(self):
        url="https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0&range=A1:I193"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        total = soup.findAll('td',class_="s6")[0].text.replace(",","")
        deaths = soup.findAll('td',class_="s6")[1].text.replace(",","")
        recov = soup.findAll('td',class_="s7")[0].text.replace(",","")
        return int(total), int(deaths), int(recov)


    def get_latest(self):
        url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
        url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
        url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

        data_dict = {}
        prov_dict = {}

        # Fetching the data from the Johns Hopkins CSSE's repository
        conf = pd.read_csv(url_confirmed, error_bad_lines=False)
        deaths = pd.read_csv(url_deaths, error_bad_lines=False)
        recov = pd.read_csv(url_recovered, error_bad_lines=False)

        # We do not need Latitude / Logitude information, so we'll just delete these columns
        del conf['Lat'], conf['Long'], deaths['Lat'], deaths['Long'], recov['Lat'], recov['Long']
        
        # Making a list containing the last date in the .csv
        cols = list(conf.columns.values)[-1:]
        inf = 0
        d = 0
        rec = 0 

        # Building the dict
        for index, row in conf.iterrows():
            data_deaths = deaths.iloc[index]
            data_rec = recov.loc[index]
            
            if not row[1] in data_dict:
                data_dict[row[1]] = {}
                data_dict[row[1]][cols[0]] = [row[cols[0]], data_rec[cols[0]], data_deaths[cols[0]]]
            elif row[0] in ['French Guiana', 'Guadeloupe', 'Guam', 'Mayotte', 'occupied Palestinian territory', 'Puerto Rico', 'Reunion']:
                # the states in the list above are listed as territories in the .csv's, however they are countries at the same time,
                # so we'll need to make an exception
                data_dict[row[0]] = {}
                data_dict[row[0]][cols[0]] = [row[cols[0]], data_rec[cols[0]], data_deaths[cols[0]]]
            else:
                data_dict[row[1]][cols[0]] = [x + y for x, y in zip(data_dict[row[1]][cols[0]], [row[cols[0]], data_rec[cols[0]], data_deaths[cols[0]]])]
     
        return data_dict



    def get_all(self):
        """
        Gets number of infections, deaths and recovered patients for every country.

        Returns:
            (Dict) A dict: {"country":"{"date":[cases, recoveries, deaths]}, ...}"
        """
        url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
        url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
        url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
        
        self.countries_dict = self.get_infected_countries(url_confirmed, url_deaths, url_recovered)
        
        return self.countries_dict


    def get_infected_countries(self, url_confirmed, url_deaths, url_recovered):
        """ Queries the Johns Hopkins CSSE's repository for all infected countries 
            and builds a dict with confirmed cases, deaths and recoveries for every
            country.

            Arguments:
            -- url_confirmed: (String) Url pointing to the .csv containing the numbers of confirmed cases
            -- url_deaths: (String) Url pointing to the .csv containing the numbers of deaths
            -- url_recovered: (String) Url pointing to the .csv containing the numbers of recovered cases

            Returns: 
                (Dict) A dict with the format {"country":"{"date":[cases, recoveries, deaths]}, ...}"
               
        """
        data_dict = {}
        prov_dict = {}

        # Fetching the data from the Johns Hopkins CSSE's repository
        conf = pd.read_csv(url_confirmed, error_bad_lines=False)
        deaths = pd.read_csv(url_deaths, error_bad_lines=False)
        recov = pd.read_csv(url_recovered, error_bad_lines=False)

        # We do not need Latitude / Logitude information, so we'll just delete these columns
        del conf['Lat'], conf['Long'], deaths['Lat'], deaths['Long'], recov['Lat'], recov['Long']
        
        # Making a list containing all dates in the .csv
        cols = list(conf.columns.values)[2:]
        inf = 0
        d = 0
        rec = 0 

        # Building the dict
        for index, row in conf.iterrows():

            data_deaths = deaths.iloc[index]
            data_rec = recov.loc[index]
            
            if not row[1] in data_dict and row[1] != "US":
                data_dict[row[1]] = {}
                for x in range(0, len(cols)):
                    data_dict[row[1]][cols[x]] = [row[cols[x]], data_rec[cols[x]], data_deaths[cols[x]]]
            elif row[0] in ['French Guiana', 'Guadeloupe', 'Guam', 'Mayotte', 'occupied Palestinian territory', 'Puerto Rico', 'Reunion', 'US']:
                # the states in the list above are listed as territories in the .csv's, however they are countries at the same time,
                # so we'll need to make an exception
                data_dict[row[0]] = {}
                for x in range(0, len(cols)):
                    data_dict[row[0]][cols[x]] = [row[cols[x]], data_rec[cols[x]], data_deaths[cols[x]]]
            elif row[1] != "US":
                for x in range(0, len(cols)):
                    data_dict[row[1]][cols[x]] = [x + y for x, y in zip(data_dict[row[1]][cols[x]], [row[cols[x]], data_rec[cols[x]], data_deaths[cols[x]]])]
        return data_dict

            


if __name__=="__main__":
    # For debugging purposes you can run the api.py script ob its own
    api = API()
    api.get_all()
