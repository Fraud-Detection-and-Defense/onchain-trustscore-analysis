# Gitcoin Grants Round 14
# Onchain Trustscore Analysis

A collection of query, analysis, and visualization modules to support Sybil detection and public goods funding.

Discussion and presentation of the results are available [here](https://carlcervone.com/public/images/Towards_a_Pluralism_Passport_Built_from_DeSoc_Legos.pdf).

## Getting started
1. Clone the repo and ensure you have the requirements installed.
2. You will need access to two private `.csv` files from Gitcoin's metabase. The first file contains all transactions from GR14, including both wallet addresses and grant contributions as well as trust bonus scores (from Gitcoin Passport) and squelching (from the Sybil defense team). The second file is not critical, but has useful metadata about grants. Contact someone at FDD for a copy of these datasets.
3. Modify the pathnames in `settings.py`. The ones I've used are:

```
# PRIVATE USER DATA FROM GITCOIN
_rawfile   = 'contribs_with_trust_is_squelched.csv' 
_results   = 'GR14 Final Results - 6 29 2022 - Total Round Amount.csv'
```


4. Review the GraphQL query instructions in the `utils` directory. The Zora API requires some creative batching to avoid rate limits. I've handled this by pulling the most popular NFT collections first, and then searching for others. These include:

```
'0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85': 'ENS',
'0x932261f9fc8da46c4a22e31b45c4de60623848bf': 'Zerion',
'0xc36442b4a4522e871399cd717abdd847ab11fe88': 'Uniswap V3: Positions NFT (UNI-V3-POS)',
'0xd945f759d422ae30a6166838317b937de08380e3': 'Zora API Genesis Hackathon (ZRPG)',
'0xca21d4228cdcc68d4e23807e5e370c07577dd152': 'Zorbs',
'0xabefbc9fd2f806065b4f3c237d4b59d9a97bcac7': 'Zora (ZORA)',    
'0xa97d3eb991303cf3b9b759bd026bacb55256e9db': 'State of Mind (ZSD)',    
'0xc9a42690912f6bd134dbc4e2493158b3d72cad21': 'RabbitHole Credentials: DAOs (RHC-DAO)',
'0xa3b61c077da9da080d22a4ce24f9fd5f139634ca': 'RabbitHole Credentials: NFTs (RHC-NFT)',
'0x2face815247a997eaa29881c16f75fd83f4df65b': 'RabbitHole Credentials: DeFi (RHC-DEFI)',
'0x90b3832e2f2ade2fe382a911805b6933c056d6ed': 'Pooly - Supporter (POOLY1)',
'0x92b971d307ebfc7331c23429e204a5e4adf7a833': 'Club Pooly (CLUBPOOLY)',
```

5. Finally, run the Part 1 Notebook to query on-chain data for all GR14 wallet addresses. (This can take a couple hours due to rate limits on most of the APIs. Contact someone at FDD for an archived dataset.)

## Processing
Part 2 includes some a variety of processing steps to derive DeSoc metrics from the onchain data. These include things like number of Lens followers, which NFTs/POAPs people hold, and how active they are on Snapshot (and which DAOs they vote in). 

There is a wealth of data here and we only scratch the surface of what's possible!

## Analysis and Visualization
Part 3 includes several notebooks for analysis and visualization. Here are some screenshots.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/42869436/187330821-403c2c2d-feee-493b-94ed-95825ded19f3.png">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/42869436/187330878-4eabebb4-7955-49c1-99b9-0b18080cc2da.png">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/42869436/187330922-458d17de-15c7-4c35-b03d-321e8eb375d8.png">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/42869436/187330972-f12974d3-58bd-4008-92da-761a0611cd8d.png">

## Troubleshooting

Feel free to send me a DM on Twitter if you have questions.
