/**
 * Zenthral AI Platform - Main JavaScript
 */

// Global state
const ZenthralApp = {
    currentProvider: 'anthropic',
    currentModel: 'claude-sonnet-4-20250514',
    apiKeys: {},
    usage: { total_input: 0, total_output: 0, requests: 0 }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentModel();
    checkApiKeys();
    loadUsage();
});

// Load current model selection
async function loadCurrentModel() {
    try {
        const response = await fetch('/api/current-model');
        const data = await response.json();
        if (data.status === 'success') {
            ZenthralApp.currentProvider = data.provider;
            ZenthralApp.currentModel = data.model;
            updateModelDisplay();
        }
    } catch (error) {
        console.error('Failed to load current model:', error);
    }
}

// Update model display in UI
function updateModelDisplay() {
    const quickModel = document.getElementById('quick-model');
    if (quickModel) {
        quickModel.value = ZenthralApp.currentModel;
    }
}

// Check which API keys are configured
async function checkApiKeys() {
    try {
        const response = await fetch('/api/check-keys');
        const data = await response.json();
        if (data.status === 'success') {
            ZenthralApp.apiKeys = data.configured;
            updateKeyStatus();
        }
    } catch (error) {
        console.error('Failed to check API keys:', error);
    }
}

// Update API key status indicators
function updateKeyStatus() {
    // Update integration cards if on integration page
    const integrationCards = document.querySelectorAll('.integration-card');
    integrationCards.forEach(card => {
        const provider = card.dataset.provider;
        if (provider && ZenthralApp.apiKeys[provider]) {
            const statusBadge = card.querySelector('.status-badge');
            if (statusBadge) {
                statusBadge.textContent = 'Connected';
                statusBadge.classList.add('connected');
            }
        }
    });
}

// Load usage statistics
async function loadUsage() {
    try {
        const response = await fetch('/api/usage');
        const data = await response.json();
        if (data.status === 'success') {
            ZenthralApp.usage = data.usage;
            updateUsageDisplay();
        }
    } catch (error) {
        console.error('Failed to load usage:', error);
    }
}

// Update usage display
function updateUsageDisplay() {
    const totalTokens = document.getElementById('total-tokens');
    const apiCalls = document.getElementById('api-calls');

    if (totalTokens) {
        const total = ZenthralApp.usage.total_input + ZenthralApp.usage.total_output;
        totalTokens.textContent = formatNumber(total);
    }
    if (apiCalls) {
        apiCalls.textContent = formatNumber(ZenthralApp.usage.requests);
    }
}

// Format large numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(2) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Show notification toast
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
        <span class="notification-message">${message}</span>
    `;

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Connect API modal functionality
function showConnectModal(provider) {
    const modal = document.getElementById('connect-modal');
    const title = document.getElementById('modal-provider-title');
    const input = document.getElementById('modal-api-key');

    if (modal && title && input) {
        title.textContent = getProviderName(provider);
        modal.dataset.provider = provider;
        input.value = '';
        input.placeholder = getPlaceholder(provider);
        modal.style.display = 'flex';
    }
}

function hideConnectModal() {
    const modal = document.getElementById('connect-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function getProviderName(provider) {
    const names = {
        'anthropic': 'Anthropic (Claude)',
        'openai': 'OpenAI',
        'google': 'Google (Gemini)',
        'stripe': 'Stripe',
        'shopify': 'Shopify',
        'twilio': 'Twilio',
        'slack': 'Slack',
        'smtp': 'Email (SMTP)'
    };
    return names[provider] || provider;
}

function getPlaceholder(provider) {
    const placeholders = {
        'anthropic': 'sk-ant-api...',
        'openai': 'sk-...',
        'google': 'AIza...',
        'stripe': 'sk_live_...',
        'shopify': 'shpat_...',
        'twilio': 'AC...'
    };
    return placeholders[provider] || 'Enter your API key...';
}

// Save API key
async function saveApiKey() {
    const modal = document.getElementById('connect-modal');
    const input = document.getElementById('modal-api-key');

    if (!modal || !input) return;

    const provider = modal.dataset.provider;
    const apiKey = input.value.trim();

    if (!apiKey) {
        showNotification('Please enter an API key', 'error');
        return;
    }

    try {
        const response = await fetch('/api/set-api-key', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ provider, api_key: apiKey })
        });

        const data = await response.json();
        if (data.status === 'success') {
            showNotification(`${getProviderName(provider)} connected successfully!`, 'success');
            ZenthralApp.apiKeys[provider] = true;
            updateKeyStatus();
            hideConnectModal();
        } else {
            showNotification('Failed to save API key', 'error');
        }
    } catch (error) {
        showNotification('Error connecting to server', 'error');
    }
}

// Handle model selection change
function handleModelChange(selectElement) {
    const model = selectElement.value;
    const option = selectElement.options[selectElement.selectedIndex];
    const provider = option.dataset?.provider || detectProvider(model);

    setProvider(provider, model);
}

function detectProvider(model) {
    if (model.startsWith('gpt') || model.startsWith('o1')) return 'openai';
    if (model.startsWith('claude')) return 'anthropic';
    if (model.startsWith('gemini')) return 'google';
    return 'anthropic';
}

async function setProvider(provider, model) {
    try {
        const response = await fetch('/api/set-provider', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ provider, model })
        });

        const data = await response.json();
        if (data.status === 'success') {
            ZenthralApp.currentProvider = provider;
            ZenthralApp.currentModel = model;
            showNotification(`Model set to ${model}`, 'success');
        }
    } catch (error) {
        showNotification('Failed to update model', 'error');
    }
}

// Markdown rendering helper
function renderMarkdown(text) {
    // Basic markdown rendering
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
        .replace(/\n/g, '<br>');
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
