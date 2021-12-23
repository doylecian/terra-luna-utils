# TODO: Fetch price data from API instead of hardcoding
luna_current_price = 91.83
luna_market_cap = 33921802986
luna_circulating_supply = 369382931
luna_max_supply = 841881771
ust_market_cap = 9396787691

def comma(number):
    return ("{:,}".format(number))

def getCurrentSupply(mCap: int, curPrice: float)->int:
    return(mCap / curPrice)

def getMarketCap(circSupply: int, curPrice: float)->int:
    return (circSupply * curPrice)

def mintUST(amount: int):
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
    str_luna_price_impact = "{:.4f}".format(luna_price_impact)
    str_luna_burned = "{:.4f}".format(luna_burned)
    str_luna_old_price = "{:.4f}".format(luna_old_price)
    str_luna_current_price = "{:.4f}".format(luna_current_price)
    print(str(amount) + " UST minted (-" + str_luna_burned + " Luna) (+$" + str_luna_price_impact + ") $" + str_luna_old_price + " -> $" + str_luna_current_price)

def simulateUSTMarketCap(target: int, mintBatchSize=5000000): 
    """Returns the projected price and circulating supply of Luna, given a UST market cap"""
    global ust_market_cap 

    ust_needed = target - ust_market_cap
    while(ust_market_cap < target):
        if(ust_needed < mintBatchSize):
            mintUST(ust_needed)
        else:
            mintUST(mintBatchSize)
            ust_needed -= mintBatchSize

# Simulate luna price at 10 Billion UST market cap
simulateUSTMarketCap(100000000000)
str_ust_market_cap = comma(ust_market_cap)
str_luna_circulating_supply = "{:.2f}".format(luna_circulating_supply)
str_luna_current_price = "{:.2f}".format(luna_current_price)
print("\nUST Market cap: $" + str_ust_market_cap + "\nCirculating supply: " 
        + str_luna_circulating_supply + "\nLuna price: $" + str_luna_current_price + "\n")
