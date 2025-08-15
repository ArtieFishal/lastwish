# API Documentation

## Overview

LastWish.eth integrates with several external APIs to provide comprehensive blockchain functionality. This document outlines the API integrations, endpoints, and usage patterns.

## Moralis Web3 API

### Base URL
```
https://deep-index.moralis.io/api/v2.2/
```

### Authentication
All requests require the `X-API-Key` header with your Moralis API key.

### Endpoints Used

#### ENS Resolution
```http
GET /resolve/ens/{domain}
```

**Parameters:**
- `domain` (string): The ENS domain to resolve (e.g., "alice.eth")

**Response:**
```json
{
  "address": "0x1234567890123456789012345678901234567890"
}
```

**Usage in Application:**
```javascript
async function resolveENS(ensName) {
  const response = await fetch(`https://deep-index.moralis.io/api/v2.2/resolve/ens/${ensName}`, {
    headers: { 'X-API-Key': cfg.moralisApiKey }
  });
  return response.json();
}
```

#### Get ERC-20 Token Balances
```http
GET /{address}/erc20
```

**Parameters:**
- `address` (string): Ethereum wallet address
- `chain` (string): Blockchain identifier (default: "eth")

**Response:**
```json
[
  {
    "token_address": "0xa0b86a33e6776e681e9f29e32a1f8b1c8e8b8c8d",
    "name": "Example Token",
    "symbol": "EXT",
    "logo": "https://example.com/logo.png",
    "thumbnail": "https://example.com/thumb.png",
    "decimals": 18,
    "balance": "1000000000000000000"
  }
]
```

#### Get NFT Collections
```http
GET /{address}/nft
```

**Parameters:**
- `address` (string): Ethereum wallet address
- `chain` (string): Blockchain identifier (default: "eth")
- `format` (string): Response format ("decimal" or "hex")

**Response:**
```json
{
  "total": 10,
  "page": 0,
  "page_size": 100,
  "result": [
    {
      "token_address": "0x1234567890123456789012345678901234567890",
      "token_id": "1",
      "amount": "1",
      "owner_of": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
      "token_hash": "hash123",
      "block_number_minted": "12345678",
      "block_number": "12345679",
      "contract_type": "ERC721",
      "name": "Example NFT",
      "symbol": "ENFT",
      "token_uri": "https://example.com/metadata/1",
      "metadata": {
        "name": "Example NFT #1",
        "description": "An example NFT",
        "image": "https://example.com/image/1.png"
      }
    }
  ]
}
```

## WalletConnect Integration

### Project Configuration
WalletConnect requires a project ID for wallet connection functionality.

### Implementation
```javascript
// Initialize WalletConnect
const walletConnectConfig = {
  projectId: cfg.walletConnectProjectId,
  chains: [1], // Ethereum Mainnet
  methods: ['eth_sendTransaction', 'personal_sign'],
  events: ['chainChanged', 'accountsChanged']
};
```

## Ethereum JSON-RPC API

### Standard Methods Used

#### eth_requestAccounts
Request access to user accounts.

```javascript
const accounts = await window.ethereum.request({
  method: 'eth_requestAccounts'
});
```

#### eth_accounts
Get currently connected accounts.

```javascript
const accounts = await window.ethereum.request({
  method: 'eth_accounts'
});
```

#### eth_chainId
Get the current chain ID.

```javascript
const chainId = await window.ethereum.request({
  method: 'eth_chainId'
});
```

#### wallet_switchEthereumChain
Switch to a different Ethereum chain.

```javascript
await window.ethereum.request({
  method: 'wallet_switchEthereumChain',
  params: [{ chainId: '0x1' }] // Mainnet
});
```

#### personal_sign
Sign a message with the user's private key.

```javascript
const signature = await window.ethereum.request({
  method: 'personal_sign',
  params: [message, account]
});
```

#### eth_sendTransaction
Send an Ethereum transaction.

```javascript
const txHash = await window.ethereum.request({
  method: 'eth_sendTransaction',
  params: [{
    from: account,
    to: payToAddress,
    value: '0x5af3107a4000' // 0.0001 ETH in wei
  }]
});
```

## Error Handling

### Common Error Codes

| Code | Description | Handling |
|------|-------------|----------|
| 4001 | User rejected request | Show user-friendly message |
| 4100 | Unauthorized | Request account access |
| 4200 | Unsupported method | Fallback to alternative |
| 4900 | Disconnected | Attempt reconnection |
| -32002 | Request pending | Wait for user action |
| -32603 | Internal error | Retry with exponential backoff |

### Error Handling Implementation

```javascript
async function handleWeb3Error(error) {
  switch (error.code) {
    case 4001:
      console.log('User rejected the request');
      break;
    case 4100:
      console.log('Account access unauthorized');
      break;
    case 4200:
      console.log('Unsupported method');
      break;
    case 4900:
      console.log('Provider disconnected');
      break;
    case -32002:
      console.log('Request pending');
      break;
    case -32603:
      console.log('Internal error');
      break;
    default:
      console.log('Unknown error:', error);
  }
}
```

## Rate Limiting

### Moralis API Limits
- Free tier: 40,000 requests per month
- Pro tier: 3,000,000 requests per month
- Enterprise: Custom limits

### Best Practices
- Implement request caching
- Use batch requests when possible
- Handle rate limit responses gracefully
- Implement exponential backoff

### Rate Limit Handling
```javascript
async function makeAPIRequest(url, options) {
  try {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
      // Rate limited - wait and retry
      const retryAfter = response.headers.get('Retry-After') || 60;
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      return makeAPIRequest(url, options);
    }
    
    return response;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}
```

## Security Considerations

### API Key Protection
- Never expose API keys in client-side code
- Use environment variables for configuration
- Implement server-side proxy for sensitive operations
- Rotate API keys regularly

### Request Validation
- Validate all user inputs before API calls
- Sanitize addresses and ENS names
- Implement request signing for critical operations
- Use HTTPS for all API communications

### Data Privacy
- Minimize data collection and storage
- Implement proper data retention policies
- Use local storage for sensitive user data
- Comply with privacy regulations (GDPR, CCPA)

## Testing

### API Testing
```javascript
// Test ENS resolution
async function testENSResolution() {
  try {
    const result = await resolveENS('vitalik.eth');
    console.log('ENS resolved:', result);
  } catch (error) {
    console.error('ENS resolution failed:', error);
  }
}

// Test asset loading
async function testAssetLoading() {
  const testAddress = '0x1234567890123456789012345678901234567890';
  try {
    const tokens = await loadERC20Tokens(testAddress);
    const nfts = await loadNFTs(testAddress);
    console.log('Assets loaded:', { tokens, nfts });
  } catch (error) {
    console.error('Asset loading failed:', error);
  }
}
```

### Mock Data for Development
```javascript
const mockTokens = [
  {
    token_address: '0xa0b86a33e6776e681e9f29e32a1f8b1c8e8b8c8d',
    name: 'Ethereum',
    symbol: 'ETH',
    decimals: 18,
    balance: '1000000000000000000'
  }
];

const mockNFTs = [
  {
    token_address: '0x1234567890123456789012345678901234567890',
    token_id: '1',
    name: 'Example NFT',
    metadata: {
      name: 'Example NFT #1',
      image: 'https://example.com/image.png'
    }
  }
];
```

## Troubleshooting

### Common Issues

#### API Key Invalid
- Verify API key is correct
- Check API key permissions
- Ensure proper header formatting

#### Network Connectivity
- Check internet connection
- Verify API endpoint URLs
- Test with curl or Postman

#### Rate Limiting
- Implement proper retry logic
- Monitor API usage
- Consider upgrading API plan

#### CORS Issues
- Configure proper CORS headers
- Use server-side proxy if needed
- Check browser console for errors

### Debug Mode
Enable debug mode for detailed logging:

```javascript
const DEBUG = true;

function debugLog(message, data) {
  if (DEBUG) {
    console.log(`[DEBUG] ${message}:`, data);
  }
}
```

## API Versioning

### Current Versions
- Moralis API: v2.2
- Ethereum JSON-RPC: 2.0
- WalletConnect: v2

### Migration Guidelines
- Monitor API deprecation notices
- Test new versions in development
- Implement gradual rollout
- Maintain backward compatibility

---

For additional support, please refer to the official API documentation:
- [Moralis Documentation](https://docs.moralis.io/)
- [Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [WalletConnect Documentation](https://docs.walletconnect.com/)

