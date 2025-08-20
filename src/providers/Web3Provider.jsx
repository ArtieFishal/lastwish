import React, { useState, useEffect } from 'react';
import { WagmiProvider } from 'wagmi';
import { initializeWeb3Modal } from '@/lib/web3modal';

export function Web3Provider({ children }) {
  const [config, setConfig] = useState(null);

  useEffect(() => {
    async function loadConfig() {
      const wagmiConfig = await initializeWeb3Modal();
      setConfig(wagmiConfig);
    }
    loadConfig();
  }, []);

  if (!config) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <p>Initializing Web3 Provider...</p>
      </div>
    );
  }

  return (
    <WagmiProvider config={config}>
      {children}
    </WagmiProvider>
  );
}
