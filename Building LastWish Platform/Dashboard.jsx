import React, { useState } from 'react';
import { FileText, Users, DollarSign, Shield, Plus, TrendingUp, Clock, CheckCircle, AlertTriangle, Bitcoin } from 'lucide-react';
import WillCreationWizard from '../wills/WillCreationWizard';
import AssetManager from '../assets/AssetManager';
import BeneficiaryManager from '../beneficiaries/BeneficiaryManager';
import CryptoWalletManager from '../crypto/CryptoWalletManager';
import CryptoAssetPortfolio from '../crypto/CryptoAssetPortfolio';

const Dashboard = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [showWillWizard, setShowWillWizard] = useState(false);

  const renderContent = () => {
    switch (activeSection) {
      case 'wills':
        return <div className="p-6"><h2 className="text-2xl font-bold text-white">Wills Management</h2></div>;
      case 'assets':
        return <AssetManager />;
      case 'beneficiaries':
        return <BeneficiaryManager />;
      case 'crypto-wallets':
        return <CryptoWalletManager />;
      case 'crypto-portfolio':
        return <CryptoAssetPortfolio />;
      default:
        return (
          <div className="p-6 space-y-6">
            {/* Welcome Section */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
              <h2 className="text-2xl font-bold mb-2">Welcome to LastWish</h2>
              <p className="text-blue-100 mb-4">
                Secure your legacy with our comprehensive estate planning platform
              </p>
              <button
                onClick={() => setShowWillWizard(true)}
                className="bg-white text-blue-600 px-6 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors"
              >
                Start Your Will
              </button>
            </div>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-blue-600/20 rounded-lg">
                    <FileText className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Wills Created</p>
                    <p className="text-2xl font-bold text-white">1</p>
                  </div>
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-green-600/20 rounded-lg">
                    <DollarSign className="w-6 h-6 text-green-400" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Total Assets</p>
                    <p className="text-2xl font-bold text-white">$125,450</p>
                  </div>
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-purple-600/20 rounded-lg">
                    <Users className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Beneficiaries</p>
                    <p className="text-2xl font-bold text-white">3</p>
                  </div>
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-orange-600/20 rounded-lg">
                    <Bitcoin className="w-6 h-6 text-orange-400" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Crypto Value</p>
                    <p className="text-2xl font-bold text-white">$89,421</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h3 className="text-xl font-semibold text-white mb-4">Quick Actions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <button
                  onClick={() => setShowWillWizard(true)}
                  className="flex items-center gap-3 p-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="w-5 h-5" />
                  <span>Create Will</span>
                </button>
                
                <button
                  onClick={() => setActiveSection('assets')}
                  className="flex items-center gap-3 p-4 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <DollarSign className="w-5 h-5" />
                  <span>Add Assets</span>
                </button>
                
                <button
                  onClick={() => setActiveSection('beneficiaries')}
                  className="flex items-center gap-3 p-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                >
                  <Users className="w-5 h-5" />
                  <span>Manage Beneficiaries</span>
                </button>
                
                <button
                  onClick={() => setActiveSection('crypto-wallets')}
                  className="flex items-center gap-3 p-4 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
                >
                  <Bitcoin className="w-5 h-5" />
                  <span>Add Crypto Wallet</span>
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h3 className="text-xl font-semibold text-white mb-4">Recent Activity</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3 p-3 bg-gray-700 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <div className="flex-1">
                    <p className="text-white">Will document created successfully</p>
                    <p className="text-sm text-gray-400">2 hours ago</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3 p-3 bg-gray-700 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-blue-400" />
                  <div className="flex-1">
                    <p className="text-white">Bitcoin wallet added to portfolio</p>
                    <p className="text-sm text-gray-400">1 day ago</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3 p-3 bg-gray-700 rounded-lg">
                  <Users className="w-5 h-5 text-purple-400" />
                  <div className="flex-1">
                    <p className="text-white">Beneficiary Sarah Johnson added</p>
                    <p className="text-sm text-gray-400">3 days ago</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Progress Checklist */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h3 className="text-xl font-semibold text-white mb-4">Estate Planning Progress</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-white">Create your will document</span>
                </div>
                
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-white">Add beneficiaries</span>
                </div>
                
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-white">Document your assets</span>
                </div>
                
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-white">Set up crypto inheritance</span>
                </div>
                
                <div className="flex items-center gap-3">
                  <Clock className="w-5 h-5 text-yellow-400" />
                  <span className="text-gray-300">Review and finalize documents</span>
                </div>
                
                <div className="flex items-center gap-3">
                  <Clock className="w-5 h-5 text-yellow-400" />
                  <span className="text-gray-300">Set up digital asset transfers</span>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 border-r border-gray-700">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-white">LastWish</h1>
          <p className="text-gray-400 text-sm mt-1">Estate Planning</p>
        </div>
        
        <nav className="px-4 space-y-2">
          <button
            onClick={() => setActiveSection('overview')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
              activeSection === 'overview' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            <Shield className="w-5 h-5" />
            <span>Overview</span>
          </button>
          
          <button
            onClick={() => setActiveSection('wills')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
              activeSection === 'wills' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            <FileText className="w-5 h-5" />
            <span>Wills</span>
          </button>
          
          <button
            onClick={() => setActiveSection('assets')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
              activeSection === 'assets' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            <DollarSign className="w-5 h-5" />
            <span>Assets</span>
          </button>
          
          <button
            onClick={() => setActiveSection('beneficiaries')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
              activeSection === 'beneficiaries' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            <Users className="w-5 h-5" />
            <span>Beneficiaries</span>
          </button>

          {/* Crypto Section */}
          <div className="pt-4">
            <div className="px-4 py-2">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Cryptocurrency</h3>
            </div>
            
            <button
              onClick={() => setActiveSection('crypto-wallets')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeSection === 'crypto-wallets' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              <Bitcoin className="w-5 h-5" />
              <span>Wallets</span>
            </button>
            
            <button
              onClick={() => setActiveSection('crypto-portfolio')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeSection === 'crypto-portfolio' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              <TrendingUp className="w-5 h-5" />
              <span>Portfolio</span>
            </button>
          </div>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        {renderContent()}
      </div>

      {/* Will Creation Wizard Modal */}
      {showWillWizard && (
        <WillCreationWizard
          onComplete={() => setShowWillWizard(false)}
          onCancel={() => setShowWillWizard(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
