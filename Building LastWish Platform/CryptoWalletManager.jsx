import React, { useState, useEffect } from 'react';
import { Plus, Wallet, TrendingUp, Shield, AlertTriangle, Eye, EyeOff, Copy, ExternalLink } from 'lucide-react';

const CryptoWalletManager = () => {
  const [wallets, setWallets] = useState([]);
  const [showAddWallet, setShowAddWallet] = useState(false);
  const [selectedWallet, setSelectedWallet] = useState(null);
  const [showPrivateInfo, setShowPrivateInfo] = useState({});
  const [loading, setLoading] = useState(true);

  // Mock data for demonstration
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setWallets([
        {
          id: 1,
          wallet_name: "Main Bitcoin Wallet",
          wallet_type: "hardware",
          blockchain_network: "bitcoin",
          wallet_address: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
          estimated_total_value: 45250.75,
          asset_count: 3,
          inheritance_status: "configured",
          last_balance_update: "2025-01-18T10:30:00Z"
        },
        {
          id: 2,
          wallet_name: "Ethereum DeFi Portfolio",
          wallet_type: "software",
          blockchain_network: "ethereum",
          wallet_address: "0x742d35Cc6634C0532925a3b8D4C2C3c8b4C2C3c8",
          estimated_total_value: 28750.50,
          asset_count: 12,
          inheritance_status: "in_progress",
          last_balance_update: "2025-01-18T09:15:00Z"
        },
        {
          id: 3,
          wallet_name: "Coinbase Pro Account",
          wallet_type: "custodial",
          blockchain_network: "ethereum",
          wallet_address: "coinbase_account_123",
          estimated_total_value: 15420.25,
          asset_count: 8,
          inheritance_status: "not_planned",
          last_balance_update: "2025-01-18T08:45:00Z"
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getWalletTypeIcon = (type) => {
    switch (type) {
      case 'hardware': return '🔒';
      case 'software': return '💻';
      case 'custodial': return '🏦';
      case 'multisig': return '👥';
      default: return '💼';
    }
  };

  const getNetworkIcon = (network) => {
    switch (network) {
      case 'bitcoin': return '₿';
      case 'ethereum': return 'Ξ';
      case 'binance_smart_chain': return '🟡';
      case 'polygon': return '🟣';
      default: return '🔗';
    }
  };

  const getInheritanceStatusColor = (status) => {
    switch (status) {
      case 'configured': return 'text-green-400 bg-green-400/10';
      case 'in_progress': return 'text-yellow-400 bg-yellow-400/10';
      case 'active': return 'text-blue-400 bg-blue-400/10';
      case 'not_planned': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  const formatAddress = (address) => {
    if (address.length > 20) {
      return `${address.slice(0, 8)}...${address.slice(-8)}`;
    }
    return address;
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  const togglePrivateInfo = (walletId) => {
    setShowPrivateInfo(prev => ({
      ...prev,
      [walletId]: !prev[walletId]
    }));
  };

  const AddWalletForm = () => {
    const [formData, setFormData] = useState({
      wallet_name: '',
      wallet_type: 'software',
      blockchain_network: 'ethereum',
      wallet_address: '',
      wallet_description: ''
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      // Add wallet logic here
      console.log('Adding wallet:', formData);
      setShowAddWallet(false);
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-gray-900 rounded-xl p-6 w-full max-w-md mx-4 border border-gray-700">
          <h3 className="text-xl font-bold text-white mb-4">Add New Wallet</h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Wallet Name
              </label>
              <input
                type="text"
                value={formData.wallet_name}
                onChange={(e) => setFormData({...formData, wallet_name: e.target.value})}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                placeholder="My Bitcoin Wallet"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Wallet Type
              </label>
              <select
                value={formData.wallet_type}
                onChange={(e) => setFormData({...formData, wallet_type: e.target.value})}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                <option value="software">Software Wallet</option>
                <option value="hardware">Hardware Wallet</option>
                <option value="custodial">Custodial (Exchange)</option>
                <option value="multisig">Multi-Signature</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Blockchain Network
              </label>
              <select
                value={formData.blockchain_network}
                onChange={(e) => setFormData({...formData, blockchain_network: e.target.value})}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                <option value="bitcoin">Bitcoin</option>
                <option value="ethereum">Ethereum</option>
                <option value="binance_smart_chain">Binance Smart Chain</option>
                <option value="polygon">Polygon</option>
                <option value="avalanche">Avalanche</option>
                <option value="solana">Solana</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Wallet Address
              </label>
              <input
                type="text"
                value={formData.wallet_address}
                onChange={(e) => setFormData({...formData, wallet_address: e.target.value})}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                placeholder="0x742d35Cc6634C0532925a3b8D4C2C3c8b4C2C3c8"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Description (Optional)
              </label>
              <textarea
                value={formData.wallet_description}
                onChange={(e) => setFormData({...formData, wallet_description: e.target.value})}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                rows="3"
                placeholder="Additional notes about this wallet..."
              />
            </div>

            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={() => setShowAddWallet(false)}
                className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add Wallet
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-700 rounded w-1/3"></div>
          <div className="grid gap-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-gray-800 rounded-xl"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Crypto Wallets</h2>
          <p className="text-gray-400 mt-1">
            Manage your cryptocurrency wallets and digital assets
          </p>
        </div>
        <button
          onClick={() => setShowAddWallet(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Wallet
        </button>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600/20 rounded-lg">
              <Wallet className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Wallets</p>
              <p className="text-xl font-bold text-white">{wallets.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-600/20 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Value</p>
              <p className="text-xl font-bold text-white">
                ${wallets.reduce((sum, wallet) => sum + wallet.estimated_total_value, 0).toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-600/20 rounded-lg">
              <Shield className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Protected</p>
              <p className="text-xl font-bold text-white">
                {wallets.filter(w => w.inheritance_status !== 'not_planned').length}/{wallets.length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-yellow-600/20 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-yellow-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Needs Setup</p>
              <p className="text-xl font-bold text-white">
                {wallets.filter(w => w.inheritance_status === 'not_planned').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Wallets List */}
      <div className="space-y-4">
        {wallets.map((wallet) => (
          <div
            key={wallet.id}
            className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-gray-700 rounded-xl text-2xl">
                  {getWalletTypeIcon(wallet.wallet_type)}
                </div>
                
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-white">
                      {wallet.wallet_name}
                    </h3>
                    <span className="text-2xl">{getNetworkIcon(wallet.blockchain_network)}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getInheritanceStatusColor(wallet.inheritance_status)}`}>
                      {wallet.inheritance_status.replace('_', ' ')}
                    </span>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-400">Address:</span>
                      <code className="text-sm text-gray-300 bg-gray-900 px-2 py-1 rounded">
                        {showPrivateInfo[wallet.id] ? wallet.wallet_address : formatAddress(wallet.wallet_address)}
                      </code>
                      <button
                        onClick={() => togglePrivateInfo(wallet.id)}
                        className="p-1 text-gray-400 hover:text-white transition-colors"
                      >
                        {showPrivateInfo[wallet.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                      <button
                        onClick={() => copyToClipboard(wallet.wallet_address)}
                        className="p-1 text-gray-400 hover:text-white transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-white transition-colors">
                        <ExternalLink className="w-4 h-4" />
                      </button>
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>Type: {wallet.wallet_type.replace('_', ' ')}</span>
                      <span>•</span>
                      <span>Assets: {wallet.asset_count}</span>
                      <span>•</span>
                      <span>Updated: {new Date(wallet.last_balance_update).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="text-right">
                <div className="text-2xl font-bold text-white mb-1">
                  ${wallet.estimated_total_value.toLocaleString()}
                </div>
                <div className="text-sm text-gray-400">
                  Portfolio Value
                </div>
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-700">
              <div className="flex gap-3">
                <button
                  onClick={() => setSelectedWallet(wallet)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                >
                  View Assets
                </button>
                <button className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm">
                  Manage Inheritance
                </button>
                <button className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm">
                  Settings
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add Wallet Modal */}
      {showAddWallet && <AddWalletForm />}
    </div>
  );
};

export default CryptoWalletManager;

