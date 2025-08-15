import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Home, Car, Building, Coins, Briefcase, Plus, Edit, Trash2, Save, X, CheckCircle, AlertCircle } from 'lucide-react'

const AssetManagementForm = ({ onClose }) => {
  const [assets, setAssets] = useState([
    {
      id: 1,
      type: 'real_estate',
      name: 'Primary Residence',
      description: '123 Main Street, Anytown, ST 12345',
      value: 350000,
      beneficiary: 'Sarah Johnson',
      percentage: 100,
      status: 'verified'
    },
    {
      id: 2,
      type: 'vehicle',
      name: '2020 Toyota Camry',
      description: 'VIN: 1234567890ABCDEF',
      value: 25000,
      beneficiary: 'Michael Johnson',
      percentage: 100,
      status: 'pending'
    }
  ])

  const [showAddForm, setShowAddForm] = useState(false)
  const [editingAsset, setEditingAsset] = useState(null)
  const [formData, setFormData] = useState({
    type: '',
    name: '',
    description: '',
    value: '',
    beneficiary: '',
    percentage: 100,
    status: 'pending'
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState('')

  const assetTypes = [
    { value: 'real_estate', label: 'Real Estate', icon: Home, color: 'blue' },
    { value: 'vehicle', label: 'Vehicle', icon: Car, color: 'green' },
    { value: 'bank_account', label: 'Bank Account', icon: Building, color: 'purple' },
    { value: 'investment', label: 'Investment', icon: Coins, color: 'yellow' },
    { value: 'business', label: 'Business Asset', icon: Briefcase, color: 'orange' }
  ]

  const beneficiaries = [
    'Sarah Johnson (Spouse)',
    'Michael Johnson (Son)',
    'Emily Johnson (Daughter)',
    'Robert Smith (Brother)',
    'Charity Foundation'
  ]

  const resetForm = () => {
    setFormData({
      type: '',
      name: '',
      description: '',
      value: '',
      beneficiary: '',
      percentage: 100,
      status: 'pending'
    })
    setEditingAsset(null)
    setShowAddForm(false)
    setMessage('')
  }

  const handleEdit = (asset) => {
    setFormData({
      type: asset.type,
      name: asset.name,
      description: asset.description,
      value: asset.value,
      beneficiary: asset.beneficiary,
      percentage: asset.percentage,
      status: asset.status
    })
    setEditingAsset(asset.id)
    setShowAddForm(true)
  }

  const handleDelete = async (assetId) => {
    if (window.confirm('Are you sure you want to delete this asset?')) {
      setIsSubmitting(true)
      
      try {
        // Trigger n8n workflow for asset deletion
        await triggerN8NAssetAction('delete', { assetId })
        
        setAssets(assets.filter(asset => asset.id !== assetId))
        setMessage('Asset deleted successfully!')
        setTimeout(() => setMessage(''), 3000)
      } catch (error) {
        setMessage('Error deleting asset. Please try again.')
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
      const assetData = {
        ...formData,
        value: parseFloat(formData.value),
        id: editingAsset || Date.now()
      }

      // Trigger n8n workflow for asset management
      const action = editingAsset ? 'update' : 'create'
      await triggerN8NAssetAction(action, assetData)

      if (editingAsset) {
        setAssets(assets.map(asset => 
          asset.id === editingAsset ? assetData : asset
        ))
        setMessage('Asset updated successfully!')
      } else {
        setAssets([...assets, assetData])
        setMessage('Asset added successfully!')
      }

      resetForm()
      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      setMessage('Error saving asset. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  // Trigger n8n workflow for asset actions
  const triggerN8NAssetAction = async (action, assetData) => {
    try {
      const response = await fetch('/api/n8n/asset-management', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: action,
          asset: assetData,
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

  const getAssetIcon = (type) => {
    const assetType = assetTypes.find(t => t.value === type)
    return assetType ? assetType.icon : Home
  }

  const getAssetColor = (type) => {
    const assetType = assetTypes.find(t => t.value === type)
    return assetType ? assetType.color : 'gray'
  }

  const getTotalValue = () => {
    return assets.reduce((total, asset) => total + asset.value, 0)
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-lg w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-white flex items-center">
              <Home className="h-8 w-8 text-orange-500 mr-3" />
              Asset Management
            </h1>
            <Button variant="ghost" onClick={onClose} className="text-gray-400 hover:text-white">
              ✕
            </Button>
          </div>
          
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="bg-orange-500/10 text-orange-400 border-orange-500/20">
              🤖 n8n Powered Asset Tracking
            </Badge>
            <div className="text-right">
              <p className="text-gray-400 text-sm">Total Portfolio Value</p>
              <p className="text-2xl font-bold text-white">${getTotalValue().toLocaleString()}</p>
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
            <h2 className="text-xl font-semibold text-white">Your Assets</h2>
            <Button 
              onClick={() => setShowAddForm(true)}
              className="bg-orange-500 hover:bg-orange-600"
              disabled={isSubmitting}
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Asset
            </Button>
          </div>

          {/* Asset List */}
          <div className="grid gap-4 mb-8">
            {assets.map((asset) => {
              const IconComponent = getAssetIcon(asset.type)
              const color = getAssetColor(asset.type)
              
              return (
                <Card key={asset.id} className="bg-gray-800 border-gray-600">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className={`p-3 rounded-lg bg-${color}-500/10`}>
                          <IconComponent className={`h-6 w-6 text-${color}-500`} />
                        </div>
                        <div>
                          <h3 className="text-white font-semibold">{asset.name}</h3>
                          <p className="text-gray-400 text-sm">{asset.description}</p>
                          <div className="flex items-center space-x-4 mt-2">
                            <span className="text-white font-medium">${asset.value.toLocaleString()}</span>
                            <span className="text-gray-400">→ {asset.beneficiary} ({asset.percentage}%)</span>
                            <Badge 
                              variant="secondary" 
                              className={`${asset.status === 'verified' ? 'bg-green-500/10 text-green-400' : 'bg-yellow-500/10 text-yellow-400'}`}
                            >
                              {asset.status}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleEdit(asset)}
                          className="border-gray-600 text-white hover:bg-gray-700"
                          disabled={isSubmitting}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDelete(asset.id)}
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

          {/* Add/Edit Asset Form */}
          {showAddForm && (
            <Card className="bg-gray-800 border-gray-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Plus className="h-5 w-5 text-orange-500 mr-2" />
                  {editingAsset ? 'Edit Asset' : 'Add New Asset'}
                </CardTitle>
                <CardDescription className="text-gray-400">
                  {editingAsset ? 'Update asset information' : 'Add a new asset to your estate plan'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="type" className="text-white">Asset Type *</Label>
                      <Select 
                        value={formData.type} 
                        onValueChange={(value) => setFormData({...formData, type: value})}
                        required
                      >
                        <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                          <SelectValue placeholder="Select asset type" />
                        </SelectTrigger>
                        <SelectContent>
                          {assetTypes.map((type) => (
                            <SelectItem key={type.value} value={type.value}>
                              <div className="flex items-center space-x-2">
                                <type.icon className="h-4 w-4" />
                                <span>{type.label}</span>
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label htmlFor="name" className="text-white">Asset Name *</Label>
                      <Input
                        id="name"
                        value={formData.name}
                        onChange={(e) => setFormData({...formData, name: e.target.value})}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="e.g., Primary Residence"
                        required
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="description" className="text-white">Description</Label>
                    <Textarea
                      id="description"
                      value={formData.description}
                      onChange={(e) => setFormData({...formData, description: e.target.value})}
                      className="bg-gray-700 border-gray-600 text-white"
                      placeholder="Detailed description, address, account numbers, etc."
                      rows={3}
                    />
                  </div>
                  
                  <div className="grid md:grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="value" className="text-white">Estimated Value *</Label>
                      <Input
                        id="value"
                        type="number"
                        value={formData.value}
                        onChange={(e) => setFormData({...formData, value: e.target.value})}
                        className="bg-gray-700 border-gray-600 text-white"
                        placeholder="0"
                        required
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="beneficiary" className="text-white">Primary Beneficiary *</Label>
                      <Select 
                        value={formData.beneficiary} 
                        onValueChange={(value) => setFormData({...formData, beneficiary: value})}
                        required
                      >
                        <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                          <SelectValue placeholder="Select beneficiary" />
                        </SelectTrigger>
                        <SelectContent>
                          {beneficiaries.map((beneficiary) => (
                            <SelectItem key={beneficiary} value={beneficiary}>
                              {beneficiary}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label htmlFor="percentage" className="text-white">Inheritance %</Label>
                      <Input
                        id="percentage"
                        type="number"
                        min="1"
                        max="100"
                        value={formData.percentage}
                        onChange={(e) => setFormData({...formData, percentage: parseInt(e.target.value)})}
                        className="bg-gray-700 border-gray-600 text-white"
                      />
                    </div>
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
                      className="bg-orange-500 hover:bg-orange-600"
                      disabled={isSubmitting}
                    >
                      <Save className="h-4 w-4 mr-2" />
                      {isSubmitting ? 'Saving...' : (editingAsset ? 'Update Asset' : 'Add Asset')}
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

export default AssetManagementForm

