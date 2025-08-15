import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';

const SubscriptionManager = ({ isOpen, onClose, currentTier = 'free' }) => {
  const [tiers, setTiers] = useState([]);
  const [currentSubscription, setCurrentSubscription] = useState(null);
  const [selectedTier, setSelectedTier] = useState(null);
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [promoCode, setPromoCode] = useState('');
  const [promoValidation, setPromoValidation] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('stripe');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchSubscriptionData();
    }
  }, [isOpen]);

  const fetchSubscriptionData = async () => {
    try {
      setLoading(true);
      
      // Fetch subscription tiers
      const tiersResponse = await api.get('/subscription/tiers');
      setTiers(tiersResponse.data.tiers || []);
      
      // Fetch current subscription
      const currentResponse = await api.get('/subscription/current');
      setCurrentSubscription(currentResponse.data.subscription);
      
    } catch (error) {
      console.error('Failed to fetch subscription data:', error);
      setError('Failed to load subscription information');
    } finally {
      setLoading(false);
    }
  };

  const validatePromoCode = async () => {
    if (!promoCode.trim() || !selectedTier) return;
    
    try {
      const response = await api.post('/subscription/validate-promo', {
        promo_code: promoCode,
        tier_id: selectedTier.id,
        billing_cycle: billingCycle
      });
      
      setPromoValidation(response.data);
    } catch (error) {
      setPromoValidation({
        valid: false,
        error: error.response?.data?.error || 'Invalid promo code'
      });
    }
  };

  const handleUpgrade = async () => {
    if (!selectedTier) return;
    
    try {
      setLoading(true);
      setError('');
      
      const upgradeData = {
        tier_id: selectedTier.id,
        billing_cycle: billingCycle,
        payment_method: paymentMethod
      };
      
      if (promoCode.trim()) {
        upgradeData.promo_code = promoCode;
      }
      
      const response = await api.post('/subscription/upgrade', upgradeData);
      
      if (response.data.success) {
        // Refresh subscription data
        await fetchSubscriptionData();
        onClose();
        alert('Subscription upgraded successfully!');
      }
      
    } catch (error) {
      setError(error.response?.data?.error || 'Upgrade failed');
    } finally {
      setLoading(false);
    }
  };

  const calculatePrice = (tier) => {
    const basePrice = billingCycle === 'yearly' ? tier.price_yearly : tier.price_monthly;
    
    if (promoValidation?.valid && selectedTier?.id === tier.id) {
      return promoValidation.pricing.final_amount;
    }
    
    return basePrice;
  };

  const calculateSavings = (tier) => {
    if (billingCycle === 'yearly' && tier.yearly_savings) {
      return tier.yearly_savings;
    }
    
    if (promoValidation?.valid && selectedTier?.id === tier.id) {
      return promoValidation.pricing.discount_amount;
    }
    
    return 0;
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-700">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-white">Choose Your Plan</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-2xl"
            >
              ×
            </button>
          </div>
          
          {/* Billing Cycle Toggle */}
          <div className="mt-4 flex items-center justify-center">
            <div className="bg-gray-800 rounded-lg p-1 flex">
              <button
                onClick={() => setBillingCycle('monthly')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  billingCycle === 'monthly'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBillingCycle('yearly')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  billingCycle === 'yearly'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                Yearly
                <span className="ml-1 text-xs bg-green-600 text-white px-1 rounded">
                  Save 17%
                </span>
              </button>
            </div>
          </div>
        </div>

        <div className="p-6">
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              <p className="text-gray-400 mt-2">Loading subscription plans...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {tiers.map((tier) => {
                const price = calculatePrice(tier);
                const savings = calculateSavings(tier);
                const isCurrentTier = currentSubscription?.tier?.id === tier.id;
                const isSelected = selectedTier?.id === tier.id;
                
                return (
                  <div
                    key={tier.id}
                    className={`relative bg-gray-800 rounded-lg p-6 border-2 transition-all cursor-pointer ${
                      isSelected
                        ? 'border-blue-500 bg-gray-750'
                        : isCurrentTier
                        ? 'border-green-500'
                        : 'border-gray-700 hover:border-gray-600'
                    }`}
                    onClick={() => setSelectedTier(tier)}
                  >
                    {tier.is_popular && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                        <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-medium">
                          Most Popular
                        </span>
                      </div>
                    )}
                    
                    {tier.is_recommended && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                        <span className="bg-green-600 text-white px-3 py-1 rounded-full text-xs font-medium">
                          Recommended
                        </span>
                      </div>
                    )}
                    
                    {isCurrentTier && (
                      <div className="absolute -top-3 right-4">
                        <span className="bg-green-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                          Current
                        </span>
                      </div>
                    )}

                    <div className="text-center">
                      <h3 className="text-xl font-bold text-white mb-2">{tier.display_name}</h3>
                      <div className="mb-4">
                        <div className="text-3xl font-bold text-white">
                          ${price}
                          <span className="text-lg text-gray-400">
                            /{billingCycle === 'yearly' ? 'year' : 'month'}
                          </span>
                        </div>
                        {savings > 0 && (
                          <div className="text-sm text-green-400">
                            Save ${savings.toFixed(2)}
                          </div>
                        )}
                      </div>
                      <p className="text-gray-400 text-sm mb-6">{tier.description}</p>
                    </div>

                    {/* Features */}
                    <div className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-300">Wills</span>
                        <span className="text-white font-medium">
                          {tier.features.max_wills === 0 ? 'Unlimited' : tier.features.max_wills}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-300">Assets</span>
                        <span className="text-white font-medium">
                          {tier.features.max_assets === 0 ? 'Unlimited' : tier.features.max_assets}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-300">Crypto Assets</span>
                        <span className="text-white font-medium">
                          {tier.features.max_crypto_assets === 0 ? 'Unlimited' : tier.features.max_crypto_assets}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-300">Beneficiaries</span>
                        <span className="text-white font-medium">
                          {tier.features.max_beneficiaries === 0 ? 'Unlimited' : tier.features.max_beneficiaries}
                        </span>
                      </div>
                      
                      {/* Feature flags */}
                      <div className="pt-3 border-t border-gray-700 space-y-2">
                        {tier.features.ai_assistance && (
                          <div className="flex items-center text-sm text-green-400">
                            <span className="mr-2">✓</span>
                            AI Assistance
                          </div>
                        )}
                        {tier.features.crypto_inheritance && (
                          <div className="flex items-center text-sm text-green-400">
                            <span className="mr-2">✓</span>
                            Crypto Inheritance
                          </div>
                        )}
                        {tier.features.smart_contract_deployment && (
                          <div className="flex items-center text-sm text-green-400">
                            <span className="mr-2">✓</span>
                            Smart Contracts
                          </div>
                        )}
                        {tier.features.legal_review && (
                          <div className="flex items-center text-sm text-green-400">
                            <span className="mr-2">✓</span>
                            Legal Review
                          </div>
                        )}
                        {tier.features.priority_support && (
                          <div className="flex items-center text-sm text-green-400">
                            <span className="mr-2">✓</span>
                            Priority Support
                          </div>
                        )}
                        {tier.features.api_access && (
                          <div className="flex items-center text-sm text-green-400">
                            <span className="mr-2">✓</span>
                            API Access
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Promo Code Section */}
          {selectedTier && selectedTier.name !== 'free' && (
            <div className="mt-8 bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Promotional Code</h3>
              <div className="flex gap-4">
                <input
                  type="text"
                  value={promoCode}
                  onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
                  placeholder="Enter promo code"
                  className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={validatePromoCode}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Apply
                </button>
              </div>
              
              {promoValidation && (
                <div className={`mt-3 p-3 rounded-lg ${
                  promoValidation.valid ? 'bg-green-900 text-green-200' : 'bg-red-900 text-red-200'
                }`}>
                  {promoValidation.valid ? (
                    <div>
                      <p className="font-medium">Promo code applied!</p>
                      <p className="text-sm">
                        Save ${promoValidation.pricing.discount_amount.toFixed(2)} 
                        ({promoValidation.pricing.savings_percentage}% off)
                      </p>
                    </div>
                  ) : (
                    <p>{promoValidation.error}</p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Payment Method Selection */}
          {selectedTier && selectedTier.name !== 'free' && (
            <div className="mt-8 bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Payment Method</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => setPaymentMethod('stripe')}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    paymentMethod === 'stripe'
                      ? 'border-blue-500 bg-blue-900'
                      : 'border-gray-600 hover:border-gray-500'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-lg font-medium text-white">Credit Card</div>
                    <div className="text-sm text-gray-400">Visa, Mastercard, Amex</div>
                  </div>
                </button>
                
                <button
                  onClick={() => setPaymentMethod('crypto')}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    paymentMethod === 'crypto'
                      ? 'border-blue-500 bg-blue-900'
                      : 'border-gray-600 hover:border-gray-500'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-lg font-medium text-white">Cryptocurrency</div>
                    <div className="text-sm text-gray-400">ETH, USDC, BTC</div>
                  </div>
                </button>
                
                <button
                  onClick={() => setPaymentMethod('paypal')}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    paymentMethod === 'paypal'
                      ? 'border-blue-500 bg-blue-900'
                      : 'border-gray-600 hover:border-gray-500'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-lg font-medium text-white">PayPal</div>
                    <div className="text-sm text-gray-400">PayPal Account</div>
                  </div>
                </button>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="mt-6 p-4 bg-red-900 border border-red-700 rounded-lg">
              <p className="text-red-200">{error}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-8 flex justify-end gap-4">
            <button
              onClick={onClose}
              className="px-6 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-800 transition-colors"
            >
              Cancel
            </button>
            
            {selectedTier && selectedTier.name !== 'free' && (
              <button
                onClick={handleUpgrade}
                disabled={loading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Processing...' : `Upgrade to ${selectedTier.display_name}`}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionManager;

