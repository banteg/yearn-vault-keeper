from brownie import VaultKeeper, accounts

def main():
    deployer = accounts.load(input('brownie account: '))
    return VaultKeeper.deploy({'from': deployer})
