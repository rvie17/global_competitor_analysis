import asyncio
import pandas as pd
from pyinjective.async_client import AsyncClient
from pyinjective.client.model.pagination import PaginationOption
from pyinjective.core.network import Network
from datetime import datetime, timedelta
from pyinjective.wallet import Address

# Initialize the network and client
network = Network.local()
client = AsyncClient(network)

from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
import pandas as pd
import re

async def marketId_to_ticker(ticker) -> None:
    # select network: local, testnet, mainnet

    network = Network.local()
    client = AsyncClient(network)
    market_statuses = ["active"]
    market_fut = await client.fetch_derivative_markets(market_statuses=market_statuses )
    market_spot = await client.fetch_spot_markets(market_statuses=market_statuses )
    df_fut = pd.DataFrame(market_fut['markets'])
    df_fut = df_fut[["marketId","ticker"]]
    df_spot = pd.DataFrame(market_spot['markets'])
    df_spot = df_spot[["marketId","ticker"]]
    df_combined = pd.concat([df_fut, df_spot], ignore_index=True)
    market_Id = df_combined[df_combined["ticker"]==ticker]["marketId"].values
    
    return market_Id
    

def extract_eth_address(subaccount_id):
    
    match = re.search(r'0x[a-fA-F0-9]{40}', subaccount_id)
    
    if match:
        return match.group()
    else:
        return None


async def map_eth_to_inj(eth_address):

    eth_address_bytes = bytes.fromhex(eth_address[2:])
    
    address = Address(eth_address_bytes)

    injective_address = address.to_acc_bech32()
    
    return injective_address

async def mapper(eth_addresses_array,eth_to_inj_dict):
    for eth_address in eth_addresses_array:
        if eth_address is not None:
            inj_address = await map_eth_to_inj(eth_address)
            eth_to_inj_dict[eth_address] = inj_address


