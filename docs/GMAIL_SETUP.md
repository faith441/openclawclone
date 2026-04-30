# Gmail OAuth Integration Setup Guide

This guide will help you set up Gmail OAuth authentication in Zenthral so your boss can login and send emails using their Gmail account.

## Quick Start

### Step 1: Add Your Gmail Client Secret

1. Open the [web/.env](../web/.env) file
2. Replace `YOUR_CLIENT_SECRET_HERE` with your actual Gmail Client Secret from Google Cloud Console

```bash
GMAIL_CLIENT_SECRET=your-actual-client-secret
```

### Step 2: Update Google Cloud OAuth Redirect URI

Your app is running on `http://localhost:5001`, so you need to add the correct redirect URI:

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Click on your OAuth Client ID: `175580175862-3au3aea8mr8nll6psp9g705bt3270dr4`
3. Under "Authorized redirect URIs", add:
   ```
   http://localhost:5001/auth/gmail/callback
   ```
4. Click **Save**

### Step 3: Start the Zenthral Web App

```bash
cd web
python3 app.py
```

The app will start on: **http://localhost:5001**

### Step 4: Connect Gmail Account

1. Open your browser and go to: **http://localhost:5001/gmail**
2. Click "Connect Gmail Account"
3. Sign in with your boss's Gmail account
4. Grant the requested permissions
5. You'll be redirected back to the app

### Step 5: Send Test Email

Once connected, you can send emails:

1. Fill in the email form:
   - **To**: recipient@example.com
   - **Subject**: Test Email
   - **Message**: Your message here
2. Click "Send Email"

## API Usage

You can also send emails programmatically using the API:

```bash
curl -X POST http://localhost:5001/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Hello from Zenthral",
    "body": "This email was sent via Gmail API!"
  }'
```

## Sharing with Your Boss

### Option 1: Local Network Access

If your boss is on the same network:

1. Get your local IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Share the link: `http://YOUR_IP_ADDRESS:5001/gmail`

3. Update the Google Cloud redirect URI to:
   ```
   http://YOUR_IP_ADDRESS:5001/auth/gmail/callback
   ```

### Option 2: Share Screen

Use Zoom/Slack screenshare to help your boss authenticate from your computer.

### Option 3: Deploy to Production

For production use, deploy to a server and use HTTPS. Update:

1. **Redirect URI** in Google Cloud Console
2. **GMAIL_REDIRECT_URI** in [web/app.py](../web/app.py:28)
3. Remove the line: `os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'`

## Features

- ✓ Secure OAuth 2.0 authentication
- ✓ Send emails via Gmail API
- ✓ Access Gmail inbox (readonly)
- ✓ Modify messages
- ✓ Session-based credential storage
- ✓ Simple web interface
- ✓ REST API endpoints

## Gmail Scopes

The app requests these Gmail permissions:

- `gmail.send` - Send emails
- `gmail.readonly` - Read email messages
- `gmail.modify` - Modify messages (labels, etc.)

## Troubleshooting

### "OAuth setup failed"

Check that your `GMAIL_CLIENT_SECRET` is set correctly in [web/.env](../web/.env)

### "Redirect URI mismatch"

Make sure the redirect URI in Google Cloud Console matches exactly:
```
http://localhost:5001/auth/gmail/callback
```

### "Access blocked: This app's request is invalid"

You may need to add your boss's email as a test user in Google Cloud Console:

1. Go to [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
2. Scroll to "Test users"
3. Click "Add Users"
4. Add your boss's Gmail address
5. Click "Save"

### "Gmail not connected"

Make sure to visit `/gmail` and complete the OAuth flow before trying to send emails.

## File Structure

```
web/
├── app.py                    # Main Flask app with Gmail routes
├── .env                      # Environment variables (CLIENT_SECRET goes here)
├── templates/
│   └── gmail.html           # Gmail UI page
└── requirements.txt          # Python dependencies
```

## Next Steps

1. ✅ Gmail OAuth is integrated
2. Test sending emails
3. Integrate with your existing agents/workflows
4. Deploy to production (optional)

## Security Notes

- **Session storage**: Currently using Flask sessions. For production, store credentials in a database.
- **HTTPS**: Use HTTPS in production to secure OAuth tokens.
- **Secrets**: Never commit `.env` file to git. It's already in `.gitignore`.

---

**Need help?** Check the [troubleshooting section](#troubleshooting) or review the [Google OAuth docs](https://developers.google.com/identity/protocols/oauth2).
