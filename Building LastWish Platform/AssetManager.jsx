import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  Home, 
  Car, 
  Banknote, 
  Briefcase, 
  Plus, 
  Edit, 
  Trash2, 
  DollarSign,
  Building,
  Gem,
  Smartphone,
  AlertCircle,
  CheckCircle
} from 'lucide-react'

const assetTypes = [
  { value: 'real_estate', label: 'Real Estate', icon: Home },
  { value: 'vehicle', label: 'Vehicle', icon: Car },
  { value: 'bank_account', label: 'Bank Account', icon: Banknote },
  { value: 'investment', label: 'Investment', icon: Briefcase },
  { value: 'business', label: 'Business', icon: Building },
  { value: 'jewelry', label: 'Jewelry', icon: Gem },
  { value: 'electronics', label: 'Electronics', icon: Smartphone },
  { value: 'other', label: 'Other', icon: DollarSign },
]

function AssetManager() {
  const [assets, setAssets] = useState([
    {
      id: 1,
      type: 'real_estate',
      name: 'Primary Residence',
      description: '123 Main St, Anytown, ST 12345',
      estimatedValue: 350000,
      beneficiaries: ['John Doe Jr.', 'Jane Doe'],
      status: 'verified'
    },
    {
      id: 2,
      type: 'bank_account',
      name: 'Checking Account',
      description: 'First National Bank - Account ending in 1234',
      estimatedValue: 25000,
      beneficiaries: ['John Doe Jr.'],
      status: 'pending'
    }
  ])
  
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingAsset, setEditingAsset] = useState(null)
  const [formData, setFormData] = useState({
    type: '',
    name: '',
    description: '',
    estimatedValue: '',
    beneficiaries: '',
    accountNumber: '',
    location: ''
  })

  const handleAddAsset = () => {
    const newAsset = {
      id: Date.now(),
      type: formData.type,
      name: formData.name,
      description: formData.description,
      estimatedValue: parseFloat(formData.estimatedValue) || 0,
      beneficiaries: formData.beneficiaries.split(',').map(b => b.trim()).filter(b => b),
      status: 'pending'
    }
    setAssets([...assets, newAsset])
    setFormData({
      type: '',
      name: '',
      description: '',
      estimatedValue: '',
      beneficiaries: '',
      accountNumber: '',
      location: ''
    })
    setShowAddForm(false)
  }

  const handleEditAsset = (asset) => {
    setEditingAsset(asset.id)
    setFormData({
      type: asset.type,
      name: asset.name,
      description: asset.description,
      estimatedValue: asset.estimatedValue.toString(),
      beneficiaries: asset.beneficiaries.join(', '),
      accountNumber: '',
      location: ''
    })
    setShowAddForm(true)
  }

  const handleUpdateAsset = () => {
    setAssets(assets.map(asset => 
      asset.id === editingAsset 
        ? {
            ...asset,
            type: formData.type,
            name: formData.name,
            description: formData.description,
            estimatedValue: parseFloat(formData.estimatedValue) || 0,
            beneficiaries: formData.beneficiaries.split(',').map(b => b.trim()).filter(b => b)
          }
        : asset
    ))
    setEditingAsset(null)
    setFormData({
      type: '',
      name: '',
      description: '',
      estimatedValue: '',
      beneficiaries: '',
      accountNumber: '',
      location: ''
    })
    setShowAddForm(false)
  }

  const handleDeleteAsset = (id) => {
    setAssets(assets.filter(asset => asset.id !== id))
  }

  const getAssetIcon = (type) => {
    const assetType = assetTypes.find(t => t.value === type)
    return assetType ? assetType.icon : DollarSign
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'verified': return 'bg-green-500'
      case 'pending': return 'bg-yellow-500'
      case 'incomplete': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const totalValue = assets.reduce((sum, asset) => sum + asset.estimatedValue, 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Asset Management</h2>
          <p className="text-muted-foreground">
            Organize and distribute your assets to beneficiaries
          </p>
        </div>
        <Button onClick={() => setShowAddForm(true)} disabled={showAddForm}>
          <Plus className="mr-2 h-4 w-4" />
          Add Asset
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{assets.length}</div>
            <p className="text-xs text-muted-foreground">
              {assets.filter(a => a.status === 'verified').length} verified
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Value</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalValue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Estimated market value
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Distribution</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round((assets.filter(a => a.beneficiaries.length > 0).length / assets.length) * 100)}%
            </div>
            <p className="text-xs text-muted-foreground">
              Assets assigned to beneficiaries
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Add/Edit Asset Form */}
      {showAddForm && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle>
              {editingAsset ? 'Edit Asset' : 'Add New Asset'}
            </CardTitle>
            <CardDescription>
              Provide details about your asset for estate planning
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="assetType">Asset Type</Label>
                <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
                  <SelectTrigger>
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

              <div className="space-y-2">
                <Label htmlFor="assetName">Asset Name</Label>
                <Input 
                  id="assetName" 
                  placeholder="e.g., Primary Residence, Savings Account"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="assetDescription">Description</Label>
              <Textarea 
                id="assetDescription" 
                placeholder="Detailed description, location, account numbers, etc."
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="estimatedValue">Estimated Value ($)</Label>
                <Input 
                  id="estimatedValue" 
                  type="number"
                  placeholder="0"
                  value={formData.estimatedValue}
                  onChange={(e) => setFormData({...formData, estimatedValue: e.target.value})}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="beneficiaries">Beneficiaries</Label>
                <Input 
                  id="beneficiaries" 
                  placeholder="John Doe, Jane Smith (comma separated)"
                  value={formData.beneficiaries}
                  onChange={(e) => setFormData({...formData, beneficiaries: e.target.value})}
                />
              </div>
            </div>

            <div className="flex space-x-2">
              <Button onClick={editingAsset ? handleUpdateAsset : handleAddAsset}>
                {editingAsset ? 'Update Asset' : 'Add Asset'}
              </Button>
              <Button variant="outline" onClick={() => {
                setShowAddForm(false)
                setEditingAsset(null)
                setFormData({
                  type: '',
                  name: '',
                  description: '',
                  estimatedValue: '',
                  beneficiaries: '',
                  accountNumber: '',
                  location: ''
                })
              }}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Assets List */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Your Assets</h3>
        {assets.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Briefcase className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium mb-2">No assets added yet</h3>
              <p className="text-muted-foreground text-center mb-4">
                Start by adding your first asset to begin estate planning
              </p>
              <Button onClick={() => setShowAddForm(true)}>
                <Plus className="mr-2 h-4 w-4" />
                Add Your First Asset
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {assets.map((asset) => {
              const IconComponent = getAssetIcon(asset.type)
              return (
                <Card key={asset.id} className="hover:bg-accent/50 transition-colors">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <IconComponent className="h-5 w-5 text-primary" />
                        <CardTitle className="text-lg">{asset.name}</CardTitle>
                      </div>
                      <div className="flex items-center space-x-1">
                        <div className={`w-2 h-2 rounded-full ${getStatusColor(asset.status)}`} />
                        <span className="text-xs text-muted-foreground capitalize">
                          {asset.status}
                        </span>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-sm text-muted-foreground">{asset.description}</p>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-semibold">
                        ${asset.estimatedValue.toLocaleString()}
                      </span>
                      <div className="flex space-x-1">
                        <Button size="sm" variant="outline" onClick={() => handleEditAsset(asset)}>
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleDeleteAsset(asset.id)}>
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>

                    {asset.beneficiaries.length > 0 && (
                      <div>
                        <p className="text-xs text-muted-foreground mb-1">Beneficiaries:</p>
                        <div className="flex flex-wrap gap-1">
                          {asset.beneficiaries.map((beneficiary, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {beneficiary}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {asset.beneficiaries.length === 0 && (
                      <Alert>
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription className="text-xs">
                          No beneficiaries assigned to this asset
                        </AlertDescription>
                      </Alert>
                    )}
                  </CardContent>
                </Card>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}



export default AssetManager

