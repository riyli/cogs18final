from covidgraph import *

covid = pd.read_csv(r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')
x = Country(covid[covid['Country'] == "Algeria"])

assert type(x.make_sentence()) == str
assert type(x.daily_change()) == int