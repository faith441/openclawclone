# Lovable Prompts for Zenthral Cloud Mode UI

## 📦 What's Already Built (Backend)

The following backend features are **already implemented** in the `/lovable-app/` folder:

- ✅ Cloud execution engine ([lib/cloud-executor.ts](lovable-app/lib/cloud-executor.ts))
- ✅ Encryption utilities ([lib/encryption.ts](lovable-app/lib/encryption.ts))
- ✅ Supabase client ([lib/supabase.ts](lovable-app/lib/supabase.ts))
- ✅ API routes:
  - `POST /api/ai-keys` - Save AI API keys
  - `GET /api/ai-keys` - List AI providers
  - `DELETE /api/ai-keys` - Remove API keys
  - `POST /api/execute` - Execute workflows in cloud
- ✅ Database schema with:
  - `user_ai_keys` table (encrypted API key storage)
  - `installed_skills` table (track installed skills)
  - `executions` table (execution history)

---

## 🎨 UI Components to Build in Lovable

Use these prompts **one by one** in Lovable to build the complete UI.

### Prompt 1: Settings Page with AI Key Management

```
Create a Settings page at /settings with AI API key management:

1. **Page Title**: "Settings - AI Keys"

2. **Tab Navigation**:
   - AI Keys (active)
   - Account
   - Billing (grayed out for now)

3. **AI Keys Section**:
   - Heading: "AI Provider Keys"
   - Description: "Add your AI API keys to enable cloud execution. Keys are encrypted with AES-256."

4. **Provider Cards** (show 4 cards):
   Each card shows:
   - Logo (OpenAI, Anthropic, Google, Groq)
   - Provider name
   - Status badge: "Connected" (green) or "Not configured" (gray)
   - If connected: "Added on [date]" + "Test Status: ✓ Valid"
   - Button: "Add Key" or "Update Key" or "Remove" (red)

5. **Add/Edit Key Modal**:
   When clicking "Add Key":
   - Modal title: "Add [Provider] API Key"
   - Input field: "API Key" (password type, shows dots)
   - Checkbox: "Test key before saving" (checked by default)
   - Buttons: "Cancel" | "Save"
   - Show loading spinner when testing
   - Show success/error message

6. **How to Get Keys** (expandable section):
   - OpenAI: Link to platform.openai.com/api-keys
   - Anthropic: Link to console.anthropic.com
   - Google: Link to aistudio.google.com/apikey

7. **API Implementation**:
   - GET /api/ai-keys on page load
   - POST /api/ai-keys when saving (with testKey: true)
   - DELETE /api/ai-keys?provider=openai when removing
   - Show toast notifications for success/errors

Use Supabase auth for the user session. Style with Tailwind, use Lucide icons.
```

---

### Prompt 2: Enhanced Marketplace with Install Button

```
Update the Skills Marketplace page to support cloud mode:

1. **Page Layout**:
   - Header: "Skills Marketplace"
   - Tabs: "All Skills" | "Installed" | "Finance" | "Healthcare" | etc.
   - Search bar at top

2. **Skill Card** (for each skill):
   - Skill icon/emoji
   - Skill name
   - Category badge
   - Short description
   - "Execution Mode" dropdown: Cloud ☁️ | Local 💻
   - Button state logic:
     - If NOT installed: "Install" (primary blue)
     - If installed: "✓ Installed" (green) + "Run" button
     - If no AI keys configured: "Configure AI Keys First" (disabled)

3. **Install Flow**:
   When clicking "Install":
   - Check if user has AI keys (GET /api/ai-keys)
   - If NO keys: Show modal "Please add an AI key in Settings first"
   - If HAS keys:
     - Insert into Supabase: installed_skills table
     - Fields: user_id, skill_id, skill_name, execution_mode (from dropdown), is_enabled: true
     - Show success toast: "✓ [Skill] installed in Cloud mode"
     - Update button to "✓ Installed" + show "Run" button

4. **Installed Tab**:
   - Shows only skills where installed_skills.user_id = current user
   - Each card shows execution mode badge
   - Can toggle "Cloud" <-> "Local" mode
   - "Remove" button (deletes from installed_skills)

5. **API Implementation**:
   - GET /api/ai-keys (check if configured)
   - Supabase query: installed_skills.insert()
   - Supabase query: installed_skills.select() for "Installed" tab
   - Update execution_mode when toggling

Use Supabase RLS policies (already configured). Style consistently with the app.
```

---

### Prompt 3: Workflow Execution with Cloud Mode

```
Create a workflow execution page at /run/[skillId]:

1. **Page Header**:
   - Breadcrumb: Marketplace > [Skill Name]
   - Skill title and description
   - Execution mode badge: ☁️ Cloud or 💻 Local
   - If Cloud mode: "Runs in browser, ~10 seconds"
   - If Local mode: "Requires CLI daemon running"

2. **Input Form** (dynamic based on skill):
   - Auto-generate form fields from skill metadata
   - Example for "Invoice Generator":
     - Client Name (text input)
     - Amount (number input with $ prefix)
     - Service Description (textarea)
     - Due Date (date picker)
   - "Advanced Options" (collapsible):
     - AI Model selector: GPT-4o | GPT-4o-mini | Claude Sonnet | Claude Haiku
     - Max tokens (slider: 1000-4000)

3. **Run Button**:
   - Large primary button: "Generate Invoice"
   - Disabled states:
     - If Cloud mode AND no AI keys: "Configure AI Keys First"
     - If Local mode AND daemon not running: "Start CLI Daemon"
   - Loading state: Show spinner + "Executing..."

4. **Execution Flow (Cloud Mode)**:
   When clicking "Run":
   ```javascript
   const response = await fetch('/api/execute', {
     method: 'POST',
     headers: {
       'Authorization': `Bearer ${supabase.auth.session.access_token}`,
       'Content-Type': 'application/json'
     },
     body: JSON.stringify({
       workflowId: workflowId, // from Supabase workflows table
       skillId: skillId,
       parameters: {
         client: formData.client,
         amount: formData.amount,
         service: formData.service
       }
     })
   });
   ```

5. **Results Display**:
   After execution completes:
   - Success card with green checkmark
   - Output text area (read-only, formatted)
   - Metadata: "Completed in 8.2s | 1,234 tokens | $0.02"
   - Buttons: "Copy Output" | "Download" | "Run Again"
   - "View Logs" (expandable):
     - Show logs array from API response
     - Formatted with timestamps

6. **Error Handling**:
   - If API returns error: Show red alert with error message
   - Common errors:
     - "No AI keys configured" → Link to Settings
     - "API key invalid" → Link to Settings to update
     - "Insufficient credits" → Show OpenAI/Anthropic billing link

7. **Execution History** (bottom of page):
   - Table: Date | Status | Tokens | Cost | Actions
   - Load from Supabase: executions table
   - Filter: where workflow_id = current workflow AND user's workspace
   - Click row to view logs

Use real-time updates if possible (Supabase subscriptions). Style with Tailwind.
```

---

### Prompt 4: Dashboard with Execution Stats

```
Create a Dashboard at /dashboard showing user activity:

1. **Stats Cards** (4 cards in a row):
   - Total Workflows: Count from workflows table
   - Executions This Month: Count from executions (current month)
   - Total Cost: Sum of executions.cost (current month)
   - Active Skills: Count from installed_skills (is_enabled = true)

2. **Recent Executions** (table):
   - Columns: Workflow | Status | Time | Cost | Logs
   - Query: SELECT * FROM executions WHERE workspace_id = user's workspace ORDER BY started_at DESC LIMIT 10
   - Status badge: Completed (green) | Failed (red) | Running (yellow)
   - Click "Logs" → Show modal with execution.logs

3. **Quick Actions**:
   - Button: "Install New Skill" → /marketplace
   - Button: "Run Workflow" → /workflows
   - Button: "Configure AI Keys" → /settings

4. **Usage Chart** (optional):
   - Bar chart: Executions per day (last 7 days)
   - Line chart: Cost per day
   - Use a simple chart library like recharts

5. **API Implementation**:
   - Supabase queries for all stats
   - Use Supabase real-time subscriptions for live updates
   - Cache stats with React Query or SWR

Style consistently with modern SaaS dashboard (shadcn/ui style).
```

---

### Prompt 5: Onboarding Flow for New Users

```
Create a smooth onboarding experience for first-time users:

1. **Welcome Modal** (shows on first login):
   - Title: "Welcome to Zenthral!"
   - Steps indicator: 1/3, 2/3, 3/3

2. **Step 1: Choose Execution Mode**:
   - Two large cards:
     - **Cloud Mode** (recommended badge):
       - Icon: ☁️
       - "No installation required"
       - "Perfect for beginners"
       - "Limited to 5-minute workflows"
       - Button: "Use Cloud Mode"
     - **Local Mode**:
       - Icon: 💻
       - "Install desktop app"
       - "Unlimited workflows"
       - "For power users"
       - Button: "Use Local Mode"

3. **Step 2: Add AI Key** (if Cloud Mode selected):
   - Title: "Add Your First AI Key"
   - Description: "You need an API key from OpenAI or Anthropic. Both offer $5 free credit."
   - Two provider cards (OpenAI, Anthropic):
     - Each shows: Logo, "Get $5 free credit", "Sign up" link
     - Paste API key field below
     - "Test & Continue" button
   - Skip button: "I'll do this later"

4. **Step 3: Install First Skill**:
   - Title: "Install Your First Skill"
   - Show 3 recommended skills:
     - Invoice Generator (Finance)
     - Email Writer (Productivity)
     - Research Assistant (Research)
   - Each has "Install Now" button
   - Install directly from onboarding
   - After install: "✓ Installed! Let's run it."

5. **Complete**:
   - Confetti animation 🎉
   - "You're all set!"
   - Button: "Go to Dashboard"
   - Save onboarding completion: user_profiles.onboarding_completed = true

6. **Implementation**:
   - Store progress in localStorage (step 1/2/3)
   - POST /api/ai-keys for step 2
   - Insert into installed_skills for step 3
   - Update user_profiles in Supabase for completion
   - Don't show again if onboarding_completed = true

Make it delightful with smooth animations and encouraging copy.
```

---

## 🔧 Additional Prompts (Optional)

### Prompt 6: Mobile-Responsive Design

```
Make the entire app mobile-friendly:

1. Use Tailwind's responsive classes (sm:, md:, lg:)
2. Settings page: Stack cards vertically on mobile
3. Marketplace: Show 1 card per row on mobile
4. Execution page: Stack form + results vertically
5. Dashboard: Show 2 stats cards per row on mobile
6. Navigation: Convert to bottom tab bar on mobile
7. Add hamburger menu for mobile navigation

Test on iPhone SE (375px) and iPad (768px) viewports.
```

---

### Prompt 7: Error States and Loading Skeletons

```
Add loading states and error handling:

1. **Loading Skeletons**:
   - Marketplace: Show 6 skeleton cards while loading
   - Dashboard: Skeleton for stats cards
   - Settings: Skeleton for provider cards

2. **Empty States**:
   - Marketplace → Installed tab: "No skills installed yet"
   - Dashboard: "No executions yet. Install a skill to get started."
   - Execution history: "No previous executions"

3. **Error States**:
   - API errors: Toast notifications with retry button
   - Network errors: "Connection lost. Retrying..."
   - Auth errors: Redirect to /login

Use Sonner for toast notifications. Style empty states with illustrations.
```

---

## 📋 Implementation Checklist

Use these prompts in order:

- [ ] Prompt 1: Settings + AI Key Management
- [ ] Prompt 2: Marketplace with Install
- [ ] Prompt 3: Workflow Execution
- [ ] Prompt 4: Dashboard
- [ ] Prompt 5: Onboarding Flow
- [ ] Prompt 6: Mobile Responsive (optional)
- [ ] Prompt 7: Error States (optional)

After each prompt, test the feature in Lovable's preview before moving to the next.

---

## 🧪 Testing in Lovable

After building the UI, test this flow:

1. Sign up → Should show onboarding
2. Add OpenAI API key → Should validate and save
3. Install a skill from marketplace → Should show in "Installed" tab
4. Run the skill → Should execute in cloud and show results
5. Check dashboard → Should show execution stats
6. View settings → Should show connected providers

---

## 🚀 Deployment Checklist

Before deploying to production:

1. ✅ Run Supabase schema: `supabase-schema.sql`
2. ✅ Set environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `ENCRYPTION_SECRET` (generate with: `openssl rand -base64 32`)
3. ✅ Test API endpoints in Lovable
4. ✅ Deploy to Lovable
5. ✅ Test full flow in production

---

## 📚 Documentation Links

- Backend code: `/lovable-app/lib/`
- API routes: `/lovable-app/app/api/`
- Database schema: `/lovable-app/supabase-schema.sql`
- Setup guide: `/SIMPLIFIED_SETUP.md`

---

**Ready to build!** 🎨

Start with Prompt 1 and work your way through the list. Each prompt builds on the previous one.
