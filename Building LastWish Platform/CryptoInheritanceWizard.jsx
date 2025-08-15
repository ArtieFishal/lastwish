import React, { useState, useEffect } from 'react';
import { ArrowLeft, ArrowRight, Check, Shield, Users, Clock, Settings, AlertTriangle, Zap } from 'lucide-react';

const CryptoInheritanceWizard = ({ walletId, onComplete, onCancel }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    plan_name: '',
    plan_description: '',
    beneficiaries: [],
    backup_beneficiaries: [],
    trigger_conditions: {
      inactivity_period: 365,
      verification_methods: ['email', 'legal_document'],
      require_death_certificate: true
    },
    time_delay: 30,
    automated_execution: false,
    manual_approval_required: true,
    multi_signature_required: false,
    smart_contract_enabled: false,
    smart_contract_network: 'ethereum',
    access_instructions: '',
    security_questions: [],
    emergency_contacts: [],
    legal_documentation: ''
  });

  const [availableBeneficiaries, setAvailableBeneficiaries] = useState([]);
  const [walletInfo, setWalletInfo] = useState(null);

  // Mock data for demonstration
  useEffect(() => {
    setAvailableBeneficiaries([
      {
        id: 1,
        beneficiary_name: "Sarah Johnson",
        relationship_to_user: "spouse",
        email_address: "sarah@example.com",
        crypto_wallet_address: "0x742d35Cc6634C0532925a3b8D4C2C3c8b4C2C3c8",
        crypto_experience_level: "intermediate"
      },
      {
        id: 2,
        beneficiary_name: "Michael Johnson",
        relationship_to_user: "child",
        email_address: "michael@example.com",
        crypto_wallet_address: "",
        crypto_experience_level: "beginner"
      },
      {
        id: 3,
        beneficiary_name: "Jennifer Smith",
        relationship_to_user: "sibling",
        email_address: "jennifer@example.com",
        crypto_wallet_address: "0x123d35Cc6634C0532925a3b8D4C2C3c8b4C2C3c8",
        crypto_experience_level: "advanced"
      }
    ]);

    setWalletInfo({
      id: walletId,
      wallet_name: "Main Bitcoin Wallet",
      blockchain_network: "bitcoin",
      estimated_total_value: 45250.75,
      asset_count: 3
    });
  }, [walletId]);

  const steps = [
    { id: 1, title: "Plan Details", icon: Settings },
    { id: 2, title: "Beneficiaries", icon: Users },
    { id: 3, title: "Trigger Conditions", icon: Clock },
    { id: 4, title: "Security & Access", icon: Shield },
    { id: 5, title: "Smart Contracts", icon: Zap },
    { id: 6, title: "Review & Complete", icon: Check }
  ];

  const addBeneficiary = (beneficiary, allocation) => {
    const newBeneficiary = {
      ...beneficiary,
      allocation_percentage: allocation,
      id: Date.now() // Temporary ID
    };
    setFormData(prev => ({
      ...prev,
      beneficiaries: [...prev.beneficiaries, newBeneficiary]
    }));
  };

  const removeBeneficiary = (index) => {
    setFormData(prev => ({
      ...prev,
      beneficiaries: prev.beneficiaries.filter((_, i) => i !== index)
    }));
  };

  const updateBeneficiaryAllocation = (index, allocation) => {
    setFormData(prev => ({
      ...prev,
      beneficiaries: prev.beneficiaries.map((b, i) => 
        i === index ? { ...b, allocation_percentage: allocation } : b
      )
    }));
  };

  const getTotalAllocation = () => {
    return formData.beneficiaries.reduce((sum, b) => sum + (b.allocation_percentage || 0), 0);
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return formData.plan_name.trim() !== '';
      case 2:
        return formData.beneficiaries.length > 0 && getTotalAllocation() === 100;
      case 3:
        return formData.trigger_conditions.inactivity_period > 0;
      case 4:
        return formData.access_instructions.trim() !== '';
      case 5:
        return true; // Smart contracts are optional
      case 6:
        return true;
      default:
        return false;
    }
  };

  const nextStep = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = () => {
    console.log('Submitting inheritance plan:', formData);
    onComplete(formData);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Plan Details</h3>
              <p className="text-gray-400 mb-6">
                Set up the basic information for your crypto inheritance plan.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Plan Name *
                </label>
                <input
                  type="text"
                  value={formData.plan_name}
                  onChange={(e) => setFormData({...formData, plan_name: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  placeholder="My Bitcoin Inheritance Plan"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Description
                </label>
                <textarea
                  value={formData.plan_description}
                  onChange={(e) => setFormData({...formData, plan_description: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  rows="3"
                  placeholder="Describe the purpose and scope of this inheritance plan..."
                />
              </div>

              {walletInfo && (
                <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                  <h4 className="font-medium text-white mb-2">Wallet Information</h4>
                  <div className="space-y-1 text-sm text-gray-400">
                    <p>Name: {walletInfo.wallet_name}</p>
                    <p>Network: {walletInfo.blockchain_network}</p>
                    <p>Value: ${walletInfo.estimated_total_value.toLocaleString()}</p>
                    <p>Assets: {walletInfo.asset_count}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Beneficiaries</h3>
              <p className="text-gray-400 mb-6">
                Select beneficiaries and allocate percentages of your crypto assets.
              </p>
            </div>

            <div className="space-y-4">
              {/* Current Beneficiaries */}
              {formData.beneficiaries.length > 0 && (
                <div className="space-y-3">
                  <h4 className="font-medium text-white">Selected Beneficiaries</h4>
                  {formData.beneficiaries.map((beneficiary, index) => (
                    <div key={index} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                      <div className="flex items-center justify-between">
                        <div>
                          <h5 className="font-medium text-white">{beneficiary.beneficiary_name}</h5>
                          <p className="text-sm text-gray-400">{beneficiary.relationship_to_user}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="flex items-center gap-2">
                            <input
                              type="number"
                              min="0"
                              max="100"
                              value={beneficiary.allocation_percentage || 0}
                              onChange={(e) => updateBeneficiaryAllocation(index, parseInt(e.target.value) || 0)}
                              className="w-16 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white text-center"
                            />
                            <span className="text-gray-400">%</span>
                          </div>
                          <button
                            onClick={() => removeBeneficiary(index)}
                            className="text-red-400 hover:text-red-300"
                          >
                            Remove
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  <div className="bg-gray-800 rounded-lg p-3 border border-gray-700">
                    <div className="flex items-center justify-between">
                      <span className="text-white font-medium">Total Allocation:</span>
                      <span className={`font-bold ${getTotalAllocation() === 100 ? 'text-green-400' : 'text-yellow-400'}`}>
                        {getTotalAllocation()}%
                      </span>
                    </div>
                    {getTotalAllocation() !== 100 && (
                      <p className="text-sm text-yellow-400 mt-1">
                        Total allocation must equal 100%
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Available Beneficiaries */}
              <div className="space-y-3">
                <h4 className="font-medium text-white">Available Beneficiaries</h4>
                {availableBeneficiaries
                  .filter(b => !formData.beneficiaries.find(fb => fb.id === b.id))
                  .map((beneficiary) => (
                    <div key={beneficiary.id} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                      <div className="flex items-center justify-between">
                        <div>
                          <h5 className="font-medium text-white">{beneficiary.beneficiary_name}</h5>
                          <p className="text-sm text-gray-400">{beneficiary.relationship_to_user}</p>
                          <p className="text-xs text-gray-500">
                            Crypto Experience: {beneficiary.crypto_experience_level}
                          </p>
                        </div>
                        <div className="flex items-center gap-3">
                          <input
                            type="number"
                            min="0"
                            max="100"
                            placeholder="0"
                            className="w-16 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white text-center"
                            id={`allocation-${beneficiary.id}`}
                          />
                          <span className="text-gray-400">%</span>
                          <button
                            onClick={() => {
                              const allocation = parseInt(document.getElementById(`allocation-${beneficiary.id}`).value) || 0;
                              if (allocation > 0) {
                                addBeneficiary(beneficiary, allocation);
                                document.getElementById(`allocation-${beneficiary.id}`).value = '';
                              }
                            }}
                            className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                          >
                            Add
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Trigger Conditions</h3>
              <p className="text-gray-400 mb-6">
                Define when and how the inheritance process should be triggered.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Inactivity Period (days) *
                </label>
                <input
                  type="number"
                  min="1"
                  value={formData.trigger_conditions.inactivity_period}
                  onChange={(e) => setFormData({
                    ...formData,
                    trigger_conditions: {
                      ...formData.trigger_conditions,
                      inactivity_period: parseInt(e.target.value) || 0
                    }
                  })}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Number of days of inactivity before inheritance process begins
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Verification Methods
                </label>
                <div className="space-y-2">
                  {['email', 'legal_document', 'family_verification', 'court_order'].map((method) => (
                    <label key={method} className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={formData.trigger_conditions.verification_methods.includes(method)}
                        onChange={(e) => {
                          const methods = formData.trigger_conditions.verification_methods;
                          if (e.target.checked) {
                            setFormData({
                              ...formData,
                              trigger_conditions: {
                                ...formData.trigger_conditions,
                                verification_methods: [...methods, method]
                              }
                            });
                          } else {
                            setFormData({
                              ...formData,
                              trigger_conditions: {
                                ...formData.trigger_conditions,
                                verification_methods: methods.filter(m => m !== method)
                              }
                            });
                          }
                        }}
                        className="rounded bg-gray-800 border-gray-600 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-white capitalize">{method.replace('_', ' ')}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Execution Delay (days)
                </label>
                <input
                  type="number"
                  min="0"
                  value={formData.time_delay}
                  onChange={(e) => setFormData({...formData, time_delay: parseInt(e.target.value) || 0})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Additional delay before assets are transferred to beneficiaries
                </p>
              </div>

              <div className="space-y-3">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.trigger_conditions.require_death_certificate}
                    onChange={(e) => setFormData({
                      ...formData,
                      trigger_conditions: {
                        ...formData.trigger_conditions,
                        require_death_certificate: e.target.checked
                      }
                    })}
                    className="rounded bg-gray-800 border-gray-600 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-white">Require death certificate</span>
                </label>

                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.manual_approval_required}
                    onChange={(e) => setFormData({...formData, manual_approval_required: e.target.checked})}
                    className="rounded bg-gray-800 border-gray-600 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-white">Require manual approval</span>
                </label>
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Security & Access</h3>
              <p className="text-gray-400 mb-6">
                Provide instructions and security measures for accessing your crypto assets.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Access Instructions *
                </label>
                <textarea
                  value={formData.access_instructions}
                  onChange={(e) => setFormData({...formData, access_instructions: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  rows="4"
                  placeholder="Provide detailed instructions on how beneficiaries can access the crypto assets..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Legal Documentation
                </label>
                <textarea
                  value={formData.legal_documentation}
                  onChange={(e) => setFormData({...formData, legal_documentation: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  rows="3"
                  placeholder="Reference to legal documents, attorney contact information, etc..."
                />
              </div>

              <div className="bg-yellow-900/20 border border-yellow-600/30 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-yellow-400 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-yellow-400 mb-1">Security Notice</h4>
                    <p className="text-sm text-yellow-200">
                      Never include private keys, seed phrases, or passwords in these instructions. 
                      Store sensitive information securely and reference their location only.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Smart Contract Automation</h3>
              <p className="text-gray-400 mb-6">
                Enable blockchain-based automation for your inheritance plan (optional).
              </p>
            </div>

            <div className="space-y-4">
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={formData.smart_contract_enabled}
                  onChange={(e) => setFormData({...formData, smart_contract_enabled: e.target.checked})}
                  className="rounded bg-gray-800 border-gray-600 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-white font-medium">Enable Smart Contract Automation</span>
              </label>

              {formData.smart_contract_enabled && (
                <div className="space-y-4 ml-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Blockchain Network
                    </label>
                    <select
                      value={formData.smart_contract_network}
                      onChange={(e) => setFormData({...formData, smart_contract_network: e.target.value})}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="ethereum">Ethereum</option>
                      <option value="polygon">Polygon</option>
                      <option value="binance_smart_chain">Binance Smart Chain</option>
                      <option value="avalanche">Avalanche</option>
                    </select>
                  </div>

                  <div className="bg-blue-900/20 border border-blue-600/30 rounded-lg p-4">
                    <h4 className="font-medium text-blue-400 mb-2">Smart Contract Features</h4>
                    <ul className="text-sm text-blue-200 space-y-1">
                      <li>• Automated asset distribution based on predefined conditions</li>
                      <li>• Time-locked transfers with configurable delays</li>
                      <li>• Multi-signature requirements for enhanced security</li>
                      <li>• Immutable execution once conditions are met</li>
                    </ul>
                  </div>
                </div>
              )}

              <div className="space-y-3">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.automated_execution}
                    onChange={(e) => setFormData({...formData, automated_execution: e.target.checked})}
                    className="rounded bg-gray-800 border-gray-600 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-white">Enable automated execution</span>
                </label>

                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.multi_signature_required}
                    onChange={(e) => setFormData({...formData, multi_signature_required: e.target.checked})}
                    className="rounded bg-gray-800 border-gray-600 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-white">Require multiple signatures</span>
                </label>
              </div>
            </div>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Review & Complete</h3>
              <p className="text-gray-400 mb-6">
                Review your inheritance plan details before finalizing.
              </p>
            </div>

            <div className="space-y-4">
              <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <h4 className="font-medium text-white mb-2">Plan Overview</h4>
                <div className="space-y-1 text-sm">
                  <p><span className="text-gray-400">Name:</span> <span className="text-white">{formData.plan_name}</span></p>
                  <p><span className="text-gray-400">Beneficiaries:</span> <span className="text-white">{formData.beneficiaries.length}</span></p>
                  <p><span className="text-gray-400">Inactivity Period:</span> <span className="text-white">{formData.trigger_conditions.inactivity_period} days</span></p>
                  <p><span className="text-gray-400">Execution Delay:</span> <span className="text-white">{formData.time_delay} days</span></p>
                  <p><span className="text-gray-400">Smart Contracts:</span> <span className="text-white">{formData.smart_contract_enabled ? 'Enabled' : 'Disabled'}</span></p>
                </div>
              </div>

              <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <h4 className="font-medium text-white mb-2">Beneficiary Allocations</h4>
                <div className="space-y-1 text-sm">
                  {formData.beneficiaries.map((beneficiary, index) => (
                    <p key={index}>
                      <span className="text-gray-400">{beneficiary.beneficiary_name}:</span> 
                      <span className="text-white ml-2">{beneficiary.allocation_percentage}%</span>
                    </p>
                  ))}
                </div>
              </div>

              <div className="bg-green-900/20 border border-green-600/30 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <Check className="w-5 h-5 text-green-400 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-green-400 mb-1">Ready to Create</h4>
                    <p className="text-sm text-green-200">
                      Your inheritance plan is configured and ready to be created. 
                      You can modify it later if needed.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-900 rounded-xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-hidden border border-gray-700">
        {/* Header */}
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white">Crypto Inheritance Wizard</h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-white"
            >
              ✕
            </button>
          </div>
          
          {/* Progress Steps */}
          <div className="flex items-center gap-4 mt-6">
            {steps.map((step, index) => {
              const Icon = step.icon;
              const isActive = step.id === currentStep;
              const isCompleted = step.id < currentStep;
              
              return (
                <div key={step.id} className="flex items-center">
                  <div className={`flex items-center gap-2 px-3 py-2 rounded-lg ${
                    isActive ? 'bg-blue-600 text-white' : 
                    isCompleted ? 'bg-green-600 text-white' : 
                    'bg-gray-700 text-gray-400'
                  }`}>
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-medium">{step.title}</span>
                  </div>
                  {index < steps.length - 1 && (
                    <div className="w-8 h-px bg-gray-600 mx-2"></div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {renderStepContent()}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-700">
          <div className="flex items-center justify-between">
            <button
              onClick={prevStep}
              disabled={currentStep === 1}
              className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-4 h-4" />
              Previous
            </button>

            <div className="text-sm text-gray-400">
              Step {currentStep} of {steps.length}
            </div>

            {currentStep < steps.length ? (
              <button
                onClick={nextStep}
                disabled={!canProceed()}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                className="flex items-center gap-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Check className="w-4 h-4" />
                Create Plan
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CryptoInheritanceWizard;

