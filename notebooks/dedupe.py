import json
import pandas as pd
from settings import PATHS

df = pd.read_pickle(PATHS['outdata'])
wallets = list(df.index)

for name, fname in PATHS['graphs'].items():
    
    print("Reading graph for:", name)
    
    try:
        with open(fname, 'r') as infile:
            
            data = json.load(infile)

            graph_wallets = data['wallets']
            print("Num wallets in list:", len(graph_wallets))

            deduped = set([w.lower() for w in data['wallets']])
            print("Deduped list", len(deduped))

            overlap = set(wallets).intersection(deduped)
            print("Tracked wallets", len(overlap))

        # uncomment to update records
        # data['wallets'] = list(deduped)        
        # with open(fname, 'w') as outfile:
        #     json.dump(data, outfile, indent=2)

    except Exception as e:        
        print("No wallet list for", name)
    
    print()