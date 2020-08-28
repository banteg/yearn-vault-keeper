# Yearn Vault Keeper

## Abstract

Yearn vaults maintain a certain buffer to not deployed into a strategy to allow for cheaper deposits/withdrawals.

This keeper bot ensures the buffer is kept as tight as possible by calling `earn()` on vaults when `available / balance > ratio`.

It consists of a contract that can batch call `earn()` on all vaults and a script that determines which vaults need poking. 

## Usage

Import a keystore to Brownie:
```
brownie accounts import keeper keystore.json
```

One-off script can be launched like this:

```
brownie run vault_keeper --network mainnet
```

It will prompt you to unlock the account and do its magic. If you want to run it headless, it can also load an account from `VAULT_KEEPER_PRIV` environment variable.
