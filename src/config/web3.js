import { http, createConfig } from 'wagmi'
import { mainnet, polygon, bsc, avalanche, arbitrum, optimism } from 'wagmi/chains'

// Define the chains we will support
export const chains = [mainnet, polygon, bsc, avalanche, arbitrum, optimism]

// Create the Wagmi config object
export const config = createConfig({
  chains: chains,
  // Configure transports for each chain
  transports: {
    [mainnet.id]: http(),
    [polygon.id]: http(),
    [bsc.id]: http(),
    [avalanche.id]: http(),
    [arbitrum.id]: http(),
    [optimism.id]: http(),
  },
})

// Define a custom object for our application's use, including Zapper API slugs
export const BLOCKCHAIN_NETWORKS = {
  ethereum: {
    id: 'ethereum',
    name: 'Ethereum',
    chainId: 1,
    wagmiChain: mainnet,
    symbol: 'ETH',
    explorerUrl: 'https://etherscan.io',
  },
  polygon: {
    id: 'polygon',
    name: 'Polygon',
    chainId: 137,
    wagmiChain: polygon,
    symbol: 'MATIC',
    explorerUrl: 'https://polygonscan.com',
  },
  'binance-smart-chain': {
    id: 'binance-smart-chain',
    name: 'BNB Chain',
    chainId: 56,
    wagmiChain: bsc,
    symbol: 'BNB',
    explorerUrl: 'https://bscscan.com',
  },
  avalanche: {
    id: 'avalanche',
    name: 'Avalanche',
    chainId: 43114,
    wagmiChain: avalanche,
    symbol: 'AVAX',
    explorerUrl: 'https://snowtrace.io',
  },
  arbitrum: {
    id: 'arbitrum',
    name: 'Arbitrum',
    chainId: 42161,
    wagmiChain: arbitrum,
    symbol: 'ETH',
    explorerUrl: 'https://arbiscan.io',
  },
  optimism: {
    id: 'optimism',
    name: 'Optimism',
    chainId: 10,
    wagmiChain: optimism,
    symbol: 'ETH',
    explorerUrl: 'https://optimistic.etherscan.io',
  },
}
