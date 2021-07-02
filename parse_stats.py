import json

with open('harvest_stats.json') as f:
   stats = json.load(f)

pcount = 0
fcount = 0
for s in stats.keys():
    if stats[s]['status'] == 'publised':
        pcount += 1
    else:
        fcount += 1

        print("{} --- Schema ERRORS {} --- ODP ERRORS {}".format(s, stats[s]['schema_errors'], stats[s]['odp_errors']))

print("published count: {}\nfailed count {}".format(pcount, fcount))


#print(stats[stats.keys()[0]])
