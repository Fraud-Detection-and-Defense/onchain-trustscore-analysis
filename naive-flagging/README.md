# Naive Flagging (🤖,💚)

A simple, naive flagging algorithm for identifying Sybil-like user behaviors and suspicious grants.

## Getting started
1. Clone the repo and ensure you have the requirements installed.
2. You will need access to a private `.csv` file from Gitcoin's metabase. The file contains all transactions from the latest grants round, including wallet addresses, user handles, and grant contributions, as well as trust bonus scores (from Gitcoin Passport) and squelching (from the Sybil defense team). 

## Run the script in command line
```
python naive_flagging.py pathname_of_your_datafile.csv
```

## Perform exploratory data analysis in the Jupyter Notebook

A Jupyter notebook recreates the script above and includes further analysis and visualizations.
