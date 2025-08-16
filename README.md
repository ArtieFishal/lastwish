# LastWish.eth - Decentralized Digital Will Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://your-username.github.io/lastwish-eth)
[![Web3](https://img.shields.io/badge/Web3-Enabled-blue)](https://ethereum.org/)
[![ENS](https://img.shields.io/badge/ENS-Supported-purple)](https://ens.domains/)

> **The decentralized solution for managing your digital legacy**

LastWish.eth is a revolutionary decentralized platform that enables users to create legally binding digital wills for their cryptocurrency and NFT assets. Built on Ethereum, it provides a secure, transparent, and user-friendly way to ensure your digital assets are properly distributed to your beneficiaries.

## 🌟 Features

### 🔐 **Secure Web3 Integration**
- **Multi-Wallet Support**: Connect with MetaMask, WalletConnect, Coinbase Wallet, and more
- **ENS Resolution**: Support for Ethereum Name Service addresses (alice.eth)
- **Session Management**: Secure off-chain session signing for enhanced security
- **Network Validation**: Automatic network switching and validation

### 💰 **Comprehensive Asset Management**
- **ERC-20 Tokens**: Automatic detection and management of all your tokens
- **NFT Support**: Full support for ERC-721 and ERC-1155 non-fungible tokens
- **Multi-Wallet Assets**: Include up to 20 different wallet addresses
- **Real-time Valuation**: Live asset pricing and portfolio tracking

### 👥 **Advanced Beneficiary System**
- **Multiple Beneficiaries**: Add unlimited beneficiaries with detailed information
- **Percentage Allocation**: Precise percentage-based asset distribution
- **Contact Management**: Store names, addresses, emails, and relationships
- **ENS Integration**: Beneficiaries can use ENS names for easy identification

### 💳 **Transparent Payment System**
- **Fair Pricing**: Only 0.0001 ETH platform fee
- **ENS Discounts**: 20% discount for ENS domain holders
- **On-chain Payments**: All payments processed transparently on Ethereum
- **Transaction Tracking**: Complete payment history and receipts

### 📄 **Professional Will Generation**
- **Legal Formatting**: Properly formatted legal documents
- **PDF Export**: Download and print your complete will
- **Comprehensive Details**: All assets, beneficiaries, and instructions included
- **Instant Generation**: Create your will in minutes, not hours

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:
- A Web3-compatible browser (Chrome, Firefox, Safari, Edge)
- A cryptocurrency wallet (MetaMask recommended)
- Some ETH for transaction fees
- Moralis API key
- WalletConnect Project ID

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/lastwish-eth.git
   cd lastwish-eth
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   MORALIS_API_KEY=your_moralis_api_key_here
   WALLETCONNECT_PROJECT_ID=your_walletconnect_project_id_here
   ```

3. **Update configuration**
   
   Edit `src/config.js` with your API keys:
   ```javascript
   window.LASTWISH_CONFIG = {
     chainId: 1,
     payToAddress: "0x016ae25Ac494B123C40EDb2418d9b1FC2d62279b",
     payAmountEth: 0.0001,
     ensDiscountPercent: 20,
     n8nWebhookUrl: "",
     moralisApiKey: "YOUR_MORALIS_API_KEY_HERE",
     walletConnectProjectId: "YOUR_WALLETCONNECT_PROJECT_ID_HERE"
   };
   ```

4. **Start the development server**
   ```bash
   npm start
   ```
   
   Open `http://localhost:8000` in your browser.

### Getting API Keys

#### Moralis API Key
1. Visit [moralis.io](https://moralis.io/)
2. Create a free account
3. Navigate to "Web3 APIs"
4. Create a new project
5. Copy your API key

#### WalletConnect Project ID
1. Visit [cloud.walletconnect.com](https://cloud.walletconnect.com/)
2. Create an account
3. Create a new project
4. Copy your Project ID

## 📖 How to Use

### Step 1: Connect Your Wallet
1. Click the "Connect" button
2. Select your preferred wallet
3. Approve the connection request
4. Sign the session message (free, off-chain)

### Step 2: Enter Owner Information
1. Fill in your full legal name
2. Add any special instructions for your executor
3. Your primary wallet address is automatically detected

### Step 3: Add Additional Wallets (Optional)
1. Enter wallet addresses or ENS names
2. Add up to 20 different wallets
3. Include all wallets containing your digital assets

### Step 4: Add Beneficiaries
1. Enter beneficiary details (name, wallet/ENS, email, relationship)
2. Add as many beneficiaries as needed
3. Ensure contact information is accurate

### Step 5: Load and Assign Assets
1. Click "Load Assets" to fetch your tokens and NFTs
2. Or use "Load Demo Data" to explore the platform
3. Assign percentages to each beneficiary for each asset
4. Ensure total percentages equal 100% per asset

### Step 6: Make Payment
1. Review the platform fee (0.0001 ETH)
2. ENS holders automatically receive 20% discount
3. Click "Pay" and confirm the transaction
4. Wait for blockchain confirmation

### Step 7: Generate Your Will
1. Click "Generate & Print"
2. Review the generated document
3. Download the PDF
4. Store copies in secure locations

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Blockchain**: Ethereum mainnet with testnet support
- **APIs**: Moralis for blockchain data, WalletConnect for wallet integration
- **Storage**: Browser localStorage for user data persistence
- **Deployment**: GitHub Pages with automated CI/CD

### File Structure
```
lastwish-eth/
├── index.html              # Main application entry point
├── src/
│   ├── app.js             # Core application logic
│   ├── config.js          # Configuration settings
│   └── styles.css         # Application styling
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD configuration
├── .env.example          # Environment template
├── package.json          # Project metadata
└── README.md             # This file
```

### Security Features
- **Client-side Processing**: No server required, all data stays local
- **Secure Sessions**: Off-chain session signing for authentication
- **Input Validation**: Comprehensive validation of all user inputs
- **Transaction Verification**: All blockchain transactions are verified
- **API Key Protection**: Environment variables for sensitive data

## 🌐 Deployment

### GitHub Pages (Recommended)

The repository includes GitHub Actions workflow for automatic deployment to GitHub Pages:

1. Push your code to the `main` branch
2. GitHub Actions will automatically build and deploy
3. Your site will be available at `https://your-username.github.io/lastwish-eth`

### Custom Hosting
For custom hosting providers:

1. Upload all files to your web server
2. Ensure HTTPS is enabled
3. Configure proper MIME types for JavaScript files
4. Update API keys in `src/config.js`

### IPFS Deployment (Decentralized)
For fully decentralized hosting:

1. Install IPFS CLI
2. Add your project: `ipfs add -r .`
3. Pin the content: `ipfs pin add <hash>`
4. Access via IPFS gateway

## 🔧 Development

### Local Development
```bash
# Start development server
npm start

# The application will be available at http://localhost:8000
```

### Testing
- Test wallet connections with multiple providers
- Verify asset loading with real and demo data
- Test payment flow on testnet first
- Validate responsive design on mobile devices

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Brave

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Submitting issues
- Creating pull requests
- Testing requirements

### Areas for Contribution
- Multi-chain support (Polygon, BSC, Arbitrum)
- Mobile application development
- Smart contract automation
- Additional wallet integrations
- Accessibility improvements
- Documentation enhancements

## 📄 Legal Considerations

### Important Disclaimers
- This platform provides tools for creating digital wills but does not constitute legal advice
- Users should consult with qualified legal professionals for estate planning guidance
- Will validity requirements vary by jurisdiction
- Proper execution and notarization may be required in some locations

### Compliance
- GDPR compliant for EU users
- Data privacy protection implemented
- No personal data stored on servers
- Users maintain full control of their information

## 🛡️ Security

### Best Practices
- Never share your seed phrase or private keys
- Always verify transaction details before signing
- Use hardware wallets for large amounts
- Keep your browser and wallet software updated

### Reporting Security Issues
If you discover a security vulnerability, please:
1. Do not create a public issue
2. Email security concerns to [security@lastwish.eth]
3. Provide detailed information about the vulnerability
4. Allow time for investigation and resolution

## 📊 Roadmap

### Phase 1: Core Platform ✅
- [x] Web3 wallet integration
- [x] Asset management system
- [x] Beneficiary management
- [x] Payment processing
- [x] Will generation

### Phase 2: Enhanced Features 🚧
- [ ] Multi-chain support
- [ ] Smart contract automation
- [ ] Mobile application
- [ ] Advanced asset management
- [ ] Legal service integration

### Phase 3: Ecosystem Growth 📋
- [ ] Partnership integrations
- [ ] Community governance
- [ ] Advanced analytics
- [ ] Enterprise features
- [ ] Global expansion

## 📈 Statistics

- **Supported Networks**: Ethereum Mainnet (more coming soon)
- **Supported Assets**: ERC-20 tokens, ERC-721 NFTs, ERC-1155 tokens
- **Wallet Integrations**: MetaMask, WalletConnect, Coinbase Wallet, and more
- **Platform Fee**: 0.0001 ETH (20% discount for ENS holders)
- **Maximum Wallets**: 20 per will
- **Maximum Beneficiaries**: Unlimited

## 🆘 Support

### Getting Help
- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs on [GitHub Issues](https://github.com/your-username/lastwish-eth/issues)
- **Discussions**: Join community discussions on GitHub
- **FAQ**: Common questions answered in documentation

### Community
- **Discord**: Join our community server
- **Twitter**: Follow [@LastWishEth](https://twitter.com/LastWishEth)
- **Blog**: Read updates on our blog
- **Newsletter**: Subscribe for important updates

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ethereum Foundation** for the blockchain infrastructure
- **Moralis** for blockchain data APIs
- **WalletConnect** for wallet integration
- **ENS** for domain name services
- **Open source community** for tools and libraries

## 📞 Contact

- **Website**: [lastwish.eth](https://lastwish.eth)
- **Email**: contact@lastwish.eth
- **GitHub**: [github.com/your-username/lastwish-eth](https://github.com/your-username/lastwish-eth)
- **Twitter**: [@LastWishEth](https://twitter.com/LastWishEth)

---

**Made with ❤️ by the LastWish.eth team**

*Securing your digital legacy for future generations*

