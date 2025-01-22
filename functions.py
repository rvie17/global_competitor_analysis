import asyncio
import pandas as pd
from pyinjective.async_client import AsyncClient
from pyinjective.client.model.pagination import PaginationOption
from pyinjective.core.network import Network
from datetime import datetime, timedelta

# Initialize the network and client
network = Network.local()
client = AsyncClient(network)

from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network


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
    


