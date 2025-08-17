import { useAccount } from 'wagmi'
import { Badge } from './ui/badge'

export function NetworkDisplay() {
  const { chain, isConnected } = useAccount()

  if (!isConnected || !chain) {
    return null
  }

  return (
    <Badge variant="outline">
      {chain.name}
    </Badge>
  )
}
