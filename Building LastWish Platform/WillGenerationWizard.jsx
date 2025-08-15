import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ArrowLeft, ArrowRight, FileText, Users, Home, Heart, Shield, CheckCircle } from 'lucide-react'

const WillGenerationWizard = ({ onClose }) => {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState({
    // Personal Information
    fullName: '',
    dateOfBirth: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    maritalStatus: '',
    
    // Executor Information
    executorName: '',
    executorRelationship: '',
    executorPhone: '',
    executorEmail: '',
    alternateExecutorName: '',
    
    // Beneficiaries
    beneficiaries: [
      { name: '', relationship: '', percentage: '', address: '', phone: '' }
    ],
    
    // Assets
    realEstate: '',
    bankAccounts: '',
    investments: '',
    personalProperty: '',
    digitalAssets: '',
    
    // Guardianship (if applicable)
    hasMinorChildren: false,
    guardianName: '',
    guardianRelationship: '',
    
    // Final Wishes
    funeralPreferences: '',
    burialPreferences: '',
    specialInstructions: '',
    
    // Digital Assets
    cryptoWallets: '',
    onlineAccounts: '',
    digitalFiles: ''
  })

  const totalSteps = 7
  const progress = (currentStep / totalSteps) * 100

  const updateFormData = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const addBeneficiary = () => {
    setFormData(prev => ({
      ...prev,
      beneficiaries: [...prev.beneficiaries, { name: '', relationship: '', percentage: '', address: '', phone: '' }]
    }))
  }

  const updateBeneficiary = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      beneficiaries: prev.beneficiaries.map((ben, i) => 
        i === index ? { ...ben, [field]: value } : ben
      )
    }))
  }

  const removeBeneficiary = (index) => {
    setFormData(prev => ({
      ...prev,
      beneficiaries: prev.beneficiaries.filter((_, i) => i !== index)
    }))
  }

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const submitToN8N = async () => {
    try {
      // This would trigger the n8n workflow for will generation
      const response = await fetch('/api/n8n/generate-will', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          willData: formData,
          timestamp: new Date().toISOString(),
          userId: 'demo-user'
        })
      })
      
      const result = await response.json()
      
      if (result.success) {
        alert('Will generation initiated! You will receive an email with your completed will document within 24 hours.')
        onClose()
      } else {
        alert('Error generating will. Please try again.')
      }
    } catch (error) {
      console.error('Error submitting will data:', error)
      alert('Error connecting to will generation service. Please try again.')
    }
  }

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <FileText className="h-12 w-12 text-blue-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Personal Information</h2>
              <p className="text-gray-400">Let's start with your basic information</p>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="fullName" className="text-white">Full Legal Name *</Label>
                <Input
                  id="fullName"
                  value={formData.fullName}
                  onChange={(e) => updateFormData('fullName', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Enter your full legal name"
                />
              </div>
              
              <div>
                <Label htmlFor="dateOfBirth" className="text-white">Date of Birth *</Label>
                <Input
                  id="dateOfBirth"
                  type="date"
                  value={formData.dateOfBirth}
                  onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                />
              </div>
              
              <div className="md:col-span-2">
                <Label htmlFor="address" className="text-white">Address *</Label>
                <Input
                  id="address"
                  value={formData.address}
                  onChange={(e) => updateFormData('address', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Street address"
                />
              </div>
              
              <div>
                <Label htmlFor="city" className="text-white">City *</Label>
                <Input
                  id="city"
                  value={formData.city}
                  onChange={(e) => updateFormData('city', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                />
              </div>
              
              <div>
                <Label htmlFor="state" className="text-white">State *</Label>
                <Select value={formData.state} onValueChange={(value) => updateFormData('state', value)}>
                  <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                    <SelectValue placeholder="Select state" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="AL">Alabama</SelectItem>
                    <SelectItem value="CA">California</SelectItem>
                    <SelectItem value="FL">Florida</SelectItem>
                    <SelectItem value="NY">New York</SelectItem>
                    <SelectItem value="TX">Texas</SelectItem>
                    {/* Add more states as needed */}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="zipCode" className="text-white">ZIP Code *</Label>
                <Input
                  id="zipCode"
                  value={formData.zipCode}
                  onChange={(e) => updateFormData('zipCode', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                />
              </div>
              
              <div>
                <Label htmlFor="maritalStatus" className="text-white">Marital Status *</Label>
                <Select value={formData.maritalStatus} onValueChange={(value) => updateFormData('maritalStatus', value)}>
                  <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="single">Single</SelectItem>
                    <SelectItem value="married">Married</SelectItem>
                    <SelectItem value="divorced">Divorced</SelectItem>
                    <SelectItem value="widowed">Widowed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Shield className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Executor Selection</h2>
              <p className="text-gray-400">Choose who will manage your estate</p>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="executorName" className="text-white">Executor Full Name *</Label>
                <Input
                  id="executorName"
                  value={formData.executorName}
                  onChange={(e) => updateFormData('executorName', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Primary executor name"
                />
              </div>
              
              <div>
                <Label htmlFor="executorRelationship" className="text-white">Relationship *</Label>
                <Select value={formData.executorRelationship} onValueChange={(value) => updateFormData('executorRelationship', value)}>
                  <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                    <SelectValue placeholder="Select relationship" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="spouse">Spouse</SelectItem>
                    <SelectItem value="child">Child</SelectItem>
                    <SelectItem value="parent">Parent</SelectItem>
                    <SelectItem value="sibling">Sibling</SelectItem>
                    <SelectItem value="friend">Friend</SelectItem>
                    <SelectItem value="attorney">Attorney</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="executorPhone" className="text-white">Phone Number *</Label>
                <Input
                  id="executorPhone"
                  value={formData.executorPhone}
                  onChange={(e) => updateFormData('executorPhone', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="(555) 123-4567"
                />
              </div>
              
              <div>
                <Label htmlFor="executorEmail" className="text-white">Email Address *</Label>
                <Input
                  id="executorEmail"
                  type="email"
                  value={formData.executorEmail}
                  onChange={(e) => updateFormData('executorEmail', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="executor@email.com"
                />
              </div>
              
              <div className="md:col-span-2">
                <Label htmlFor="alternateExecutorName" className="text-white">Alternate Executor (Optional)</Label>
                <Input
                  id="alternateExecutorName"
                  value={formData.alternateExecutorName}
                  onChange={(e) => updateFormData('alternateExecutorName', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Backup executor name"
                />
              </div>
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Users className="h-12 w-12 text-purple-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Beneficiaries</h2>
              <p className="text-gray-400">Who will inherit your assets?</p>
            </div>
            
            {formData.beneficiaries.map((beneficiary, index) => (
              <Card key={index} className="bg-gray-800 border-gray-600">
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-white">Beneficiary {index + 1}</CardTitle>
                    {formData.beneficiaries.length > 1 && (
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => removeBeneficiary(index)}
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label className="text-white">Full Name *</Label>
                      <Input
                        value={beneficiary.name}
                        onChange={(e) => updateBeneficiary(index, 'name', e.target.value)}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="Beneficiary name"
                      />
                    </div>
                    
                    <div>
                      <Label className="text-white">Relationship *</Label>
                      <Select 
                        value={beneficiary.relationship} 
                        onValueChange={(value) => updateBeneficiary(index, 'relationship', value)}
                      >
                        <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                          <SelectValue placeholder="Select relationship" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="spouse">Spouse</SelectItem>
                          <SelectItem value="child">Child</SelectItem>
                          <SelectItem value="parent">Parent</SelectItem>
                          <SelectItem value="sibling">Sibling</SelectItem>
                          <SelectItem value="grandchild">Grandchild</SelectItem>
                          <SelectItem value="friend">Friend</SelectItem>
                          <SelectItem value="charity">Charity</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-white">Inheritance Percentage *</Label>
                      <Input
                        type="number"
                        min="0"
                        max="100"
                        value={beneficiary.percentage}
                        onChange={(e) => updateBeneficiary(index, 'percentage', e.target.value)}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="25"
                      />
                    </div>
                    
                    <div>
                      <Label className="text-white">Phone Number</Label>
                      <Input
                        value={beneficiary.phone}
                        onChange={(e) => updateBeneficiary(index, 'phone', e.target.value)}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="(555) 123-4567"
                      />
                    </div>
                    
                    <div className="md:col-span-2">
                      <Label className="text-white">Address</Label>
                      <Input
                        value={beneficiary.address}
                        onChange={(e) => updateBeneficiary(index, 'address', e.target.value)}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="Full address"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
            
            <Button
              onClick={addBeneficiary}
              variant="outline"
              className="w-full border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white"
            >
              Add Another Beneficiary
            </Button>
          </div>
        )

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Home className="h-12 w-12 text-orange-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Asset Information</h2>
              <p className="text-gray-400">Tell us about your assets</p>
            </div>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="realEstate" className="text-white">Real Estate</Label>
                <Textarea
                  id="realEstate"
                  value={formData.realEstate}
                  onChange={(e) => updateFormData('realEstate', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Describe your real estate properties (addresses, estimated values)"
                  rows={3}
                />
              </div>
              
              <div>
                <Label htmlFor="bankAccounts" className="text-white">Bank Accounts & Investments</Label>
                <Textarea
                  id="bankAccounts"
                  value={formData.bankAccounts}
                  onChange={(e) => updateFormData('bankAccounts', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="List bank accounts, investment accounts, retirement accounts"
                  rows={3}
                />
              </div>
              
              <div>
                <Label htmlFor="personalProperty" className="text-white">Personal Property</Label>
                <Textarea
                  id="personalProperty"
                  value={formData.personalProperty}
                  onChange={(e) => updateFormData('personalProperty', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Vehicles, jewelry, artwork, collectibles, etc."
                  rows={3}
                />
              </div>
            </div>
          </div>
        )

      case 5:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Coins className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Digital & Crypto Assets</h2>
              <p className="text-gray-400">Modern assets require special handling</p>
            </div>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="cryptoWallets" className="text-white">Cryptocurrency Wallets</Label>
                <Textarea
                  id="cryptoWallets"
                  value={formData.cryptoWallets}
                  onChange={(e) => updateFormData('cryptoWallets', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="List wallet addresses, types of crypto, storage methods (hardware wallet, exchange, etc.)"
                  rows={3}
                />
              </div>
              
              <div>
                <Label htmlFor="onlineAccounts" className="text-white">Digital Accounts</Label>
                <Textarea
                  id="onlineAccounts"
                  value={formData.onlineAccounts}
                  onChange={(e) => updateFormData('onlineAccounts', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Social media, email, cloud storage, subscription services, etc."
                  rows={3}
                />
              </div>
              
              <div>
                <Label htmlFor="digitalFiles" className="text-white">Digital Files & NFTs</Label>
                <Textarea
                  id="digitalFiles"
                  value={formData.digitalFiles}
                  onChange={(e) => updateFormData('digitalFiles', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Important digital files, NFT collections, digital art, etc."
                  rows={3}
                />
              </div>
            </div>
          </div>
        )

      case 6:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <Heart className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Guardianship & Care</h2>
              <p className="text-gray-400">Protecting those who depend on you</p>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="hasMinorChildren"
                  checked={formData.hasMinorChildren}
                  onCheckedChange={(checked) => updateFormData('hasMinorChildren', checked)}
                />
                <Label htmlFor="hasMinorChildren" className="text-white">
                  I have minor children who need guardianship
                </Label>
              </div>
              
              {formData.hasMinorChildren && (
                <div className="grid md:grid-cols-2 gap-4 p-4 bg-gray-800 rounded-lg">
                  <div>
                    <Label htmlFor="guardianName" className="text-white">Guardian Name *</Label>
                    <Input
                      id="guardianName"
                      value={formData.guardianName}
                      onChange={(e) => updateFormData('guardianName', e.target.value)}
                      className="bg-gray-700 border-gray-600 text-white"
                      placeholder="Proposed guardian name"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="guardianRelationship" className="text-white">Relationship *</Label>
                    <Select value={formData.guardianRelationship} onValueChange={(value) => updateFormData('guardianRelationship', value)}>
                      <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                        <SelectValue placeholder="Select relationship" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="parent">Parent</SelectItem>
                        <SelectItem value="sibling">Sibling</SelectItem>
                        <SelectItem value="grandparent">Grandparent</SelectItem>
                        <SelectItem value="aunt_uncle">Aunt/Uncle</SelectItem>
                        <SelectItem value="friend">Close Friend</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}
            </div>
          </div>
        )

      case 7:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white">Final Wishes</h2>
              <p className="text-gray-400">Your personal preferences and instructions</p>
            </div>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="funeralPreferences" className="text-white">Funeral Preferences</Label>
                <Textarea
                  id="funeralPreferences"
                  value={formData.funeralPreferences}
                  onChange={(e) => updateFormData('funeralPreferences', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Describe your funeral service preferences"
                  rows={3}
                />
              </div>
              
              <div>
                <Label htmlFor="burialPreferences" className="text-white">Burial/Cremation Preferences</Label>
                <Textarea
                  id="burialPreferences"
                  value={formData.burialPreferences}
                  onChange={(e) => updateFormData('burialPreferences', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Burial, cremation, or other preferences"
                  rows={3}
                />
              </div>
              
              <div>
                <Label htmlFor="specialInstructions" className="text-white">Special Instructions</Label>
                <Textarea
                  id="specialInstructions"
                  value={formData.specialInstructions}
                  onChange={(e) => updateFormData('specialInstructions', e.target.value)}
                  className="bg-gray-800 border-gray-600 text-white"
                  placeholder="Any additional instructions or wishes"
                  rows={4}
                />
              </div>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-white">Will Generation Wizard</h1>
            <Button variant="ghost" onClick={onClose} className="text-gray-400 hover:text-white">
              ✕
            </Button>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-400">
              <span>Step {currentStep} of {totalSteps}</span>
              <span>{Math.round(progress)}% Complete</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
          
          <div className="flex items-center justify-center mt-4">
            <Badge variant="secondary" className="bg-blue-500/10 text-blue-400 border-blue-500/20">
              🤖 Powered by n8n Automation
            </Badge>
          </div>
        </div>
        
        <div className="p-6">
          {renderStep()}
        </div>
        
        <div className="p-6 border-t border-gray-700 flex justify-between">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={currentStep === 1}
            className="border-gray-600 text-white hover:bg-gray-800"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Previous
          </Button>
          
          {currentStep === totalSteps ? (
            <Button
              onClick={submitToN8N}
              className="bg-green-500 hover:bg-green-600"
            >
              Generate Will with n8n
              <FileText className="h-4 w-4 ml-2" />
            </Button>
          ) : (
            <Button
              onClick={nextStep}
              className="bg-blue-500 hover:bg-blue-600"
            >
              Next
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}

export default WillGenerationWizard

