# API Documentation

## Overview

LastWish.eth integrates with several external APIs and blockchain services to provide comprehensive functionality. This document outlines all API integrations, their purposes, and implementation details.

## Moralis API Integration

### Overview
Moralis provides blockchain data APIs for fetching user assets, token information, and ENS resolution.

### Base URL
```
https://deep-index.moralis.io/api/v2.2
```

### Authentication
All requests require an API key in the header:
```javascript
headers: {
  'X-API-Key': 'YOUR_MORALIS_API_KEY'
}
```

### Endpoints Used

#### 1. Get ERC-20 Tokens
**Endpoint**: `GET /{address}/erc20`

**Parameters**:
- `address` (string): Ethereum wallet address
- `chain` (string): Blockchain network (default: 'eth')

**Example Request**:
```javascript
const response = await fetch(
  `https://deep-index.moralis.io/api/v2.2/${address}/erc20?chain=eth`,
  {
    headers: {
      'X-API-Key': moralisApiKey
    }
  }
);
```

**Response Format**:
```json
[
  {
    "token_address": "0xa0b86a33e6776e681e9f29e32a1f8b1c8e8b8c8d",
    "name": "Chainlink Token",
    "symbol": "LINK",
    "logo": "https://logo.moralis.io/0x1_0x514910771af9ca656af840dff83e8264ecf986ca_c1c0e0c8c1c0c8c1c0c8c1c0c8c1c0c8",
    "thumbnail": "https://logo.moralis.io/0x1_0x514910771af9ca656af840dff83e8264ecf986ca_thumb_c1c0e0c8c1c0c8c1c0c8c1c0c8c1c0c8",
    "decimals": 18,
    "balance": "1000000000000000000",
    "possible_spam": false,
    "verified_contract": true,
    "total_supply": "1000000000000000000000000000",
    "total_supply_formatted": "1000000000",
    "percentage_relative_to_total_supply": 0.0001
  }
]
```

#### 2. Get NFTs
**Endpoint**: `GET /{address}/nft`

**Parameters**:
- `address` (string): Ethereum wallet address
- `chain` (string): Blockchain network (default: 'eth')
- `format` (string): Response format (default: 'decimal')
- `limit` (number): Number of results (default: 100)

**Example Request**:
```javascript
const response = await fetch(
  `https://deep-index.moralis.io/api/v2.2/${address}/nft?chain=eth&format=decimal&limit=100`,
  {
    headers: {
      'X-API-Key': moralisApiKey
    }
  }
);
```

**Response Format**:
```json
{
  "total": 1,
  "page": 0,
  "page_size": 100,
  "cursor": null,
  "result": [
    {
      "token_address": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
      "token_id": "1",
      "owner_of": "0x057ec652a4f150f7ff94f089a38008f49a0df88e",
      "block_number": "12021127",
      "block_number_minted": "12021127",
      "token_hash": "502cee781b0fb40ea02508b21d319ced",
      "amount": "1",
      "contract_type": "ERC721",
      "name": "BoredApeYachtClub",
      "symbol": "BAYC",
      "token_uri": "https://ipfs.moralis.io:2053/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/1",
      "metadata": {
        "image": "ipfs://QmRRPWG96cmgTn2qSzjwr2qvfNEuhunv6FNeMFGa9bx6mQ",
        "attributes": [
          {
            "trait_type": "Earring",
            "value": "Silver Hoop"
          }
        ]
      },
      "last_token_uri_sync": "2021-02-24T00:47:26.647Z",
      "last_metadata_sync": "2021-02-24T00:47:26.647Z",
      "minter_address": "0x057ec652a4f150f7ff94f089a38008f49a0df88e"
    }
  ]
}
```

#### 3. ENS Resolution
**Endpoint**: `GET /resolve/ens/{domain}`

**Parameters**:
- `domain` (string): ENS domain name (e.g., 'alice.eth')

**Example Request**:
```javascript
const response = await fetch(
  `https://deep-index.moralis.io/api/v2.2/resolve/ens/${ensName}`,
  {
    headers: {
      'X-API-Key': moralisApiKey
    }
  }
);
```

**Response Format**:
```json
{
  "address": "0x057ec652a4f150f7ff94f089a38008f49a0df88e"
}
```

### Error Handling

```javascript
async function handleMoralisRequest(url) {
  try {
    const response = await fetch(url, {
      headers: {
        'X-API-Key': moralisApiKey
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Moralis API error:', error);
    throw error;
  }
}
```

### Rate Limits
- Free tier: 25,000 requests per month
- Paid tiers: Higher limits available
- Implement caching to reduce API calls

## WalletConnect Integration

### Overview
WalletConnect enables connection to various Web3 wallets through QR codes and deep links.

### Configuration
```javascript
const walletConnectOptions = {
  projectId: 'YOUR_WALLETCONNECT_PROJECT_ID',
  chains: [1], // Ethereum Mainnet
  methods: [
    'eth_sendTransaction',
    'eth_signTransaction',
    'eth_sign',
    'personal_sign',
    'eth_signTypedData'
  ],
  events: ['chainChanged', 'accountsChanged'],
  metadata: {
    name: 'LastWish.eth',
    description: 'Decentralized Digital Will Platform',
    url: 'https://lastwish.eth',
    icons: ['https://lastwish.eth/icon.png']
  }
};
```

### Connection Flow
```javascript
async function connectWalletConnect() {
  try {
    // Initialize WalletConnect
    const connector = new WalletConnect(walletConnectOptions);
    
    // Check if already connected
    if (!connector.connected) {
      // Create new session
      await connector.createSession();
    }
    
    // Subscribe to connection events
    connector.on('connect', (error, payload) => {
      if (error) {
        throw error;
      }
      
      const { accounts, chainId } = payload.params[0];
      handleConnection(accounts[0], chainId);
    });
    
    connector.on('session_update', (error, payload) => {
      if (error) {
        throw error;
      }
      
      const { accounts, chainId } = payload.params[0];
      handleAccountChange(accounts[0], chainId);
    });
    
    connector.on('disconnect', (error, payload) => {
      if (error) {
        throw error;
      }
      
      handleDisconnection();
    });
    
  } catch (error) {
    console.error('WalletConnect error:', error);
    throw error;
  }
}
```

## Ethereum JSON-RPC API

### Overview
Direct interaction with Ethereum blockchain through JSON-RPC calls.

### Common Methods

#### 1. Get Account Balance
```javascript
async function getBalance(address) {
  const balance = await window.ethereum.request({
    method: 'eth_getBalance',
    params: [address, 'latest']
  });
  
  return parseInt(balance, 16) / Math.pow(10, 18); // Convert to ETH
}
```

#### 2. Send Transaction
```javascript
async function sendTransaction(to, value, data = '0x') {
  const txHash = await window.ethereum.request({
    method: 'eth_sendTransaction',
    params: [{
      from: currentAccount,
      to: to,
      value: `0x${(value * Math.pow(10, 18)).toString(16)}`,
      data: data
    }]
  });
  
  return txHash;
}
```

#### 3. Sign Message
```javascript
async function signMessage(message) {
  const signature = await window.ethereum.request({
    method: 'personal_sign',
    params: [message, currentAccount]
  });
  
  return signature;
}
```

#### 4. Get Transaction Receipt
```javascript
async function getTransactionReceipt(txHash) {
  const receipt = await window.ethereum.request({
    method: 'eth_getTransactionReceipt',
    params: [txHash]
  });
  
  return receipt;
}
```

### Network Management

#### Switch Network
```javascript
async function switchNetwork(chainId) {
  try {
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: `0x${chainId.toString(16)}` }]
    });
  } catch (error) {
    if (error.code === 4902) {
      // Network not added to wallet
      await addNetwork(chainId);
    } else {
      throw error;
    }
  }
}
```

#### Add Network
```javascript
async function addNetwork(chainId) {
  const networkConfig = {
    1: {
      chainId: '0x1',
      chainName: 'Ethereum Mainnet',
      nativeCurrency: {
        name: 'Ether',
        symbol: 'ETH',
        decimals: 18
      },
      rpcUrls: ['https://mainnet.infura.io/v3/YOUR_INFURA_KEY'],
      blockExplorerUrls: ['https://etherscan.io']
    }
  };
  
  await window.ethereum.request({
    method: 'wallet_addEthereumChain',
    params: [networkConfig[chainId]]
  });
}
```

## Error Handling Best Practices

### API Error Types
```javascript
class APIError extends Error {
  constructor(message, status, endpoint) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.endpoint = endpoint;
  }
}

class NetworkError extends Error {
  constructor(message, chainId) {
    super(message);
    this.name = 'NetworkError';
    this.chainId = chainId;
  }
}

class WalletError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'WalletError';
    this.code = code;
  }
}
```

### Retry Logic
```javascript
async function retryRequest(requestFn, maxRetries = 3, delay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await requestFn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      
      console.warn(`Request failed, retrying in ${delay}ms...`, error);
      await new Promise(resolve => setTimeout(resolve, delay));
      delay *= 2; // Exponential backoff
    }
  }
}
```

## Caching Strategy

### Local Storage Cache
```javascript
class APICache {
  constructor(ttl = 300000) { // 5 minutes default
    this.cache = new Map();
    this.ttl = ttl;
  }
  
  set(key, value) {
    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });
  }
  
  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return item.value;
  }
  
  clear() {
    this.cache.clear();
  }
}

const apiCache = new APICache();
```

### Usage Example
```javascript
async function getCachedAssets(address) {
  const cacheKey = `assets_${address}`;
  let assets = apiCache.get(cacheKey);
  
  if (!assets) {
    assets = await loadAssetsFromAPI(address);
    apiCache.set(cacheKey, assets);
  }
  
  return assets;
}
```

## Security Considerations

### API Key Protection
- Never expose API keys in client-side code
- Use environment variables for configuration
- Implement server-side proxy for sensitive operations
- Rotate API keys regularly

### Request Validation
```javascript
function validateAddress(address) {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
}

function validateENS(name) {
  return /^[a-zA-Z0-9-]+\.eth$/.test(name);
}

function sanitizeInput(input) {
  return input.trim().toLowerCase();
}
```

### Rate Limiting
```javascript
class RateLimiter {
  constructor(maxRequests = 10, windowMs = 60000) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }
  
  canMakeRequest() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.windowMs);
    
    if (this.requests.length >= this.maxRequests) {
      return false;
    }
    
    this.requests.push(now);
    return true;
  }
}

const rateLimiter = new RateLimiter();
```

## Testing APIs

### Mock Data for Development
```javascript
const mockTokens = [
  {
    token_address: '0xa0b86a33e6776e681e9f29e32a1f8b1c8e8b8c8d',
    name: 'Test Token',
    symbol: 'TEST',
    decimals: 18,
    balance: '1000000000000000000'
  }
];

const mockNFTs = [
  {
    token_address: '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d',
    token_id: '1',
    name: 'Test NFT Collection',
    symbol: 'TNFT',
    metadata: {
      name: 'Test NFT #1',
      image: 'https://example.com/nft1.png'
    }
  }
];
```

### API Testing Functions
```javascript
async function testMoralisConnection() {
  try {
    const response = await fetch(
      'https://deep-index.moralis.io/api/v2.2/0x057ec652a4f150f7ff94f089a38008f49a0df88e/erc20?chain=eth',
      {
        headers: {
          'X-API-Key': moralisApiKey
        }
      }
    );
    
    console.log('Moralis API Status:', response.status);
    return response.ok;
  } catch (error) {
    console.error('Moralis API test failed:', error);
    return false;
  }
}

async function testWalletConnection() {
  try {
    if (!window.ethereum) {
      throw new Error('No wallet detected');
    }
    
    const accounts = await window.ethereum.request({
      method: 'eth_accounts'
    });
    
    console.log('Wallet connection test:', accounts.length > 0 ? 'Connected' : 'Not connected');
    return accounts.length > 0;
  } catch (error) {
    console.error('Wallet connection test failed:', error);
    return false;
  }
}
```

## Performance Optimization

### Batch Requests
```javascript
async function batchLoadAssets(addresses) {
  const promises = addresses.map(address => 
    Promise.all([
      loadERC20Tokens(address),
      loadNFTs(address)
    ])
  );
  
  const results = await Promise.all(promises);
  return results.flat();
}
```

### Lazy Loading
```javascript
async function lazyLoadAssetMetadata(assets) {
  const loadMetadata = async (asset) => {
    if (asset.metadata) return asset;
    
    try {
      const metadata = await fetchTokenMetadata(asset.token_address);
      return { ...asset, metadata };
    } catch (error) {
      console.warn(`Failed to load metadata for ${asset.token_address}:`, error);
      return asset;
    }
  };
  
  return Promise.all(assets.map(loadMetadata));
}
```

This API documentation provides comprehensive coverage of all external integrations used by LastWish.eth. For additional technical details or troubleshooting, refer to the respective service documentation or contact the development team.

