import React from 'react'
import { Shield, Wallet, FileText, Users, Zap, Globe, ArrowRight, Check } from 'lucide-react'

const LandingPage = ({ onGetStarted, onDemo }) => {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-black/50 backdrop-blur-sm fixed w-full z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Shield className="h-8 w-8 text-blue-500" />
              <span className="text-xl font-bold">LastWish.eth</span>
            </div>
            <div className="flex items-center space-x-4">
              <button 
                onClick={onDemo}
                className="text-gray-300 hover:text-white transition-colors"
              >
                Demo
              </button>
              <button 
                onClick={onGetStarted}
                className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
              >
                Connect Wallet
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <div className="mb-8">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-900/30 text-blue-300 border border-blue-800">
              <Globe className="w-4 h-4 mr-2" />
              Powered by Web3 & Blockchain Technology
            </span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-blue-100 to-blue-300 bg-clip-text text-transparent">
            Secure Your
            <br />
            Digital Legacy
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
            The world's first Web3-native estate planning platform. Manage traditional assets, 
            cryptocurrency, NFTs, and smart contracts all in one secure, decentralized platform.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button 
              onClick={onGetStarted}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105 flex items-center"
            >
              <Wallet className="w-5 h-5 mr-2" />
              Connect Wallet & Start
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <button 
              onClick={onDemo}
              className="border border-gray-600 hover:border-gray-500 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all hover:bg-gray-900"
            >
              View Demo
            </button>
          </div>
          
          <div className="mt-12 text-sm text-gray-400">
            <p>✓ No credit card required • ✓ Connect with any Web3 wallet • ✓ Decentralized & secure</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-gray-900/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Complete Estate Planning for the Digital Age</h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Manage all your assets - traditional and digital - with cutting-edge blockchain technology 
              and AI-powered automation.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Digital Wills */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-blue-500 transition-all">
              <FileText className="w-12 h-12 text-blue-500 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Smart Contract Wills</h3>
              <p className="text-gray-300 mb-4">
                Create legally compliant digital wills with automated execution through smart contracts. 
                No lawyers required.
              </p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ Multi-jurisdiction compliance</li>
                <li>✓ Automated execution</li>
                <li>✓ Immutable blockchain storage</li>
              </ul>
            </div>

            {/* Crypto Assets */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-blue-500 transition-all">
              <Wallet className="w-12 h-12 text-green-500 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Multi-Chain Crypto Management</h3>
              <p className="text-gray-300 mb-4">
                Manage cryptocurrency, NFTs, and DeFi positions across Ethereum, Polygon, BSC, and Avalanche.
              </p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ Multi-wallet support</li>
                <li>✓ NFT inheritance planning</li>
                <li>✓ DeFi position tracking</li>
              </ul>
            </div>

            {/* Beneficiary Management */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-blue-500 transition-all">
              <Users className="w-12 h-12 text-purple-500 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Smart Beneficiary System</h3>
              <p className="text-gray-300 mb-4">
                Automated beneficiary notifications and inheritance distribution with Web3 wallet integration.
              </p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ ENS domain support</li>
                <li>✓ Automated notifications</li>
                <li>✓ Guardian management</li>
              </ul>
            </div>

            {/* AI Automation */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-blue-500 transition-all">
              <Zap className="w-12 h-12 text-yellow-500 mb-4" />
              <h3 className="text-xl font-semibold mb-3">AI-Powered Automation</h3>
              <p className="text-gray-300 mb-4">
                Advanced AI workflows handle document generation, legal compliance, and asset monitoring automatically.
              </p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ Document generation</li>
                <li>✓ Legal compliance monitoring</li>
                <li>✓ Asset valuation tracking</li>
              </ul>
            </div>

            {/* Security */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-blue-500 transition-all">
              <Shield className="w-12 h-12 text-red-500 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Bank-Level Security</h3>
              <p className="text-gray-300 mb-4">
                Enterprise-grade security with decentralized storage, encryption, and multi-signature protection.
              </p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ End-to-end encryption</li>
                <li>✓ IPFS decentralized storage</li>
                <li>✓ Multi-signature wallets</li>
              </ul>
            </div>

            {/* Decentralized */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-blue-500 transition-all">
              <Globe className="w-12 h-12 text-cyan-500 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Fully Decentralized</h3>
              <p className="text-gray-300 mb-4">
                Built on IPFS and blockchain technology. Your data is truly yours, stored across a decentralized network.
              </p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ IPFS storage</li>
                <li>✓ ENS domain integration</li>
                <li>✓ Censorship resistant</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Choose Your Plan</h2>
            <p className="text-xl text-gray-300">Start free, upgrade as your estate grows</p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Free Tier */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700">
              <h3 className="text-xl font-semibold mb-2">Free</h3>
              <div className="text-3xl font-bold mb-4">$0<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />1 Will</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />5 Traditional Assets</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />3 Crypto Assets</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />3 Beneficiaries</li>
              </ul>
              <button 
                onClick={onGetStarted}
                className="w-full border border-gray-600 hover:border-gray-500 text-white py-3 rounded-lg transition-all"
              >
                Get Started Free
              </button>
            </div>

            {/* Basic Tier */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700">
              <h3 className="text-xl font-semibold mb-2">Basic</h3>
              <div className="text-3xl font-bold mb-4">$9<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />3 Wills</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />25 Traditional Assets</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />15 Crypto Assets</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />10 Beneficiaries</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />Smart Contracts</li>
              </ul>
              <button 
                onClick={onGetStarted}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg transition-all"
              >
                Start Basic Plan
              </button>
            </div>

            {/* Premium Tier */}
            <div className="bg-gradient-to-b from-blue-900/50 to-gray-800/50 p-8 rounded-xl border border-blue-500 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm">Most Popular</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Premium</h3>
              <div className="text-3xl font-bold mb-4">$29<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />10 Wills</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />100 Traditional Assets</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />50 Crypto Assets</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />25 Beneficiaries</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />Advanced Features</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />Priority Support</li>
              </ul>
              <button 
                onClick={onGetStarted}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg transition-all"
              >
                Start Premium Plan
              </button>
            </div>

            {/* Enterprise Tier */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700">
              <h3 className="text-xl font-semibold mb-2">Enterprise</h3>
              <div className="text-3xl font-bold mb-4">$99<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />Unlimited Everything</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />White-label Options</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />API Access</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />Custom Integrations</li>
                <li className="flex items-center"><Check className="w-4 h-4 text-green-500 mr-2" />Dedicated Support</li>
              </ul>
              <button 
                onClick={onGetStarted}
                className="w-full border border-gray-600 hover:border-gray-500 text-white py-3 rounded-lg transition-all"
              >
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-900/20 to-purple-900/20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Secure Your Digital Legacy?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of users who trust LastWish.eth with their most important assets. 
            Start with our free plan and upgrade as your estate grows.
          </p>
          <button 
            onClick={onGetStarted}
            className="bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 rounded-lg text-xl font-semibold transition-all transform hover:scale-105 flex items-center mx-auto"
          >
            <Wallet className="w-6 h-6 mr-3" />
            Connect Your Wallet Now
            <ArrowRight className="w-6 h-6 ml-3" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Shield className="h-6 w-6 text-blue-500" />
              <span className="text-lg font-semibold">LastWish.eth</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2024 LastWish. Securing digital legacies on the blockchain.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

