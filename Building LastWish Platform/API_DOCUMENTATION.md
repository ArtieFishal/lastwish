# LastWish.eth API Documentation

## Overview

The LastWish.eth platform provides a comprehensive REST API for Web3 estate planning functionality. All endpoints support JSON request/response format and include proper error handling.

**Base URL**: `https://your-domain.com/api`

## Authentication

The API uses Web3 wallet-based authentication. Users must connect their wallet and maintain a valid session.

### Authentication Flow
1. Connect wallet via `/auth/wallet-connect`
2. Receive session token
3. Include session in subsequent requests
4. Session persists until logout or expiration

## API Endpoints

### Authentication Endpoints

#### Connect Wallet
```http
POST /auth/wallet-connect
```

Connect a Web3 wallet to the platform.

**Request Body:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b8D0C9C2d1234567890",
  "network": "ethereum",
  "ens_domain": "user.eth",
  "wallet_type": "metamask",
  "session_data": {}
}
```

**Response:**
```json
{
  "success": true,
  "message": "Wallet connected successfully",
  "user": {
    "id": 1,
    "wallet_address": "0x742d35cc6634c0532925a3b8d0c9c2d1234567890",
    "ens_domain": "user.eth",
    "primary_network": "ethereum",
    "wallet_type": "metamask",
    "created_at": "2024-01-01T00:00:00",
    "subscription_tier": "free"
  }
}
```

#### Resolve ENS Domain
```http
POST /auth/resolve-ens
```

Resolve an ENS domain to an Ethereum address.

**Request Body:**
```json
{
  "ens_domain": "vitalik.eth"
}
```

**Response:**
```json
{
  "success": true,
  "ens_domain": "vitalik.eth",
  "resolved_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "message": "Successfully resolved vitalik.eth"
}
```

#### Authentication Status
```http
GET /auth/status
```

Check current authentication status.

**Response:**
```json
{
  "authenticated": true,
  "user": {
    "id": 1,
    "wallet_address": "0x742d35cc6634c0532925a3b8d0c9c2d1234567890",
    "ens_domain": "user.eth",
    "primary_network": "ethereum",
    "wallet_type": "metamask",
    "subscription_tier": "free"
  }
}
```

#### Disconnect Wallet
```http
POST /auth/disconnect
```

Disconnect wallet and clear session.

**Response:**
```json
{
  "success": true,
  "message": "Wallet disconnected successfully"
}
```

#### Get Supported Networks
```http
GET /auth/networks
```

Get list of supported blockchain networks.

**Response:**
```json
{
  "success": true,
  "networks": {
    "ethereum": {
      "name": "Ethereum",
      "chain_id": 1,
      "currency": "ETH",
      "rpc_url": "https://mainnet.infura.io/v3/",
      "explorer": "https://etherscan.io"
    },
    "polygon": {
      "name": "Polygon",
      "chain_id": 137,
      "currency": "MATIC",
      "rpc_url": "https://polygon-rpc.com/",
      "explorer": "https://polygonscan.com"
    }
  }
}
```

#### Verify Signature
```http
POST /auth/verify-signature
```

Verify wallet signature for enhanced security.

**Request Body:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b8D0C9C2d1234567890",
  "signature": "0x...",
  "message": "Sign this message to verify your identity"
}
```

**Response:**
```json
{
  "success": true,
  "verified": true,
  "message": "Signature verified successfully"
}
```

### Estate Planning Endpoints

#### Get Dashboard Data
```http
GET /estate/dashboard
```

Get comprehensive estate planning dashboard data.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_assets": 375000,
    "total_crypto_value": 13000,
    "beneficiary_count": 2,
    "will_count": 1,
    "completion_percentage": 85,
    "recent_activity": [
      {
        "action": "asset_added",
        "description": "Added Primary Residence",
        "timestamp": "2024-01-01T00:00:00",
        "value": 350000
      }
    ],
    "recommendations": [
      "Consider adding a backup executor",
      "Update beneficiary contact information"
    ]
  }
}
```

#### Create Will
```http
POST /estate/wills
```

Create a new digital will.

**Request Body:**
```json
{
  "personal_info": {
    "full_name": "John Smith",
    "date_of_birth": "1980-01-01",
    "address": "123 Main St, City, State 12345"
  },
  "executor": {
    "primary_name": "Jane Smith",
    "primary_email": "jane@example.com",
    "backup_name": "Bob Johnson",
    "backup_email": "bob@example.com"
  },
  "beneficiaries": [1, 2],
  "asset_distributions": [
    {
      "asset_id": 1,
      "beneficiary_id": 1,
      "percentage": 100
    }
  ],
  "guardianship": {
    "guardian_name": "Alice Johnson",
    "guardian_email": "alice@example.com"
  },
  "final_wishes": {
    "funeral_preferences": "Cremation",
    "charitable_donations": "Red Cross - $1000"
  }
}
```

**Response:**
```json
{
  "success": true,
  "will_id": 1,
  "message": "Will created successfully",
  "completion_percentage": 100
}
```

#### Get Assets
```http
GET /estate/assets
```

Get all user assets.

**Response:**
```json
{
  "success": true,
  "assets": [
    {
      "id": 1,
      "name": "Primary Residence",
      "type": "real_estate",
      "description": "Family home in downtown",
      "estimated_value": 350000,
      "beneficiary_id": 1,
      "inheritance_percentage": 100,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total_value": 375000
}
```

#### Add Asset
```http
POST /estate/assets
```

Add a new asset to the estate.

**Request Body:**
```json
{
  "name": "2020 Toyota Camry",
  "type": "vehicle",
  "description": "Family car in excellent condition",
  "estimated_value": 25000,
  "beneficiary_id": 2,
  "inheritance_percentage": 100
}
```

**Response:**
```json
{
  "success": true,
  "asset_id": 2,
  "message": "Asset added successfully"
}
```

#### Update Asset
```http
PUT /estate/assets/{asset_id}
```

Update an existing asset.

**Request Body:**
```json
{
  "name": "Updated Asset Name",
  "estimated_value": 30000,
  "beneficiary_id": 1,
  "inheritance_percentage": 50
}
```

**Response:**
```json
{
  "success": true,
  "message": "Asset updated successfully"
}
```

#### Delete Asset
```http
DELETE /estate/assets/{asset_id}
```

Delete an asset from the estate.

**Response:**
```json
{
  "success": true,
  "message": "Asset deleted successfully"
}
```

#### Get Crypto Assets
```http
GET /estate/crypto-assets
```

Get all cryptocurrency assets.

**Response:**
```json
{
  "success": true,
  "crypto_assets": [
    {
      "id": 1,
      "name": "Ethereum",
      "symbol": "ETH",
      "network": "ethereum",
      "wallet_address": "0x742d35Cc6634C0532925a3b8D0C9C2d1234567890",
      "amount": 2.5,
      "estimated_value": 4250,
      "asset_type": "cryptocurrency",
      "beneficiary_id": 1,
      "inheritance_percentage": 100
    }
  ],
  "total_value": 13000
}
```

#### Add Crypto Asset
```http
POST /estate/crypto-assets
```

Add a new cryptocurrency asset.

**Request Body:**
```json
{
  "name": "Bitcoin",
  "symbol": "BTC",
  "network": "bitcoin",
  "wallet_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "amount": 0.15,
  "estimated_value": 6750,
  "asset_type": "cryptocurrency",
  "beneficiary_id": 1,
  "inheritance_percentage": 100
}
```

**Response:**
```json
{
  "success": true,
  "crypto_asset_id": 2,
  "message": "Crypto asset added successfully"
}
```

#### Get Beneficiaries
```http
GET /estate/beneficiaries
```

Get all beneficiaries.

**Response:**
```json
{
  "success": true,
  "beneficiaries": [
    {
      "id": 1,
      "name": "Sarah Smith",
      "relationship": "spouse",
      "email": "sarah@example.com",
      "phone": "+1-555-0123",
      "address": "123 Main St, City, State 12345",
      "date_of_birth": "1985-05-15",
      "is_minor": false,
      "guardian_id": null,
      "inheritance_percentage": 60,
      "wallet_address": "0x8ba1f109551bd432803012645bd132fdc3b4f132"
    }
  ]
}
```

#### Add Beneficiary
```http
POST /estate/beneficiaries
```

Add a new beneficiary.

**Request Body:**
```json
{
  "name": "Michael Smith",
  "relationship": "child",
  "email": "michael@example.com",
  "phone": "+1-555-0124",
  "address": "456 Oak Ave, City, State 12345",
  "date_of_birth": "2010-03-20",
  "guardian_id": 1,
  "inheritance_percentage": 40,
  "wallet_address": "0x1234567890123456789012345678901234567890"
}
```

**Response:**
```json
{
  "success": true,
  "beneficiary_id": 2,
  "message": "Beneficiary added successfully"
}
```

### NLWeb AI Integration Endpoints

#### Analyze Estate Completeness
```http
POST /nlweb/analyze-estate
```

Get AI-powered analysis of estate planning completeness.

**Request Body:**
```json
{
  "user_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "completeness_score": 85,
    "recommendations": [
      "Consider adding a backup executor",
      "Update beneficiary contact information",
      "Add digital asset instructions"
    ],
    "risk_assessment": {
      "estate_tax_risk": "low",
      "probate_complexity": "medium",
      "digital_asset_risk": "high"
    },
    "priority_actions": [
      "Add backup executor",
      "Create digital asset inventory"
    ]
  }
}
```

#### Generate Will Document
```http
POST /nlweb/generate-will
```

Generate a comprehensive will document using AI.

**Request Body:**
```json
{
  "will_id": 1,
  "jurisdiction": "california",
  "include_digital_assets": true
}
```

**Response:**
```json
{
  "success": true,
  "document": {
    "content": "LAST WILL AND TESTAMENT OF JOHN SMITH...",
    "format": "legal_document",
    "jurisdiction": "california",
    "digital_asset_provisions": true,
    "witness_requirements": "Two witnesses required",
    "notarization_required": false
  }
}
```

#### Get Estate Consultation
```http
POST /nlweb/consultation
```

Get AI-powered estate planning consultation.

**Request Body:**
```json
{
  "question": "How should I handle my cryptocurrency in my will?",
  "context": {
    "user_id": 1,
    "estate_value": 388000,
    "has_crypto": true,
    "jurisdiction": "california"
  }
}
```

**Response:**
```json
{
  "success": true,
  "consultation": {
    "response": "For cryptocurrency inheritance in California, you should...",
    "recommendations": [
      "Create detailed wallet access instructions",
      "Consider using a crypto inheritance service",
      "Ensure beneficiaries understand crypto management"
    ],
    "legal_considerations": [
      "California recognizes digital assets in estate planning",
      "Private keys must be securely stored and accessible"
    ],
    "next_steps": [
      "Document all wallet addresses and access methods",
      "Create secure key storage solution"
    ]
  }
}
```

### Subscription Management Endpoints

#### Get Current Subscription
```http
GET /subscription/current
```

Get current user subscription details.

**Response:**
```json
{
  "success": true,
  "subscription": {
    "tier": "basic",
    "price": 9.99,
    "billing_cycle": "monthly",
    "features": [
      "3 wills",
      "25 traditional assets",
      "15 crypto assets",
      "10 beneficiaries",
      "AI assistance",
      "Smart contracts"
    ],
    "usage": {
      "wills_used": 1,
      "assets_used": 2,
      "crypto_assets_used": 2,
      "beneficiaries_used": 2
    },
    "next_billing_date": "2024-02-01T00:00:00",
    "status": "active"
  }
}
```

#### Upgrade Subscription
```http
POST /subscription/upgrade
```

Upgrade to a higher subscription tier.

**Request Body:**
```json
{
  "new_tier": "premium",
  "payment_method": "credit_card",
  "billing_cycle": "monthly"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Subscription upgraded successfully",
  "new_tier": "premium",
  "effective_date": "2024-01-01T00:00:00",
  "next_billing_amount": 29.99
}
```

#### Get Usage Statistics
```http
GET /subscription/usage
```

Get detailed usage statistics.

**Response:**
```json
{
  "success": true,
  "usage": {
    "current_period": {
      "wills_created": 1,
      "assets_added": 5,
      "crypto_assets_added": 3,
      "beneficiaries_added": 2,
      "ai_consultations": 12,
      "documents_generated": 3
    },
    "limits": {
      "wills": 3,
      "assets": 25,
      "crypto_assets": 15,
      "beneficiaries": 10
    },
    "percentage_used": {
      "wills": 33,
      "assets": 20,
      "crypto_assets": 20,
      "beneficiaries": 20
    }
  }
}
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "details": {
    "field": "Additional error details"
  }
}
```

### Common Error Codes

- `AUTHENTICATION_REQUIRED` - User must be authenticated
- `INVALID_WALLET_ADDRESS` - Wallet address format is invalid
- `SUBSCRIPTION_LIMIT_EXCEEDED` - User has exceeded their subscription limits
- `RESOURCE_NOT_FOUND` - Requested resource does not exist
- `VALIDATION_ERROR` - Request data validation failed
- `INTERNAL_SERVER_ERROR` - Server encountered an error

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Rate Limiting

API requests are rate limited to prevent abuse:

- **Authenticated users**: 1000 requests per hour
- **Unauthenticated users**: 100 requests per hour
- **Premium users**: 5000 requests per hour

Rate limit headers are included in all responses:
- `X-RateLimit-Limit` - Request limit per hour
- `X-RateLimit-Remaining` - Remaining requests in current window
- `X-RateLimit-Reset` - Time when rate limit resets

## Webhooks

The platform supports webhooks for real-time notifications:

### Webhook Events

- `will.created` - New will created
- `asset.added` - New asset added
- `beneficiary.added` - New beneficiary added
- `subscription.upgraded` - Subscription tier upgraded
- `document.generated` - Legal document generated

### Webhook Payload Example

```json
{
  "event": "will.created",
  "timestamp": "2024-01-01T00:00:00Z",
  "user_id": 1,
  "data": {
    "will_id": 1,
    "completion_percentage": 100
  }
}
```

## SDK and Libraries

### JavaScript/TypeScript SDK

```bash
npm install @lastwish/sdk
```

```javascript
import { LastWishSDK } from '@lastwish/sdk';

const sdk = new LastWishSDK({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.lastwish.eth'
});

// Connect wallet
const user = await sdk.auth.connectWallet({
  address: '0x...',
  network: 'ethereum'
});

// Create will
const will = await sdk.estate.createWill({
  personal_info: { /* ... */ },
  executor: { /* ... */ }
});
```

### Python SDK

```bash
pip install lastwish-sdk
```

```python
from lastwish import LastWishClient

client = LastWishClient(
    api_key='your-api-key',
    base_url='https://api.lastwish.eth'
)

# Connect wallet
user = client.auth.connect_wallet(
    address='0x...',
    network='ethereum'
)

# Create will
will = client.estate.create_will({
    'personal_info': { /* ... */ },
    'executor': { /* ... */ }
})
```

## Testing

### Test Environment

Base URL: `https://test-api.lastwish.eth`

### Test Wallets

Use these test wallet addresses for development:

- `0x742d35Cc6634C0532925a3b8D0C9C2d1234567890` - Test User 1
- `0x8ba1f109551bd432803012645bd132fdc3b4f132` - Test User 2
- `0x1234567890123456789012345678901234567890` - Test Beneficiary

### Test ENS Domains

- `demo.eth` - Resolves to test address
- `lastwish.eth` - Platform test domain
- `test.eth` - General testing domain

## Support

For API support and questions:

- **Documentation**: [https://docs.lastwish.eth](https://docs.lastwish.eth)
- **GitHub Issues**: [https://github.com/lastwish-eth/issues](https://github.com/lastwish-eth/issues)
- **Email**: api-support@lastwish.eth
- **Discord**: [https://discord.gg/lastwish](https://discord.gg/lastwish)

