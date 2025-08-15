# WalletConnect Integration Setup for LastWish.eth

## Overview
This document provides complete setup instructions for integrating WalletConnect v2 with your LastWish.eth estate planning platform.

## Prerequisites
1. WalletConnect Cloud Registry account
2. Project ID from WalletConnect Cloud
3. Local SDK installation (optional for development)

## Step 1: Register Your Application

### 1.1 Go to WalletConnect Cloud Registry
- Visit: https://cloud.walletconnect.com/
- Sign up or log in to your account
- Click "Create Project" or "New Project"

### 1.2 Configure Your Project
```
Project Name: LastWish.eth
Project Description: Web3 Estate Planning Platform
Project URL: https://lastwish.eth (or your domain)
Project Icon: Upload your LastWish logo
```

### 1.3 Get Your Project ID
- After creating the project, copy your **Project ID**
- This is a unique identifier like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

## Step 2: Environment Configuration

### 2.1 Frontend Environment Variables
Create a `.env` file in your React frontend directory:

```bash
# WalletConnect Configuration
REACT_APP_WALLETCONNECT_PROJECT_ID=your_project_id_here

# Optional: Custom RPC endpoints
REACT_APP_ETHEREUM_RPC=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
REACT_APP_POLYGON_RPC=https://polygon-rpc.com/
REACT_APP_BSC_RPC=https://bsc-dataseed.binance.org/
REACT_APP_AVALANCHE_RPC=https://api.avax.network/ext/bc/C/rpc
```

### 2.2 Backend Environment Variables
Add to your Flask backend `.env` file:

```bash
# WalletConnect Configuration
WALLETCONNECT_PROJECT_ID=your_project_id_here

# Optional: ENS Resolution
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
```

## Step 3: Local SDK Installation (Optional)

### 3.1 Install WalletConnect SDK
```bash
# For React frontend
npm install @walletconnect/universal-provider @walletconnect/modal ethers

# For additional Web3 utilities
npm install @walletconnect/utils @walletconnect/types
```

### 3.2 Install Backend Dependencies
```bash
# For Python backend (ENS resolution, signature verification)
pip install web3 eth-account eth-utils
```

## Step 4: Update Configuration Files

### 4.1 Update HTML Template
Replace `YOUR_PROJECT_ID` in `/public/index.html`:

```html
<script>
  window.WALLETCONNECT_CONFIG = {
    projectId: 'your_actual_project_id_here', // Replace this
    metadata: {
      name: 'LastWish.eth',
      description: 'Web3 Estate Planning Platform',
      url: 'https://lastwish.eth',
      icons: ['https://lastwish.eth/icon.png']
    }
  };
</script>
```

### 4.2 Update React Component
In `WalletConnect.jsx`, update the project ID:

```javascript
const wcProvider = await window.WalletConnectUniversalProvider.init({
  projectId: process.env.REACT_APP_WALLETCONNECT_PROJECT_ID, // This will use your .env value
  metadata: {
    name: "LastWish.eth",
    description: "Web3 Estate Planning Platform", 
    url: "https://lastwish.eth",
    icons: ["https://lastwish.eth/icon.png"],
  },
});
```

## Step 5: Testing the Integration

### 5.1 Test Wallet Connections
1. **MetaMask**: Should work immediately if extension is installed
2. **WalletConnect**: Will show QR code for mobile wallet scanning
3. **Coinbase Wallet**: Will redirect to Coinbase Wallet app
4. **Trust Wallet**: Will redirect to Trust Wallet app

### 5.2 Test Multi-Chain Support
The integration supports:
- **Ethereum Mainnet** (Chain ID: 1)
- **Polygon** (Chain ID: 137)
- **BSC** (Chain ID: 56)
- **Avalanche** (Chain ID: 43114)

### 5.3 Test ENS Resolution
Try resolving these test domains:
- `vitalik.eth`
- `nick.eth`
- `lastwish.eth`
- `demo.eth`

## Step 6: Production Deployment

### 6.1 Update Domain Configuration
In WalletConnect Cloud Registry:
1. Update your project URL to production domain
2. Add production domain to allowed origins
3. Update redirect URIs if using deep links

### 6.2 Security Considerations
- Never expose private keys or seed phrases
- Validate all wallet addresses on backend
- Implement rate limiting for wallet connections
- Use HTTPS in production
- Validate signatures for sensitive operations

### 6.3 Error Handling
Common issues and solutions:

**"Project ID not found"**
- Verify your project ID is correct
- Check that project is active in WalletConnect Cloud

**"Connection failed"**
- Check network connectivity
- Verify supported networks match wallet
- Ensure wallet app is updated

**"QR code not showing"**
- Check that WalletConnect Modal is loaded
- Verify project ID is set correctly
- Check browser console for errors

## Step 7: Advanced Features

### 7.1 Session Persistence
The integration automatically saves sessions to localStorage:
```javascript
localStorage.setItem('walletconnect_session', JSON.stringify(provider.session));
```

### 7.2 Multi-Chain Asset Management
Each connected wallet can manage assets across all supported chains:
- Ethereum: ETH, ERC-20 tokens, NFTs
- Polygon: MATIC, ERC-20 tokens, NFTs  
- BSC: BNB, BEP-20 tokens, NFTs
- Avalanche: AVAX, ERC-20 tokens, NFTs

### 7.3 Smart Contract Interactions
The integration supports:
- Transaction signing
- Message signing
- Contract interactions
- Multi-signature operations

## Step 8: Monitoring and Analytics

### 8.1 WalletConnect Analytics
- Monitor connection success rates
- Track popular wallet types
- Analyze network usage patterns

### 8.2 Custom Analytics
Track in your backend:
- Wallet connection events
- Network preferences
- User retention by wallet type
- Estate planning completion rates

## Troubleshooting

### Common Issues

**1. "WalletConnect SDK not loaded"**
- Check internet connection
- Verify CDN links in HTML
- Check browser console for 404 errors

**2. "Invalid project ID"**
- Verify project ID from WalletConnect Cloud
- Check environment variables are set
- Ensure no extra spaces or characters

**3. "Network not supported"**
- Check wallet supports the requested network
- Verify network configuration in code
- Update wallet to latest version

**4. "Session expired"**
- Clear localStorage and reconnect
- Check session timeout settings
- Verify wallet app is still connected

### Support Resources
- WalletConnect Documentation: https://docs.walletconnect.com/
- WalletConnect Discord: https://discord.gg/walletconnect
- GitHub Issues: https://github.com/WalletConnect/walletconnect-monorepo

## Next Steps
1. Register your application in WalletConnect Cloud Registry
2. Get your Project ID
3. Update environment variables
4. Test wallet connections
5. Deploy to production
6. Monitor analytics and user feedback

Your LastWish.eth platform will then have full Web3 wallet integration with support for all major wallets and blockchain networks!

