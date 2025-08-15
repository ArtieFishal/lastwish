import React, { useState, useEffect } from 'react'
import { 
  ArrowLeft, 
  Plus, 
  Wallet, 
  Link,
  Edit,
  Trash2,
  AlertCircle,
  CheckCircle,
  Save,
  ExternalLink,
  Copy,
  Zap
} from 'lucide-react'
import { getCryptoAssets, createCryptoAsset, updateCryptoAsset, getBeneficiaries, formatCrypto, truncateAddress } from '../lib/api'

const CryptoAssetManager = ({ user, onBack }) => {
  const [cryptoAssets, setCryptoAssets] = useState([])
  const [beneficiaries, setBeneficiaries] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingAsset, setEditingAsset] = useState(null)
  const [saving, setSaving] = useState(false)
  const [connectedWallets, setConnectedWallets] = useState([])

  const [formData, setFormData] = useState({
    asset_type: '',
    symbol: '',
    name: '',
    wallet_address: '',
    network: '',
    balance: '',
    estimated_value_usd: '',
    contract_address: '',
    token_id: '',
    collection_name: '',
    primary_beneficiary_id: '',
    inheritance_percentage: 100,
    private_key_location: '',
    seed_phrase_location: '',
    access_instructions: '',
    notes: ''
  })

  const assetTypes = [
    { value: 'cryptocurrency', label: 'Cryptocurrency', description: 'Bitcoin, Ethereum, etc.' },
    { value: 'nft', label: 'NFT', description: 'Non-fungible tokens' },
    { value: 'defi_position', label: 'DeFi Position', description: 'Staking, liquidity pools' },
    { value: 'dao_token', label: 'DAO Token', description: 'Governance tokens' },
    { value: 'other', label: 'Other Digital Asset', description: 'Other blockchain assets' }
  ]

  const networks = [
    { value: 'ethereum', label: 'Ethereum', color: '#627EEA' },
    { value: 'polygon', label: 'Polygon', color: '#8247E5' },
    { value: 'bsc', label: 'Binance Smart Chain', color: '#F3BA2F' },
    { value: 'avalanche', label: 'Avalanche', color: '#E84142' },
    { value: 'arbitrum', label: 'Arbitrum', color: '#28A0F0' },
    { value: 'optimism', label: 'Optimism', color: '#FF0420' },
    { value: 'bitcoin', label: 'Bitcoin', color: '#F7931A' },
    { value: 'other', label: 'Other', color: '#6B7280' }
  ]

  const popularTokens = [
    { symbol: 'ETH', name: 'Ethereum' },
    { symbol: 'BTC', name: 'Bitcoin' },
    { symbol: 'USDC', name: 'USD Coin' },
    { symbol: 'USDT', name: 'Tether' },
    { symbol: 'MATIC', name: 'Polygon' },
    { symbol: 'BNB', name: 'Binance Coin' },
    { symbol: 'AVAX', name: 'Avalanche' },
    { symbol: 'UNI', name: 'Uniswap' },
    { symbol: 'LINK', name: 'Chainlink' },
    { symbol: 'AAVE', name: 'Aave' }
  ]

  useEffect(() => {
    loadData()
    loadConnectedWallets()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [cryptoData, beneficiariesData] = await Promise.all([
        getCryptoAssets(),
        getBeneficiaries()
      ])
      setCryptoAssets(cryptoData.crypto_assets || [])
      setBeneficiaries(beneficiariesData.beneficiaries || [])
    } catch (err) {
      setError('Failed to load data: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadConnectedWallets = () => {
    // Simulate connected wallets - in real app, this would come from Web3 provider
    const mockWallets = [
      {
        address: user?.wallet_address || '0x742d35Cc6634C0532925a3b8D0C9e3e7e8b4c2d1',
        network: 'ethereum',
        balance: '2.5 ETH',
        usdValue: 4250
      },
      {
        address: '0x8ba1f109551bD432803012645Hac136c22C177e9',
        network: 'polygon',
        balance: '1,250 MATIC',
        usdValue: 875
      }
    ]
    setConnectedWallets(mockWallets)
  }

  const resetForm = () => {
    setFormData({
      asset_type: '',
      symbol: '',
      name: '',
      wallet_address: '',
      network: '',
      balance: '',
      estimated_value_usd: '',
      contract_address: '',
      token_id: '',
      collection_name: '',
      primary_beneficiary_id: '',
      inheritance_percentage: 100,
      private_key_location: '',
      seed_phrase_location: '',
      access_instructions: '',
      notes: ''
    })
    setEditingAsset(null)
    setShowAddForm(false)
  }

  const handleEdit = (asset) => {
    setFormData({
      asset_type: asset.asset_type || '',
      symbol: asset.symbol || '',
      name: asset.name || '',
      wallet_address: asset.wallet_address || '',
      network: asset.network || '',
      balance: asset.balance?.toString() || '',
      estimated_value_usd: asset.estimated_value_usd?.toString() || '',
      contract_address: asset.contract_address || '',
      token_id: asset.token_id || '',
      collection_name: asset.collection_name || '',
      primary_beneficiary_id: asset.primary_beneficiary_id || '',
      inheritance_percentage: asset.inheritance_percentage || 100,
      private_key_location: asset.private_key_location || '',
      seed_phrase_location: asset.seed_phrase_location || '',
      access_instructions: asset.access_instructions || '',
      notes: asset.notes || ''
    })
    setEditingAsset(asset)
    setShowAddForm(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')

    try {
      const assetData = {
        ...formData,
        balance: parseFloat(formData.balance) || 0,
        estimated_value_usd: parseFloat(formData.estimated_value_usd) || 0
      }

      if (editingAsset) {
        await updateCryptoAsset(editingAsset.id, assetData)
      } else {
        await createCryptoAsset(assetData)
      }

      await loadData()
      resetForm()
      alert(editingAsset ? 'Crypto asset updated successfully!' : 'Crypto asset added successfully!')
    } catch (err) {
      setError('Failed to save crypto asset: ' + err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleTokenSelect = (token) => {
    setFormData(prev => ({
      ...prev,
      symbol: token.symbol,
      name: token.name
    }))
  }

  const handleWalletSelect = (wallet) => {
    setFormData(prev => ({
      ...prev,
      wallet_address: wallet.address,
      network: wallet.network
    }))
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  const getNetworkColor = (network) => {
    const net = networks.find(n => n.value === network)
    return net ? net.color : '#6B7280'
  }

  const getNetworkLabel = (network) => {
    const net = networks.find(n => n.value === network)
    return net ? net.label : 'Unknown'
  }

  const getBeneficiaryName = (beneficiaryId) => {
    const beneficiary = beneficiaries.find(b => b.id === beneficiaryId)
    return beneficiary ? beneficiary.name : 'Unassigned'
  }

  const totalCryptoValue = cryptoAssets.reduce((sum, asset) => sum + (asset.estimated_value_usd || 0), 0)

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-300">Loading your crypto assets...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="border-b border-gray-800 bg-black/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <button 
              onClick={onBack}
              className="flex items-center text-gray-300 hover:text-white transition-colors"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back to Dashboard
            </button>
            
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-400">
                Total Value: ${totalCryptoValue.toLocaleString()}
              </span>
              <button
                onClick={() => setShowAddForm(true)}
                className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors flex items-center"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Crypto Asset
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Crypto Asset Management</h1>
          <p className="text-gray-300">
            Manage your cryptocurrency, NFTs, and DeFi positions for inheritance planning.
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-6">
            <div className="flex items-center text-red-300">
              <AlertCircle className="w-5 h-5 mr-2" />
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Connected Wallets */}
        <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700 mb-8">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Wallet className="w-5 h-5 mr-2 text-blue-500" />
            Connected Wallets
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {connectedWallets.map((wallet, index) => (
              <div key={index} className="bg-gray-800/50 p-4 rounded-lg border border-gray-600">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div 
                      className="w-3 h-3 rounded-full mr-2"
                      style={{ backgroundColor: getNetworkColor(wallet.network) }}
                    ></div>
                    <span className="font-medium">{getNetworkLabel(wallet.network)}</span>
                  </div>
                  <button
                    onClick={() => copyToClipboard(wallet.address)}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    <Copy className="w-4 h-4" />
                  </button>
                </div>
                <p className="text-gray-400 text-sm mb-1">
                  {truncateAddress(wallet.address)}
                </p>
                <div className="flex justify-between items-center">
                  <span className="text-green-400 font-semibold">{wallet.balance}</span>
                  <span className="text-gray-400 text-sm">${wallet.usdValue.toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Crypto Portfolio Summary */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <Wallet className="w-8 h-8 text-green-500" />
              <span className="text-2xl font-bold text-green-400">
                ${totalCryptoValue.toLocaleString()}
              </span>
            </div>
            <h3 className="text-lg font-semibold mb-1">Total Value</h3>
            <p className="text-gray-400 text-sm">All crypto assets</p>
          </div>

          <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-sm font-bold">₿</div>
              <span className="text-2xl font-bold text-blue-400">
                {cryptoAssets.filter(a => a.asset_type === 'cryptocurrency').length}
              </span>
            </div>
            <h3 className="text-lg font-semibold mb-1">Cryptocurrencies</h3>
            <p className="text-gray-400 text-sm">Tokens & coins</p>
          </div>

          <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-sm font-bold">N</div>
              <span className="text-2xl font-bold text-purple-400">
                {cryptoAssets.filter(a => a.asset_type === 'nft').length}
              </span>
            </div>
            <h3 className="text-lg font-semibold mb-1">NFTs</h3>
            <p className="text-gray-400 text-sm">Digital collectibles</p>
          </div>

          <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <Zap className="w-8 h-8 text-orange-500" />
              <span className="text-2xl font-bold text-orange-400">
                {cryptoAssets.filter(a => a.asset_type === 'defi_position').length}
              </span>
            </div>
            <h3 className="text-lg font-semibold mb-1">DeFi Positions</h3>
            <p className="text-gray-400 text-sm">Staking & liquidity</p>
          </div>
        </div>

        {/* Add/Edit Crypto Asset Form */}
        {showAddForm && (
          <div className="bg-gray-900/50 p-8 rounded-xl border border-gray-700 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">
                {editingAsset ? 'Edit Crypto Asset' : 'Add New Crypto Asset'}
              </h2>
              <button
                onClick={resetForm}
                className="text-gray-400 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Asset Type *</label>
                  <select
                    value={formData.asset_type}
                    onChange={(e) => setFormData(prev => ({ ...prev, asset_type: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    required
                  >
                    <option value="">Select asset type</option>
                    {assetTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label} - {type.description}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Network *</label>
                  <select
                    value={formData.network}
                    onChange={(e) => setFormData(prev => ({ ...prev, network: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    required
                  >
                    <option value="">Select network</option>
                    {networks.map(network => (
                      <option key={network.value} value={network.value}>
                        {network.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Token Symbol *</label>
                  <input
                    type="text"
                    value={formData.symbol}
                    onChange={(e) => setFormData(prev => ({ ...prev, symbol: e.target.value.toUpperCase() }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="e.g., ETH, BTC, USDC"
                    required
                  />
                  <div className="mt-2 flex flex-wrap gap-2">
                    {popularTokens.map(token => (
                      <button
                        key={token.symbol}
                        type="button"
                        onClick={() => handleTokenSelect(token)}
                        className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-xs transition-colors"
                      >
                        {token.symbol}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Asset Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="e.g., Ethereum, Bitcoin"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Wallet Address *</label>
                  <input
                    type="text"
                    value={formData.wallet_address}
                    onChange={(e) => setFormData(prev => ({ ...prev, wallet_address: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="0x..."
                    required
                  />
                  <div className="mt-2 space-y-1">
                    {connectedWallets.map((wallet, index) => (
                      <button
                        key={index}
                        type="button"
                        onClick={() => handleWalletSelect(wallet)}
                        className="block w-full text-left px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded text-xs transition-colors"
                      >
                        {truncateAddress(wallet.address)} ({getNetworkLabel(wallet.network)})
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Balance *</label>
                  <input
                    type="number"
                    step="0.000001"
                    value={formData.balance}
                    onChange={(e) => setFormData(prev => ({ ...prev, balance: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="0.0"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Estimated USD Value</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.estimated_value_usd}
                    onChange={(e) => setFormData(prev => ({ ...prev, estimated_value_usd: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="0.00"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Primary Beneficiary</label>
                  <select
                    value={formData.primary_beneficiary_id}
                    onChange={(e) => setFormData(prev => ({ ...prev, primary_beneficiary_id: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                  >
                    <option value="">Select beneficiary</option>
                    {beneficiaries.map(beneficiary => (
                      <option key={beneficiary.id} value={beneficiary.id}>
                        {beneficiary.name} ({beneficiary.relationship})
                      </option>
                    ))}
                  </select>
                </div>

                {formData.asset_type === 'nft' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium mb-2">Contract Address</label>
                      <input
                        type="text"
                        value={formData.contract_address}
                        onChange={(e) => setFormData(prev => ({ ...prev, contract_address: e.target.value }))}
                        className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                        placeholder="0x..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Token ID</label>
                      <input
                        type="text"
                        value={formData.token_id}
                        onChange={(e) => setFormData(prev => ({ ...prev, token_id: e.target.value }))}
                        className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                        placeholder="Token ID"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium mb-2">Collection Name</label>
                      <input
                        type="text"
                        value={formData.collection_name}
                        onChange={(e) => setFormData(prev => ({ ...prev, collection_name: e.target.value }))}
                        className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                        placeholder="e.g., Bored Ape Yacht Club"
                      />
                    </div>
                  </>
                )}
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Private Key Location</label>
                  <input
                    type="text"
                    value={formData.private_key_location}
                    onChange={(e) => setFormData(prev => ({ ...prev, private_key_location: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="e.g., Hardware wallet, safe deposit box"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Seed Phrase Location</label>
                  <input
                    type="text"
                    value={formData.seed_phrase_location}
                    onChange={(e) => setFormData(prev => ({ ...prev, seed_phrase_location: e.target.value }))}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="e.g., Safe, bank vault"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Access Instructions</label>
                <textarea
                  value={formData.access_instructions}
                  onChange={(e) => setFormData(prev => ({ ...prev, access_instructions: e.target.value }))}
                  className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                  rows="3"
                  placeholder="Detailed instructions for accessing this asset..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Additional Notes</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                  className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
                  rows="3"
                  placeholder="Any additional notes or special instructions..."
                />
              </div>

              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 flex items-center"
                >
                  {saving ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4 mr-2" />
                      {editingAsset ? 'Update Asset' : 'Add Asset'}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Crypto Assets List */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Your Crypto Assets ({cryptoAssets.length})</h2>
          
          {cryptoAssets.length > 0 ? (
            <div className="grid gap-6">
              {cryptoAssets.map((asset) => (
                <div key={asset.id} className="bg-gray-900/50 p-6 rounded-xl border border-gray-700">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4">
                      <div className="p-3 bg-gray-800 rounded-lg">
                        <div 
                          className="w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold text-white"
                          style={{ backgroundColor: getNetworkColor(asset.network) }}
                        >
                          {asset.symbol?.charAt(0) || '?'}
                        </div>
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h3 className="text-xl font-semibold">{asset.symbol}</h3>
                          <span className="text-gray-400">•</span>
                          <span className="text-gray-400">{asset.name}</span>
                        </div>
                        
                        <p className="text-gray-400 text-sm mb-3 capitalize">
                          {asset.asset_type.replace('_', ' ')} on {getNetworkLabel(asset.network)}
                        </p>
                        
                        <div className="grid md:grid-cols-3 gap-4 text-sm mb-3">
                          <div>
                            <span className="text-gray-400">Balance:</span>
                            <span className="ml-2 font-semibold text-blue-400">
                              {formatCrypto(asset.balance, asset.symbol)}
                            </span>
                          </div>
                          
                          <div>
                            <span className="text-gray-400">USD Value:</span>
                            <span className="ml-2 font-semibold text-green-400">
                              ${asset.estimated_value_usd?.toLocaleString() || '0'}
                            </span>
                          </div>
                          
                          <div>
                            <span className="text-gray-400">Beneficiary:</span>
                            <span className="ml-2 text-purple-400">
                              {getBeneficiaryName(asset.primary_beneficiary_id)}
                            </span>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm">
                          <div className="flex items-center">
                            <span className="text-gray-400">Wallet:</span>
                            <span className="ml-2 text-gray-300 font-mono">
                              {truncateAddress(asset.wallet_address)}
                            </span>
                            <button
                              onClick={() => copyToClipboard(asset.wallet_address)}
                              className="ml-2 text-gray-400 hover:text-white transition-colors"
                            >
                              <Copy className="w-3 h-3" />
                            </button>
                          </div>
                        </div>
                        
                        {asset.collection_name && (
                          <div className="mt-2 text-sm">
                            <span className="text-gray-400">Collection:</span>
                            <span className="ml-2 text-gray-300">{asset.collection_name}</span>
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(asset)}
                        className="p-2 text-gray-400 hover:text-blue-400 transition-colors"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <Wallet className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No Crypto Assets Added Yet</h3>
              <p className="text-gray-400 mb-6">
                Start by adding your cryptocurrency, NFTs, or DeFi positions.
              </p>
              <button
                onClick={() => setShowAddForm(true)}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg transition-colors flex items-center mx-auto"
              >
                <Plus className="w-5 h-5 mr-2" />
                Add Your First Crypto Asset
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default CryptoAssetManager

