import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import LoginForm from '@/components/auth/LoginForm.jsx'
import RegisterForm from '@/components/auth/RegisterForm.jsx'
import Dashboard from '@/components/dashboard/Dashboard.jsx'
import { 
  Shield, 
  FileText, 
  Users, 
  Smartphone, 
  Lock, 
  CheckCircle, 
  ArrowRight,
  Heart,
  Home,
  Banknote,
  Globe,
  Menu,
  X
} from 'lucide-react'
import './App.css'

// Landing Page Component
function LandingPage({ onShowLogin, onShowRegister }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <Heart className="h-8 w-8 text-primary" />
              <span className="text-2xl font-bold">LastWish</span>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">
                Features
              </a>
              <a href="#security" className="text-muted-foreground hover:text-foreground transition-colors">
                Security
              </a>
              <a href="#legal" className="text-muted-foreground hover:text-foreground transition-colors">
                Legal
              </a>
              <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </a>
            </nav>

            {/* Desktop Auth Buttons */}
            <div className="hidden md:flex items-center space-x-4">
              <Button variant="ghost" className="text-muted-foreground hover:text-foreground" onClick={onShowLogin}>
                Sign In
              </Button>
              <Button className="bg-primary hover:bg-primary/90 text-primary-foreground" onClick={onShowRegister}>
                Get Started
              </Button>
            </div>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden py-4 border-t border-border">
              <nav className="flex flex-col space-y-4">
                <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">
                  Features
                </a>
                <a href="#security" className="text-muted-foreground hover:text-foreground transition-colors">
                  Security
                </a>
                <a href="#legal" className="text-muted-foreground hover:text-foreground transition-colors">
                  Legal
                </a>
                <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                  Pricing
                </a>
                <div className="flex flex-col space-y-2 pt-4">
                  <Button variant="ghost" className="justify-start" onClick={onShowLogin}>
                    Sign In
                  </Button>
                  <Button className="justify-start bg-primary hover:bg-primary/90" onClick={onShowRegister}>
                    Get Started
                  </Button>
                </div>
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto text-center">
          <div className="max-w-4xl mx-auto">
            <Badge variant="secondary" className="mb-6">
              Trusted by 10,000+ Families
            </Badge>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Secure Your Legacy with{' '}
              <span className="text-primary">LastWish</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Comprehensive digital estate planning platform. Create wills, manage assets, 
              organize digital legacies, and ensure your final wishes are honored.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground" onClick={onShowRegister}>
                Create Your Will
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button size="lg" variant="outline">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              Everything You Need for Estate Planning
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Modern tools for traditional needs. Plan your legacy with confidence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Will Creation */}
            <Card className="border-border bg-card hover:bg-card/80 transition-colors">
              <CardHeader>
                <FileText className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Legal Will Creation</CardTitle>
                <CardDescription>
                  Step-by-step guided process to create legally compliant wills with witness verification.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    State-specific legal compliance
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Digital signature support
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Witness verification system
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Asset Management */}
            <Card className="border-border bg-card hover:bg-card/80 transition-colors">
              <CardHeader>
                <Home className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Asset Management</CardTitle>
                <CardDescription>
                  Organize and distribute all your assets including real estate, investments, and personal property.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Real estate tracking
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Financial account integration
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Beneficiary assignment
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Digital Assets */}
            <Card className="border-border bg-card hover:bg-card/80 transition-colors">
              <CardHeader>
                <Globe className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Digital Legacy</CardTitle>
                <CardDescription>
                  Manage social media accounts, cryptocurrency, and digital assets for the modern age.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Social media management
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Cryptocurrency wallets
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Cloud storage access
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Beneficiary Management */}
            <Card className="border-border bg-card hover:bg-card/80 transition-colors">
              <CardHeader>
                <Users className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Beneficiary Management</CardTitle>
                <CardDescription>
                  Organize family members, friends, and organizations with detailed contact information.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Contact management
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Relationship tracking
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Notification system
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Security */}
            <Card className="border-border bg-card hover:bg-card/80 transition-colors">
              <CardHeader>
                <Shield className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Bank-Level Security</CardTitle>
                <CardDescription>
                  Your sensitive information is protected with enterprise-grade encryption and security.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    End-to-end encryption
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Two-factor authentication
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Secure cloud backup
                  </li>
                </ul>
              </CardContent>
            </Card>

            {/* Mobile Friendly */}
            <Card className="border-border bg-card hover:bg-card/80 transition-colors">
              <CardHeader>
                <Smartphone className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Mobile Friendly</CardTitle>
                <CardDescription>
                  Access your estate planning documents anywhere, anytime with our responsive design.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Responsive design
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Touch-friendly interface
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="h-4 w-4 text-primary mr-2" />
                    Offline access
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Security Section */}
      <section id="security" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto">
          <div className="max-w-4xl mx-auto text-center">
            <Lock className="h-16 w-16 text-primary mx-auto mb-6" />
            <h2 className="text-3xl sm:text-4xl font-bold mb-6">
              Your Privacy is Our Priority
            </h2>
            <p className="text-xl text-muted-foreground mb-12">
              We use the same security standards as major financial institutions to protect your sensitive information.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
              <div className="space-y-4">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <Shield className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">256-bit Encryption</h3>
                <p className="text-muted-foreground">
                  All data is encrypted using AES-256 encryption, the same standard used by banks and government agencies.
                </p>
              </div>
              
              <div className="space-y-4">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <Lock className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">Zero-Knowledge Architecture</h3>
                <p className="text-muted-foreground">
                  We cannot access your sensitive data. Only you and your designated beneficiaries can decrypt your information.
                </p>
              </div>
              
              <div className="space-y-4">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <CheckCircle className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">SOC 2 Compliant</h3>
                <p className="text-muted-foreground">
                  Regular security audits and compliance with industry standards ensure your data remains protected.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-primary/5">
        <div className="container mx-auto text-center">
          <div className="max-w-2xl mx-auto">
            <h2 className="text-3xl sm:text-4xl font-bold mb-6">
              Start Planning Your Legacy Today
            </h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join thousands of families who have secured their future with LastWish.
            </p>
            <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground" onClick={onShowRegister}>
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 border-t border-border">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Heart className="h-6 w-6 text-primary" />
                <span className="text-lg font-bold">LastWish</span>
              </div>
              <p className="text-muted-foreground">
                Secure digital estate planning for the modern family.
              </p>
            </div>
            
            <div className="space-y-4">
              <h3 className="font-semibold">Product</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Security</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">API</a></li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="font-semibold">Legal</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Legal Resources</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Compliance</a></li>
              </ul>
            </div>
            
            <div className="space-y-4">
              <h3 className="font-semibold">Support</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Contact Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Community</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Status</a></li>
              </ul>
            </div>
          </div>
          
          <div className="mt-8 pt-8 border-t border-border text-center text-muted-foreground">
            <p>&copy; 2025 LastWish. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Main App Component
function App() {
  const [currentView, setCurrentView] = useState('landing') // 'landing', 'login', 'register', 'dashboard'
  const [user, setUser] = useState(null)

  // Force dark mode for x.com-like appearance
  useEffect(() => {
    document.documentElement.classList.add('dark')
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
    setCurrentView('dashboard')
  }

  const handleRegister = (userData) => {
    setUser(userData)
    setCurrentView('dashboard')
  }

  const handleLogout = () => {
    setUser(null)
    setCurrentView('landing')
  }

  const showLogin = () => setCurrentView('login')
  const showRegister = () => setCurrentView('register')
  const showLanding = () => setCurrentView('landing')

  return (
    <div className="App">
      {currentView === 'landing' && (
        <LandingPage 
          onShowLogin={showLogin} 
          onShowRegister={showRegister} 
        />
      )}
      
      {currentView === 'login' && (
        <LoginForm 
          onLogin={handleLogin} 
          onSwitchToRegister={showRegister} 
        />
      )}
      
      {currentView === 'register' && (
        <RegisterForm 
          onRegister={handleRegister} 
          onSwitchToLogin={showLogin} 
        />
      )}
      
      {currentView === 'dashboard' && user && (
        <Dashboard 
          user={user} 
          onLogout={handleLogout} 
        />
      )}
    </div>
  )
}

export default App

