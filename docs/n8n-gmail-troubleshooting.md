# n8n Gmail OAuth Troubleshooting

## Issue: Client ID/Secret Fields Not Showing

### Quick Fix

The credential type you need is: **"Google OAuth2 API"** (not "Gmail OAuth2")

### Step-by-Step

1. **Go to n8n Credentials page**
   ```
   http://localhost:5678/credentials
   ```

2. **Create New Credential**
   - Click "+ Add Credential" button
   - In search box, type: "Google OAuth2 API"
   - Select "Google OAuth2 API" from results

3. **Fill in the form:**
   ```
   Credential Name: My Gmail OAuth

   Client ID:
   123456789-abcdefghijklmnop.apps.googleusercontent.com

   Client Secret:
   GOCSPX-xxxxxxxxxxxxxxxxxxxxxxx

   Authorization URL: (leave default)
   https://accounts.google.com/o/oauth2/v2/auth

   Access Token URL: (leave default)
   https://oauth2.googleapis.com/token

   Scope:
   https://www.googleapis.com/auth/gmail.send
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/gmail.modify
   https://www.googleapis.com/auth/gmail.compose

   Auth URI Query Parameters: (leave empty)

   Authentication: (select) Body
   ```

4. **Save and Connect**
   - Click "Save"
   - Then click "Connect my account"
   - Sign in with Google
   - Grant permissions

## Alternative: Using n8n Environment Variables

If you prefer to set credentials via environment variables:

### 1. Create `.env` file in n8n directory:

```bash
# Google OAuth Credentials
GOOGLE_OAUTH_CLIENT_ID=123456789-xxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxx

# n8n Configuration
N8N_PROTOCOL=http
N8N_HOST=localhost
N8N_PORT=5678
WEBHOOK_URL=http://localhost:5678/
```

### 2. Restart n8n:

```bash
# Docker
docker-compose restart

# Or if running directly
pkill -f n8n
n8n start
```

## Common Errors & Solutions

### Error: "Redirect URI Mismatch"

**Problem:** OAuth callback URL doesn't match Google Cloud Console

**Solution:**
1. Go to Google Cloud Console → Credentials
2. Edit your OAuth 2.0 Client ID
3. Under "Authorized redirect URIs", add:
   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```
4. Click Save
5. Wait 5 minutes for changes to propagate
6. Try connecting again in n8n

### Error: "Invalid Scope"

**Problem:** Wrong Gmail API scopes

**Solution:** Use these exact scopes:
```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.compose
```

### Error: "Access Blocked: This app's request is invalid"

**Problem:** Your email not added as test user

**Solution:**
1. Go to Google Cloud Console
2. Navigate to: APIs & Services → OAuth consent screen
3. Scroll to "Test users"
4. Click "+ Add Users"
5. Add your Gmail address
6. Click "Save"
7. Try again in n8n

### Error: "Gmail API has not been used in project"

**Problem:** Gmail API not enabled

**Solution:**
1. Go to Google Cloud Console
2. Search for "Gmail API" in top search bar
3. Click "Enable"
4. Wait 1-2 minutes
5. Try again

## Testing Your Gmail Connection

### Simple Test Workflow

1. **Create new workflow in n8n**
2. **Add Manual Trigger node**
3. **Add Gmail node:**
   ```
   Operation: Send Email
   To: your-email@gmail.com
   Subject: Test from n8n
   Message: This is a test!
   ```
4. **Select your Google OAuth2 API credential**
5. **Click "Execute Node"**

If it works, you'll receive the test email!

## Checking n8n Version

Some older n8n versions have different credential interfaces.

```bash
# Check n8n version
n8n --version

# Update to latest
npm install -g n8n@latest

# Or with Docker
docker pull n8nio/n8n:latest
```

## Manual OAuth Flow (Advanced)

If the UI method doesn't work, you can manually get the tokens:

### 1. Get Authorization Code:

Visit this URL (replace CLIENT_ID):
```
https://accounts.google.com/o/oauth2/v2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:5678/rest/oauth2-credential/callback&response_type=code&scope=https://www.googleapis.com/auth/gmail.send%20https://www.googleapis.com/auth/gmail.readonly&access_type=offline&prompt=consent
```

### 2. Exchange code for tokens:

```bash
curl -X POST https://oauth2.googleapis.com/token \
  -d "code=YOUR_AUTH_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:5678/rest/oauth2-credential/callback" \
  -d "grant_type=authorization_code"
```

### 3. Add tokens to n8n database manually (not recommended)

## Still Not Working?

### Check n8n Logs

```bash
# Docker
docker logs n8n-container-name

# PM2
pm2 logs n8n

# Direct run - add debug flag
N8N_LOG_LEVEL=debug n8n start
```

### Verify Google Cloud Console Setup

Checklist:
- [ ] Gmail API is enabled
- [ ] OAuth 2.0 Client ID created
- [ ] Redirect URI added: `http://localhost:5678/rest/oauth2-credential/callback`
- [ ] OAuth consent screen configured
- [ ] Your email added as test user
- [ ] Scopes added to consent screen
- [ ] Client ID and Secret copied correctly (no extra spaces)

### Try Different Credential Type

In some n8n versions, try:
1. "Google Cloud Platform OAuth2 API"
2. "Google Service Account"
3. "HTTP Request" node with custom OAuth

## Example Working Configuration

Here's a screenshot of what your credential form should look like:

```
┌─────────────────────────────────────────┐
│ Google OAuth2 API                       │
├─────────────────────────────────────────┤
│ Credential Name: Gmail OAuth            │
│                                         │
│ Client ID:                              │
│ [123456789-xxx.apps.googleusercontent...│
│                                         │
│ Client Secret:                          │
│ [GOCSPX-xxxxxxxxxxxxx]                  │
│                                         │
│ Scope:                                  │
│ [https://www.googleapis.com/auth/gmai...│
│                                         │
│ [ Save ]  [ Connect my account ]        │
└─────────────────────────────────────────┘
```

## Need More Help?

- n8n Forum: https://community.n8n.io/
- n8n Discord: https://discord.gg/n8n
- GitHub Issues: https://github.com/n8n-io/n8n/issues
