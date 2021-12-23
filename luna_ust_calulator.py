import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
  
cfg = open('config.json')
config = json.load(cfg)
api_key = config['API_KEY']

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

def fetchMetaData(): 
    """Fetches luna price, circulating supply and market cap, and UST market cap"""
    print("\nFetching Luna and UST metadata...\n")
    session = Session()
    session.headers.update(headers)

    # Get luna information
    try:
        r = session.get(url, params={'symbol':'LUNA', 'convert':'USD'})
        luna_data = json.loads(r.text)
        if(luna_data['status']['error_code'] != 0):
            print("Error fetching luna metadata -> " + luna_data['status']['error_message'])
    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

    # Get UST information
    try:
        r = session.get(url, params={'symbol':'UST', 'convert':'USD'})
        ust_data = json.loads(r.text)
        if(ust_data['status']['error_code'] != 0):
            print("Error fetching UST metadata -> " + ust_data['status']['error_message'])
        else: 
            print("Metadata fetched successfully!\n")
            return [luna_data['data']['LUNA'], ust_data['data']['UST']]
    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def mintUST(amount: int, log=False):
    """Mints the given amount of UST and changes luna price and circulating supply to reflect the impact of minting said UST"""
    global ust_market_cap
    global luna_circulating_supply
    global luna_current_price

    # Increase UST market cap
    ust_market_cap += amount
    # Calculate luna burned in minting process
    luna_burned = (amount / luna_current_price)  
    # Reduce circulating supply
    luna_circulating_supply -= luna_burned 
    # Cache pre mint price
    luna_old_price = luna_current_price
    # Update price according to new circulating supply
    luna_current_price = (luna_market_cap / luna_circulating_supply) 
    # Calculate luna price impact of mint 
    luna_price_impact = (luna_current_price - luna_old_price)
    # Print results of mint
    if (log):
        str_amount = "{:.2f}".format(amount)
        str_luna_price_impact = "{:.4f}".format(luna_price_impact)
        str_luna_burned = "{:.4f}".format(luna_burned)
        str_luna_old_price = "{:.4f}".format(luna_old_price)
        str_luna_current_price = "{:.2f}".format(luna_current_price)
        print(str_amount + " UST minted (-" + str_luna_burned + " Luna) (+$" + str_luna_price_impact + ") $" + str_luna_old_price + " -> $" + str_luna_current_price)

def simulateUSTMarketCap(target: int, mintBatchSize=5000000, log=False): 
    """Calculates the projected price and circulating supply of Luna, given a UST market cap"""
    global ust_market_cap 

    ust_needed = target - ust_market_cap
    while(ust_market_cap < target):
        if(ust_needed < mintBatchSize):
            mintUST(ust_needed, log=log)
        else:
            mintUST(mintBatchSize, log=log)
            ust_needed -= mintBatchSize

def printSimulationResults():
    """Prints the results of the UST market cap simulation"""
    str_ust_market_cap = comma(ust_market_cap)
    str_luna_circulating_supply = "{:.2f}".format(luna_circulating_supply)
    str_luna_current_price = "{:.2f}".format(luna_current_price)
    print("Results of UST mint:\n---------------------\nUST Market cap: $" + str_ust_market_cap + 
        "\nCirculating supply: " + str_luna_circulating_supply + "\nLuna price: $" + str_luna_current_price + "\n")

def comma(number: int):
    return ("{:,}".format(number))

# Simulate luna price at 10 Billion UST market cap
[luna_metadata, ust_metadata] = fetchMetaData()

luna_current_price = luna_metadata['quote']['USD']['price'] 
luna_market_cap = luna_metadata['quote']['USD']['market_cap']
luna_circulating_supply = luna_metadata['circulating_supply']
ust_market_cap = ust_metadata['quote']['USD']['market_cap']

simulateUSTMarketCap(100000000000)
printSimulationResults()

