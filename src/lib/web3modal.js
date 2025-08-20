import { createWeb3Modal } from '@web3modal/wagmi/react'
import { defaultWagmiConfig } from '@web3modal/wagmi/react/config'
import { mainnet, polygon, bsc, avalanche } from 'viem/chains'

let config;
let projectId;

async function fetchConfig() {
  try {
    const response = await fetch('/.netlify/functions/config');
    const data = await response.json();
    if (data.error) {
      throw new Error(data.error);
    }
    return data.projectId;
  } catch (error) {
    console.error("Could not fetch WalletConnect projectId:", error);
    return null;
  }
}

export async function initializeWeb3Modal() {
  projectId = await fetchConfig();

  if (!projectId) {
    console.error("Web3Modal initialization failed: No projectId.");
    return null;
  }

  const metadata = {
    name: 'LastWish.eth',
    description: 'A decentralized web application for cryptocurrency estate planning.',
    url: 'https://lastwish.eth',
    icons: ['https://avatars.githubusercontent.com/u/37784886']
  };

  const chains = [mainnet, polygon, bsc, avalanche];

  config = defaultWagmiConfig({
    chains,
    projectId,
    metadata,
  });

  createWeb3Modal({
    wagmiConfig: config,
    projectId,
    chains
  });

  return config;
}
