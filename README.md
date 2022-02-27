# capture-the-ether-solutions-brownie

Solutions to smart contract security CTF [Capture The Ether](https://capturetheether.com/) written in [Brownie](https://eth-brownie.readthedocs.io/en/stable/). All solution work both on local ganache fork of Ropsten testnet and on the real Ropsten testnet. Running solutions on local fork is quicker and allows to check if solution is correct without spending actual testnet ETH.

### How to run

[Install Brownie v1.17.0](https://eth-brownie.readthedocs.io/en/stable/install.html)

Add `.env` file to the project directory with the following content:
    
    export WEB3_INFURA_PROJECT_ID=yourinfuraprojectkey
    export PRIVATE_KEY_PLAYER=yourprivatekey
    export PRIVATE_KEY_NON_PLAYER=anotherprivatekey
    
(Replace `yourinfuraprojectkey`, `yourprivatekey` and `anotherprivatekey` with appropriate values).

Get some test ETH from a Ropsten faucet (2 ETH per account should be enough).

Then create `ropsten-fork-dev` network with the following command:

    brownie networks add development ropsten-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-ropsten.alchemyapi.io/v2/your_alchemy_key accounts=10 mnemonic=brownie port=8545
    
(Replace value `your_alchemy_key` with your [Alchemy](https://www.alchemy.com/) key.)

Run:
    
    brownie compile
    
To solve a challenge (e.g. `token-bank`) on local ganache chain (Ropsten fork), simply run:
  
    brownie run scripts/solve_level_token_bank.py

To solve this challenge on actual Ropsten testnet:

1. Go to the challenge page on Capture The Ether (for `token-bank` it's: https://capturetheether.com/challenges/miscellaneous/token-bank/)
2. Press the big red button with "Begin Challenge" or "Do It Again" written on it and then wait for the challenge contract to get deployed.
3. Copy the resulting address of the challenge contract and replace with it the corresponding address in `brownie-config.yaml`
4. Run:
  
        brownie run scripts/solve_level_token_bank.py --network ropsten
5. Go back to the webpage of the challenge and press big button with "Check Solution" written on it. Wait a bit until the challenge is solved.
