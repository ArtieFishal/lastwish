import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, DollarSign, Percent, PieChart, BarChart3, Plus, Filter, Search, RefreshCw } from 'lucide-react';

const CryptoAssetPortfolio = () => {
  const [assets, setAssets] = useState([]);
  const [portfolioSummary, setPortfolioSummary] = useState(null);
  const [selectedAssetType, setSelectedAssetType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('value');
  const [loading, setLoading] = useState(true);

  // Mock data for demonstration
  useEffect(() => {
    setTimeout(() => {
      setAssets([
        {
          id: 1,
          asset_name: "Bitcoin",
          asset_symbol: "BTC",
          asset_type: "cryptocurrency",
          quantity: 1.25,
          current_price_usd: 42500.00,
          current_value_usd: 53125.00,
          purchase_price_usd: 38000.00,
          price_change_24h: 2.5,
          inheritance_percentage: 100,
          wallet_name: "Main Bitcoin Wallet",
          risk_level: "medium"
        },
        {
          id: 2,
          asset_name: "Ethereum",
          asset_symbol: "ETH",
          asset_type: "cryptocurrency",
          quantity: 8.5,
          current_price_usd: 2650.00,
          current_value_usd: 22525.00,
          purchase_price_usd: 2200.00,
          price_change_24h: -1.2,
          inheritance_percentage: 100,
          wallet_name: "Ethereum DeFi Portfolio",
          risk_level: "medium"
        },
        {
          id: 3,
          asset_name: "Bored Ape #1234",
          asset_symbol: "BAYC",
          asset_type: "nft",
          quantity: 1,
          current_price_usd: 15000.00,
          current_value_usd: 15000.00,
          purchase_price_usd: 25000.00,
          price_change_24h: 0.0,
          inheritance_percentage: 100,
          wallet_name: "Ethereum DeFi Portfolio",
          risk_level: "high"
        },
        {
          id: 4,
          asset_name: "Uniswap LP Token",
          asset_symbol: "UNI-V2",
          asset_type: "defi_position",
          quantity: 150.75,
          current_price_usd: 45.20,
          current_value_usd: 6813.90,
          purchase_price_usd: 42.00,
          price_change_24h: 1.8,
          inheritance_percentage: 75,
          wallet_name: "Ethereum DeFi Portfolio",
          risk_level: "high"
        },
        {
          id: 5,
          asset_name: "Chainlink",
          asset_symbol: "LINK",
          asset_type: "token",
          quantity: 500,
          current_price_usd: 14.25,
          current_value_usd: 7125.00,
          purchase_price_usd: 12.50,
          price_change_24h: 3.2,
          inheritance_percentage: 100,
          wallet_name: "Coinbase Pro Account",
          risk_level: "medium"
        }
      ]);

      setPortfolioSummary({
        total_value_usd: 104588.90,
        total_assets: 5,
        total_wallets: 3,
        price_change_24h: 1.8,
        inheritance_coverage: 95.2,
        asset_breakdown: {
          cryptocurrency: { count: 2, value: 75650.00 },
          nft: { count: 1, value: 15000.00 },
          token: { count: 1, value: 7125.00 },
          defi_position: { count: 1, value: 6813.90 }
        }
      });

      setLoading(false);
    }, 1000);
  }, []);

  const getAssetTypeIcon = (type) => {
    switch (type) {
      case 'cryptocurrency': return '₿';
      case 'nft': return '🎨';
      case 'token': return '🪙';
      case 'defi_position': return '🏦';
      case 'staking_reward': return '💰';
      default: return '💎';
    }
  };

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'low': return 'text-green-400 bg-green-400/10';
      case 'medium': return 'text-yellow-400 bg-yellow-400/10';
      case 'high': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  const filteredAssets = assets
    .filter(asset => {
      const matchesType = selectedAssetType === 'all' || asset.asset_type === selectedAssetType;
      const matchesSearch = asset.asset_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           asset.asset_symbol.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesType && matchesSearch;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'value': return b.current_value_usd - a.current_value_usd;
        case 'change': return b.price_change_24h - a.price_change_24h;
        case 'name': return a.asset_name.localeCompare(b.asset_name);
        default: return 0;
      }
    });

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-700 rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-24 bg-gray-800 rounded-xl"></div>
            ))}
          </div>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="h-20 bg-gray-800 rounded-xl"></div>
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
          <h2 className="text-2xl font-bold text-white">Crypto Portfolio</h2>
          <p className="text-gray-400 mt-1">
            Track and manage your digital asset investments
          </p>
        </div>
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <Plus className="w-4 h-4" />
            Add Asset
          </button>
        </div>
      </div>

      {/* Portfolio Summary Cards */}
      {portfolioSummary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600/20 rounded-lg">
                <DollarSign className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Total Value</p>
                <p className="text-xl font-bold text-white">
                  ${portfolioSummary.total_value_usd.toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg ${portfolioSummary.price_change_24h >= 0 ? 'bg-green-600/20' : 'bg-red-600/20'}`}>
                {portfolioSummary.price_change_24h >= 0 ? 
                  <TrendingUp className="w-5 h-5 text-green-400" /> : 
                  <TrendingDown className="w-5 h-5 text-red-400" />
                }
              </div>
              <div>
                <p className="text-sm text-gray-400">24h Change</p>
                <p className={`text-xl font-bold ${portfolioSummary.price_change_24h >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {portfolioSummary.price_change_24h >= 0 ? '+' : ''}{portfolioSummary.price_change_24h.toFixed(2)}%
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-600/20 rounded-lg">
                <PieChart className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Assets</p>
                <p className="text-xl font-bold text-white">{portfolioSummary.total_assets}</p>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-600/20 rounded-lg">
                <Percent className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Inheritance Coverage</p>
                <p className="text-xl font-bold text-white">{portfolioSummary.inheritance_coverage}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Asset Breakdown Chart */}
      {portfolioSummary && (
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4">Asset Allocation</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(portfolioSummary.asset_breakdown).map(([type, data]) => (
              <div key={type} className="text-center">
                <div className="text-3xl mb-2">{getAssetTypeIcon(type)}</div>
                <div className="text-sm text-gray-400 capitalize mb-1">
                  {type.replace('_', ' ')}
                </div>
                <div className="text-lg font-semibold text-white">
                  ${data.value.toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">
                  {data.count} asset{data.count !== 1 ? 's' : ''}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters and Search */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex items-center gap-2">
          <Search className="w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search assets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={selectedAssetType}
            onChange={(e) => setSelectedAssetType(e.target.value)}
            className="px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="all">All Types</option>
            <option value="cryptocurrency">Cryptocurrency</option>
            <option value="nft">NFTs</option>
            <option value="token">Tokens</option>
            <option value="defi_position">DeFi Positions</option>
            <option value="staking_reward">Staking Rewards</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-gray-400" />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="value">Sort by Value</option>
            <option value="change">Sort by Change</option>
            <option value="name">Sort by Name</option>
          </select>
        </div>
      </div>

      {/* Assets List */}
      <div className="space-y-3">
        {filteredAssets.map((asset) => (
          <div
            key={asset.id}
            className="bg-gray-800 rounded-xl p-4 border border-gray-700 hover:border-gray-600 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gray-700 rounded-xl text-2xl">
                  {getAssetTypeIcon(asset.asset_type)}
                </div>
                
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="text-lg font-semibold text-white">
                      {asset.asset_name}
                    </h3>
                    <span className="text-sm text-gray-400 uppercase font-mono">
                      {asset.asset_symbol}
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(asset.risk_level)}`}>
                      {asset.risk_level} risk
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm text-gray-400">
                    <span>Qty: {asset.quantity.toLocaleString()}</span>
                    <span>•</span>
                    <span>Price: ${asset.current_price_usd.toLocaleString()}</span>
                    <span>•</span>
                    <span>Wallet: {asset.wallet_name}</span>
                  </div>
                </div>
              </div>
              
              <div className="text-right">
                <div className="text-xl font-bold text-white mb-1">
                  ${asset.current_value_usd.toLocaleString()}
                </div>
                <div className={`text-sm font-medium ${asset.price_change_24h >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {asset.price_change_24h >= 0 ? '+' : ''}{asset.price_change_24h.toFixed(2)}%
                </div>
                <div className="text-xs text-gray-500">
                  Inheritance: {asset.inheritance_percentage}%
                </div>
              </div>
            </div>
            
            {/* Progress bar for inheritance percentage */}
            <div className="mt-3">
              <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
                <span>Inheritance Coverage</span>
                <span>{asset.inheritance_percentage}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${asset.inheritance_percentage}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredAssets.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-semibold text-white mb-2">No assets found</h3>
          <p className="text-gray-400">
            Try adjusting your search or filter criteria
          </p>
        </div>
      )}
    </div>
  );
};

export default CryptoAssetPortfolio;

