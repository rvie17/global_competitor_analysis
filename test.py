import asyncio

from pyinjective.async_client import AsyncClient
from pyinjective.client.model.pagination import PaginationOption
from pyinjective.core.network import Network


async def main() -> None:
    # select network: local, testnet, mainnet
    network = Network.mainnet()
    client = AsyncClient(network)
    market_ids = ["0x4ca0f92fc28be0c9761326016b5a1a2177dd6375558365116b5bdda9abc229ce"] #BTCUSDT MarketId to get a slow response 
    #market_ids = ["0x3569a541bfae59b8a92215e3cb31133bff21455f1a18a1303df87fecab2839e4"] #PLUME MarketId to get a "fast" response

    subaccount_id = "0x935b705b5943b0e1b859651d2ccf375bc96dfdd7000000000000000000000002"
    
    is_conditional = "false"
    skip = 0
    limit = 20
    pagination = PaginationOption(skip=skip, limit=limit)
    orders = await client.fetch_derivative_orders_history(
        subaccount_id=subaccount_id,
        market_ids=market_ids,
        is_conditional=is_conditional,
        pagination=pagination,
    )
    print(orders)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())