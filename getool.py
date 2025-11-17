#!/usr/bin/env python3
"""
GETool - Generate ElevenLabs Twilio Outbound Integration Blueprint
A tool to generate JSON configuration for Make.com scenarios connecting Clay Webhooks
to ElevenLabs Conversational AI Outbound Call API.
"""

import json
import argparse
import sys


def generate_clay_webhook_input():
    """Generate the expected JSON structure for Clay Webhook payload (input)."""
    return {
        "to_number": "+14155551212",
        "personalized_opener": "just saw you raised your Series A last week",
        "prospect_name": "Jane Doe"
    }


def generate_makecom_http_output():
    """Generate the templated JSON payload for Make.com HTTP Module (output)."""
    return {
        "agent_id": "[YOUR_AGENT_ID]",
        "agent_phone_number_id": "[YOUR_PHONE_NUMBER_ID]",
        "to_number": "{{to_number}}",
        "custom_variables": {
            "opener": "{{personalized_opener}}",
            "name": "{{prospect_name}}"
        }
    }


def generate_makecom_config():
    """Generate the complete Make.com HTTP Module configuration."""
    return {
        "method": "POST",
        "url": "https://api.elevenlabs.io/v1/convai/twilio/outbound-call",
        "headers": {
            "Content-Type": "application/json",
            "xi-api-key": "[YOUR_ELEVENLABS_API_KEY]"
        },
        "body": generate_makecom_http_output()
    }


def generate_full_blueprint():
    """Generate the complete blueprint with both input and output configurations."""
    return {
        "blueprint": {
            "description": "Make.com scenario connecting Clay Webhook to ElevenLabs Conversational AI Outbound Call API",
            "modules": {
                "webhook": {
                    "type": "trigger",
                    "description": "Listens for HTTP POST request from Clay",
                    "expected_input": generate_clay_webhook_input()
                },
                "http": {
                    "type": "action",
                    "description": "Makes authenticated API call to ElevenLabs Outbound Call API",
                    "configuration": generate_makecom_config()
                }
            },
            "variable_mapping": {
                "to_number": "Maps from webhook to_number to API to_number parameter",
                "personalized_opener": "Maps from webhook personalized_opener to custom_variables.opener",
                "prospect_name": "Maps from webhook prospect_name to custom_variables.name"
            },
            "setup_instructions": [
                "1. Create a new Make.com scenario",
                "2. Add a Webhook module as the trigger",
                "3. Configure the webhook to accept POST requests",
                "4. Add an HTTP module as the action",
                "5. Configure the HTTP module with the provided configuration",
                "6. Replace [YOUR_AGENT_ID] with your ElevenLabs Agent ID",
                "7. Replace [YOUR_PHONE_NUMBER_ID] with your Twilio Phone Number ID",
                "8. Replace [YOUR_ELEVENLABS_API_KEY] with your ElevenLabs API key",
                "9. Map webhook variables using the double-brace syntax: {{variable_name}}",
                "10. Test the scenario with a sample Clay webhook payload"
            ]
        }
    }


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Generate JSON blueprints for Make.com/ElevenLabs integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input          # Generate Clay webhook input example
  %(prog)s --output         # Generate Make.com HTTP output configuration
  %(prog)s --config         # Generate Make.com HTTP module configuration
  %(prog)s --full           # Generate complete blueprint (default)
  %(prog)s --pretty         # Output with pretty formatting
        """
    )
    
    parser.add_argument(
        "--input",
        action="store_true",
        help="Generate only the Clay webhook input JSON structure"
    )
    
    parser.add_argument(
        "--output",
        action="store_true",
        help="Generate only the Make.com HTTP output payload"
    )
    
    parser.add_argument(
        "--config",
        action="store_true",
        help="Generate the complete Make.com HTTP module configuration"
    )
    
    parser.add_argument(
        "--full",
        action="store_true",
        help="Generate the complete blueprint (default)"
    )
    
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Pretty print JSON output (default: True)"
    )
    
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Compact JSON output (overrides --pretty)"
    )
    
    args = parser.parse_args()
    
    # Determine what to generate
    if args.input:
        data = generate_clay_webhook_input()
    elif args.output:
        data = generate_makecom_http_output()
    elif args.config:
        data = generate_makecom_config()
    else:
        # Default to full blueprint
        data = generate_full_blueprint()
    
    # Determine output formatting
    if args.compact:
        output = json.dumps(data)
    else:
        output = json.dumps(data, indent=2)
    
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
