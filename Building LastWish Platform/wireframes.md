# LastWish Platform - Wireframes and Layout Structure

## Page Hierarchy and User Flow

```
Landing Page
├── Sign Up / Login
├── Dashboard (Post-Login)
│   ├── Will Creation Wizard
│   │   ├── Personal Information
│   │   ├── Asset Distribution
│   │   ├── Beneficiaries
│   │   ├── Guardianship
│   │   ├── Executor Selection
│   │   ├── Final Wishes
│   │   └── Review & Execute
│   ├── Document Library
│   ├── Asset Management
│   ├── Beneficiary Management
│   ├── Digital Assets
│   └── Account Settings
└── Legal Resources
```

## 1. Landing Page Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ [LastWish Logo]                    [Login] [Get Started]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              Secure Your Legacy with LastWish              │
│           Comprehensive Digital Estate Planning            │
│                                                             │
│    [Create Your Will]  [Manage Assets]  [Digital Legacy]   │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   Will Creation │ │ Asset Management│ │ Digital Assets  │ │
│  │   • Legal Forms │ │ • Property      │ │ • Social Media  │ │
│  │   • Beneficiary │ │ • Investments   │ │ • Crypto        │ │
│  │   • Guardianship│ │ • Bank Accounts │ │ • Online Accts  │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│                                                             │
│              Trusted by 10,000+ Families                   │
│    [Security Features] [Legal Compliance] [24/7 Support]   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Footer: Privacy | Terms | Legal | Contact | © LastWish     │
└─────────────────────────────────────────────────────────────┘
```

## 2. Dashboard Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ [LastWish] [Dashboard] [Documents] [Assets] [Profile] [⚙️]  │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐                                         │
│ │ Quick Actions   │  Welcome back, [User Name]              │
│ │ • Create Will   │                                         │
│ │ • Add Asset     │  ┌─────────────────────────────────────┐ │
│ │ • Add Benefic.  │  │ Document Status                     │ │
│ │ • Digital Asset │  │ ┌─────┐ Will: 75% Complete         │ │
│ │ • Schedule Rev. │  │ │ ███ │ Power of Attorney: Done    │ │
│ └─────────────────┘  │ └─────┘ Health Directive: Pending  │ │
│                      └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Recent Activity                                         │ │
│ │ • Will updated - 2 days ago                            │ │
│ │ • Asset added: Home - 1 week ago                       │ │
│ │ • Beneficiary added: Jane Doe - 2 weeks ago            │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Assets Summary  │ │ Beneficiaries   │ │ Security Status │ │
│ │ Total: $500K    │ │ Primary: 3      │ │ ✅ Encrypted   │ │
│ │ Real Estate: 2  │ │ Contingent: 2   │ │ ✅ Backed Up   │ │
│ │ Accounts: 5     │ │ Organizations:1 │ │ ✅ Verified    │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 3. Will Creation Wizard Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ [LastWish] [Back to Dashboard]                   [Save Draft]│
├─────────────────────────────────────────────────────────────┤
│ Create Your Will - Step 2 of 7: Asset Distribution         │
│ ●●○○○○○ Progress: 28% Complete                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Asset Distribution                                      │ │
│ │                                                         │ │
│ │ Real Estate                                             │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ 📍 Primary Residence                               │ │ │
│ │ │ 123 Main St, City, State                           │ │ │
│ │ │ Estimated Value: $350,000                          │ │ │
│ │ │ Beneficiary: [Dropdown: Spouse - 100%]            │ │ │
│ │ │ Contingent: [Dropdown: Children - Equal Split]    │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ [+ Add Real Estate]                                     │ │
│ │                                                         │ │
│ │ Financial Assets                                        │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ 🏦 Checking Account - Bank of America              │ │ │
│ │ │ Account: ****1234                                  │ │ │
│ │ │ Estimated Value: $25,000                           │ │ │
│ │ │ Beneficiary: [Dropdown: Spouse - 100%]            │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ [+ Add Financial Asset]                                 │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│                    [Previous] [Next: Beneficiaries]        │
└─────────────────────────────────────────────────────────────┘
```

## 4. Asset Management Page Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ [LastWish] [Dashboard] [Documents] [Assets] [Profile]       │
├─────────────────────────────────────────────────────────────┤
│ Asset Management                                            │
│                                                             │
│ ┌─────────────────┐ [Search Assets...] [Filter ▼] [+ Add]  │
│ │ Categories      │                                         │
│ │ ✓ All Assets    │ ┌─────────────────────────────────────┐ │
│ │ □ Real Estate   │ │ Real Estate                         │ │
│ │ □ Bank Accounts │ │ ┌─────────────────────────────────┐ │ │
│ │ □ Investments   │ │ │ 🏠 Primary Residence           │ │ │
│ │ □ Insurance     │ │ │ 123 Main St, City, State       │ │ │
│ │ □ Vehicles      │ │ │ Value: $350,000                │ │ │
│ │ □ Personal      │ │ │ Beneficiary: Spouse (100%)     │ │ │
│ │ □ Digital       │ │ │ [Edit] [View] [Remove]         │ │ │
│ └─────────────────┘ │ └─────────────────────────────────┘ │ │
│                     │                                     │ │
│                     │ ┌─────────────────────────────────┐ │ │
│                     │ │ 🏖️ Vacation Home              │ │ │
│                     │ │ 456 Beach Ave, Coast, State    │ │ │
│                     │ │ Value: $200,000                │ │ │
│                     │ │ Beneficiary: Children (Split)  │ │ │
│                     │ │ [Edit] [View] [Remove]         │ │ │
│                     │ └─────────────────────────────────┘ │ │
│                     └─────────────────────────────────────┘ │
│                                                             │
│ Total Asset Value: $575,000                                │
│ Assets Assigned: 8/10                                      │
│ Unassigned Value: $25,000                                  │
└─────────────────────────────────────────────────────────────┘
```

## 5. Digital Assets Management Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ [LastWish] Digital Assets                        [+ Add]    │
├─────────────────────────────────────────────────────────────┤
│ Manage Your Digital Legacy                                  │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Social Media Accounts                                   │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ 📘 Facebook                                        │ │ │
│ │ │ Username: john.doe@email.com                       │ │ │
│ │ │ Action: Memorialize Account                        │ │ │
│ │ │ Contact: Jane Doe (Spouse)                         │ │ │
│ │ │ [Edit] [Test Access] [Remove]                      │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ 📷 Instagram                                       │ │ │
│ │ │ Username: @johndoe                                 │ │ │
│ │ │ Action: Delete Account                             │ │ │
│ │ │ Contact: Jane Doe (Spouse)                         │ │ │
│ │ │ [Edit] [Test Access] [Remove]                      │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Cryptocurrency & Digital Wallets                       │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ ₿ Bitcoin Wallet                                   │ │ │
│ │ │ Wallet Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa │ │ │
│ │ │ Estimated Value: $15,000                           │ │ │
│ │ │ Recovery Method: Seed Phrase (Secured)             │ │ │
│ │ │ Beneficiary: Spouse                                │ │ │
│ │ │ [Edit] [View Details] [Remove]                     │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ⚠️ Security Notice: Digital asset information is encrypted │
│ and stored securely. Recovery instructions will be         │
│ provided to designated beneficiaries.                      │
└─────────────────────────────────────────────────────────────┘
```

## 6. Mobile Responsive Layout

```
Mobile View (320px - 767px):
┌─────────────────────┐
│ ☰ LastWish    [👤]  │
├─────────────────────┤
│                     │
│ Welcome, John       │
│                     │
│ ┌─────────────────┐ │
│ │ Will Progress   │ │
│ │ ████████░░ 80%  │ │
│ └─────────────────┘ │
│                     │
│ Quick Actions:      │
│ [Create Will]       │
│ [Add Asset]         │
│ [Add Beneficiary]   │
│                     │
│ Recent Activity:    │
│ • Will updated      │
│ • Asset added       │
│                     │
│ ┌─────────────────┐ │
│ │ Assets: $500K   │ │
│ │ Beneficiaries:5 │ │
│ │ Security: ✅    │ │
│ └─────────────────┘ │
└─────────────────────┘

Tablet View (768px - 1023px):
┌─────────────────────────────────────┐
│ LastWish [Dashboard][Docs][Assets]  │
├─────────────────────────────────────┤
│ Welcome, John                       │
│                                     │
│ ┌─────────────┐ ┌─────────────────┐ │
│ │Quick Actions│ │ Document Status │ │
│ │• Create Will│ │ Will: 80% ████  │ │
│ │• Add Asset  │ │ POA: Done ✅    │ │
│ │• Add Benef. │ │ Health: Pending │ │
│ └─────────────┘ └─────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Recent Activity                 │ │
│ │ • Will updated - 2 days ago     │ │
│ │ • Asset added - 1 week ago      │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Design Principles

### 1. Progressive Disclosure
- Start with essential information
- Reveal details as needed
- Use expandable sections
- Clear information hierarchy

### 2. Trust and Security Indicators
- Visible security badges
- Encryption status indicators
- Legal compliance notices
- Professional design elements

### 3. Accessibility Features
- High contrast ratios (4.5:1 minimum)
- Keyboard navigation support
- Screen reader compatibility
- Clear focus indicators
- Alternative text for images

### 4. Mobile-First Design
- Touch-friendly interface elements
- Simplified navigation for mobile
- Responsive grid system
- Optimized form layouts

### 5. Legal Document Clarity
- Clear section headings
- Plain language explanations
- Visual progress indicators
- Review and confirmation steps

## Navigation Structure

```
Primary Navigation:
- Dashboard (Home)
- Documents (Will, POA, Health Directive)
- Assets (Real Estate, Financial, Personal, Digital)
- Beneficiaries (People, Organizations)
- Settings (Account, Security, Preferences)

Secondary Navigation:
- Help & Support
- Legal Resources
- Account Profile
- Notifications
```

This wireframe structure provides a comprehensive foundation for the LastWish platform, ensuring a user-friendly experience while maintaining the professional standards required for estate planning documentation.

