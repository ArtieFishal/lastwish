import { Alchemy, Network } from 'alchemy-sdk';

const settings = {
  apiKey: "9Q4XgctIPC051oHSI63R0QtDO3PYNT-i",
  network: Network.ETH_MAINNET,
};

export const alchemy = new Alchemy(settings);
