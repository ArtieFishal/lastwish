import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Wallet, ExternalLink, Copy, CheckCircle, AlertCircle, Coins, Shield, Zap } from 'lucide-react'

const WalletConnect = ({ onClose }) => {
  const [connectedWallet, setConnectedWallet] = useState(null)
  const [walletAddress, setWalletAddress] = useState('')
  const [balance, setBalance] = useState(null)
  const [chainId, setChainId] = useState(null)
  const [isConnecting, setIsConnecting] = useState(false)
  const [error, setError] = useState('')
  const [cryptoAssets, setCryptoAssets] = useState([])

  // Supported networks
  const supportedNetworks = [
    { id: 1, name: 'Ethereum', symbol: 'ETH', color: 'blue' },
    { id: 137, name: 'Polygon', symbol: 'MATIC', color: 'purple' },
    { id: 56, name: 'BSC', symbol: 'BNB', color: 'yellow' },
    { id: 43114, name: 'Avalanche', symbol: 'AVAX', color: 'red' }
  ]

  // Mock wallet providers (in production, these would be real wallet integrations)
  const walletProviders = [
    {
      name: 'MetaMask',
      icon: '🦊',
      description: 'Connect using MetaMask browser extension',
      available: typeof window !== 'undefined' && window.ethereum
    },
    {
      name: 'WalletConnect',
      icon: '🔗',
      description: 'Connect using WalletConnect protocol',
      available: true
    },
    {
      name: 'Coinbase Wallet',
      icon: '🔵',
      description: 'Connect using Coinbase Wallet',
      available: true
    },
    {
      name: 'Trust Wallet',
      icon: '🛡️',
      description: 'Connect using Trust Wallet',
      available: true
    }
  ]

  // Mock crypto assets data
  const mockCryptoAssets = [
    {
      symbol: 'ETH',
      name: 'Ethereum',
      balance: '2.5',
      value: '$6,250.00',
      network: 'Ethereum',
      address: '0x742d35Cc6634C0532925a3b8D4C9db96'
    },
    {
      symbol: 'BTC',
      name: 'Bitcoin',
      balance: '0.15',
      value: '$6,750.00',
      network: 'Bitcoin',
      address: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
    },
    {
      symbol: 'MATIC',
      name: 'Polygon',
      balance: '1,250',
      value: '$1,125.00',
      network: 'Polygon',
      address: '0x742d35Cc6634C0532925a3b8D4C9db96'
    },
    {
      symbol: 'USDC',
      name: 'USD Coin',
      balance: '5,000',
      value: '$5,000.00',
      network: 'Ethereum',
      address: '0x742d35Cc6634C0532925a3b8D4C9db96'
    }
  ]

  // Mock NFT collections
  const mockNFTs = [
    {
      name: 'Bored Ape #1234',
      collection: 'Bored Ape Yacht Club',
      value: '$45,000',
      network: 'Ethereum'
    },
    {
      name: 'CryptoPunk #5678',
      collection: 'CryptoPunks',
      value: '$85,000',
      network: 'Ethereum'
    }
  ]

  // Connect wallet function (mock implementation)
  const connectWallet = async (provider) => {
    setIsConnecting(true)
    setError('')
    
    try {
      // Simulate wallet connection delay
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Mock successful connection
      const mockAddress = '0x742d35Cc6634C0532925a3b8D4C9db96C0B1Df8f'
      const mockBalance = '2.5'
      const mockChainId = 1
      
      setConnectedWallet(provider)
      setWalletAddress(mockAddress)
      setBalance(mockBalance)
      setChainId(mockChainId)
      setCryptoAssets(mockCryptoAssets)
      
      // In production, this would trigger n8n workflow to save wallet connection
      await triggerN8NWalletConnection(provider, mockAddress)
      
    } catch (err) {
      setError(`Failed to connect to ${provider.name}. Please try again.`)
    } finally {
      setIsConnecting(false)
    }
  }

  // Disconnect wallet
  const disconnectWallet = () => {
    setConnectedWallet(null)
    setWalletAddress('')
    setBalance(null)
    setChainId(null)
    setCryptoAssets([])
    setError('')
  }

  // Copy address to clipboard
  const copyAddress = async () => {
    try {
      await navigator.clipboard.writeText(walletAddress)
      // Show success feedback (in production, use a toast notification)
      alert('Address copied to clipboard!')
    } catch (err) {
      console.error('Failed to copy address:', err)
    }
  }

  // Trigger n8n workflow for wallet connection
  const triggerN8NWalletConnection = async (provider, address) => {
    try {
      const response = await fetch('/api/n8n/wallet-connected', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider: provider.name,
          address: address,
          chainId: chainId,
          timestamp: new Date().toISOString(),
          userId: 'demo-user'
        })
      })
      
      if (!response.ok) {
        console.error('Failed to trigger n8n wallet connection workflow')
      }
    } catch (error) {
      console.error('Error triggering n8n workflow:', error)
    }
  }

  // Get current network info
  const getCurrentNetwork = () => {
    return supportedNetworks.find(network => network.id === chainId) || supportedNetworks[0]
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-white flex items-center">
              <Wallet className="h-8 w-8 text-blue-500 mr-3" />
              Crypto Wallet Manager
            </h1>
            <Button variant="ghost" onClick={onClose} className="text-gray-400 hover:text-white">
              ✕
            </Button>
          </div>
          
          <div className="flex items-center justify-center">
            <Badge variant="secondary" className="bg-blue-500/10 text-blue-400 border-blue-500/20">
              🔗 Multi-Chain Wallet Connect
            </Badge>
          </div>
        </div>
        
        <div className="p-6">
          {!connectedWallet ? (
            // Wallet Connection Interface
            <div className="space-y-6">
              <div className="text-center mb-8">
                <Wallet className="h-16 w-16 text-blue-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Connect Your Crypto Wallet</h2>
                <p className="text-gray-400">
                  Connect your wallet to manage cryptocurrency inheritance and digital assets
                </p>
              </div>

              {error && (
                <Alert className="bg-red-500/10 border-red-500/20">
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <AlertDescription className="text-red-400">
                    {error}
                  </AlertDescription>
                </Alert>
              )}

              <div className="grid md:grid-cols-2 gap-4">
                {walletProviders.map((provider, index) => (
                  <Card 
                    key={index}
                    className={`bg-gray-800 border-gray-600 hover:border-blue-500/50 transition-all duration-300 cursor-pointer ${
                      !provider.available ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                    onClick={() => provider.available && !isConnecting && connectWallet(provider)}
                  >
                    <CardHeader>
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{provider.icon}</span>
                        <div>
                          <CardTitle className="text-white">{provider.name}</CardTitle>
                          <CardDescription className="text-gray-400">
                            {provider.description}
                          </CardDescription>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      {!provider.available ? (
                        <Badge variant="secondary" className="bg-gray-600 text-gray-300">
                          Not Available
                        </Badge>
                      ) : isConnecting ? (
                        <Badge variant="secondary" className="bg-blue-500/10 text-blue-400">
                          Connecting...
                        </Badge>
                      ) : (
                        <Badge variant="secondary" className="bg-green-500/10 text-green-400">
                          Available
                        </Badge>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>

              <div className="bg-gray-800/50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <Shield className="h-5 w-5 text-green-500 mr-2" />
                  Supported Networks
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {supportedNetworks.map((network) => (
                    <div key={network.id} className="flex items-center space-x-2 p-3 bg-gray-700 rounded-lg">
                      <div className={`w-3 h-3 rounded-full bg-${network.color}-500`}></div>
                      <span className="text-white text-sm font-medium">{network.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            // Connected Wallet Interface
            <div className="space-y-6">
              <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-500" />
                    <div>
                      <h3 className="text-white font-semibold">Wallet Connected</h3>
                      <p className="text-gray-400 text-sm">Connected via {connectedWallet.name}</p>
                    </div>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={disconnectWallet}
                    className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
                  >
                    Disconnect
                  </Button>
                </div>
              </div>

              {/* Wallet Info */}
              <Card className="bg-gray-800 border-gray-600">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Wallet className="h-5 w-5 text-blue-500 mr-2" />
                    Wallet Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Address:</span>
                    <div className="flex items-center space-x-2">
                      <code className="text-white bg-gray-700 px-2 py-1 rounded text-sm">
                        {walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}
                      </code>
                      <Button variant="ghost" size="sm" onClick={copyAddress}>
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Network:</span>
                    <Badge className={`bg-${getCurrentNetwork().color}-500/10 text-${getCurrentNetwork().color}-400`}>
                      {getCurrentNetwork().name}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">ETH Balance:</span>
                    <span className="text-white font-semibold">{balance} ETH</span>
                  </div>
                </CardContent>
              </Card>

              {/* Crypto Assets */}
              <Card className="bg-gray-800 border-gray-600">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Coins className="h-5 w-5 text-yellow-500 mr-2" />
                    Cryptocurrency Assets
                  </CardTitle>
                  <CardDescription className="text-gray-400">
                    Manage your crypto assets for inheritance planning
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {cryptoAssets.map((asset, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                            <span className="text-white text-xs font-bold">{asset.symbol}</span>
                          </div>
                          <div>
                            <p className="text-white font-medium">{asset.name}</p>
                            <p className="text-gray-400 text-sm">{asset.network}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-white font-semibold">{asset.balance} {asset.symbol}</p>
                          <p className="text-gray-400 text-sm">{asset.value}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                    <div className="flex items-center justify-between">
                      <span className="text-blue-400 font-semibold">Total Portfolio Value</span>
                      <span className="text-blue-400 font-bold text-lg">$19,125.00</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* NFT Collections */}
              <Card className="bg-gray-800 border-gray-600">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Zap className="h-5 w-5 text-purple-500 mr-2" />
                    NFT Collections
                  </CardTitle>
                  <CardDescription className="text-gray-400">
                    Digital collectibles and NFTs
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {mockNFTs.map((nft, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                        <div>
                          <p className="text-white font-medium">{nft.name}</p>
                          <p className="text-gray-400 text-sm">{nft.collection}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-white font-semibold">{nft.value}</p>
                          <p className="text-gray-400 text-sm">{nft.network}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Inheritance Actions */}
              <Card className="bg-gray-800 border-gray-600">
                <CardHeader>
                  <CardTitle className="text-white">Inheritance Planning Actions</CardTitle>
                  <CardDescription className="text-gray-400">
                    Set up inheritance for your crypto assets
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button className="w-full bg-blue-500 hover:bg-blue-600">
                    <Shield className="h-4 w-4 mr-2" />
                    Create Smart Contract Inheritance
                  </Button>
                  
                  <Button variant="outline" className="w-full border-gray-600 text-white hover:bg-gray-700">
                    <FileText className="h-4 w-4 mr-2" />
                    Add to Digital Asset Schedule
                  </Button>
                  
                  <Button variant="outline" className="w-full border-gray-600 text-white hover:bg-gray-700">
                    <Users className="h-4 w-4 mr-2" />
                    Assign Beneficiaries
                  </Button>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default WalletConnect

