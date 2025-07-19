# LastWish.eth - Web3 Estate Planning Platform

![LastWish.eth Logo](https://img.shields.io/badge/LastWish.eth-Web3%20Estate%20Planning-blue?style=for-the-badge&logo=ethereum)

The world's first comprehensive Web3-native estate planning platform. Manage traditional assets, cryptocurrency, NFTs, and smart contracts all in one secure, decentralized platform.

## 🌟 Features

### 🔗 Web3 Integration
- **Multi-Wallet Support**: MetaMask, WalletConnect, Coinbase Wallet, Trust Wallet
- **Multi-Chain Compatible**: Ethereum, Polygon, BSC, Avalanche
- **ENS Domain Integration**: Full support for .eth domains
- **Smart Contract Automation**: Automated inheritance execution

### 💼 Estate Planning
- **Digital Will Creation**: 7-step comprehensive wizard
- **Asset Management**: Traditional assets (real estate, vehicles, bank accounts)
- **Crypto Asset Management**: Cryptocurrency, NFTs, DeFi positions
- **Beneficiary Management**: Complete inheritance allocation system
- **Guardian Management**: Minor children protection

### 🤖 AI-Powered Automation
- **NLWeb Integration**: AI-powered estate planning assistance
- **Document Generation**: Automated legal document creation
- **Legal Compliance**: Multi-jurisdiction compliance monitoring
- **Smart Recommendations**: Personalized estate planning guidance

### 💰 Monetization
- **Subscription Tiers**: Free, Basic ($9/mo), Premium ($29/mo), Enterprise ($99/mo)
- **Feature Limits**: Tier-based asset and beneficiary limits
- **Payment Processing**: Credit card, crypto, and PayPal support
- **Usage Analytics**: Comprehensive business intelligence

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- WalletConnect Project ID (from [WalletConnect Cloud](https://cloud.walletconnect.com/))

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/lastwish-eth.git
cd lastwish-eth
```

### 2. Backend Setup
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export WALLETCONNECT_PROJECT_ID=your_project_id_here
export SECRET_KEY=your_secret_key_here

# Run backend
cd src
python main.py
```

### 3. Frontend Setup
```bash
# Install dependencies
cd lastwish-frontend
npm install

# Set environment variables
echo "REACT_APP_WALLETCONNECT_PROJECT_ID=your_project_id_here" > .env

# Run frontend
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

## 📁 Project Structure

```
lastwish-eth/
├── src/                          # Flask Backend
│   ├── main.py                   # Main Flask application
│   ├── models/                   # Database models
│   │   ├── user.py              # User model with Web3 integration
│   │   ├── estate_models.py     # Estate planning models
│   │   └── subscription_models.py # Subscription and payment models
│   ├── routes/                   # API routes
│   │   ├── web3_auth.py         # Web3 authentication
│   │   ├── estate_planning.py   # Estate planning APIs
│   │   ├── nlweb_routes.py      # AI integration
│   │   └── subscription_routes.py # Subscription management
│   ├── utils/                    # Utility functions
│   │   ├── nlweb_integration.py # NLWeb AI integration
│   │   └── blockchain_integration.py # Blockchain utilities
│   └── static/                   # Built React frontend
├── lastwish-frontend/            # React Frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── WalletConnect.jsx # Wallet connection
│   │   │   ├── Dashboard.jsx    # Main dashboard
│   │   │   ├── WillCreationWizard.jsx # Will creation
│   │   │   ├── AssetManager.jsx # Asset management
│   │   │   ├── CryptoAssetManager.jsx # Crypto assets
│   │   │   └── BeneficiaryManager.jsx # Beneficiaries
│   │   ├── lib/
│   │   │   └── api.js           # API utilities
│   │   └── App.jsx              # Main React app
│   ├── public/
│   │   └── index.html           # HTML with WalletConnect SDK
│   └── package.json             # Frontend dependencies
├── docs/                         # Documentation
│   ├── WALLETCONNECT_SETUP.md   # WalletConnect setup guide
│   ├── API_DOCUMENTATION.md     # API documentation
│   └── DEPLOYMENT_GUIDE.md      # Deployment instructions
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///lastwish_web3.db

# WalletConnect
WALLETCONNECT_PROJECT_ID=your_project_id_here

# Blockchain RPC URLs (Optional)
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
POLYGON_RPC_URL=https://polygon-rpc.com/
BSC_RPC_URL=https://bsc-dataseed.binance.org/
AVALANCHE_RPC_URL=https://api.avax.network/ext/bc/C/rpc

# NLWeb Integration
NLWEB_API_KEY=your_nlweb_api_key_here
NLWEB_API_BASE=your_nlweb_api_base_url
```

#### Frontend (.env)
```bash
# WalletConnect
REACT_APP_WALLETCONNECT_PROJECT_ID=your_project_id_here

# API Base URL
REACT_APP_API_BASE_URL=http://localhost:5000

# Optional: Custom RPC endpoints
REACT_APP_ETHEREUM_RPC=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
REACT_APP_POLYGON_RPC=https://polygon-rpc.com/
REACT_APP_BSC_RPC=https://bsc-dataseed.binance.org/
REACT_APP_AVALANCHE_RPC=https://api.avax.network/ext/bc/C/rpc
```

## 🔐 WalletConnect Setup

1. **Register Application**: Go to [WalletConnect Cloud](https://cloud.walletconnect.com/)
2. **Create Project**: Set up "LastWish.eth" project
3. **Get Project ID**: Copy your unique project identifier
4. **Configure Environment**: Set `WALLETCONNECT_PROJECT_ID` in both frontend and backend
5. **Test Integration**: Verify wallet connections work properly

See [WALLETCONNECT_SETUP.md](./WALLETCONNECT_SETUP.md) for detailed instructions.

## 🤖 NLWeb AI Integration

The platform integrates with Microsoft's NLWeb package for AI-powered estate planning assistance:

- **Estate Analysis**: AI-powered portfolio completeness scoring
- **Document Generation**: Automated will and legal document creation
- **Legal Compliance**: Jurisdiction-specific compliance checking
- **Smart Recommendations**: Personalized estate planning guidance

Configure your local NLWeb package by setting the appropriate environment variables.

## 💰 Subscription Tiers

| Feature | Free | Basic ($9/mo) | Premium ($29/mo) | Enterprise ($99/mo) |
|---------|------|---------------|------------------|---------------------|
| Wills | 1 | 3 | 10 | Unlimited |
| Traditional Assets | 5 | 25 | 100 | Unlimited |
| Crypto Assets | 3 | 15 | 50 | Unlimited |
| Beneficiaries | 3 | 10 | 25 | Unlimited |
| AI Assistance | ❌ | ✅ | ✅ | ✅ |
| Smart Contracts | ❌ | ✅ | ✅ | ✅ |
| Priority Support | ❌ | ❌ | ✅ | ✅ |
| Legal Review | ❌ | ❌ | ✅ | ✅ |
| API Access | ❌ | ❌ | ❌ | ✅ |
| Custom Branding | ❌ | ❌ | ❌ | ✅ |

## 🚀 Deployment

### Production Deployment
1. **Build Frontend**: `npm run build` in `lastwish-frontend/`
2. **Copy Static Files**: Copy `dist/*` to `src/static/`
3. **Set Environment Variables**: Configure production environment
4. **Deploy Backend**: Deploy Flask application to your hosting provider
5. **Configure Domain**: Set up lastwish.eth ENS domain

### Docker Deployment (Optional)
```bash
# Build and run with Docker
docker build -t lastwish-eth .
docker run -p 5000:5000 -e WALLETCONNECT_PROJECT_ID=your_id lastwish-eth
```

### IPFS/Decentralized Deployment
The platform is designed for decentralized deployment:
- Frontend can be deployed to IPFS
- Backend can run on decentralized infrastructure
- ENS domain integration for censorship resistance

## 🧪 Testing

### Backend Tests
```bash
cd src
python -m pytest tests/
```

### Frontend Tests
```bash
cd lastwish-frontend
npm test
```

### Integration Tests
```bash
# Test wallet connections
npm run test:wallet

# Test estate planning workflows
npm run test:estate

# Test subscription features
npm run test:subscription
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/wallet-connect` - Connect Web3 wallet
- `POST /api/auth/resolve-ens` - Resolve ENS domain
- `GET /api/auth/status` - Check authentication status
- `POST /api/auth/disconnect` - Disconnect wallet

### Estate Planning Endpoints
- `GET /api/estate/dashboard` - Get estate planning dashboard
- `POST /api/estate/wills` - Create new will
- `GET /api/estate/assets` - Get user assets
- `POST /api/estate/assets` - Add new asset
- `GET /api/estate/beneficiaries` - Get beneficiaries
- `POST /api/estate/beneficiaries` - Add beneficiary

### Subscription Endpoints
- `GET /api/subscription/current` - Get current subscription
- `POST /api/subscription/upgrade` - Upgrade subscription
- `GET /api/subscription/usage` - Get usage statistics

See [API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md) for complete API reference.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Write tests for new features
- Update documentation for API changes
- Ensure mobile responsiveness for UI changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Live Demo**: [https://zmhqivcvngem.manus.space](https://zmhqivcvngem.manus.space)
- **Documentation**: [docs/](./docs/)
- **WalletConnect Cloud**: [https://cloud.walletconnect.com/](https://cloud.walletconnect.com/)
- **ENS Domains**: [https://ens.domains/](https://ens.domains/)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/lastwish-eth/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/lastwish-eth/discussions)
- **Email**: support@lastwish.eth

## 🙏 Acknowledgments

- **WalletConnect** for Web3 wallet integration
- **Microsoft NLWeb** for AI-powered assistance
- **Ethereum Foundation** for blockchain infrastructure
- **React Team** for the frontend framework
- **Flask Team** for the backend framework

---

**Built with ❤️ for the Web3 community**

*Secure your digital legacy with LastWish.eth - The future of estate planning is here.*

