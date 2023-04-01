import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import string
import os



dict = { }

## Valid Char Files for generating the files
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
#''.join(c for c in filename if c in valid_chars)


# Structure needed for each line
# - name (key)
# - date
# - sellPrice
# - qty
# - earnings
# - type
class sellLine:
    name = "object name"
    date = datetime.date
    month = "YYYY-MM"
    day = "YYYY-MM-DD"
    sellPrice = 1.0
    qty = 1
    earning = 0.65
    type = "PDF"

finalDate = datetime.strptime('01-01-1900', '%d-%m-%Y')

## Reading the DTRPG CSV files

dir_path = 'dtrpg-csv'
for path in os.listdir('dtrpg-csv'):
    if os.path.isfile(os.path.join(dir_path, path)):
        print("Analyse du fichier : " + dir_path + '\\' + path)
        df = pd.read_csv(dir_path + '\\' + path)

        for index, row in df.iterrows():
            itemName = str(row['Name'])
            if itemName != '' and itemName != 'nan':
                
                # Creating the object
                line = sellLine()
                line.name = row['Name']
                line.qty = row['Quantity']
                line.date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
                line.month = line.date.strftime("%Y-%m")
                line.day = line.date.strftime("%Y-%m-%d")
                finalDate = max(finalDate, line.date)
                line.sellPrice = row['SellPrice']
                line.earning = row['Earnings']
                line.type = row['Order Type']
                    
                if itemName in dict:
                    dict[itemName].append(line)
                else:
                    dict[itemName] = [ line ]    

## Markdown output
mkdOutput = ''
print("finalDate = " + str(finalDate))

###################
## For each game ##
###################
for key, value in dict.items():
    keyFilename = ''.join(c for c in key if c in valid_chars)

    ## Display stuff in Console (for testing)
    print(key)
    sumEarning = sum(l.earning for l in value)
    sumQty = sum(l.qty for l in value)
    print("Earnings : " + str(sumEarning) + " / Qty : " + str(sumQty))

    ## Collecting the dates
    firstSell = min(l.date for l in value)
    lastSell = max(l.date for l in value)
    '''
    tMonths = []
    tMonthsDT = []
    curDate = firstSell
    while (curDate.year < lastSell.year) or (curDate.year == lastSell.year and curDate.month <= lastSell.month):
        tMonthsDT.append(curDate)
        tMonths.append(curDate.strftime("%Y-%b"))
        if (curDate.month == 12):
            curDate = datetime(curDate.year + 1, 1, 1)
        else:
            curDate = datetime(curDate.year, curDate.month + 1, 1)
    
    tCounts = [ ]
    tCumulated = [ ]
    iCumulated = 0
    
    for month in tMonthsDT:
        count = 0
        for item in value:
            if (item.date.year == month.year) and (item.date.month == month.month):
                count += item.qty
        tCounts.append(count)
        iCumulated += count
        tCumulated.append(iCumulated)
    '''

    ###################################################
    ## Generate a graph for each game,               ##
    #   showing month by month the evolution of sales #
    ###################################################
    '''
    fig, ax = plt.subplots()

    bar_colors = [ 'blue' ]
    plot_colors = [ 'red' ]

    # Sales, month by month (bar)
    ax.bar(tMonths, tCounts, color=bar_colors)
    ax.set_ylabel('Sales')
    ax.set_title('Evolution des ventes')
    ax.legend(title=key)

    # Sales, cumulated
    aCumul = ax.twinx()
    aCumul.plot(tMonths, tCumulated,'r')
    aCumul.set_ylabel('log')

    plt.savefig("month-by-month\\" + keyFilename + '.png')
    plt.cla()
    '''
    #############################
    ## End of graph generation ##
    #############################

    ###################################
    ## Markdown Output for this game ##
    ###################################
    mkdGame = '# ' + key + '\r'
    mkdGame += firstSell.strftime("%d-%m-%Y") + ' - ' + lastSell.strftime("%d-%m-%Y") + '\r'
    totalSell = sum(l.qty for l in value if l.earning > 0)
    totalDwnl = sum(l.qty for l in value)
    totalEarn = sum(l.earning for l in value)
    mkdGame += str(totalSell) + '/' + str(totalDwnl) + ' ventes/téléchargements pour un total de $' + format(sumEarning, '.2f') + '\r'
    
    #####################
    # Analysis by month #
    value.sort(key=lambda x: x.date)
    # Best month/day (most sells #)
    bestMonth = { 'month': '0000-00', 'sells': -1 }
    curMonth = bestMonth
    bestDay = { 'day': '0000-00-00', 'sells': -1 }
    curDay = bestDay
    # Also a breakdown of the last 3 months
    lastMonthMinus2 = { 'month': '0000-00', 'sells': 0, 'downloads' : 0 }
    lastMonthMinus1 = { 'month': '0000-00', 'sells': 0, 'downloads' : 0 }
    lastMonth = { 'month': '0000-00', 'sells': 0, 'downloads' : 0 }
    if (finalDate.month == 1): # January
        lastMonthMinus2['month'] = str(finalDate.year - 1) + '-11'
        lastMonthMinus1['month'] = str(finalDate.year - 1) + '-12'
        lastMonth['month'] = str(finalDate.year) + '-01'
    elif (finalDate.month == 2): # February
        lastMonthMinus2['month'] = str(finalDate.year - 1) + '-12'
        lastMonthMinus1['month'] = str(finalDate.year) + '-01'
        lastMonth['month'] = str(finalDate.year) + '-01'        
    else:
        lastMonthMinus2['month'] = str(finalDate.year) + '-' + format(finalDate.month - 2, '02d')
        lastMonthMinus1['month'] = str(finalDate.year) + '-' + format(finalDate.month - 1, '02d')
        lastMonth['month'] = str(finalDate.year) + '-' + format(finalDate.month, '02d')        
    
    for val in value:
        # Best Month
        if curMonth['month'] != val.month: # a new moth
            if curMonth['sells'] > bestMonth['sells']:
                bestMonth = curMonth
            curMonth = { 'month': val.month, 'sells': 0 }
        if val.earning > 0:
            curMonth['sells'] += val.qty
        # Best Day
        if curDay['day'] != val.day: # a new day
            if curDay['sells'] > bestDay['sells']:
                bestDay = curDay
            curDay = { 'day': val.day, 'sells': 0 }
        if val.earning > 0:
            curDay['sells'] += val.qty
        # Last 3 months
        if lastMonth['month'] == val.month:
            lastMonth['downloads'] += val.qty
            if (val.earning > 0):
                lastMonth['sells'] += val.qty
        elif lastMonthMinus1['month'] == val.month:
            lastMonthMinus1['downloads'] += val.qty
            if (val.earning > 0):
                lastMonthMinus1['sells'] += val.qty
        elif lastMonthMinus2['month'] == val.month:
            lastMonthMinus2['downloads'] += val.qty
            if (val.earning > 0):
                lastMonthMinus2['sells'] += val.qty

    if curMonth['sells'] > bestMonth['sells']:
        bestMonth = curMonth
    if curDay['sells'] > bestDay['sells']:
        bestDay = curDay
    mkdGame += 'Meilleur mois : ' + bestMonth['month'] + ' (' + str(bestMonth['sells']) + ' ventes)\r'
    mkdGame += 'Meilleur jour : ' + bestDay['day'] + ' (' + str(bestDay['sells']) + ' ventes)\r'
    mkdGame += 'Mois M-2 : ' + str(lastMonthMinus2['sells']) + ' / ' + str(lastMonthMinus2['downloads'])
    mkdGame += ' ventes/downloads\r'
    mkdGame += 'Mois M-1 : ' + str(lastMonthMinus1['sells']) + ' / ' + str(lastMonthMinus1['downloads'])
    mkdGame += ' ventes/downloads ('
    mkdGame += format(100 * (lastMonthMinus1['sells'] - lastMonthMinus2['sells']) / max(lastMonthMinus2['sells'], 0.1), '+.0f') + '% / '
    mkdGame += format(100 * (lastMonthMinus1['downloads'] - lastMonthMinus2['downloads']) / max(lastMonthMinus2['downloads'], 0.1), '+.0f') + '% )\r'
    mkdGame += 'Dernier mois : ' + str(lastMonth['sells']) + ' / ' + str(lastMonth['downloads'])
    mkdGame += ' ventes/downloads ('
    mkdGame += format(100 * (lastMonth['sells'] - lastMonthMinus1['sells']) / max(lastMonthMinus1['sells'], 0.1), '+.0f') + '% / '
    mkdGame += format(100 * (lastMonth['downloads'] - lastMonthMinus1['downloads']) / max(lastMonthMinus1['downloads'], 0.1), '+.0f') + '% )\r'
    mkdOutput += mkdGame + '\r'

## Final Markdown file
mkdFile = open("global.md", "w", encoding='utf-8')
mkdFile.write(mkdOutput)
mkdFile.close()