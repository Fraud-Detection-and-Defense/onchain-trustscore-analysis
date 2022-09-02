import pandas as pd


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

    data['wallet'] = data.apply(
        lambda x: 
        set_address(x['address'], x['contributor_address']),
        axis=1)

    data = (data
            .iloc[:,1:]
            .query("success == True")
            .drop(columns=['address', 'contributor_address', 'success'])
            .rename(columns={'wallet': 'address'})
            .sort_index())

    data = data[data['address'].isna() == False]

    return data
