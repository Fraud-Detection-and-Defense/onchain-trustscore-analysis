import os

# for charts and graphics
BGCOLOR = "#FAFAFA"

_graphdir  = 'graphs/'
_graphs    = ['poaps', 'snapshot', 'lens', 'poh', 'nfts', 'verses']
_outfile   = 'gr14'

# PRIVATE USER DATA FROM GITCOIN
_parentdir = '../private_data/'
_rawfile   = 'contribs_with_trust_is_squelched.csv' 
_results   = 'GR14 Final Results - 6 29 2022 - Total Round Amount.csv' 


PATHS = {
    'rawdata': os.path.join(_parentdir, _rawfile),
    'cleancsv': os.path.join(_parentdir, f"{_outfile}.csv"),
    'outdata': os.path.join(_parentdir, f"{_outfile}.pickle"),
    'results': os.path.join(_parentdir, _results),
    'graphs': {
        g: os.path.join(_parentdir, _graphdir, f'{g}.json') 
        for g in _graphs
    }
}