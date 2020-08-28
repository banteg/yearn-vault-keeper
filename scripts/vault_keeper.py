import os
import json
import warnings
from tabulate import tabulate
from brownie import interface, accounts, rpc, VaultKeeper

warnings.simplefilter('ignore')

# vault addresses from https://github.com/iearn-finance/iearn-finance/blob/master/src/stores/store.jsx
vault_data = json.loads('[{"id":"YFI","name":"yearn.finance","symbol":"YFI","description":"yearn.finance","vaultSymbol":"yYFI","erc20address":"0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e","vaultContractAddress":"0xBA2E7Fed597fd0E3e70f5130BcDbbFE06bB94fe1","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"lastMeasurement":10695309,"measurement":1000000000000000000},{"id":"CRV","name":"curve.fi/y LP","symbol":"yCRV","description":"yDAI/yUSDC/yUSDT/yTUSD","vaultSymbol":"yUSD","erc20address":"0xdf5e0e81dff6faf3a7e52ba697820c5e32d806a8","vaultContractAddress":"0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":false,"withdraw":true,"withdrawAll":false,"lastMeasurement":10559448,"measurement":1000000000000000000},{"id":"crvBUSD","name":"curve.fi/busd LP","symbol":"crvBUSD","description":"yDAI/yUSDC/yUSDT/yBUSD","vaultSymbol":"ycrvBUSD","erc20address":"0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B","vaultContractAddress":"0x2994529c0652d127b7842094103715ec5299bbed","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"depositDisabled":false,"lastMeasurement":10709740,"measurement":1000000000000000000},{"id":"crvBTC","name":"curve.fi/sbtc LP","symbol":"crvBTC","description":"renBTC/wBTC/sBTC","vaultSymbol":"ycrvBTC","erc20address":"0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3","vaultContractAddress":"0x7Ff566E1d69DEfF32a7b244aE7276b9f90e9D0f6","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"lastMeasurement":10734341,"measurement":1000000000000000000},{"id":"DAI","name":"DAI","symbol":"DAI","description":"DAI Stablecoin","vaultSymbol":"yDAI","erc20address":"0x6b175474e89094c44da98b954eedeac495271d0f","vaultContractAddress":"0xACd43E627e64355f1861cEC6d3a6688B31a6F952","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"lastMeasurement":10650116,"measurement":1000000000000000000},{"id":"TUSD","name":"TUSD","symbol":"TUSD","description":"TrueUSD","vaultSymbol":"yTUSD","erc20address":"0x0000000000085d4780B73119b644AE5ecd22b376","vaultContractAddress":"0x37d19d1c4E1fa9DC47bD1eA12f742a0887eDa74a","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"lastMeasurement":10603368,"measurement":1000000000000000000},{"id":"USDC","name":"USD Coin","symbol":"USDC","description":"USD//C","vaultSymbol":"yUSDC","erc20address":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48","vaultContractAddress":"0x597aD1e0c13Bfe8025993D9e79C69E1c0233522e","balance":0,"vaultBalance":0,"decimals":6,"deposit":true,"depositAll":false,"withdraw":true,"withdrawAll":false,"lastMeasurement":10532708,"measurement":1000000000000000000},{"id":"USDT","name":"USDT","symbol":"USDT","description":"Tether USD","vaultSymbol":"yUSDT","erc20address":"0xdAC17F958D2ee523a2206206994597C13D831ec7","vaultContractAddress":"0x2f08119C6f07c006695E079AAFc638b8789FAf18","balance":0,"vaultBalance":0,"decimals":6,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"lastMeasurement":10651402,"measurement":1000000000000000000},{"id":"aLINK","name":"aLINK","symbol":"aLINK","description":"Aave Interest bearing LINK","vaultSymbol":"yaLINK","erc20address":"0xA64BD6C70Cb9051F6A9ba1F163Fdc07E0DfB5F84","vaultContractAddress":"0x29E240CFD7946BA20895a7a02eDb25C210f9f324","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"lastMeasurement":10599617,"measurement":1000000000000000000},{"id":"LINK","name":"ChainLink","symbol":"LINK","description":"ChainLink","vaultSymbol":"yLINK","erc20address":"0x514910771af9ca656af840dff83e8264ecf986ca","vaultContractAddress":"0x881b06da56BB5675c54E4Ed311c21E54C5025298","balance":0,"vaultBalance":0,"decimals":18,"deposit":true,"depositAll":true,"withdraw":true,"withdrawAll":true,"depositDisabled":true,"lastMeasurement":10604016,"measurement":1000000000000000000}]')
skipped = ['aLINK', 'yearn.finance']
keeper = VaultKeeper.at('0x8f3228A67Fde7BD306716904E1d086462f8711f8')

def main():
    if rpc.is_active():
        sender = accounts[0]
    else:
        priv = os.environ.get('VAULT_KEEPER_PRIV')
        sender = accounts.add(priv) if priv else accounts.load(input('brownie account: '))

    table = []
    vaults = []
    for data in vault_data:
        if data['name'] in skipped:
            print('aLINK not supported yet')
            continue
        token = interface.ERC20(data['erc20address'])
        vault = interface.YearnVault(data['vaultContractAddress'])
        decimals = token.decimals()
        available = vault.available()
        balance = vault.balance()
        ratio = 1 - vault.min() / vault.max()
        can_earn = available / balance > ratio if balance > 0 else False
        if can_earn:
            vaults.append(data['vaultContractAddress'])
        table.append([data['name'], available / 10**decimals, balance / 10**decimals, can_earn])
    
    print(tabulate(table, headers=['name', 'available', 'balance', 'can_earn']))

    if vaults:
        print('poking these vaults:', vaults)
        keeper.earn(vaults, {'from': sender, 'gas_limit': 2_500_000})
    else:
        print('no vaults to poke, exiting')
