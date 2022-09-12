# Open GraphQL APIs for Querying DeSoc Data

## Sites

- POAPs (xDAI only) via [The Graph API](https://api.thegraph.com/subgraphs/name/poap-xyz/poap-xdai)
- Snapshot votes (all EVM chains) via [Snapshot API](https://hub.snapshot.org/graphql/)
- NFT ownership (ETH Mainnet only) via [Zora API](https://api.zora.co/graphql)
- Lens profiles via [Lens API](https://api.lens.dev/)
- Proof of Humanity via [PoH API](https://api.poh.dev)

## Some sample queries to get you started

In each of the cases below, substitute the `$WALLETS` field with a list of wallet addresses (0x...)

#### Lens Protocol

```
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
```

####  POAP

```
query POAPs {
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
```

#### Snapshot

```
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
```

## Automating queries

Once you've configured your queries, here are some simple Python scripts for automating requests. 
Note: these scripts are fine for ad hoc analysis, not for building applications.

You'll need to provide values for `my_api_url`, `my_graphql_docstring` and `my_list_of_wallets`.

#### Method 1: Using `requests`

```
str_list = ", ".join(f'"{w}"' for w in my_list_of_wallets)
query = my_graphql_docstring.replace("$WALLETS", str_list)
r = requests.post(my_api_url, json={"query": query})
json_data = json.loads(r.text)
```

#### Method 2: Using `gql`

This approach is better for more complex tasking and uses a Python GraphQL client (gql3).

Get the gql package [here](https://gql.readthedocs.io/en/stable/).


```
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
sample_transport=RequestsHTTPTransport(
    url=my_api_url,
    verify=True,
    retries=3,
)
client = Client(
    transport=sample_transport
)
str_list = ", ".join(f'"{w}"' for w in my_list_of_wallets)
query = my_graphql_docstring.replace("$WALLETS", str_list)
q = gql(my_graphql_docstring)
r = client.execute(q)
json_data = json.loads(r.text)
```