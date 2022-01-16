from brownie import Contract, accounts, interface
from brownie_tokens import MintableForkToken

def main():
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    usdc_address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    registry_address = "0x7002B727Ef8F5571Cb5F9D70D13DBEEb4dFAe9d1"
    amount = 100_000 * 10 ** 18
    dai = MintableForkToken(dai_address)
    dai._mint_for_testing(accounts[0], amount)

    registry = Contract(registry_address)
    pool_address = registry.find_pool_for_coins(
        dai_address,
        usdc_address)
    pool = Contract(pool_address)

    dai.approve(pool_address, amount, {'from': accounts[0]})
    pool.add_liquidity(
        [amount,0,0], 0, 
        {'from': accounts[0]}
    )

    gauges = registry.get_gauges(pool_address)
    gauge_address = gauges[0][0]
    gauge_contract = interface.LiquidityGauge(gauge_address)
    
    lp_token = MintableForkToken(gauge_contract.lp_token())
    lp_token.approve(gauge_address, amount, {'from': accounts[0]})
    gauge_contract.deposit(
        lp_token.balanceOf(accounts[0]),
        {'from': accounts[0]}
    )


