from collections import Counter
from utils.zora import POPULAR_NFTS


# sets used for NFT classifiers
rabbithole_nfts = set([v for v in POPULAR_NFTS.values() if 'RabbitHole' in v])
zora_nfts = set([v for v in POPULAR_NFTS.values() if 'Zor' in v])
pooly_nfts = set([v for v in POPULAR_NFTS.values() if 'Pooly' in v])

# sets used for POAP classifiers
poap_farmer_set = {8902, 9436, 9675, 8716, 6948, 7604, 6365, 6681, 8222, 8053}
bankless_poaps = {25571, 885, 204}
clr_poaps = {873, 2844, 2845, 2846, 16516}
poapart_poaps = {1868, 1912, 2117, 2270, 2424, 2582, 2758, 2987, 3242, 3490, 3808, 
                 4052, 4303, 4608, 4975, 5381, 5756, 6153, 6602, 7011, 7496, 8084, 
                 8716, 9436, 10241, 10941, 11645, 12404, 13052, 13915, 14818, 15863, 
                 16868, 17998, 19068, 20328, 20835, 23254, 24248, 25381, 26565, 27974, 32427}


# helper class
class Classifier:

    def __init__(self, name, label, func):
        self.name = name
        self.label = label
        self.func = func
        
    def __repr__(self):
        return self.label

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Classifier):
            return self.name == other.name
        else:
            return False


CLASSIFIERS = [
    Classifier(name, label, func)
    for name, (label,func) in {
        
        'burner': (
            '"burners" (no on-chain credentials)',
            lambda x: (x['numSpaces'] == 0 and
                       x['numPOAPs'] == 0 and
                       x['numCollections'] == 0 and
                       x['numLens'] == 0 and
                       x['hasProofOfHumanity'] == False)
        ),
        'ens_nft': (
            'NFTs: ENS domain',
            lambda x: (x['countNFTs']['ENS'] > 0 
                        if isinstance(x['countNFTs'], Counter) 
                        else False)
        ),
        'rabbithole_nfts': (
            'NFTs: Rabbithole',
            lambda x: (rabbithole_nfts.issubset(x['setCollections'])
                       if isinstance(x['setCollections'], set)
                       else False)
        ),
        'pooly_nft': (
            'NFTs: Club Pooly',
            lambda x: (len(pooly_nfts.intersection(x['setCollections'])) >= 1
                       if isinstance(x['setCollections'], set)
                       else False)
        ),
        'uniswap_nft': (
            'NFTs: Uniswap v3 ',
            lambda x: ('Uniswap V3: Positions NFT (UNI-V3-POS)' in x['setCollections']
                        if isinstance(x['setCollections'], set)
                        else False)
        ),
        'bankless_poaps': (
            'POAPs: Bankless badge',
            lambda x: (len(bankless_poaps.intersection(x['setPOAPs'])) >= 1
                       if isinstance(x['setPOAPs'], set)
                       else False)
        ),
        'clr_poaps': (
            'POAPs: clr.fund contributor',
            lambda x: (len(clr_poaps.intersection(x['setPOAPs'])) >= 1
                       if isinstance(x['setPOAPs'], set)
                       else False)
        ),
        'arbitrum_launch_poap': (
            'POAPs: Arbitrum launch',
            lambda x: (6642 in x['setPOAPs']
                       if isinstance(x['setPOAPs'], set)
                       else False)
        ),
        'poap_art_poaps': (
            'POAPs: POAP.art Weekly Sandbox',
            lambda x: (len(poapart_poaps.intersection(x['setPOAPs'])) >= 3
                       if isinstance(x['setPOAPs'], set)
                       else False)
        ),
        'dao_voter': (
            'Voting: active in 2+ DAOs',
            lambda x: (x['numSpaces'] >= 2 and x['numVotes'] >= 20)
        ),
        'ens_voter': (
            'Voting: ENS',
            lambda x: ('ens.eth' in x['setSpaces']
                       if isinstance(x['setSpaces'], set)
                       else False)
        ),
        'gitcoin_voter': (
            'Voting: Gitcoin DAO',
            lambda x: ('gitcoindao.eth' in x['setSpaces']
                       if isinstance(x['setSpaces'], set)
                       else False)
        ),
        'optimism_voter': (
            'Voting: Optimism Collective',
            lambda x: ('opcollective.eth' in x['setSpaces']
                       if isinstance(x['setSpaces'], set)
                       else False)
        ),
        'arbitrum_voter': (
            'Voting: Arbitrum Odyssey',
            lambda x: ('arbitrum-odyssey.eth' in x['setSpaces']
                       if isinstance(x['setSpaces'], set)
                       else False)
        ),                
        'lens_active': (
            'Lens: has profile', 
            lambda x: (x['numLens'] > 0)
        ),
        'lens_followers': (
            'Lens: 5+ followers ', 
            lambda x: (x['numLensFollowers'] >= 5)
        ),        
        'proof_of_humanity': (
            'PoH: has profile', 
            lambda x: (x['hasProofOfHumanity'])
        )

    }.items()
]
