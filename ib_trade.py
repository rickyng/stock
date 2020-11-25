#('Trades', 'Trades'), ('Header', 'SubTotal'), ('DataDiscriminator', ''), 
#('Asset Category', 'Equity and Index Options'), ('Currency', 'USD'), 
#('Symbol', 'V     200821C00207500'), ('Date/Time', ''), ('Quantity', '0'), 
#('T. Price', ''), ('C. Price', ''), ('Proceeds', '115'), ('Comm/Fee', '-1.0983415'), 
#('Basis', '-0.0000005'), ('Realized P/L', '113.901658'), ('MTM P/L', '54.35'), ('Code', '')

import csv

from collections import defaultdict
from datetime import datetime, timedelta

trades = defaultdict(lambda:  defaultdict( lambda:  defaultdict( lambda:  defaultdict( float)) ))
week = defaultdict(lambda:  defaultdict( lambda:  defaultdict( lambda:  defaultdict( float)) ))
def parseTrade(row):
    stock = row['Symbol'] if row['Asset Category'] == 'Stocks' else row['Symbol'].split(' ')[0]
    stock = '{num:04d}'.format(num = int(stock))+'.HK' if row['Currency'] == 'HKD' else stock
    
    trade_date_time = datetime.strptime(row['Date/Time'], '%Y-%m-%d, %H:%M:%S')
    trade_date_time_str = trade_date_time.strftime("%d/%m/%Y %H:%M:%S")
    proceed = row['Proceeds'] if row['Proceeds'].find('&nbsp') == -1 else row['Proceeds'][:(row['Proceeds'].find('&nbsp'))]
    price = row['T. Price'] if row['T. Price'].find('&nbsp') == -1 else row['T. Price'][:(row['T. Price'].find('&nbsp'))]
    #print (row['Proceeds'], proceed)
    
    
    week_start = trade_date_time - timedelta(days=trade_date_time.weekday())
    #print (trade_date_time.strftime("%d/%m/%Y" ), week_start.strftime("%d/%m/%Y"     ))
    week_time_str = week_start.strftime("%d/%m/%Y")
    
    #print ("%s, %s, %s, %s, %s, %s, %s, %s"%(trade_date_time_str,row['Currency'],stock, row['Symbol'], row['Quantity'], price, proceed, row['Comm/Fee']))
    
    #trades[stock]['Total']['amount'] += (float(proceed) + float(row['Comm/Fee']))
    #trades[stock]['Total']['position'] += int(row['Quantity'].replace(',', ''))
    week [week_time_str][row['Asset Category']][stock + ", " + row['Currency']]['amount'] += (float(proceed) + float(row['Comm/Fee']))
    week [week_time_str][row['Asset Category']][stock + ", " + row['Currency']]['position'] += int(row['Quantity'].replace(',', ''))

    trades[row['Asset Category']][stock][trade_date_time_str+', '+row['Symbol']+', '+row['Currency']]['amount'] += (float(proceed) + float(row['Comm/Fee']))
    trades[row['Asset Category']][stock][trade_date_time_str+', '+row['Symbol']+', '+row['Currency']]['position'] += int(row['Quantity'].replace(',', ''))
    trades[row['Asset Category']][stock][trade_date_time_str+', '+row['Symbol']+', '+row['Currency']]['price'] += float(price.replace(',', ''))
    

skip = 0
with open("C:/Users/u8009900/Downloads/U5668308_20200101_20201124.csv", 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        if row[0] == 'Trades':
            header = row
            #print (header)
            trade_reader = csv.DictReader(csvfile, fieldnames=header)
            for row in trade_reader:
                if row['Trades'] != 'Trades':
                    break
                #if row['Asset Category'] == 'Equity and Index Options' and row['DataDiscriminator'] == 'Trade':
                #if row['Asset Category'] == 'Stocks' and row['DataDiscriminator'] == 'Trade':
                if (row['Asset Category'] == 'Stocks' or row['Asset Category'] == 'Equity and Index Options' ) and row['DataDiscriminator'] == 'Trade':
                    if row['Header'] == 'Data':
                        #date_time_obj = datetime. strptime(row['Date/Time'], '%d/%m/%y %H:%M:%S')
                        parseTrade(row)
                
            
    for c , j in trades.items():
        for key, value in j.items():
            for k, v in value.items():
                print ('%s, %s, %.2f, %.0f, %.2f '%(key, k, v['amount'], v['position'], v['price']))       
                pass
                
    for c , j in week.items():
        for key, value in j.items():
            for k, v in value.items():
                #print ('%s, %s, %s, %.2f, %.0f, %.2f '%(c, key, k, v['amount'], v['position'], v['price']))       
                pass