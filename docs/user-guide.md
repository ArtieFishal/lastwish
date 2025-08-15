# LastWish.eth User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Wallet Setup](#wallet-setup)
3. [Creating Your Digital Will](#creating-your-digital-will)
4. [Managing Assets](#managing-assets)
5. [Beneficiary Management](#beneficiary-management)
6. [Payment Process](#payment-process)
7. [Generating Your Will](#generating-your-will)
8. [Security Best Practices](#security-best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Legal Considerations](#legal-considerations)

## Getting Started

LastWish.eth is a decentralized platform that helps you create legally binding digital wills for your cryptocurrency and NFT assets. This guide will walk you through the entire process of creating your digital will.

### Prerequisites

Before you begin, ensure you have:
- A Web3-compatible browser (Chrome, Firefox, Safari, Edge)
- A cryptocurrency wallet (MetaMask, Coinbase Wallet, etc.)
- Some ETH for transaction fees
- Your digital assets on Ethereum mainnet

### First Visit

When you first visit LastWish.eth, you'll see the main interface with several sections:
- **Owner Information**: Your personal details
- **Additional Wallets**: Multiple wallet management
- **Wallet Connection**: Web3 wallet integration
- **Assets & Assignments**: Your digital asset portfolio
- **Beneficiaries**: People who will inherit your assets
- **Payment**: Platform fee processing
- **Generate & Print**: Final will creation

## Wallet Setup

### Supported Wallets

LastWish.eth supports all major Ethereum wallets:
- **MetaMask**: Most popular browser extension wallet
- **Coinbase Wallet**: User-friendly mobile and browser wallet
- **WalletConnect**: Connect mobile wallets via QR code
- **Brave Wallet**: Built into Brave browser
- **Trust Wallet**: Mobile wallet with WalletConnect support

### Installing MetaMask

If you don't have a wallet, we recommend MetaMask:

1. Visit [metamask.io](https://metamask.io/)
2. Click "Download" and select your browser
3. Install the browser extension
4. Create a new wallet or import existing one
5. Secure your seed phrase (write it down safely!)
6. Add some ETH for transaction fees

### Network Configuration

Ensure your wallet is connected to Ethereum Mainnet:
1. Open your wallet
2. Click the network dropdown
3. Select "Ethereum Mainnet"
4. If not available, add it manually:
   - Network Name: Ethereum Mainnet
   - RPC URL: https://mainnet.infura.io/v3/YOUR_KEY
   - Chain ID: 1
   - Currency Symbol: ETH
   - Block Explorer: https://etherscan.io

## Creating Your Digital Will

### Step 1: Connect Your Wallet

1. Click the "Connect" button in the Wallet section
2. Select your preferred wallet from the popup
3. Approve the connection request in your wallet
4. Your wallet address will appear in the interface

### Step 2: Sign Session

1. Click "Sign Session" after connecting
2. Sign the message in your wallet (this is free)
3. This creates a secure session for the platform
4. Your session status will show as "Signed"

### Step 3: Enter Owner Information

Fill out your personal details:

**Full Legal Name**
- Enter your complete legal name as it appears on official documents
- This will be used in the legal will document
- Ensure spelling is correct and matches your ID

**Primary Wallet Address**
- This is automatically filled from your connected wallet
- This is your main wallet that will be included in the will
- Cannot be edited (determined by your connected wallet)

**Special Instructions (Optional)**
- Add any specific instructions for your executor
- Include details about asset management preferences
- Mention any special circumstances or wishes
- Keep it clear and legally appropriate

Example special instructions:
```
"Please distribute my NFT collection to my children equally. 
My DeFi positions should be liquidated and converted to stablecoins 
before distribution. Contact my lawyer John Smith at (555) 123-4567 
for assistance with the legal process."
```

## Managing Assets

### Adding Additional Wallets

You can include up to 20 wallet addresses in your will:

1. **Enter Wallet Address or ENS**
   - Type a wallet address (0x...) or ENS name (alice.eth)
   - The platform will validate the format
   - ENS names are automatically resolved to addresses

2. **Click "Add Wallet"**
   - The wallet is added to your list
   - ENS names show both the name and resolved address
   - You can remove wallets using the "Remove" button

3. **Wallet Validation**
   - Addresses are checked for proper format
   - Duplicate addresses are prevented
   - ENS resolution is performed automatically

### Loading Your Assets

**Load Assets Button**
- Fetches real-time data from your connected wallet
- Shows ERC-20 tokens and NFTs
- Displays current balances and metadata
- May take a few moments to load

**Load Demo Data Button**
- Loads sample data for testing
- Useful for exploring the platform
- Shows example tokens and NFTs
- Does not affect your real assets

### Asset Types Supported

**ERC-20 Tokens**
- Standard cryptocurrency tokens
- Includes popular tokens like USDC, USDT, LINK
- Shows token name, symbol, and balance
- Displays current USD value when available

**NFTs (Non-Fungible Tokens)**
- ERC-721 and ERC-1155 tokens
- Includes art, collectibles, gaming items
- Shows collection name and token ID
- Displays metadata and images when available

### Asset Assignment

For each asset, you can assign percentages to beneficiaries:

1. **Select Beneficiary**
   - Choose from your added beneficiaries
   - Use the dropdown menu for each asset
   - Multiple beneficiaries can share one asset

2. **Set Percentage**
   - Enter percentage (1-100%)
   - Total percentages per asset should equal 100%
   - Remaining percentage shows unassigned portion

3. **Save Assignments**
   - Click "Save Assignments" to store your choices
   - Assignments are saved locally in your browser
   - You can modify assignments anytime before payment

## Beneficiary Management

### Adding Beneficiaries

**Required Information:**
- **Name**: Full legal name of the beneficiary
- **Wallet or ENS (Optional)**: Their Ethereum address or ENS name
- **Email (Optional)**: Contact email for notifications
- **Relationship (Optional)**: Your relationship to them

**Best Practices:**
- Use full legal names for clarity
- Include contact information when possible
- Specify relationships for legal clarity
- Add backup beneficiaries if desired

### Beneficiary Examples

**Family Member:**
```
Name: Sarah Johnson
Wallet: sarah.eth
Email: sarah@email.com
Relationship: Daughter
```

**Friend:**
```
Name: Michael Chen
Wallet: 0x1234567890123456789012345678901234567890
Email: mike@email.com
Relationship: Close Friend
```

**Charity:**
```
Name: Electronic Frontier Foundation
Wallet: 0xb189f76323678E094D4996d182A792E52369c005
Email: donations@eff.org
Relationship: Charitable Organization
```

### Managing Beneficiaries

- **Edit**: Click the edit button to modify beneficiary details
- **Remove**: Use the remove button to delete beneficiaries
- **Reorder**: Beneficiaries appear in the order you add them
- **Validation**: Email addresses and wallet addresses are validated

## Payment Process

### Platform Fee

LastWish.eth charges a small fee to cover platform costs:
- **Standard Fee**: 0.0001 ETH
- **ENS Discount**: 20% off for ENS holders
- **Payment Method**: Direct Ethereum transaction

### ENS Discount Eligibility

If your connected wallet owns an ENS name, you automatically receive a 20% discount:
- Discount is applied automatically
- Original price shows with strikethrough
- Final price is displayed prominently
- No additional steps required

### Payment Process

1. **Review Fee**
   - Check the payment amount
   - Verify discount application if applicable
   - Ensure you have sufficient ETH for gas fees

2. **Click "Pay"**
   - Initiates the payment transaction
   - Your wallet will prompt for confirmation
   - Review transaction details carefully

3. **Confirm Transaction**
   - Approve the transaction in your wallet
   - Wait for blockchain confirmation
   - Transaction hash will be displayed

4. **Payment Confirmation**
   - Success message appears when confirmed
   - Transaction details are saved
   - You can now generate your will

### Transaction Fees

In addition to the platform fee, you'll pay Ethereum gas fees:
- **Gas fees vary** based on network congestion
- **Typical range**: $5-50 USD equivalent
- **Check gas tracker** websites for current rates
- **Consider timing** your transaction during low-traffic periods

## Generating Your Will

### Prerequisites for Generation

Before generating your will, ensure:
- ✅ Owner information is complete
- ✅ At least one beneficiary is added
- ✅ Assets are loaded and assigned
- ✅ Payment is completed successfully
- ✅ All information is reviewed for accuracy

### Generation Process

1. **Click "Generate & Print"**
   - Compiles all your information
   - Creates a formatted legal document
   - Processes asset assignments
   - Generates PDF for download

2. **Review Generated Will**
   - Check all personal information
   - Verify beneficiary details
   - Confirm asset assignments
   - Review special instructions

3. **Download and Save**
   - Save multiple copies of the PDF
   - Store in secure locations
   - Consider cloud backup
   - Print physical copies

### Will Document Contents

Your generated will includes:
- **Personal Information**: Your legal name and details
- **Asset Inventory**: Complete list of digital assets
- **Beneficiary Information**: All designated recipients
- **Asset Assignments**: Specific percentage allocations
- **Special Instructions**: Your custom directives
- **Legal Language**: Proper will formatting and clauses
- **Execution Instructions**: Guidance for executors

## Security Best Practices

### Wallet Security

**Seed Phrase Protection:**
- Never share your seed phrase with anyone
- Store it offline in multiple secure locations
- Consider using a hardware wallet for large amounts
- Use a password manager for additional security

**Transaction Verification:**
- Always verify transaction details before signing
- Check recipient addresses carefully
- Confirm amounts and gas fees
- Be cautious of phishing attempts

### Platform Security

**Session Management:**
- Sign sessions only on the official website
- Log out when finished using the platform
- Clear browser data if using a public computer
- Monitor for suspicious activity

**Data Protection:**
- Your data is stored locally in your browser
- Clear browser data to remove information
- Use private browsing for additional privacy
- Keep your browser updated

### Legal Security

**Document Storage:**
- Store will documents in multiple secure locations
- Inform trusted parties of document locations
- Consider using a safe deposit box
- Keep digital and physical copies

**Regular Updates:**
- Review your will annually
- Update after major life changes
- Modify beneficiaries as needed
- Adjust asset assignments for new holdings

## Troubleshooting

### Common Connection Issues

**Wallet Won't Connect:**
- Refresh the page and try again
- Check if wallet is unlocked
- Ensure you're on Ethereum Mainnet
- Try a different browser or wallet

**Transaction Fails:**
- Check if you have enough ETH for gas
- Increase gas limit if needed
- Wait for network congestion to decrease
- Try again with higher gas price

### Asset Loading Problems

**Assets Don't Appear:**
- Ensure wallet contains ERC-20 tokens or NFTs
- Check if you're on the correct network
- Try the "Load Demo Data" button to test
- Refresh the page and reconnect wallet

**Slow Loading:**
- Network congestion can cause delays
- Wait a few minutes and try again
- Check your internet connection
- Try during off-peak hours

### Payment Issues

**Payment Button Disabled:**
- Ensure wallet is connected and signed
- Check that you have sufficient ETH
- Verify you're on Ethereum Mainnet
- Try disconnecting and reconnecting wallet

**Transaction Pending:**
- Check transaction status on Etherscan
- Wait for network confirmation
- Consider increasing gas price for faster confirmation
- Contact support if stuck for hours

### Browser Compatibility

**Supported Browsers:**
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Brave

**Browser Issues:**
- Clear cache and cookies
- Disable ad blockers temporarily
- Try incognito/private mode
- Update browser to latest version

## Legal Considerations

### Will Validity

**Legal Requirements:**
- Consult with a local attorney
- Understand your jurisdiction's laws
- Consider notarization requirements
- Follow proper execution procedures

**State-Specific Laws:**
- Will requirements vary by location
- Some states have specific digital asset laws
- Witness requirements may apply
- Consider holographic will rules

### Estate Planning Integration

**Traditional Estate Planning:**
- Integrate with existing wills and trusts
- Coordinate with estate planning attorney
- Update beneficiary designations
- Consider tax implications

**Executor Responsibilities:**
- Choose technically capable executors
- Provide clear instructions for digital assets
- Include wallet access information
- Consider professional digital asset services

### Tax Implications

**Inheritance Taxes:**
- Digital assets may be subject to estate taxes
- Valuation can be complex for NFTs
- Consider gift tax implications
- Consult with tax professionals

**Record Keeping:**
- Maintain detailed asset records
- Document acquisition costs and dates
- Track transactions and transfers
- Keep tax-related documentation

### Disclaimer

LastWish.eth provides tools for creating digital wills but does not provide legal advice. The platform generates documents that may require additional legal review and proper execution according to your local laws. Always consult with qualified legal professionals for estate planning advice specific to your situation and jurisdiction.

---

For additional support, please visit our [GitHub repository](https://github.com/your-username/lastwish-eth) or contact our support team.

