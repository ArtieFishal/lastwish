import { Alchemy, Network } from 'alchemy-sdk';

const apiKey = import.meta.env.VITE_ALCHEMY_API_KEY;

if (!apiKey) {
  throw new Error('VITE_ALCHEMY_API_KEY is not set');
}

const settings = {
  apiKey: apiKey,
  network: Network.ETH_MAINNET,
};

export const alchemy = new Alchemy(settings);
