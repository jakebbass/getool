# Clay AI Agent Setup Guide

This guide explains how to use the agentic setup helper to configure your Clay + Make.com + ElevenLabs integration with the help of AI agents.

## Overview

The `clay_agent_helper.py` module provides an intelligent setup assistant that can be used either:
1. **Interactively** - Run the script directly to set up the integration step-by-step
2. **With AI Agents** - Provide generated instructions to AI agents in Clay for automated setup

## Quick Start

### Option 1: Generate AI Agent Prompt

Get a ready-to-use prompt that you can give to an AI agent in Clay:

```bash
getool --agent-prompt
```

Copy the output and paste it into your AI agent helper in Clay. The AI will guide you through the setup process.

### Option 2: Generate Structured Agent Instructions

Get a detailed JSON structure with setup instructions:

```bash
getool --agent-setup
```

This outputs a comprehensive JSON document that AI agents can parse and use to:
- Understand the integration requirements
- Collect necessary credentials
- Generate proper configurations
- Validate inputs
- Provide step-by-step guidance

### Option 3: Interactive Setup

Run the helper script directly for an interactive setup experience:

```bash
python3 clay_agent_helper.py
```

The script will:
1. Prompt you for your credentials:
   - ElevenLabs API Key
   - ElevenLabs Agent ID
   - Twilio Phone Number ID
2. Validate your inputs
3. Generate a complete configuration file
4. Save it to `/tmp/makecom_elevenlabs_config.json`

## Using with Clay AI Agents

### Step 1: Get the AI Prompt

```bash
getool --agent-prompt > clay_ai_instructions.txt
```

### Step 2: Paste into Clay

In Clay's AI agent helper interface:
1. Open the AI agent chat or automation builder
2. Paste the entire prompt from `clay_ai_instructions.txt`
3. The AI will now understand how to help you set up the integration

### Step 3: Provide Your Credentials

When the AI asks, provide:
- **ElevenLabs API Key**: Found in your ElevenLabs dashboard under API settings
- **Agent ID**: The ID of your conversational AI agent in ElevenLabs
- **Phone Number ID**: Your Twilio phone number ID connected to the agent

### Step 4: Follow AI Guidance

The AI will guide you through:
1. Creating the Make.com scenario
2. Configuring the webhook module
3. Setting up the HTTP module
4. Mapping variables correctly
5. Configuring Clay to send data
6. Testing the integration

## Python Helper API

If you're building your own automation or AI agent, you can use the Python API directly:

```python
from clay_agent_helper import AgenticSetupHelper

# Initialize the helper
helper = AgenticSetupHelper()

# Generate agent instructions
instructions = helper.generate_agent_instructions()

# Generate HTTP body for Make.com
http_body = helper.generate_http_body(
    agent_id="your_agent_id",
    phone_number_id="your_phone_number_id"
)

# Validate configuration
config = {
    "elevenlabs_api_key": "your_api_key",
    "agent_id": "your_agent_id",
    "agent_phone_number_id": "your_phone_number_id"
}
is_valid, errors = helper.validate_configuration(config)

# Generate complete setup configuration
complete_config = helper.get_complete_setup_config(
    elevenlabs_api_key="your_api_key",
    agent_id="your_agent_id",
    agent_phone_number_id="your_phone_number_id"
)
```

## What You'll Get

The helper generates a complete configuration including:

### 1. Make.com Scenario Configuration
- Webhook module setup with expected data structure
- HTTP module configuration with proper headers and body
- Variable mapping instructions

### 2. Clay Configuration
- Required table columns
- HTTP API enrichment setup
- Request body structure

### 3. Testing Information
- Sample webhook payload
- Expected API call structure
- Validation steps

### 4. Step-by-Step Instructions
- Detailed setup process
- Configuration validation
- Troubleshooting tips

## Required Information

Before starting, gather these items:

### ElevenLabs API Key
- Location: ElevenLabs Dashboard → Profile → API Keys
- Format: String (typically 32+ characters)
- Example: `sk_abc123xyz...`

### ElevenLabs Agent ID
- Location: ElevenLabs Dashboard → Agents → [Your Agent] → Settings
- Format: Alphanumeric ID
- Example: `agent_abc123`

### Twilio Phone Number ID
- Location: ElevenLabs Dashboard → Phone Numbers (connected via Twilio)
- Format: Alphanumeric ID
- Example: `phone_num_xyz789`

## Configuration Validation

The helper automatically validates:
- ✅ API key format and length
- ✅ Agent ID is not a placeholder
- ✅ Phone number ID is not a placeholder
- ✅ All required fields are present

## Example Output

When you run `getool --agent-setup`, you'll get a JSON structure like:

```json
{
  "setup_type": "Make.com + Clay + ElevenLabs Integration",
  "required_information": {
    "elevenlabs_api_key": { ... },
    "agent_id": { ... },
    "agent_phone_number_id": { ... }
  },
  "setup_steps": [
    {
      "step": 1,
      "action": "gather_credentials",
      "description": "Collect all required credentials"
    },
    ...
  ],
  "helper_methods": {
    "generate_http_body": "...",
    "validate_config": "...",
    "get_complete_setup": "..."
  }
}
```

## Troubleshooting

### "API key seems too short"
- Make sure you copied the complete API key from ElevenLabs
- API keys are typically 32+ characters long

### "Please replace placeholder with actual API key"
- Don't use `[YOUR_API_KEY]` - use your real API key
- Remove any brackets or placeholder text

### "Phone number must be in E.164 format"
- Format: `+[country code][number]`
- Example: `+14155551212` (US number)
- Must start with `+`

## Integration with Other Tools

The helper can be integrated with:
- **Clay automation workflows** - Use the generated configurations
- **Make.com blueprint imports** - Export configurations as blueprints
- **CI/CD pipelines** - Automate testing with sample payloads
- **Documentation systems** - Generate setup documentation

## Security Notes

⚠️ **Important Security Considerations:**
- Never commit API keys to version control
- Store credentials securely (use environment variables or secret management)
- The interactive setup saves to `/tmp` for temporary use
- Always validate credentials before using in production

## Next Steps

After setup is complete:
1. Test with sample data
2. Configure your ElevenLabs agent's system prompt to use custom variables
3. Set up your Clay table with prospect data
4. Run a test call to verify everything works

## Support

For issues or questions:
- Check the main README.md for general tool usage
- Review `agentinstructions.md` for integration details
- See the example configurations in the JSON output

## License

Same as the main getool project.
