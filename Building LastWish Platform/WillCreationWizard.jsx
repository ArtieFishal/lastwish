import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  FileText, 
  User, 
  Users, 
  Heart, 
  Briefcase, 
  Shield, 
  Check, 
  ArrowLeft, 
  ArrowRight, 
  AlertCircle 
} from 'lucide-react'

const steps = [
  { id: 'personal', title: 'Personal Information', icon: User },
  { id: 'executor', title: 'Executor', icon: Briefcase },
  { id: 'beneficiaries', title: 'Beneficiaries', icon: Users },
  { id: 'assets', title: 'Asset Distribution', icon: Briefcase },
  { id: 'guardians', title: 'Guardianship', icon: Heart },
  { id: 'final', title: 'Final Wishes', icon: Shield },
  { id: 'review', title: 'Review & Sign', icon: Check },
]

export function WillCreationWizard({ onComplete }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState({
    personal: { fullName: '', address: '', city: '', state: '', zip: '' },
    executor: { fullName: '', relationship: '', backupFullName: '', backupRelationship: '' },
    beneficiaries: [{ fullName: '', relationship: '', share: '' }],
    assets: { specificGifts: '', residualEstate: '' },
    guardians: { hasMinors: false, guardianName: '', backupGuardianName: '' },
    final: { funeralWishes: '', burialWishes: '' },
  })
  const [error, setError] = useState('')

  const progress = Math.round(((currentStep + 1) / steps.length) * 100)

  const handleNext = () => {
    // Add validation logic here for each step
    setError('')
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleFormChange = (step, field, value) => {
    setFormData(prev => ({
      ...prev,
      [step]: {
        ...prev[step],
        [field]: value
      }
    }))
  }

  const handleBeneficiaryChange = (index, field, value) => {
    const newBeneficiaries = [...formData.beneficiaries]
    newBeneficiaries[index][field] = value
    setFormData(prev => ({ ...prev, beneficiaries: newBeneficiaries }))
  }

  const addBeneficiary = () => {
    setFormData(prev => ({ 
      ...prev, 
      beneficiaries: [...prev.beneficiaries, { fullName: '', relationship: '', share: '' }] 
    }))
  }

  const removeBeneficiary = (index) => {
    const newBeneficiaries = formData.beneficiaries.filter((_, i) => i !== index)
    setFormData(prev => ({ ...prev, beneficiaries: newBeneficiaries }))
  }

  const handleSubmit = () => {
    // Final validation
    onComplete(formData)
  }

  const renderStepContent = () => {
    switch (steps[currentStep].id) {
      case 'personal':
        return (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input id="fullName" value={formData.personal.fullName} onChange={(e) => handleFormChange('personal', 'fullName', e.target.value)} />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="address">Address</Label>
              <Input id="address" value={formData.personal.address} onChange={(e) => handleFormChange('personal', 'address', e.target.value)} />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input id="city" value={formData.personal.city} onChange={(e) => handleFormChange('personal', 'city', e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input id="state" value={formData.personal.state} onChange={(e) => handleFormChange('personal', 'state', e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="zip">ZIP Code</Label>
                <Input id="zip" value={formData.personal.zip} onChange={(e) => handleFormChange('personal', 'zip', e.target.value)} />
              </div>
            </div>
          </div>
        )
      case 'executor':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="font-medium mb-2">Primary Executor</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="executorFullName">Full Name</Label>
                  <Input id="executorFullName" value={formData.executor.fullName} onChange={(e) => handleFormChange('executor', 'fullName', e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="executorRelationship">Relationship</Label>
                  <Input id="executorRelationship" value={formData.executor.relationship} onChange={(e) => handleFormChange('executor', 'relationship', e.target.value)} />
                </div>
              </div>
            </div>
            <div>
              <h3 className="font-medium mb-2">Backup Executor</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="backupExecutorFullName">Full Name</Label>
                  <Input id="backupExecutorFullName" value={formData.executor.backupFullName} onChange={(e) => handleFormChange('executor', 'backupFullName', e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="backupExecutorRelationship">Relationship</Label>
                  <Input id="backupExecutorRelationship" value={formData.executor.backupRelationship} onChange={(e) => handleFormChange('executor', 'backupRelationship', e.target.value)} />
                </div>
              </div>
            </div>
          </div>
        )
      case 'beneficiaries':
        return (
          <div className="space-y-4">
            {formData.beneficiaries.map((beneficiary, index) => (
              <Card key={index} className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor={`beneficiaryName-${index}`}>Full Name</Label>
                    <Input id={`beneficiaryName-${index}`} value={beneficiary.fullName} onChange={(e) => handleBeneficiaryChange(index, 'fullName', e.target.value)} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor={`beneficiaryRelationship-${index}`}>Relationship</Label>
                    <Input id={`beneficiaryRelationship-${index}`} value={beneficiary.relationship} onChange={(e) => handleBeneficiaryChange(index, 'relationship', e.target.value)} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor={`beneficiaryShare-${index}`}>Share (%)</Label>
                    <Input id={`beneficiaryShare-${index}`} type="number" value={beneficiary.share} onChange={(e) => handleBeneficiaryChange(index, 'share', e.target.value)} />
                  </div>
                </div>
                {formData.beneficiaries.length > 1 && (
                  <Button variant="destructive" size="sm" className="mt-4" onClick={() => removeBeneficiary(index)}>Remove</Button>
                )}
              </Card>
            ))}
            <Button onClick={addBeneficiary}>Add Beneficiary</Button>
          </div>
        )
      case 'assets':
        return (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="specificGifts">Specific Gifts</Label>
              <Textarea id="specificGifts" placeholder="e.g., My 1965 Ford Mustang to my son, John Doe Jr." value={formData.assets.specificGifts} onChange={(e) => handleFormChange('assets', 'specificGifts', e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="residualEstate">Residual Estate</Label>
              <Textarea id="residualEstate" placeholder="How should the rest of your property be distributed?" value={formData.assets.residualEstate} onChange={(e) => handleFormChange('assets', 'residualEstate', e.target.value)} />
            </div>
          </div>
        )
      case 'guardians':
        return (
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Checkbox id="hasMinors" checked={formData.guardians.hasMinors} onCheckedChange={(checked) => handleFormChange('guardians', 'hasMinors', checked)} />
              <Label htmlFor="hasMinors">I have minor children</Label>
            </div>
            {formData.guardians.hasMinors && (
              <div className="space-y-6">
                <div>
                  <h3 className="font-medium mb-2">Primary Guardian</h3>
                  <div className="space-y-2">
                    <Label htmlFor="guardianName">Full Name</Label>
                    <Input id="guardianName" value={formData.guardians.guardianName} onChange={(e) => handleFormChange('guardians', 'guardianName', e.target.value)} />
                  </div>
                </div>
                <div>
                  <h3 className="font-medium mb-2">Backup Guardian</h3>
                  <div className="space-y-2">
                    <Label htmlFor="backupGuardianName">Full Name</Label>
                    <Input id="backupGuardianName" value={formData.guardians.backupGuardianName} onChange={(e) => handleFormChange('guardians', 'backupGuardianName', e.target.value)} />
                  </div>
                </div>
              </div>
            )}
          </div>
        )
      case 'final':
        return (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="funeralWishes">Funeral Wishes</Label>
              <Textarea id="funeralWishes" placeholder="e.g., Type of service, music, readings" value={formData.final.funeralWishes} onChange={(e) => handleFormChange('final', 'funeralWishes', e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="burialWishes">Burial/Cremation Wishes</Label>
              <Textarea id="burialWishes" placeholder="e.g., Burial, cremation, location" value={formData.final.burialWishes} onChange={(e) => handleFormChange('final', 'burialWishes', e.target.value)} />
            </div>
          </div>
        )
      case 'review':
        return (
          <div>
            <h3 className="text-lg font-medium mb-4">Review Your Will</h3>
            <pre className="bg-muted p-4 rounded-md overflow-x-auto text-sm">
              {JSON.stringify(formData, null, 2)}
            </pre>
            <div className="mt-4">
              <Button onClick={handleSubmit} className="w-full">Sign & Finalize</Button>
            </div>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <Card className="border-border bg-card">
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <FileText className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-bold">Create Your Will</h2>
            </div>
            <div className="text-sm text-muted-foreground">
              Step {currentStep + 1} of {steps.length}
            </div>
          </div>
          <Progress value={progress} className="w-full" />
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Sidebar */}
            <div className="col-span-1">
              <nav className="space-y-1">
                {steps.map((step, index) => (
                  <button
                    key={step.id}
                    onClick={() => setCurrentStep(index)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-left transition-colors ${
                      currentStep === index
                        ? 'bg-primary text-primary-foreground'
                        : 'hover:bg-accent'
                    }`}
                  >
                    <step.icon className="h-5 w-5" />
                    <span>{step.title}</span>
                  </button>
                ))}
              </nav>
            </div>

            {/* Form Content */}
            <div className="col-span-3">
              <Card className="p-6 bg-background">
                <h3 className="text-xl font-semibold mb-4">{steps[currentStep].title}</h3>
                {error && (
                  <Alert variant="destructive" className="mb-4">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
                {renderStepContent()}
              </Card>
            </div>
          </div>
        </CardContent>
        <div className="p-6 border-t border-border flex justify-between">
          <Button variant="outline" onClick={handleBack} disabled={currentStep === 0}>
            <ArrowLeft className="mr-2 h-4 w-4" /> Back
          </Button>
          {currentStep < steps.length - 1 ? (
            <Button onClick={handleNext}>
              Next <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button onClick={handleSubmit}>
              Review & Finalize
            </Button>
          )}
        </div>
      </Card>
    </div>
  )
}


