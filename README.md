# What's this?

This is an app that does some data analysis on the covid19 latest dataset.

# How to use?

First things first: If you want to run this from source, you have to install pandas first.  
"pip install pandas"  
I think you might need numpy too:  
"pip install numpy"  
Using the app is simple. You just have to open it and wait for it to generate a report. When it's done, it'll print a message telling you that the report is generated and saved.
It will ask you if you want to view the report or not, answer yes if you want to read it or just press enter if not.
It will tell you that the report has been saved in a file called "report.html" so you can read it any time you like.

# The report

The report itself contains the usual stats for all countries that have been infected with the virus so far, along with other stats like:

* Top 10 countries with the most cases
* Top 10 countries with the most active cases.
* List of countries progress toward full recovery from corona virus.
* Estimated date for a country  to fully recover from the corona virus.

And more...

Unfortunately, the api doesn't give me access to the data sets for the previous few days, or else I probably would have been able to improve the accuracy of the date estimated for full recovery.
However, if you see a country's estimaded date say 29/09/2020 and you check it the next day and find it changed to 27/09/2020, that means that they're on the right track.

# Contributions

Contributions are always welcome.

# Released version

At first I couldn't upload a released version to github, that was because the file size was larger than 10 mb. However, I upload it using the binary option and it worked.
You can grab the released version from [here](https://github.com/mohammad-aloufi/COVID19-data-analysis-/releases/download/V1.0/Covid19_Data_Analysis.zip)