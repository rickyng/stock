import yahoo_fin.options as ops
import pandas
#expiration_dates = ops.get_expiration_dates("aapl")
#print(expiration_dates)

stocks =  ["aapl", "nflx", "msft"]
for s in stocks:
    options = ops.get_options_chain(s)
    call_file_name = s +"_call.csv"
    put_file_name = s + "_put.csv"
    options["calls"].to_csv(call_file_name)
    options["puts"].to_csv(put_file_name)
#chain = pandas.read_csv(file_name)
#print(chain.columns)
#['Strike'], d['Last Price']