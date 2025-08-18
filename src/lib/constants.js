import { mainnet } from 'viem/chains';

export const ERC20_TOKENS = {
  [mainnet.id]: [
    {
      address: '0x514910771AF9Ca656af840dff83E8264EcF986CA',
      name: 'Chainlink',
      symbol: 'LINK',
      decimals: 18,
    },
    {
      address: '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE',
      name: 'Shiba Inu',
      symbol: 'SHIB',
      decimals: 18,
    },
    // I can add more tokens here later
  ]
};

// A generic ERC20 ABI for the `balanceOf` function
export const ERC20_ABI = [
  {
    "constant": true,
    "inputs": [{ "name": "_owner", "type": "address" }],
    "name": "balanceOf",
    "outputs": [{ "name": "balance", "type": "uint256" }],
    "type": "function"
  }
];
