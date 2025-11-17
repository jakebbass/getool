# getool

A tool for generating JSON blueprints for Make.com scenarios that connect Clay Webhooks to ElevenLabs Conversational AI Outbound Call API.

## Overview

`getool` (Generate ElevenLabs Twilio Outbound Integration Blueprint) helps you quickly generate the necessary JSON configurations for setting up Make.com automation scenarios that integrate Clay webhooks with ElevenLabs AI-powered outbound calling.

## Features

- Generate Clay webhook input JSON structure
- Generate Make.com HTTP module output configuration
- Generate complete Make.com HTTP module configuration with headers
- Generate full blueprint with setup instructions
- **NEW: AI Agent Setup Assistant** - Get instructions and code for AI agents in Clay to automate setup
- **NEW: Interactive Setup** - Guided configuration with validation
- Pretty-printed or compact JSON output
- Command-line interface for easy integration with scripts

## Installation

```bash
# Clone the repository
git clone https://github.com/jakebbass/getool.git
cd getool

# Install the tool
pip install -e .
```

Or install directly from the repository:

```bash
pip install git+https://github.com/jakebbass/getool.git
```

## Usage

### Generate Clay Webhook Input Example

```bash
getool --input
```

Output:
```json
{
  "to_number": "+14155551212",
  "personalized_opener": "just saw you raised your Series A last week",
  "prospect_name": "Jane Doe"
}
```

### Generate Make.com HTTP Output Payload

```bash
getool --output
```

Output:
```json
{
  "agent_id": "[YOUR_AGENT_ID]",
  "agent_phone_number_id": "[YOUR_PHONE_NUMBER_ID]",
  "to_number": "{{to_number}}",
  "custom_variables": {
    "opener": "{{personalized_opener}}",
    "name": "{{prospect_name}}"
  }
}
```

### Generate Complete Make.com HTTP Configuration

```bash
getool --config
```

This includes the HTTP method, URL, headers, and body payload.

### Generate Full Blueprint

```bash
getool --full
# or simply
getool
```

This generates a complete blueprint including:
- Webhook module configuration
- HTTP module configuration
- Variable mapping documentation
- Step-by-step setup instructions

### Generate AI Agent Setup Instructions (NEW!)

Get structured instructions that can be used by AI agents in Clay to set up the integration:

```bash
getool --agent-setup
```

This outputs a comprehensive JSON structure that AI agents can parse and use to guide users through setup.

### Generate AI Agent Prompt (NEW!)

Get a ready-to-use prompt that you can give to an AI agent helper in Clay:

```bash
getool --agent-prompt
```

Copy the output and paste it into your AI agent in Clay. The AI will understand how to help you set up the integration step-by-step.

### Interactive Setup (NEW!)

Run the interactive setup script to configure your integration with validation:

```bash
python3 clay_agent_helper.py
```

The script will:
1. Prompt you for your ElevenLabs API key, Agent ID, and Phone Number ID
2. Validate your inputs
3. Generate a complete configuration file at `/tmp/makecom_elevenlabs_config.json`
4. Provide next steps for completing the setup

### Output Options

- `--pretty`: Pretty-print JSON (default)
- `--compact`: Output compact JSON

Example:
```bash
getool --output --compact
```

## How It Works

The tool generates JSON configurations based on the requirements specified in `agentinstructions.md`:

1. **Webhook Module (Trigger)**: Listens for HTTP POST requests from Clay containing prospect data
2. **HTTP Module (Action)**: Makes authenticated API calls to ElevenLabs with personalized variables
3. **Variable Mapping**: Maps Clay webhook data to ElevenLabs custom variables for call personalization

## Agentic Setup (NEW!)

The new **Clay AI Agent Helper** provides an intelligent setup assistant that can be used by AI agents in Clay or run interactively:

### For AI Agents in Clay

1. Generate the AI prompt:
   ```bash
   getool --agent-prompt
   ```

2. Copy the output and paste it into your AI agent in Clay

3. The AI will guide you through:
   - Collecting your credentials
   - Setting up the Make.com scenario
   - Configuring the webhook and HTTP modules
   - Testing the integration

### For Interactive Setup

Run the helper script directly:
```bash
python3 clay_agent_helper.py
```

The script collects your credentials, validates them, and generates a complete configuration file.

### For Developers

Use the Python API to build custom automation:
```python
from clay_agent_helper import AgenticSetupHelper

helper = AgenticSetupHelper()
instructions = helper.generate_agent_instructions()
config = helper.get_complete_setup_config(api_key, agent_id, phone_id)
```

See [CLAY_AGENT_SETUP.md](CLAY_AGENT_SETUP.md) for detailed documentation on the agentic setup features.

## API Integration Details

- **ElevenLabs API Endpoint**: `https://api.elevenlabs.io/v1/convai/twilio/outbound-call`
- **Authentication**: Uses `xi-api-key` header
- **Required Parameters**:
  - `agent_id`: Your ElevenLabs Agent ID
  - `agent_phone_number_id`: Your Twilio Phone Number ID
  - `to_number`: Prospect's phone number (from webhook)
  - `custom_variables`: Personalization data (opener, name)

## Development

### Running Tests

```bash
# Run the tool directly with Python
python3 getool.py --help
python3 getool.py --input
python3 getool.py --output
```

### Project Structure

```
getool/
├── getool.py                  # Main CLI tool
├── clay_agent_helper.py       # NEW: Agentic setup assistant
├── setup.py                   # Package setup configuration
├── requirements.txt           # Python dependencies (empty - uses stdlib only)
├── README.md                  # This file
├── CLAY_AGENT_SETUP.md        # NEW: Agentic setup documentation
├── agentinstructions.md       # Original requirements specification
├── test_getool.py             # Tests for main tool
├── test_clay_agent_helper.py  # NEW: Tests for agentic setup
└── .gitignore                 # Git ignore patterns
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

(License information to be added)
