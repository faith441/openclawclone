# Gmail API Integration for n8n

## Step 1: Set Up Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project**
   ```
   - Click "Select a project" at the top
   - Click "New Project"
   - Name: "n8n Gmail Integration" (or your choice)
   - Click "Create"
   ```

3. **Enable Gmail API**
   ```
   - In the search bar, type "Gmail API"
   - Click on "Gmail API"
   - Click "Enable"
   ```

## Step 2: Create OAuth 2.0 Credentials

1. **Navigate to Credentials**
   ```
   - In the left sidebar, click "APIs & Services" → "Credentials"
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   ```

2. **Configure OAuth Consent Screen** (if first time)
   ```
   - Click "Configure Consent Screen"
   - Select "External" (for public use) or "Internal" (for organization only)
   - Click "Create"
   ```

3. **Fill OAuth Consent Screen Details**
   ```
   App information:
   - App name: "n8n Gmail Automation"
   - User support email: your-email@gmail.com
   - Developer contact: your-email@gmail.com

   Scopes:
   - Click "Add or Remove Scopes"
   - Select Gmail scopes you need:
     ✓ .../auth/gmail.send (Send email)
     ✓ .../auth/gmail.readonly (Read email)
     ✓ .../auth/gmail.compose (Compose email)
     ✓ .../auth/gmail.modify (Modify email)
   - Click "Update"

   Test users (for testing phase):
   - Add your email and test user emails
   - Click "Save and Continue"
   ```

4. **Create OAuth Client ID**
   ```
   - Go back to "Credentials" tab
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "n8n Gmail Client"
   ```

5. **Add Authorized Redirect URIs**
   ```
   Important: Add your n8n OAuth callback URL

   Format: https://your-n8n-domain.com/rest/oauth2-credential/callback

   Examples:
   - Local: http://localhost:5678/rest/oauth2-credential/callback
   - Production: https://n8n.yourdomain.com/rest/oauth2-credential/callback

   Click "Create"
   ```

6. **Save Your Credentials**
   ```
   You'll receive:
   - Client ID: 123456789-abcdefg.apps.googleusercontent.com
   - Client Secret: GOCSPX-xxxxxxxxxxxxx

   ⚠️ IMPORTANT: Copy these immediately!
   ```

## Step 3: Configure n8n

### Method 1: Using n8n UI (Recommended)

1. **Open n8n Credentials**
   ```
   - Go to n8n dashboard
   - Click "Credentials" in the left menu
   - Click "Add Credential"
   - Search for "Gmail OAuth2 API"
   ```

2. **Enter Google OAuth Credentials**
   ```
   - Client ID: [paste from Google Cloud Console]
   - Client Secret: [paste from Google Cloud Console]
   - Click "Connect my account"
   - Sign in with Google
   - Grant permissions
   ```

### Method 2: Using Environment Variables

Add to your `.env` file or n8n configuration:

```bash
# Gmail OAuth Credentials
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxx

# n8n Configuration
N8N_PROTOCOL=https
N8N_HOST=your-n8n-domain.com
WEBHOOK_URL=https://your-n8n-domain.com/
```

Then restart n8n:
```bash
# If using Docker
docker-compose restart n8n

# If using npm
pm2 restart n8n
# or
systemctl restart n8n
```

## Step 4: Test Gmail Integration in n8n

1. **Create a New Workflow**
   ```
   - Click "+" to create new workflow
   - Add a "Gmail" node
   - Select operation (e.g., "Send Email")
   ```

2. **Configure Gmail Node**
   ```
   - Click on Gmail node
   - Credential to connect with: Select your Gmail OAuth2 credential
   - If not connected, click "Create New Credential"
   - Follow OAuth flow to authenticate
   ```

3. **Test Sending Email**
   ```
   Example configuration:
   - To: recipient@example.com
   - Subject: Test from n8n
   - Message: This is a test email sent via n8n!
   - Click "Execute Node" to test
   ```

## Step 5: Publishing Your App (Production)

If you want users to authenticate without "unverified app" warnings:

1. **Submit App for Verification**
   ```
   - Go to OAuth consent screen
   - Click "Publish App"
   - Fill out verification form
   - Submit privacy policy URL
   - Submit terms of service URL
   - Wait for Google review (1-2 weeks)
   ```

2. **Add Privacy Policy** (Required)
   - Create a page explaining data usage
   - Host at: https://yourdomain.com/privacy
   - Must describe:
     * What Gmail data you access
     * How you use the data
     * How you protect user data
     * Data retention policy

## Common Issues & Solutions

### Issue 1: "Redirect URI Mismatch"
```
Solution:
- Verify OAuth redirect URI in Google Console matches exactly:
  http://localhost:5678/rest/oauth2-credential/callback (local)
  https://yourdomain.com/rest/oauth2-credential/callback (production)
```

### Issue 2: "Access Blocked: This app's request is invalid"
```
Solution:
- Add your email to "Test users" in OAuth consent screen
- Make sure app is in "Testing" mode for development
```

### Issue 3: "Insufficient Scopes"
```
Solution:
- Go to OAuth consent screen → Scopes
- Add required Gmail scopes:
  - .../auth/gmail.send
  - .../auth/gmail.readonly
  - .../auth/gmail.modify
```

### Issue 4: n8n Can't Connect
```
Solution:
- Check N8N_PROTOCOL and N8N_HOST environment variables
- Verify WEBHOOK_URL is set correctly
- Restart n8n after changing environment variables
```

## Security Best Practices

1. **Never commit credentials to Git**
   ```bash
   # Add to .gitignore
   .env
   config/credentials.json
   ```

2. **Use Environment Variables**
   ```bash
   # Instead of hardcoding in n8n
   export GOOGLE_CLIENT_ID="your-client-id"
   export GOOGLE_CLIENT_SECRET="your-client-secret"
   ```

3. **Restrict OAuth Scopes**
   - Only request Gmail scopes you actually need
   - Use minimal permissions principle

4. **Enable 2FA**
   - Require 2-factor authentication for admin accounts

5. **Monitor API Usage**
   - Check Google Cloud Console for unusual activity
   - Set up quota alerts

## Example n8n Workflow: Auto-Reply to Gmail

```json
{
  "nodes": [
    {
      "parameters": {
        "triggerOn": "messageReceived",
        "filters": {
          "sender": "specific-sender@example.com"
        }
      },
      "name": "Gmail Trigger",
      "type": "n8n-nodes-base.gmailTrigger",
      "position": [250, 300],
      "credentials": {
        "gmailOAuth2": {
          "id": "1",
          "name": "Gmail OAuth2 account"
        }
      }
    },
    {
      "parameters": {
        "resource": "message",
        "operation": "send",
        "to": "={{$json['payload']['headers'].find(h => h.name === 'From')['value']}}",
        "subject": "Re: {{$json['payload']['headers'].find(h => h.name === 'Subject')['value']}}",
        "message": "Thank you for your email. We'll get back to you soon!"
      },
      "name": "Send Auto-Reply",
      "type": "n8n-nodes-base.gmail",
      "position": [450, 300],
      "credentials": {
        "gmailOAuth2": {
          "id": "1",
          "name": "Gmail OAuth2 account"
        }
      }
    }
  ],
  "connections": {
    "Gmail Trigger": {
      "main": [[{"node": "Send Auto-Reply", "type": "main", "index": 0}]]
    }
  }
}
```

## Resources

- **Google Cloud Console**: https://console.cloud.google.com/
- **n8n Gmail Documentation**: https://docs.n8n.io/integrations/builtin/credentials/google/oauth-generic/
- **Gmail API Reference**: https://developers.google.com/gmail/api/reference/rest
- **OAuth 2.0 Guide**: https://developers.google.com/identity/protocols/oauth2

## Quick Setup Checklist

- [ ] Create Google Cloud Project
- [ ] Enable Gmail API
- [ ] Configure OAuth Consent Screen
- [ ] Create OAuth 2.0 Client ID
- [ ] Add authorized redirect URI
- [ ] Copy Client ID and Client Secret
- [ ] Add credentials to n8n
- [ ] Test OAuth flow
- [ ] Create test workflow
- [ ] Verify email sending/reading works
- [ ] (Optional) Publish app for verification

---

**Need Help?**
- n8n Community: https://community.n8n.io/
- Google Cloud Support: https://cloud.google.com/support
