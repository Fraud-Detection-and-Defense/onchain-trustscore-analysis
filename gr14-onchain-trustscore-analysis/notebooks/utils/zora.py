from utils.gqltools import subgraph_query, execute_subgraph_query
import json


POPULAR_NFTS = {
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
    #'0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03': 'Nouns',
    '0xff9c1b15b16263c61d017ee9f65c50e4ae0113d7': 'Loot',
    '0xbf92a355c73de74969a75258e02a15a2764d4970': 'Octagon (8GON)',
    '0x6fa9f4b50e2950a8137a76649193816fb29dad2c': 'HAPEBADGE (HAPEBADGE)',
    '0xbe223020724cc3e2999f5dceda3120484fdbfef7': 'GURU Season Pass NFT (SeasonPass)',
    '0xabc207502ea88d9bca29b95cd2eee5f0d7936418': 'Yield Guild Badge (YGG BADGE)',
    '0xb75ecf7cd68ee8b0cf481d7e3c03a0b1c52aee3a': 'Bit islands Genesis Passport NFT',
    '0xd93206bd0062cc054e397ecccdb8436c3fa5700e': 'Decagon (10GON)',
    '0x22c1f6050e56d2876009903609a2cc3fef83b415': 'POAP (The Proof of Attendance Protocol)',
    '0x18f758c749c67aeac1faf14e9df9c68026606a23': 'ShowMe (ShowMe)'
}
_collections_list = ", ".join(f'"{c}"' for c in POPULAR_NFTS.keys())


def query_popular_nfts(lst):
    json_data = subgraph_query(
        list_of_wallets=lst,
        api_url='https://api.zora.co/graphql',
        query_docstring="""
            query NFTs {
              tokens(
                networks: [{network: ETHEREUM, chain: MAINNET}], 
                pagination: {limit: 500}, 
                where: {
                    ownerAddresses: [$WALLETS]
                    collectionAddresses: [$COLLECTIONS]
                }
              ) {
                nodes {
                  token {
                    collectionAddress
                    tokenId
                    name
                    owner
                  }
                }
              }
            }
            """.replace("$COLLECTIONS", _collections_list)
    )
    result = json_data['data']['tokens']['nodes']
    return result


def query_nfts(lst):
    json_data = subgraph_query(
        api_url='https://api.zora.co/graphql',
        query_docstring="""
            query NFTs {
              tokens(
                networks: [{network: ETHEREUM, chain: MAINNET}], 
                pagination: {limit: 500}, 
                where: {ownerAddresses: [$WALLETS]}
              ) {
                nodes {
                  token {
                    collectionAddress
                    tokenId
                    name
                    owner
                  }
                }
              }
            }
            """,
        list_of_wallets=lst
    )
    result = json_data['data']['tokens']['nodes']
    return result


def query_zora(list_of_wallets, nfts_path, num_per_call=20, return_json=False):

    j = execute_subgraph_query(
        api_function=query_popular_nfts, 
        list_of_wallets=list_of_wallets, 
        num_wallets_per_call=num_per_call,
        json_filepath=nfts_path,
        append_to_existing_file=False,
        return_json=True
    )

    located_wallets = [w['token']['owner'] for w in j['data']]
    retry_wallets = set(list_of_wallets) - set(located_wallets)

    j["wallets"] = located_wallets
    with open(nfts_path, 'w') as outfile:
        json.dump(j, outfile, indent=2)

    j = execute_subgraph_query(
        api_function=query_nfts, 
        list_of_wallets=retry_wallets, 
        num_wallets_per_call=num_per_call,
        json_filepath=nfts_path,
        append_to_existing_file=True,
        return_json=return_json
    )    

    if return_json:
        return j
    return None