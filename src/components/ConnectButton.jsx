import { useWeb3Modal } from '@web3modal/wagmi/react'
import { Button } from './ui/button'
import { useAccount } from 'wagmi'

export function ConnectButton() {
  // 4. Use modal hook
  const { open } = useWeb3Modal()
  const { address, isConnected } = useAccount()

  const formatAddress = (addr) => {
    if (!addr) return '...';
    return `${addr.substring(0, 6)}...${addr.substring(addr.length - 4)}`;
  }

  return (
    <>
      <Button onClick={() => open()}>
        {isConnected ? formatAddress(address) : 'Connect Wallet'}
      </Button>
    </>
  )
}
