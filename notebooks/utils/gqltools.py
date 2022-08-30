import glob
import json
import requests
import time


def execute_subgraph_query(
    api_function, 
    list_of_wallets, 
    num_wallets_per_call, 
    json_filepath, 
    append_to_existing_file=False,
    return_json=False):
    
    """
        Executes a large GraphQL query on a list of wallet addresses
        by batching into smaller requests. Dumps the results to JSON.
        Has some basic handling for appending new data without having
        to overwrite everything that's already been pulled.
        
        args:
        - api_function: any function that takes a list of wallets, 
                        runs a query, and returns a JSON package

        - list of wallets: a list of EVM public addresses

        - num_wallets_per_call: a batch limiter to avoid API rate
                                limits / prevent timeouts

        - json_filepath: "../private_data/graphs/*.json"
        
        - append_to_existing_file: (bool) append or overwrite data
        
        - return_json: (bool) whether to return the jsondata or not
        
    """
    
    # check if we've run this before
    if glob.glob(json_filepath) and append_to_existing_file:                
        with open(json_filepath, 'r') as infile:
            json_data = json.load(infile)
        
        list_of_wallets = [w for w in list_of_wallets 
                           if w not in json_data["wallets"]]        
    else:
        json_data = {"wallets": [], "data": []}
    
    # batch the api calls
    new_data = []
    for start in range(0, len(list_of_wallets), num_wallets_per_call):
        end = start + num_wallets_per_call
        if end < len(list_of_wallets):
            res = api_function(list_of_wallets[start:end])
        else:
            res = api_function(list_of_wallets[start:])
        new_data.extend(res)
    
    # dump the data
    json_data["wallets"].extend(list_of_wallets)
    json_data["data"].extend(new_data)
    with open(json_filepath, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)
    
    if return_json:
        return json_data
    return None
        

def subgraph_query(api_url, query_docstring, list_of_wallets):
    """
        Standard script for prepping and running GraphQL queries.
        Doesn't have any error handling, so test your queries!
        
        args:
        - api_url: the url for the GraphQL call you want to make
        - query_docstring: a GraphQL query in the form of a docstring
                           ** must have a $WALLETS field in it **
        - list of wallets: a list of EVM public addresses

        returns:
        - the (unformatted) data contained in a JSON payload

    """
    
    str_list = ", ".join(f'"{w}"' for w in list_of_wallets)
    query = query_docstring.replace("$WALLETS", str_list)
    r = requests.post(api_url, json={'query': query})

    try:
        json_data = json.loads(r.text)
    except:
        print("** ERROR **")
        print(api_url)
        print(query)
        time.sleep(30)
        return subgraph_query(api_url, query_docstring, list_of_wallets)
    
    return json_data