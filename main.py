"""Covid 19 cases report.
#Author: Mohammad Aloufi
Using this api:
https://corona.lmao.ninja/
The end goal of this project is to have a dynamicly generated html page that contains a usual report of COVID19 cases around the world, along with some stats some people like me might find intresting.
"""

#Lets import all kinds of libraries
from datetime import datetime
import requests
import json
import webbrowser
import sys
import pandas as pd

#request url
requesturl ='https://disease.sh/v3/covid-19/countries'

#We do the actual request for the data
print('Retrieving data...')
try:
   request =requests.get(requesturl)
except requests.ConnectionError as e:
   input('Error: no internet connection\nPress enter to exit')
   sys.exit()

#Now we load the list of dictionaries we got into a json object.
dict = json.loads(request.text)
print('Loaded!')

#We create a list then we iterate through the list of dictionaries we got from the api, adding them to the templist then appending that to the rowslist. The reason we just didn't hook the list of dictionaries to the DataFrame we'll create in a sec directly is because we don't need all the data we got back with the request.
print('Generating report...')
rowslist=[]
for i in dict:
    templist =[i["country"], int(i["cases"]), int(i["todayCases"]), int(i["deaths"]), int(i["todayDeaths"]), int(i["recovered"]), int(i["todayRecovered"]), int(i["active"]), int(i["critical"]), int(i["tests"]), int(i["casesPerOneMillion"]), int(i["deathsPerOneMillion"]), int(i["population"])]
    rowslist.append(templist)

#Creating the DataFrame, it'll hold the data we filtered
df =pd.DataFrame(rowslist)

#Labeling columns
df.columns =["Country","Total cases","Today's cases","Total deaths","Today's deaths","Total recoveries", "today's recoveries", "Active cases", "Critical cases", "Total tests", "Cases per million", "Deaths per million", "Population"]

#It's time for the html page generation. I wish there was an easier way of doing this, I really do.
report ='<!DOCTYPE html><html><head><title>Corona Virus Stats Report</title></head><body><h1>Introduction</h1>This is a dynamically generated page with the latest stats for Corona virus.<br>Note: The data are shown here might not be fully accurate. The data are sourced from <a href="https://corona.lmao.ninja/">this API</a><h1>Stats for all countries</h1>'
report +='<table><caption>Country stats</caption><tr>'

#We create a temparrary list that hold the table headings, then we iterate over it, creating the table hedders as we go.
templist=["Country", "Total cases", "Today's cases", "total deaths", "Today's deaths", "Total recoveries", "Today's recoveries", "Active cases", "Critical cases", "Total tests", "Cases per million", "Deaths per million", "Population"]
for i in templist:
    report +='<th>{}</th>'.format(i)
report +'</tr>'

#Now we create the rows in the html table.

for  i in range(len(df.index)):
    report +='<tr>'
    for i2 in range(len(df.columns)):
        report +='<td>{}</td>'.format(df.iloc[i][i2])
    report +'</tr>'
report +='</table><br>'

#The other stats
report +='<h1>Other stats</h1>Here are some other stats based on the stats shown in the table above.<br>'
report +='<h2>Top 10s</h2>'
report +='<h3>Top 10 countries with the most cases</h3><br><ol>'
#Top 10 countries with most cases
df.sort_values(by=['Total cases'], inplace=True, ascending=False)

total =df['Total cases'].sum()

for i in range(10):
    report +='<li>{}, with {} cases. That counts for {}% of the total world cases</li>'.format(df.iloc[i][0], df.iloc[i][1], round(df.iloc[i][1]/total*100, 2))
report +='</ol><br>'

#Top 10 countries with most active cases
df.sort_values(by=['Active cases'], inplace=True, ascending=False)
active =df['Active cases'].sum()
report +='<h3>Top 10 countries with the most active cases</h3><br><ol>'
for i in range(10):
    report +='<li>{}, with {} active cases. That counts for {}% of the total active cases in the world</li>'.format(df.iloc[i][0], df.iloc[i][7], round(df.iloc[i][7]/total*100, 2))
report +='</ol><br>'

report +="<h2>List of countries progress toward full recovery from corona virus</h2>Estimated date for full recovery might not be available for all countries. The estimation is based on the last stats that country shared.<br>The feature might be unavailable for a country either because the last stats that country has shared to the public doesn't hint at a decline in active cases. One other reason is probably because simpley that country has not updated  their stats yet for today.<br>Some countries update their stats more than once a day. in that case the date will be less accurate, like the USA for example.<br> If your country doesn't show an estimated date for full recovery, please check back again later.<br><ul>"

#List of countries progress towards recovery
for i in range(len(df.index)):
    if round(df.iloc[i][5]/df.iloc[i][1]*100, 2)>0.0:
        report +='<li>{}, {}%.'.format(df.iloc[i][0], round(df.iloc[i][5]/df.iloc[i][1]*100, 2))
        if df.iloc[i][6] > df.iloc[i][2]:
                report +=' Estimated date for full recovery: {}'.format(datetime.strftime(pd.to_datetime('today', exact=False, utc=False).today()+pd.DateOffset(days=int(df.iloc[i][7]/(df.iloc[i][6]-df.iloc[i][2]))), '%d/%m/%Y'))
        report +='</li>'
report +='</ul><br>'

#Miscellaneous stats
report +='<h2>Miscellaneous stats</h2>'
report +='<ul><li>Total cases in the world as of the time the report created: {}</li><li>Average cases per country: {}</li><li>Total active cases in all countries: {}</li><li>Average active cases per country: {}</ul><br>'.format(total, round(df['Total cases'].mean(), 2), active, round(df['Active cases'].mean(), 2))

#World progress towards full recovery
report +='World progress towards full recovery from the corona virus: {}%'.format(round(active/total*100, 2))
report +='</body></html>'
#we're done with the report. Lets save it. Open the file, write the stuff, then close the file.
file =open("report.html","w")
file.write(report)
file.close()
print('Report generated and saved')
question =input('Do you want to view the report now?\ntype "yes" or press enter to continue')
if question.lower()=='yes':
    webbrowser.open('report.html',new=0)
else:
    input('The report has been saved in a file called "report.html". You can view it any time.\nPress enter to exit')