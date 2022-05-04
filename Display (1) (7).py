'''
@author: Atharva Teli
'''
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
lobbyistIDs = ["20205046078", "20017000757", "20065077165",
               "20175040611", "20185032494", "20025000207", "20085002192"]

# Connection to SQLite DB.
conn = sqlite3.connect('lobbyistDB.sqlite')
conn.text_factory = str
cur = conn.cursor()

# Creating dictionaries and lists to hold the data in for visualization
datadict = dict()
primarylidlist = list()
reportduedatelist = list()
incomeamountlist = list()
dateincomereceivedlist = list()
fiscalyearlist = list()
reportmonthlist = list()

# Select Query to Implement
for ids in lobbyistIDs:
    cur.execute('''SELECT primarylobbyistid, incomeamount, reportduedate, dateincomereceived, fiscalyear, reportmonth FROM LobbyistDB WHERE primarylobbyistid = ? and incomeamount != 'NONE' order by dateincomereceived limit 100''', (ids,))
    for i in cur:
        primarylidlist.append(int(i[0]))
        incomeamountlist.append(float(i[1]))
        reportduedatelist.append(i[2])
        dateincomereceivedlist.append(i[3])
        fiscalyearlist.append(i[4])
        reportmonthlist.append(i[5])

# Creating a dictionary
datadict["primarylobbyistid"] = primarylidlist
datadict["incomeamount"] = incomeamountlist
datadict["reportduedate"] = reportduedatelist
datadict["dateincomereceived"] = dateincomereceivedlist
datadict["fiscalyear"] = fiscalyearlist
datadict["reportmonth"] = reportmonthlist

# Assigning the arrays to numpy
npprimarylidlist = np.array(primarylidlist)
npincomeamountlist = np.array(incomeamountlist)
npreportduedatelist = np.array(reportduedatelist)
npdateincomereceived = np.array(dateincomereceivedlist)
npfiscalyearlist = np.array(fiscalyearlist)
npreportmonthlist = np.array(reportmonthlist)

for ids in lobbyistIDs:
    idfilter = npprimarylidlist == int(ids)
    incamtfilter = npincomeamountlist[idfilter]
    print("Statistics for", ids)
    print("Minimum monthly income: ${0:8.6f}\nMaximum monthly income: ${1:8.6f}".format(
        np.amin(incamtfilter), np.amax(incamtfilter)))
    print("Median: {}\nMean: {}\nStandard Deviation: {}\nAverage: {}".format(np.median(
        incamtfilter), np.mean(incamtfilter), np.std(incamtfilter), np.average(incamtfilter)))
    print('\n')
df = pd.DataFrame(datadict)

# ScatterPlot
df2 = df.groupby(['fiscalyear']).agg({'incomeamount': 'sum'})
plt.scatter(df2.index, df2['incomeamount'])
plt.title("Income Amount by Fiscal Year")
plt.xlabel("Fiscal Year")
plt.ylabel("Income Amount")
plt.savefig("ScatterPlot.png")
plt.show()

# LineGraph
table = pd.pivot_table(df, values=['incomeamount'], index=['fiscalyear'])
table.plot()
plt.xlabel("fiscalyear")
plt.ylabel("income amount")
plt.savefig("LineGraph.png")
plt.show()

# Histogram
df.hist(column='incomeamount', by="reportmonth", figsize=(15, 12))
plt.title("Income Amount by Report Month")
plt.savefig("Histogram.png")
plt.show()

# Extra feature PieChart
colors = sns.color_palette('muted')[0:5]
explode = [0, 0, 0, 0, 0, 0, 0, 0.3, 0, 0, 0, 0]
df.groupby(['reportmonth']).sum().plot(kind='pie', y='incomeamount', explode=explode, shadow=True,
                                       startangle=135, autopct='%1.0f%%', colors=colors, title='income amount % by month', figsize=(15, 12))
plt.legend(loc="upper right")
# Resizing the piechart
plt.xlim(-1.5, 2.0)
plt.savefig("Piechart.png")
plt.show()

# BarGraph
table1 = pd.pivot_table(df, values=['incomeamount'], index=[
                        'primarylobbyistid'])
table1.plot.bar()
plt.xlabel("Primary Lobbyist ID")
plt.ylabel("Income amount")
plt.title("Income Amount by Primary Lobbyist ID")
plt.savefig("BarGraph.png")
plt.show()


conn.close()
