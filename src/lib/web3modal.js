import { createWeb3Modal } from '@web3modal/wagmi/react'
import { defaultWagmiConfig } from '@web3modal/wagmi/react/config'

import { mainnet, polygon, bsc, avalanche } from 'viem/chains'

// 1. Get projectId from https://cloud.walletconnect.com
const projectId = '49fef037b7a144df8d09cb34c87686c3'

// 2. Create wagmiConfig
const metadata = {
  name: 'LastWish.eth',
  description: 'A decentralized web application for cryptocurrency estate planning.',
  url: 'https://web3modal.com', // origin domain
  icons: ['https://avatars.githubusercontent.com/u/37784886']
}

const chains = [mainnet, polygon, bsc, avalanche]
export const config = defaultWagmiConfig({
  chains,
  projectId,
  metadata,
})

// 3. Create modal
createWeb3Modal({
  wagmiConfig: config,
  projectId,
  chains
})
