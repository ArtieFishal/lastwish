import React from 'react';
import { WagmiProvider } from 'wagmi';
import { config } from '@/lib/web3modal';

export function Web3Provider({ children }) {
  return (
    <WagmiProvider config={config}>
      {children}
    </WagmiProvider>
  );
}
