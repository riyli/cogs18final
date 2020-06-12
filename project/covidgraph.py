import pandas as pd
import matplotlib.pyplot as plt


# get a csv file of covid data, to be used as a dataframe

covid = pd.read_csv(r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')

# allow user to select the country for which they wish to see covid statistics
# set aliases for users who input 'US' as USA, America, or United States
# create a dataframe of that country's stats, through filtering the original dataframe

country = input("Select country: ")

if country == 'USA':
        country = 'US'
elif country == 'America':
        country = 'US'
elif country == 'United States':
        country = 'US'

stats_country = covid[covid['Country'] == country]

class Country():

    def __init__(self, df):
        """parameters: a dataframe"""

        self.df = df

    def get_covid_start(self):
        """gets a dataframe of covid-19 existence within a country, with the first entry being when covid-19 is introduced
        parameters: none
        returns: df_started, a new dataframe, starting from the first date of recorded covid-19 infection"""

        df_started = self.df[self.df['Confirmed'] > 0].reset_index().drop('index', 1)

        return df_started
    
    def get_covid_start_date(self):
        """gets the first date of covid-19 existence within a country, using get_covid_start()
        parameters: none
        returns: start_date, a date formatted in yyyy-mm-dd"""

        start_date = self.get_covid_start()['Date'].iloc[0]

        return start_date
    
    def add_current_col(self):
        """adds a column for current covid-19 infected individuals, through subtracting recovered and dead from confirmed case numbers
        parameters: none"
        returns: df_current, a new dataframe with another column of currently infected values"""

        # create a list of current infections, with index correlated to that of the dataframe

        rows_num = len(self.get_covid_start().index)
        i = 0
        current_infected = []

        while (i < rows_num):
            current_infected.append(self.get_covid_start()['Confirmed'].iloc[i] - \
                self.get_covid_start()['Recovered'].iloc[i] - \
                    self.get_covid_start()['Deaths'].iloc[i])
            i += 1

        # add this list as a column to the dataframe, for a new dataframe as output

        df_current = self.get_covid_start().assign(Current = current_infected)

        return df_current

    def daily_change(self):
        """calculate the difference between today and yesterday's confirmed cases
        parameters: none
        returns: change, an integer of most recent daily change"""

        change = self.df['Confirmed'].iloc[-1] - self.df['Confirmed'].iloc[-2]

        return change

    def make_sentence(self):
        """make a sentence of today's date, confirmed, current, deaths, recovered, new cases
        parameters: none
        returns: sentence, a string explaining date, confirmed, current, deaths, recovered, new cases in text"""

        sentence = "As of " + str(self.df['Date'].iloc[-1]) + ", there has been " \
         + str(self.df['Confirmed'].iloc[-1]) + " confirmed cases in " + country \
         + ", which had first contact with COVID-19 on " \
         + str(self.get_covid_start_date()) + ". Of these, " \
         + str(self.add_current_col()['Current'].iloc[-1]) \
         + " are current cases with " + str(self.df['Deaths'].iloc[-1]) \
         + " deaths and " + str(self.df['Recovered'].iloc[-1]) + " recovered." \
         + " There are " + str(self.daily_change()) + " new cases today."

        return sentence

    def graph_all(self):
        """create a graph, with x-axis being date and y-axis being population
        parameters: none
        returns: a graph"""

        ax = plt.gca()
            
        self.add_current_col().plot(kind = 'line', x = 'Date', y = 'Confirmed', \
            color = 'yellow', ax = ax)
        self.add_current_col().plot(kind = 'line', x = 'Date', y = 'Recovered', \
            color = 'green', ax = ax)
        self.add_current_col().plot(kind = 'line', x = 'Date', y = 'Deaths', \
            color = 'red', ax = ax)
        self.add_current_col().plot(kind = 'line', x = 'Date', y = 'Current', \
            color = 'orange', ax = ax)
        plt.figtext(0.5, 0.01, self.make_sentence(), wrap = True, \
            horizontalalignment = 'center', fontsize = 10)
        plt.title("COVID-19 situation in " + country, fontsize = 18, \
            fontweight = "bold")

        plt.show()

a = Country(stats_country)
a.graph_all()
