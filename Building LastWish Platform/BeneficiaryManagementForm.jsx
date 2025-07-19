import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Users, Plus, Edit, Trash2, Save, X, CheckCircle, AlertCircle, Phone, Mail, MapPin, Heart, User } from 'lucide-react'

const BeneficiaryManagementForm = ({ onClose }) => {
  const [beneficiaries, setBeneficiaries] = useState([
    {
      id: 1,
      name: 'Sarah Johnson',
      relationship: 'spouse',
      email: 'sarah.johnson@email.com',
      phone: '(555) 123-4567',
      address: '123 Main Street, Anytown, ST 12345',
      dateOfBirth: '1985-03-15',
      percentage: 50,
      guardian: '',
      notes: 'Primary beneficiary and executor',
      status: 'verified'
    },
    {
      id: 2,
      name: 'Michael Johnson',
      relationship: 'child',
      email: 'michael.johnson@email.com',
      phone: '(555) 234-5678',
      address: '456 Oak Avenue, Anytown, ST 12345',
      dateOfBirth: '2010-07-22',
      percentage: 25,
      guardian: 'Sarah Johnson',
      notes: 'Minor child - requires guardian',
      status: 'pending'
    },
    {
      id: 3,
      name: 'Emily Johnson',
      relationship: 'child',
      email: 'emily.johnson@email.com',
      phone: '(555) 345-6789',
      address: '456 Oak Avenue, Anytown, ST 12345',
      dateOfBirth: '2012-11-08',
      percentage: 25,
      guardian: 'Sarah Johnson',
      notes: 'Minor child - requires guardian',
      status: 'verified'
    }
  ])

  const [showAddForm, setShowAddForm] = useState(false)
  const [editingBeneficiary, setEditingBeneficiary] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    relationship: '',
    email: '',
    phone: '',
    address: '',
    dateOfBirth: '',
    percentage: 0,
    guardian: '',
    notes: '',
    status: 'pending'
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState('')

  const relationships = [
    { value: 'spouse', label: 'Spouse/Partner', icon: Heart },
    { value: 'child', label: 'Child', icon: User },
    { value: 'parent', label: 'Parent', icon: User },
    { value: 'sibling', label: 'Sibling', icon: User },
    { value: 'grandchild', label: 'Grandchild', icon: User },
    { value: 'friend', label: 'Friend', icon: User },
    { value: 'charity', label: 'Charity/Organization', icon: Heart },
    { value: 'other', label: 'Other', icon: User }
  ]

  const resetForm = () => {
    setFormData({
      name: '',
      relationship: '',
      email: '',
      phone: '',
      address: '',
      dateOfBirth: '',
      percentage: 0,
      guardian: '',
      notes: '',
      status: 'pending'
    })
    setEditingBeneficiary(null)
    setShowAddForm(false)
    setMessage('')
  }

  const handleEdit = (beneficiary) => {
    setFormData({
      name: beneficiary.name,
      relationship: beneficiary.relationship,
      email: beneficiary.email,
      phone: beneficiary.phone,
      address: beneficiary.address,
      dateOfBirth: beneficiary.dateOfBirth,
      percentage: beneficiary.percentage,
      guardian: beneficiary.guardian,
      notes: beneficiary.notes,
      status: beneficiary.status
    })
    setEditingBeneficiary(beneficiary.id)
    setShowAddForm(true)
  }

  const handleDelete = async (beneficiaryId) => {
    if (window.confirm('Are you sure you want to remove this beneficiary?')) {
      setIsSubmitting(true)
      
      try {
        // Trigger n8n workflow for beneficiary deletion
        await triggerN8NBeneficiaryAction('delete', { beneficiaryId })
        
        setBeneficiaries(beneficiaries.filter(beneficiary => beneficiary.id !== beneficiaryId))
        setMessage('Beneficiary removed successfully!')
        setTimeout(() => setMessage(''), 3000)
      } catch (error) {
        setMessage('Error removing beneficiary. Please try again.')
      } finally {
        setIsSubmitting(false)
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setMessage('')

    try {
      const beneficiaryData = {
        ...formData,
        percentage: parseFloat(formData.percentage),
        id: editingBeneficiary || Date.now()
      }

      // Trigger n8n workflow for beneficiary management
      const action = editingBeneficiary ? 'update' : 'create'
      await triggerN8NBeneficiaryAction(action, beneficiaryData)

      if (editingBeneficiary) {
        setBeneficiaries(beneficiaries.map(beneficiary => 
          beneficiary.id === editingBeneficiary ? beneficiaryData : beneficiary
        ))
        setMessage('Beneficiary updated successfully!')
      } else {
        setBeneficiaries([...beneficiaries, beneficiaryData])
        setMessage('Beneficiary added successfully!')
      }

      resetForm()
      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      setMessage('Error saving beneficiary. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  // Trigger n8n workflow for beneficiary actions
  const triggerN8NBeneficiaryAction = async (action, beneficiaryData) => {
    try {
      const response = await fetch('/api/n8n/beneficiary-management', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: action,
          beneficiary: beneficiaryData,
          userId: 'demo-user',
          timestamp: new Date().toISOString()
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to trigger n8n workflow')
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error triggering n8n workflow:', error)
      throw error
    }
  }

  const calculateAge = (dateOfBirth) => {
    const today = new Date()
    const birthDate = new Date(dateOfBirth)
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }
    
    return age
  }

  const isMinor = (dateOfBirth) => {
    return calculateAge(dateOfBirth) < 18
  }

  const getTotalPercentage = () => {
    return beneficiaries.reduce((total, beneficiary) => total + beneficiary.percentage, 0)
  }

  const getRelationshipIcon = (relationship) => {
    const rel = relationships.find(r => r.value === relationship)
    return rel ? rel.icon : User
  }

  const getRelationshipLabel = (relationship) => {
    const rel = relationships.find(r => r.value === relationship)
    return rel ? rel.label : 'Unknown'
  }

  const availableGuardians = beneficiaries.filter(b => 
    !isMinor(b.dateOfBirth) && b.relationship !== 'charity'
  )

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-lg w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-white flex items-center">
              <Users className="h-8 w-8 text-purple-500 mr-3" />
              Beneficiary Management
            </h1>
            <Button variant="ghost" onClick={onClose} className="text-gray-400 hover:text-white">
              ✕
            </Button>
          </div>
          
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="bg-purple-500/10 text-purple-400 border-purple-500/20">
              🤖 n8n Powered Beneficiary Tracking
            </Badge>
            <div className="text-right">
              <p className="text-gray-400 text-sm">Total Inheritance Allocation</p>
              <p className={`text-2xl font-bold ${getTotalPercentage() === 100 ? 'text-green-400' : 'text-yellow-400'}`}>
                {getTotalPercentage()}%
              </p>
            </div>
          </div>
        </div>
        
        <div className="p-6">
          {message && (
            <Alert className={`mb-6 ${message.includes('Error') ? 'bg-red-500/10 border-red-500/20' : 'bg-green-500/10 border-green-500/20'}`}>
              {message.includes('Error') ? 
                <AlertCircle className="h-4 w-4 text-red-500" /> : 
                <CheckCircle className="h-4 w-4 text-green-500" />
              }
              <AlertDescription className={message.includes('Error') ? 'text-red-400' : 'text-green-400'}>
                {message}
              </AlertDescription>
            </Alert>
          )}

          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-white">Your Beneficiaries</h2>
            <Button 
              onClick={() => setShowAddForm(true)}
              className="bg-purple-500 hover:bg-purple-600"
              disabled={isSubmitting}
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Beneficiary
            </Button>
          </div>

          {/* Beneficiary List */}
          <div className="grid gap-4 mb-8">
            {beneficiaries.map((beneficiary) => {
              const IconComponent = getRelationshipIcon(beneficiary.relationship)
              const age = calculateAge(beneficiary.dateOfBirth)
              const minor = isMinor(beneficiary.dateOfBirth)
              
              return (
                <Card key={beneficiary.id} className="bg-gray-800 border-gray-600">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="p-3 rounded-lg bg-purple-500/10">
                          <IconComponent className="h-6 w-6 text-purple-500" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="text-white font-semibold">{beneficiary.name}</h3>
                            <Badge variant="secondary" className="bg-gray-700 text-gray-300">
                              {getRelationshipLabel(beneficiary.relationship)}
                            </Badge>
                            {minor && (
                              <Badge variant="secondary" className="bg-yellow-500/10 text-yellow-400">
                                Minor ({age} years)
                              </Badge>
                            )}
                            <Badge 
                              variant="secondary" 
                              className={`${beneficiary.status === 'verified' ? 'bg-green-500/10 text-green-400' : 'bg-yellow-500/10 text-yellow-400'}`}
                            >
                              {beneficiary.status}
                            </Badge>
                          </div>
                          
                          <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-400">
                            <div className="space-y-1">
                              <div className="flex items-center">
                                <Mail className="h-4 w-4 mr-2" />
                                {beneficiary.email}
                              </div>
                              <div className="flex items-center">
                                <Phone className="h-4 w-4 mr-2" />
                                {beneficiary.phone}
                              </div>
                            </div>
                            <div className="space-y-1">
                              <div className="flex items-center">
                                <MapPin className="h-4 w-4 mr-2" />
                                {beneficiary.address}
                              </div>
                              {beneficiary.guardian && (
                                <div className="flex items-center">
                                  <User className="h-4 w-4 mr-2" />
                                  Guardian: {beneficiary.guardian}
                                </div>
                              )}
                            </div>
                          </div>
                          
                          <div className="mt-3 flex items-center space-x-4">
                            <span className="text-white font-medium">Inheritance: {beneficiary.percentage}%</span>
                            {beneficiary.notes && (
                              <span className="text-gray-400 text-sm">• {beneficiary.notes}</span>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleEdit(beneficiary)}
                          className="border-gray-600 text-white hover:bg-gray-700"
                          disabled={isSubmitting}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDelete(beneficiary.id)}
                          className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
                          disabled={isSubmitting}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>

          {/* Add/Edit Beneficiary Form */}
          {showAddForm && (
            <Card className="bg-gray-800 border-gray-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Plus className="h-5 w-5 text-purple-500 mr-2" />
                  {editingBeneficiary ? 'Edit Beneficiary' : 'Add New Beneficiary'}
                </CardTitle>
                <CardDescription className="text-gray-400">
                  {editingBeneficiary ? 'Update beneficiary information' : 'Add a new beneficiary to your estate plan'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name" className="text-white">Full Name *</Label>
                      <Input
                        id="name"
                        value={formData.name}
                        onChange={(e) => setFormData({...formData, name: e.target.value})}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="e.g., Sarah Johnson"
                        required
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="relationship" className="text-white">Relationship *</Label>
                      <Select 
                        value={formData.relationship} 
                        onValueChange={(value) => setFormData({...formData, relationship: value})}
                        required
                      >
                        <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                          <SelectValue placeholder="Select relationship" />
                        </SelectTrigger>
                        <SelectContent>
                          {relationships.map((rel) => (
                            <SelectItem key={rel.value} value={rel.value}>
                              <div className="flex items-center space-x-2">
                                <rel.icon className="h-4 w-4" />
                                <span>{rel.label}</span>
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="email" className="text-white">Email Address</Label>
                      <Input
                        id="email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="email@example.com"
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="phone" className="text-white">Phone Number</Label>
                      <Input
                        id="phone"
                        value={formData.phone}
                        onChange={(e) => setFormData({...formData, phone: e.target.value})}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="(555) 123-4567"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="address" className="text-white">Address</Label>
                    <Textarea
                      id="address"
                      value={formData.address}
                      onChange={(e) => setFormData({...formData, address: e.target.value})}
                      className="bg-gray-700 border-gray-600 text-white"
                      placeholder="Full address including city, state, and zip code"
                      rows={2}
                    />
                  </div>
                  
                  <div className="grid md:grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="dateOfBirth" className="text-white">Date of Birth</Label>
                      <Input
                        id="dateOfBirth"
                        type="date"
                        value={formData.dateOfBirth}
                        onChange={(e) => setFormData({...formData, dateOfBirth: e.target.value})}
                        className="bg-gray-700 border-gray-600 text-white"
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="percentage" className="text-white">Inheritance % *</Label>
                      <Input
                        id="percentage"
                        type="number"
                        min="0"
                        max="100"
                        step="0.1"
                        value={formData.percentage}
                        onChange={(e) => setFormData({...formData, percentage: parseFloat(e.target.value)})}
                        className="bg-gray-700 border-gray-600 text-white"
                        required
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="guardian" className="text-white">Guardian (if minor)</Label>
                      <Select 
                        value={formData.guardian} 
                        onValueChange={(value) => setFormData({...formData, guardian: value})}
                      >
                        <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                          <SelectValue placeholder="Select guardian" />
                        </SelectTrigger>
                        <SelectContent>
                          {availableGuardians.map((guardian) => (
                            <SelectItem key={guardian.id} value={guardian.name}>
                              {guardian.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="notes" className="text-white">Notes</Label>
                    <Textarea
                      id="notes"
                      value={formData.notes}
                      onChange={(e) => setFormData({...formData, notes: e.target.value})}
                      className="bg-gray-700 border-gray-600 text-white"
                      placeholder="Special instructions, conditions, or notes"
                      rows={3}
                    />
                  </div>
                  
                  <div className="flex justify-end space-x-3">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={resetForm}
                      className="border-gray-600 text-white hover:bg-gray-700"
                      disabled={isSubmitting}
                    >
                      <X className="h-4 w-4 mr-2" />
                      Cancel
                    </Button>
                    <Button
                      type="submit"
                      className="bg-purple-500 hover:bg-purple-600"
                      disabled={isSubmitting}
                    >
                      <Save className="h-4 w-4 mr-2" />
                      {isSubmitting ? 'Saving...' : (editingBeneficiary ? 'Update Beneficiary' : 'Add Beneficiary')}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default BeneficiaryManagementForm

