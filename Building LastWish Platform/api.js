// API utilities for LastWish Web3 platform
const API_BASE = '/api'

// Helper function for API requests
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies for session management
    ...options,
  }

  if (options.body && typeof options.body === 'object') {
    config.body = JSON.stringify(options.body)
  }

  const response = await fetch(url, config)
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || 'API request failed')
  }

  return data
}

// Authentication APIs
export const checkAuthStatus = () => apiRequest('/auth/profile')

export const connectWallet = (walletData) => 
  apiRequest('/auth/connect-wallet', {
    method: 'POST',
    body: walletData,
  })

export const resolveENS = (ensDomain) =>
  apiRequest('/auth/resolve-ens', {
    method: 'POST',
    body: { ens_domain: ensDomain },
  })

export const getNonce = (walletAddress) =>
  apiRequest('/auth/get-nonce', {
    method: 'POST',
    body: { wallet_address: walletAddress },
  })

export const updateProfile = (profileData) =>
  apiRequest('/auth/update-profile', {
    method: 'PUT',
    body: profileData,
  })

export const getSubscriptionStatus = () => 
  apiRequest('/auth/subscription-status')

export const logout = () =>
  apiRequest('/auth/logout', { method: 'POST' })

// Estate Planning APIs
export const getDashboard = () => apiRequest('/estate/dashboard')

// Will Management
export const getWills = () => apiRequest('/estate/wills')

export const createWill = (willData) =>
  apiRequest('/estate/wills', {
    method: 'POST',
    body: willData,
  })

export const updateWill = (willId, willData) =>
  apiRequest(`/estate/wills/${willId}`, {
    method: 'PUT',
    body: willData,
  })

// Asset Management
export const getAssets = () => apiRequest('/estate/assets')

export const createAsset = (assetData) =>
  apiRequest('/estate/assets', {
    method: 'POST',
    body: assetData,
  })

export const updateAsset = (assetId, assetData) =>
  apiRequest(`/estate/assets/${assetId}`, {
    method: 'PUT',
    body: assetData,
  })

// Crypto Asset Management
export const getCryptoAssets = () => apiRequest('/estate/crypto-assets')

export const createCryptoAsset = (cryptoAssetData) =>
  apiRequest('/estate/crypto-assets', {
    method: 'POST',
    body: cryptoAssetData,
  })

export const updateCryptoAsset = (assetId, cryptoAssetData) =>
  apiRequest(`/estate/crypto-assets/${assetId}`, {
    method: 'PUT',
    body: cryptoAssetData,
  })

// Beneficiary Management
export const getBeneficiaries = () => apiRequest('/estate/beneficiaries')

export const createBeneficiary = (beneficiaryData) =>
  apiRequest('/estate/beneficiaries', {
    method: 'POST',
    body: beneficiaryData,
  })

export const updateBeneficiary = (beneficiaryId, beneficiaryData) =>
  apiRequest(`/estate/beneficiaries/${beneficiaryId}`, {
    method: 'PUT',
    body: beneficiaryData,
  })

export const deleteBeneficiary = (beneficiaryId) =>
  apiRequest(`/estate/beneficiaries/${beneficiaryId}`, {
    method: 'DELETE',
  })

// Create api object for components that expect it
export const api = {
  get: (endpoint) => apiRequest(endpoint),
  post: (endpoint, data) => apiRequest(endpoint, { method: 'POST', body: data }),
  put: (endpoint, data) => apiRequest(endpoint, { method: 'PUT', body: data }),
  delete: (endpoint) => apiRequest(endpoint, { method: 'DELETE' })
}

// Utility functions for Web3 integration
export const isValidEthereumAddress = (address) => {
  return /^0x[a-fA-F0-9]{40}$/.test(address)
}

export const truncateAddress = (address, startLength = 6, endLength = 4) => {
  if (!address) return ''
  if (address.length <= startLength + endLength) return address
  return `${address.slice(0, startLength)}...${address.slice(-endLength)}`
}

export const formatCurrency = (amount, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount)
}

export const formatCrypto = (amount, symbol) => {
  const formatted = parseFloat(amount).toFixed(6).replace(/\.?0+$/, '')
  return `${formatted} ${symbol}`
}

// Simulated Web3 functions (replace with actual Web3 integration)
export const simulateWalletConnection = async (walletType) => {
  // Simulate wallet connection delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // Generate mock wallet data
  const mockAddresses = {
    metamask: '0x742d35Cc6634C0532925a3b8D0C9e3e7e8b4c2d1',
    walletconnect: '0x8ba1f109551bD432803012645Hac136c22C177e9',
    coinbase: '0x1234567890123456789012345678901234567890',
    trust: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd'
  }
  
  const address = mockAddresses[walletType] || mockAddresses.metamask
  
  return {
    address: address,
    network: 'ethereum',
    signature: '0x' + Array(128).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
    message: `Sign this message to authenticate with LastWish: ${Date.now()}`
  }
}

export const simulateENSResolution = async (domain) => {
  // Simulate ENS resolution
  await new Promise(resolve => setTimeout(resolve, 500))
  
  if (domain === 'lastwish.eth') {
    return '0x742d35Cc6634C0532925a3b8D0C9e3e7e8b4c2d1'
  }
  
  // Generate deterministic address from domain
  const hash = domain.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  
  return `0x${Math.abs(hash).toString(16).padStart(40, '0')}`
}

export const getNetworkInfo = (networkId) => {
  const networks = {
    1: { name: 'Ethereum', symbol: 'ETH', color: '#627EEA' },
    137: { name: 'Polygon', symbol: 'MATIC', color: '#8247E5' },
    56: { name: 'BSC', symbol: 'BNB', color: '#F3BA2F' },
    43114: { name: 'Avalanche', symbol: 'AVAX', color: '#E84142' }
  }
  
  return networks[networkId] || networks[1]
}

