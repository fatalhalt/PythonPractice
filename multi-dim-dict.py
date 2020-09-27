import sys
import re

# given following csv input, sum up the log size (last field) per each exchange per day

csv_input = """date,process,host,log,bytes
20140206,cme_trader_2,cme0001,0345-cme_trader_2.log.gz,15400000
20140206,phlx_trader_1,phlx0001,0651-phlx_trader_1.log.gz,14100000
20140206,phlx_trader_2,phlx0001,0645-phlx_trader_2.log.gz,13800000
20140207,cme_trader_2,cme0001,0345-cme_trader_2.log.gz,15800000
20140207,cme_trader_3,cme0001,0345-cme_trader_3.log.gz,14200000
20140207,phlx_trader_1,phlx0001,0651-phlx_trader_1.log.gz,24100000"""

# you need to access and update the numsize of each exch
# you want levearge multi-dim dict for auto/mapping each line of csv to avoid keeping csv like structure in memory
header = ''
exchange_logs = {}
lines = csv_input.splitlines()
for line in lines:
    l = line.split(',')
    log_exch = ''
    try:
        log_exch = re.search(r"^(.*)_trader_\d$", l[1]).group(1)
    except AttributeError:
        header = line
        continue
    #print('csv line is: ', l)
    log_date = l[0]
    log_size = l[4]

    if log_date not in exchange_logs.keys():
        exchange_logs[log_date] = {}

    if log_exch in exchange_logs[log_date].keys():
        exchange_logs[log_date][log_exch] += int(log_size)  # increment already present log size
    else:
        exchange_logs[log_date][log_exch] = int(log_size)   # inital assignment

print(header)
for k, v in sorted(exchange_logs.items()):
    for k2, v2 in sorted(v.items()):
        print("{0},{1},{2}".format(k, k2, v2))