# Zenthral CLI

Execute AI automation workflows on your own infrastructure.

## Installation

```bash
pip install zenthral-cli
```

## Quick Start

### 1. Login to Zenthral

```bash
zenthral login
```

This will open your browser to authenticate. Alternatively, use an API key:

```bash
zenthral login --api-key=zth_xxxxxxxxxxxxx
```

### 2. Configure Your AI Provider Keys

Zenthral uses your own API keys - they never leave your machine:

```bash
# Set environment variables
export OPENAI_API_KEY=sk-xxxxx
export ANTHROPIC_API_KEY=sk-ant-xxxxx
export GOOGLE_API_KEY=xxxxx

# Or use zenthral config
zenthral config set OPENAI_API_KEY sk-xxxxx
zenthral config set ANTHROPIC_API_KEY sk-ant-xxxxx
```

### 3. Run Workflows

```bash
# Execute pending workflows once
zenthral run

# Run as background daemon (continuous)
zenthral daemon start

# Run specific workflow
zenthral run --workflow-id=abc123
```

## Commands

### Authentication
- `zenthral login` - Authenticate with Zenthral SaaS
- `zenthral logout` - Remove credentials
- `zenthral whoami` - Show current user

### Configuration
- `zenthral config set KEY VALUE` - Set configuration
- `zenthral config get KEY` - Get configuration
- `zenthral config list` - List all configuration

### Execution
- `zenthral run` - Execute pending workflows
- `zenthral run --workflow-id=ID` - Execute specific workflow
- `zenthral daemon start` - Run as background service
- `zenthral daemon stop` - Stop background service
- `zenthral daemon status` - Check daemon status

### Workflows
- `zenthral list` - List available workflows
- `zenthral test workflow.json` - Test workflow locally
- `zenthral validate workflow.json` - Validate workflow syntax

### Logs & Debugging
- `zenthral logs` - View execution logs
- `zenthral logs --follow` - Stream logs in real-time
- `zenthral status` - Check CLI status

## How It Works

1. You design workflows in the Zenthral web app (https://zenthral.ai)
2. Workflows are stored in the cloud
3. CLI polls for workflows to execute
4. Workflows run on your computer using your API keys
5. Results are reported back to the web app

## Configuration File

Located at `~/.zenthral/config.yaml`:

```yaml
api_url: https://api.zenthral.ai
api_key: zth_xxxxxxxxxxxxx
workspace_id: abc123

# AI Provider Keys (stored locally)
openai_api_key: sk-xxxxx
anthropic_api_key: sk-ant-xxxxx
google_api_key: xxxxx

# Execution Settings
poll_interval: 30  # seconds
max_concurrent: 5
```

## Running as a Service

### Linux (systemd)
```bash
zenthral daemon install
sudo systemctl start zenthral
sudo systemctl enable zenthral  # Start on boot
```

### macOS (launchd)
```bash
zenthral daemon install
launchctl load ~/Library/LaunchAgents/ai.zenthral.plist
```

### Windows (Service)
```bash
zenthral daemon install
sc start Zenthral
```

### Docker
```bash
docker run -d \
  -e ZENTHRAL_API_KEY=zth_xxxxx \
  -e OPENAI_API_KEY=sk-xxxxx \
  --name zenthral \
  zenthral/cli:latest
```

## Security

- Your AI API keys are stored locally and NEVER sent to Zenthral servers
- All communication with Zenthral SaaS is over HTTPS
- API keys are encrypted at rest on your machine
- Workflows are executed in isolated environments

## Support

- Documentation: https://docs.zenthral.ai
- Issues: https://github.com/zenthral/cli/issues
- Discord: https://discord.gg/zenthral
