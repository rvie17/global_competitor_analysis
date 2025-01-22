import asyncio
import pandas as pd
from pyinjective.async_client import AsyncClient
from pyinjective.client.model.pagination import PaginationOption
from pyinjective.core.network import Network
from datetime import datetime, timedelta
# Initialize the network and client
network = Network.local()
client = AsyncClient(network)

async def fetch_derivative_orders(subaccount_id, market_ids, start_date, end_date, csv_name, client):
    # Convert start and end dates to milliseconds since epoch
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

    orders_list = []
    skip = 0
    limit = 100  # Set the number of results to fetch per request

    while True:
        pagination = PaginationOption(skip=skip, limit=limit)

        # Fetch the orders history
        orders_response = await client.fetch_derivative_orders_history(
            subaccount_id=subaccount_id,
            #market_ids=market_ids,
            is_conditional="false",
            pagination=pagination,
        )

        # orders_response = await client.fetch_spot_orders_history(
        #     subaccount_id=subaccount_id,
        #     #market_ids=market_ids,
        #     # is_conditional="false",
        #     pagination=pagination,
        # )
        
        
        # Break the loop if no orders were returned
        if not orders_response['orders']:
            break

        # Iterate through each order
        for order in orders_response['orders']:
            created_at = pd.to_datetime(order['createdAt'], unit='ms')
            updated_at = pd.to_datetime(order['updatedAt'], unit='ms')
            
            
            # Stop if we've gone past the start date

            start_timestamp = pd.to_datetime(start_timestamp, unit='ms')

            print (created_at)
            print (start_timestamp)


            if created_at < start_timestamp:
                # Save orders to CSV and return
                df_orders = pd.DataFrame(orders_list)
                df_orders.to_csv(csv_name, index=False)
                return df_orders
            
            # Generate the time range between createdAt and updatedAt
            
            # For each second in the time range, add a new row to the data
    
            orders_list.append({
                'orderHash': order['orderHash'],
                'marketId': order['marketId'],
                'subaccountId': order['subaccountId'],
                'executionType': order['executionType'],
                'orderType': order['orderType'],
                'price': order['price'],
                'quantity': order['quantity'],
                'updated_at': updated_at,
                'state': order['state'],
                'created_at': created_at,
            })

        # Increment skip for pagination
        skip += limit

    # Save remaining orders to CSV
    df_orders = pd.DataFrame(orders_list)

    return df_orders

async def fetch_spot_orders(subaccount_id, market_ids, start_date, end_date, csv_name, client):
    # Convert start and end dates to milliseconds since epoch
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

    orders_list = []
    skip = 0
    limit = 100  # Set the number of results to fetch per request

    while True:
        pagination = PaginationOption(skip=skip, limit=limit)

        # Fetch the orders histor

        orders_response = await client.fetch_spot_orders_history(
            subaccount_id=subaccount_id,
            #market_ids=market_ids,
            # is_conditional="false",
            pagination=pagination,
        )
        
        
        # Break the loop if no orders were returned
        if not orders_response['orders']:
            break

        # Iterate through each order
        for order in orders_response['orders']:
            created_at = pd.to_datetime(order['createdAt'], unit='ms')
            updated_at = pd.to_datetime(order['updatedAt'], unit='ms')
            
            
            # Stop if we've gone past the start date

            start_timestamp = pd.to_datetime(start_timestamp, unit='ms')

            print (created_at)
            print (start_timestamp)


            if created_at < start_timestamp:
                # Save orders to CSV and return
                df_orders = pd.DataFrame(orders_list)
                df_orders.to_csv(csv_name, index=False)
                return df_orders
            
            # Generate the time range between createdAt and updatedAt
            
            # For each second in the time range, add a new row to the data
    
            orders_list.append({
                'orderHash': order['orderHash'],
                'marketId': order['marketId'],
                'subaccountId': order['subaccountId'],
                'executionType': order['executionType'],
                'orderType': order['orderType'],
                'price': order['price'],
                'quantity': order['quantity'],
                'updated_at': updated_at,
                'state': order['state'],
                'created_at': created_at,
            })

        # Increment skip for pagination
        skip += limit

    # Save remaining orders to CSV
    df_orders = pd.DataFrame(orders_list)

    return df_orders

async def market_ticker() -> None:
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
    df_market = pd.concat([df_spot, df_fut], ignore_index=True)

    return df_market
