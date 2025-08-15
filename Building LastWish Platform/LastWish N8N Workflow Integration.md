# LastWish N8N Workflow Integration

This directory contains n8n workflows that automate various estate planning processes for the LastWish platform. These workflows integrate with the LastWish API to provide automated document generation, beneficiary notifications, and legal compliance checking.

## Overview

The LastWish platform uses n8n workflows to automate complex estate planning processes, ensuring users receive timely notifications, documents are generated automatically, and legal compliance is maintained.

## Available Workflows

### 1. Will Document Generation (`will-document-generation.json`)

**Purpose**: Automatically generates will documents when a user completes their will creation process.

**Trigger**: Webhook triggered when a will is created in the LastWish platform
**Webhook URL**: `http://your-n8n-instance/webhook/will-created`

**Process Flow**:
1. Receives webhook notification when will is created
2. Fetches user's estate planning data from LastWish API
3. Generates formatted will document using user's assets and beneficiaries
4. Sends notification email to user with document details
5. Returns success response

**Key Features**:
- Automatic document generation with legal formatting
- Asset and beneficiary integration
- Estate value calculation
- User notification system
- Witness signature placeholders

### 2. Beneficiary Notification (`beneficiary-notification.json`)

**Purpose**: Automatically notifies beneficiaries when they are added to an estate plan.

**Trigger**: Webhook triggered when a beneficiary is added
**Webhook URL**: `http://your-n8n-instance/webhook/beneficiary-added`

**Process Flow**:
1. Receives webhook notification when beneficiary is added
2. Checks if beneficiary has email address
3. Generates personalized notification email based on relationship
4. Sends email to beneficiary informing them of their designation
5. Sends confirmation email to estate owner
6. Handles cases where beneficiary has no email

**Key Features**:
- Personalized messages based on relationship type
- Minor beneficiary handling with guardian information
- Dual notification system (beneficiary + estate owner)
- Email validation and fallback handling

### 3. Legal Compliance Check (`legal-compliance-check.json`)

**Purpose**: Performs weekly compliance checks on all estate plans to identify legal issues.

**Trigger**: Scheduled trigger (every Monday at 9 AM)

**Process Flow**:
1. Runs weekly on schedule
2. Fetches all users from LastWish platform
3. Performs compliance check for each user
4. Identifies issues like missing wills, unassigned assets, minors without guardians
5. Sends compliance reports to users with issues
6. Generates summary report of platform-wide compliance

**Key Features**:
- Automated weekly compliance monitoring
- Issue categorization by severity (high, medium, low)
- Compliance scoring system
- Personalized recommendations
- Platform-wide compliance reporting

## API Endpoints

The workflows interact with the following LastWish API endpoints:

### Webhook Endpoints
- `POST /api/n8n/webhook/will-created` - Will creation webhook
- `POST /api/n8n/webhook/beneficiary-added` - Beneficiary addition webhook
- `POST /api/n8n/webhook/asset-updated` - Asset update webhook

### API Endpoints
- `POST /api/n8n/api/generate-document` - Document generation
- `POST /api/n8n/api/send-notification` - Notification sending
- `POST /api/n8n/api/legal-compliance-check` - Compliance checking
- `GET /api/n8n/health` - Health check

## Setup Instructions

### Prerequisites
1. N8N instance running and accessible
2. LastWish backend running on `http://localhost:5000`
3. Email service configured in n8n (for notifications)

### Installation Steps

1. **Import Workflows**
   ```bash
   # Import each workflow JSON file into your n8n instance
   # Via n8n UI: Settings > Import from file
   ```

2. **Configure Webhook URLs**
   - Update the LastWish frontend to call the webhook URLs when:
     - A will is created
     - A beneficiary is added
     - An asset is updated

3. **Set Environment Variables**
   ```bash
   # In your n8n environment
   LASTWISH_API_URL=http://localhost:5000
   LASTWISH_WEBHOOK_SECRET=your-webhook-secret
   ```

4. **Configure Email Service**
   - Set up email credentials in n8n
   - Configure SMTP settings for notification sending

5. **Test Workflows**
   - Create a test will in LastWish platform
   - Add a test beneficiary
   - Verify webhook triggers and email notifications

### Frontend Integration

Add webhook calls to your React components:

```javascript
// In WillCreationWizard.jsx
const handleSubmit = async () => {
  // Save will to database
  const willResponse = await saveWill(formData);
  
  // Trigger n8n workflow
  await fetch('http://your-n8n-instance/webhook/will-created', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: user.id,
      will_id: willResponse.id
    })
  });
};

// In BeneficiaryManager.jsx
const handleAddBeneficiary = async () => {
  // Save beneficiary to database
  const beneficiaryResponse = await saveBeneficiary(formData);
  
  // Trigger n8n workflow
  await fetch('http://your-n8n-instance/webhook/beneficiary-added', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: user.id,
      beneficiary_id: beneficiaryResponse.id
    })
  });
};
```

## Workflow Customization

### Adding New Workflows

1. **Create New Workflow**
   - Design workflow in n8n UI
   - Export as JSON
   - Add to this directory

2. **Add API Endpoint**
   - Create new route in `n8n_integration.py`
   - Add business logic
   - Register blueprint in main app

3. **Update Documentation**
   - Add workflow description
   - Document API endpoints
   - Update setup instructions

### Modifying Existing Workflows

1. **Update Workflow Logic**
   - Modify nodes in n8n UI
   - Test thoroughly
   - Export updated JSON

2. **Update API Endpoints**
   - Modify backend routes as needed
   - Ensure backward compatibility
   - Update error handling

## Security Considerations

1. **Webhook Security**
   - Use webhook secrets for authentication
   - Validate incoming webhook data
   - Implement rate limiting

2. **Data Privacy**
   - Encrypt sensitive data in transit
   - Limit data exposure in logs
   - Implement proper access controls

3. **Email Security**
   - Use secure SMTP connections
   - Validate email addresses
   - Implement anti-spam measures

## Monitoring and Logging

1. **Workflow Monitoring**
   - Monitor workflow execution status
   - Set up alerts for failures
   - Track performance metrics

2. **API Monitoring**
   - Monitor API endpoint health
   - Track response times
   - Log errors and exceptions

3. **Email Delivery**
   - Monitor email delivery rates
   - Track bounce rates
   - Handle delivery failures

## Troubleshooting

### Common Issues

1. **Webhook Not Triggering**
   - Check webhook URL configuration
   - Verify network connectivity
   - Check n8n webhook settings

2. **Email Not Sending**
   - Verify SMTP configuration
   - Check email credentials
   - Review email content for spam triggers

3. **API Errors**
   - Check LastWish backend status
   - Verify API endpoint URLs
   - Review request/response data

### Debug Steps

1. **Check N8N Execution Log**
   ```bash
   # View workflow execution history in n8n UI
   # Check for error messages and failed nodes
   ```

2. **Check LastWish Backend Logs**
   ```bash
   # Check Flask application logs
   tail -f /path/to/lastwish-backend/logs/app.log
   ```

3. **Test API Endpoints**
   ```bash
   # Test API endpoints directly
   curl -X POST http://localhost:5000/api/n8n/health
   ```

## Support

For issues with n8n workflow integration:

1. Check this documentation
2. Review n8n execution logs
3. Test API endpoints independently
4. Contact LastWish support team

## Contributing

To contribute new workflows or improvements:

1. Create workflow in n8n
2. Test thoroughly
3. Export as JSON
4. Update documentation
5. Submit pull request

---

**Note**: These workflows are designed for the LastWish estate planning platform and require proper setup of both the LastWish backend API and n8n instance for full functionality.

