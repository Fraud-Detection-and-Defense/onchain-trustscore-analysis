"""

A simple, naive flagging algorithm for identifying 
Sybil-like user behaviors and suspicious grants.

"""

import os
import pandas as pd
import sys


# column ids that need to map to columns in the csv file
ADDRESS_ID       = 'address'
HANDLE_ID        = 'handle'
GRANT_ID         = 'grant_id'
CONTRIB_ADDR_ID  = 'contributor_address'
SUCCESS_ID       = 'success'
SQUELCH_ID       = 'is_squelched'
TRUSTBONUS_ID    = 'trust_bonus'
CONTRIBUTION_ID  = 'contribution_id'
USD_AMOUNT_ID    = 'amount_in_usdt'


# special cases
GRANTS_TO_IGNORE = [12]
USERS_TO_IGNORE  = ['gitcoinbot']


def set_address(a1, a2):
    """
    Check validity of wallet addresses and convert to lower case
    Handle special case with zkSync contributions

    """
    
    a1 = a1.lower() if isinstance(a1, str) else ''
    a2 = a2.lower() if isinstance(a2, str) else ''
    if a1 == a2 and len(a1) == 42: 
        return a1
    elif len(a2) == 42: 
        return a2        
    elif len(a1) == 42: 
        return a1    
    return None


def load_transactions(csv_pathname):
    """
    Module to simplify cleaning of raw csv data
    Returns a dataframe
    
    """

    data = pd.read_csv(csv_pathname)

    data[ADDRESS_ID] = data.apply(
        lambda x: 
        set_address(x[ADDRESS_ID], x[CONTRIB_ADDR_ID]),
        axis=1)

    data = (data
            .iloc[:,1:]
            .query(f"{SUCCESS_ID} == True")
            .drop(columns=[CONTRIB_ADDR_ID, SUCCESS_ID])
            .sort_index())

    data = data[data[ADDRESS_ID].isna() == False]

    return data


def summarize_flags(data, flag_var, flagged_list, outpath=None):
    
    """
    Helper function for getting summary stats about a set of 
    user or grant behaviors

    """
    
    gby_vars = [ADDRESS_ID, HANDLE_ID, GRANT_ID]
    gby_vars.remove(flag_var)
        
    gby = data[data[flag_var].isin(flagged_list)].groupby(flag_var)
    result = pd.concat([
        gby[SQUELCH_ID].mean().rename("meanSquelchRate"),
        gby[TRUSTBONUS_ID].mean().rename("meanTrustBonus"),
        gby[CONTRIBUTION_ID].count().rename("numDonations"),
        gby[USD_AMOUNT_ID].sum().rename("sumUSD"),
        gby[gby_vars[0]].apply(set).rename(f"set{gby_vars[0].title()}"),
        gby[gby_vars[1]].apply(set).rename(f"set{gby_vars[1].title()}")
    ], axis=1)

    result[f"num{gby_vars[0].title()}"] = result[f"set{gby_vars[0].title()}"].apply(len)
    result[f"num{gby_vars[1].title()}"] = result[f"set{gby_vars[1].title()}"].apply(len)

    if outpath:
        result.to_csv(outpath)
    return result



def flag_addresses(data):

    """
    Identify wallet addresses associated with more than one user handle 
    AND that donated to the same grant more than once
    
    """

    mapping = data.groupby(ADDRESS_ID)[HANDLE_ID].agg("unique")
    return [
        a for a in mapping[mapping.apply(len)>1].index
        if (data
            .query(f"{ADDRESS_ID} == @a")[GRANT_ID]
            .value_counts()
            .max() > 1)
    ]


def flag_handles(data):

    """ 
    Identify user handles associated with more than one wallet address 
    AND that donated to the same grant more than once
    
    """

    mapping = data.groupby(HANDLE_ID)[ADDRESS_ID].agg("unique")
    return [
        h for h in mapping[mapping.apply(len)>1].index
        if (data
            .query(f"{HANDLE_ID} == @h")[GRANT_ID]
            .value_counts()
            .max() > 1)
    ]    


def flag_grants(all_data, flagged_data, flag_threshold):

    """
    A grant will be flagged if it has attracted a higher than average 
    share of transactions flagged for Sybil-like users / addresses

    """
    
    flag_ratio = (
        (flagged_data[GRANT_ID].value_counts()
            /all_data[GRANT_ID].value_counts())
        .dropna()
        .sort_values())

    return list(flag_ratio[flag_ratio >= flag_threshold].index)



def flag_transactions(data, outpath=None):
    
    """
    Flag transactions associated with one or more Sybil like behaviors
    
    """

    flagged_addresses = flag_addresses(data) 
    print("***", len(flagged_addresses), "addresses shared by multiple users.")

    flagged_handles = flag_handles(data) 
    print("***", len(flagged_handles), "users with multiple wallets.")

    flags = data[HANDLE_ID].isin(flagged_handles) | data[ADDRESS_ID].isin(flagged_addresses)    
    
    ratio = len(data[flags]) / len(data)
    print(f"Flagged {len(data[flags])} transactions ({100*ratio:.0f}% of total).")

    flagged_grants = flag_grants(data, data[flags], ratio)
    print(f"Flagged {len(flagged_grants)} grants (out of {len(data[GRANT_ID].unique())} total).\n")

    flagged_txns = data.copy()
    flagged_txns['is_flagged'] = flags
    flagged_txns = flagged_txns[flagged_txns['grant_id'].isin(flagged_grants)]

    if outpath:
        summarize_flags(data, ADDRESS_ID, flagged_addresses, outpath=outpath+"_addresses.csv")
        summarize_flags(data, HANDLE_ID, flagged_handles, outpath=outpath+"_handles.csv")
        summarize_flags(data, GRANT_ID, flagged_grants, outpath=outpath+"_grants.csv")
    else:
        return dict(
            dataframe=data,
            flagged_dataframe=flagged_txns,
            flagged_addresses=flagged_addresses,
            flagged_handles=flagged_handles,
            flagged_grants=flagged_grants,            
        )



def process_contributions(pathname, export_to_csv=True):
    """
    Primary execution module for processing a batch of contributions
    args:
        pathname (csv file in correct format -- see column headers above)
        export_to_csv (boolean)
            
    returns:
        (optional) dataframe of flagged transactions

    """

    data = load_transactions(pathname)
    data = data[~data['grant_id'].isin(GRANTS_TO_IGNORE)]
    data = data[~data['handle'].isin(USERS_TO_IGNORE)]
    print(f"\nSuccessfully imported {len(data)} transactions.")

    if export_to_csv:
        outpath = pathname.replace(".csv","")
        flag_transactions(data, outpath=outpath)
    else:
        return flag_transactions(data)

    

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        pathname = sys.argv[1]
        process_contributions(pathname)

    else:
        print("Please enter an argument containing a path to a .csv file.")