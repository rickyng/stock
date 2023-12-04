#('Trades', 'Trades'), ('Header', 'SubTotal'), ('DataDiscriminator', ''), 
#('Asset Category', 'Equity and Index Options'), ('Currency', 'USD'), 
#('Symbol', 'V     200821C00207500'), ('Date/Time', ''), ('Quantity', '0'), 
#('T. Price', ''), ('C. Price', ''), ('Proceeds', '115'), ('Comm/Fee', '-1.0983415'), 
#('Basis', '-0.0000005'), ('Realized P/L', '113.901658'), ('MTM P/L', '54.35'), ('Code', '')

import csv

from collections import defaultdict
from datetime import datetime, timedelta
class RowParser:
    header = []
    def setheader(self, list):
        self.header = list
    def get(self, row, str):
        return row[self.header.index(str)]

trades = defaultdict(lambda:  defaultdict( lambda:  defaultdict( lambda:  defaultdict( float)) ))
week = defaultdict(lambda:  defaultdict( lambda:  defaultdict( lambda:  defaultdict( float)) ))
dividend = defaultdict( lambda:  defaultdict( float))
withholdingTaxParsed = False
def parseDividend(row):
    stock = row['Description'].split('(')[0]
    amount = float(row['Amount'])
    date = row ['Date']
    dividend[date][stock] += amount
    

def parseOption(row):
    stock = row['Symbol'].split(' ')[0]
    stock = '{num:04d}'.format(num=int(stock)) + '.HK' if row['Currency'] == 'HKD' else stock
    proceed = row['Proceeds'] if row['Proceeds'].find('&nbsp') == -1 else row['Proceeds'][:(row['Proceeds'].find('&nbsp'))]
    price = float(row['T. Price'] if row['T. Price'].find('&nbsp') == -1 else row['T. Price'][:(row['T. Price'].find('&nbsp'))])
    amount = (float(proceed) + float(row['Comm/Fee']))
    position = int(row['Quantity'].replace(',', ''))
    #print('%s, %s, %.2f, %d, %.2f ' % (stock, row['Date'], amount, position, price))
    #print(stock, row['Date'], amount, position, price)


def parseTrade(row):
    if row['Symbol'] == '9618.SPO':
        return
    stock = row['Symbol'] if row['Asset Category'] == 'Stocks' else row['Symbol'].split(' ')[0]
    if stock != '3690.SPO':
        stock = '{num:04d}'.format(num = int(stock))+'.HK' if row['Currency'] == 'HKD'   else stock
    
    trade_date_time = datetime.strptime(row['Date/Time'], '%Y-%m-%d, %H:%M:%S')
    trade_date_time_str = trade_date_time.strftime("%m/%d/%Y")
    proceed = row['Proceeds'] if row['Proceeds'].find('&nbsp') == -1 else row['Proceeds'][:(row['Proceeds'].find('&nbsp'))]
    price = row['T. Price'] if row['T. Price'].find('&nbsp') == -1 else row['T. Price'][:(row['T. Price'].find('&nbsp'))]
    #print (row['Proceeds'], proceed)
    
    
    week_start = trade_date_time - timedelta(days=trade_date_time.weekday())
    #print (trade_date_time.strftime("%d/%m/%Y" ), week_start.strftime("%d/%m/%Y"))
    week_time_str = week_start.strftime("%m/%d/%Y")
    if float(proceed) + float(row['Comm/Fee']) == 0:
        #print ("skip %s, %s, %s, %s, %s, %s, %s, %s"%(trade_date_time_str,row['Currency'],stock, row['Symbol'], row['Quantity'], price, proceed, row['Comm/Fee']))
        return

    #trades[stock]['Total']['amount'] += (float(proceed) + float(row['Comm/Fee']))
    #trades[stock]['Total']['position'] += int(row['Quantity'].replace(',', ''))
    week [week_time_str][row['Asset Category']][stock + ", " + row['Currency']]['amount'] += (float(proceed) + float(row['Comm/Fee']))
    week [week_time_str][row['Asset Category']][stock + ", " + row['Currency']]['position'] += int(row['Quantity'].replace(',', ''))

    trades[row['Asset Category']][trade_date_time_str][row['Symbol']]['Symbol'] = stock
    trades[row['Asset Category']][trade_date_time_str][row['Symbol']]['Currency'] = row['Currency']
    trades[row['Asset Category']][trade_date_time_str][row['Symbol']]['amount'] += (float(proceed) + float(row['Comm/Fee']))
    trades[row['Asset Category']][trade_date_time_str][row['Symbol']]['position'] += int(row['Quantity'].replace(',', ''))
    trades[row['Asset Category']][trade_date_time_str][row['Symbol']]['price'] = float(price.replace(',', ''))

#with open("/Users/rickyng/Downloads/U5797815_20210101_20210312.csv", 'r') as csvfile:


with open("/Users/rickyng/Downloads/U5668308_20230102_20230628.csv", 'r') as csvfile:  #no1
#with open("/Users/rickyng/Downloads/U9371321_20230102_20230526.csv", 'r') as csvfile:   #no2
#with open("/Users/rickyng/Downloads/U5797815_20220103_20220113.csv", 'r') as csvfile:    #winnie
    spam_reader = csv.reader(csvfile, delimiter=',')
    header = []
    for line in spam_reader:
        if len(line) == 1:
            continue
        if line[1] == 'Header' or line[1] == 'Headers':
            header = line
            #print (header)
        else:
            row = dict(zip(header, line))
            if line[0] == "Option Exercises, Assignments and Expirations":
                if ( row['Type'] == 'Assignments' and row['Transaction Type'] != 'Assignment'):
                    parseOption(row)
            elif line[0] == 'Trades':
                if (row['Asset Category'] == 'Stocks' or row['Asset Category'] == 'Equity and Index Options' ) and row['DataDiscriminator'] == 'Trade':
                    parseTrade(row)
            elif line[0] == 'Cash Report':
                #if (row['Currency']) == 'Base Currency Summary':
                    print ("%s, %s, %0.2f"%(row['Currency Summary'], row['Currency'], float(row['Total'])))

            elif line[0] == 'Withholding Tax':
                parseDividend(row)
                withholdingTaxParsed = True
            elif not(withholdingTaxParsed) and line[0] == 'Dividends':
                parseDividend(row)

    with open('stock.csv', mode='w') as stock_file:
        stock_writer = csv.writer(stock_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for key, value in trades['Stocks'].items():
            for k, v in value.items():
                # print ('%s, %s, %.2f, %.0f, %.2f '%(key, k, v['amount'], v['position'], v['price']))
                stock_writer.writerow([key, k, v['Symbol'], v['Currency'], v['amount'], v['position'], v['price']])

    with open('option.csv', mode='w') as option_file:
        option_writer = csv.writer(option_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key, value in trades['Equity and Index Options'].items():
            for k, v in value.items():
                # print ('%s, %s, %.2f, %.0f, %.2f '%(key, k, v['amount'], v['position'], v['price']))
                option_writer.writerow([key, v['Symbol'],k,  v['Currency'], v['amount'], v['position'], v['price']])
            
    #for c , j in trades.items():
    #print (dividend)
    with open('dividend.csv', mode='w') as dividend_file:
        dividend_writer = csv.writer(dividend_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for date, value in dividend.items():
            for stock, amount in value.items():
                dividend_writer.writerow([date, stock, amount])


                
    for c , j in week.items():
        for key, value in j.items():
            for k, v in value.items():
                #print ('%s, %s, %s, %.2f, %.0f, %.2f '%(c, key, k, v['amount'], v['position'], v['price']))       
                pass
