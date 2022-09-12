from utils.gqltools import subgraph_query


def query_lens(list_of_wallets):
    
    json_data = subgraph_query(
        api_url='https://api.lens.dev/',
        query_docstring="""
            query Profiles {
              profiles(
                request: { 
                    ownedBy: [$WALLETS], 
                    limit: 50 
                }
              ) {
                items {
                  id
                  name
                  ownedBy
                  stats {
                    totalFollowers
                    totalFollowing
                  }
                }
              }
            }
        """,
        list_of_wallets=list_of_wallets
    )
    result = json_data['data']['profiles']['items']
    return result


def query_poaps_xdai(list_of_wallets):
    
    json_data = subgraph_query(
        api_url='https://api.thegraph.com/subgraphs/name/poap-xyz/poap-xdai',
        query_docstring="""
            query poap {
              accounts(
                where: {
                  id_in: [$WALLETS]
                }
              ) {
                id
                tokensOwned
                tokens (first: 1000) {
                  event {
                    id
                  }
                }
              }
            }
        """,
        list_of_wallets=list_of_wallets
    )
    result = json_data['data']['accounts']
    return result


def query_snapshot(list_of_wallets):

    json_data = subgraph_query(
        api_url='https://hub.snapshot.org/graphql/',
        query_docstring="""
            query Votes {
              votes (
                first: 10000
                skip: 0
                where: {
                  voter_in: [$WALLETS]
                }
              ) {
                id
                voter
                created
                proposal {
                  id
                }
                choice
                space {
                  id
                }
              }
            }
            """,
        list_of_wallets=list_of_wallets
    )
    
    result = json_data['data']['votes']
    return result