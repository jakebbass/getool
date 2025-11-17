#!/usr/bin/env python3
"""
Clay Agent Helper - Agentic Setup Assistant
A Python helper script designed to be used by AI agents in Clay for setting up
the Make.com/ElevenLabs integration automatically.
"""

import json
import re
from typing import Dict, List, Optional, Tuple


class SetupValidator:
    """Validates configuration inputs for the setup process."""
    
    @staticmethod
    def validate_phone_number(phone: str) -> Tuple[bool, str]:
        """Validate phone number format (E.164)."""
        if not phone:
            return False, "Phone number cannot be empty"
        
        # E.164 format: +[country code][number], typically 10-15 digits
        pattern = r'^\+[1-9]\d{1,14}$'
        if re.match(pattern, phone):
            return True, "Valid phone number format"
        return False, "Phone number must be in E.164 format (e.g., +14155551212)"
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[bool, str]:
        """Validate API key format."""
        if not api_key:
            return False, "API key cannot be empty"
        
        if len(api_key) < 10:
            return False, "API key seems too short"
        
        if api_key.startswith("[") or api_key.endswith("]"):
            return False, "Please replace placeholder with actual API key"
        
        return True, "API key format looks valid"
    
    @staticmethod
    def validate_agent_id(agent_id: str) -> Tuple[bool, str]:
        """Validate agent ID format."""
        if not agent_id:
            return False, "Agent ID cannot be empty"
        
        if agent_id.startswith("[") or agent_id.endswith("]"):
            return False, "Please replace placeholder with actual Agent ID"
        
        return True, "Agent ID format looks valid"


class AgenticSetupHelper:
    """Main helper class for AI agents to configure the integration."""
    
    def __init__(self):
        self.config = {}
        self.validator = SetupValidator()
    
    def generate_agent_instructions(self) -> Dict:
        """
        Generate instructions that an AI agent can follow to set up the integration.
        This is the primary method for AI agents to use.
        """
        return {
            "setup_type": "Make.com + Clay + ElevenLabs Integration",
            "agent_role": "You are an AI setup assistant helping configure an outbound calling integration",
            "required_information": {
                "elevenlabs_api_key": {
                    "description": "Your ElevenLabs API key (found in ElevenLabs dashboard)",
                    "format": "String (typically 32+ characters)",
                    "example": "sk_abc123xyz...",
                    "validation": "Must not be empty or a placeholder"
                },
                "agent_id": {
                    "description": "Your ElevenLabs Conversational AI Agent ID",
                    "format": "String (alphanumeric ID)",
                    "example": "agent_abc123",
                    "validation": "Must not be empty or a placeholder"
                },
                "agent_phone_number_id": {
                    "description": "Your Twilio Phone Number ID connected to the agent",
                    "format": "String (alphanumeric ID)",
                    "example": "phone_num_xyz789",
                    "validation": "Must not be empty or a placeholder"
                }
            },
            "setup_steps": [
                {
                    "step": 1,
                    "action": "gather_credentials",
                    "description": "Collect all required credentials from the user",
                    "required_fields": ["elevenlabs_api_key", "agent_id", "agent_phone_number_id"]
                },
                {
                    "step": 2,
                    "action": "create_makecom_scenario",
                    "description": "Create a new scenario in Make.com",
                    "instructions": [
                        "Log into Make.com",
                        "Create a new scenario",
                        "The scenario will have 2 modules: Webhook (trigger) and HTTP (action)"
                    ]
                },
                {
                    "step": 3,
                    "action": "configure_webhook_module",
                    "description": "Set up the Clay webhook as the trigger",
                    "configuration": {
                        "module_type": "Webhooks > Custom webhook",
                        "method": "POST",
                        "expected_data_structure": {
                            "to_number": "Phone number in E.164 format",
                            "personalized_opener": "AI-generated opener text",
                            "prospect_name": "Prospect's name"
                        }
                    }
                },
                {
                    "step": 4,
                    "action": "configure_http_module",
                    "description": "Set up the HTTP request to ElevenLabs API",
                    "configuration": {
                        "module_type": "HTTP > Make a request",
                        "method": "POST",
                        "url": "https://api.elevenlabs.io/v1/convai/twilio/outbound-call",
                        "headers_to_add": [
                            {"key": "Content-Type", "value": "application/json"},
                            {"key": "xi-api-key", "value": "{{elevenlabs_api_key}}"}
                        ],
                        "body_type": "Raw JSON",
                        "body_template": "Use the generate_http_body method"
                    }
                },
                {
                    "step": 5,
                    "action": "map_variables",
                    "description": "Map webhook data to API parameters",
                    "mappings": {
                        "to_number": "Webhook output: to_number",
                        "custom_variables.opener": "Webhook output: personalized_opener",
                        "custom_variables.name": "Webhook output: prospect_name"
                    }
                },
                {
                    "step": 6,
                    "action": "configure_clay",
                    "description": "Set up Clay to send data to the webhook",
                    "instructions": [
                        "In Clay, create a table with columns: to_number, personalized_opener, prospect_name",
                        "Add an HTTP API enrichment",
                        "Set the webhook URL from Make.com",
                        "Configure the request body with the three required fields"
                    ]
                },
                {
                    "step": 7,
                    "action": "test_integration",
                    "description": "Test the complete workflow",
                    "test_data": {
                        "to_number": "+14155551212",
                        "personalized_opener": "I saw your recent product launch",
                        "prospect_name": "Jane Doe"
                    }
                }
            ],
            "helper_methods": {
                "generate_http_body": "Call generate_http_body() to get the JSON structure",
                "validate_config": "Call validate_configuration() to check all inputs",
                "get_complete_setup": "Call get_complete_setup_config() for full configuration"
            }
        }
    
    def generate_http_body(self, agent_id: str, phone_number_id: str) -> Dict:
        """
        Generate the HTTP request body for the ElevenLabs API call.
        
        Args:
            agent_id: ElevenLabs Agent ID
            phone_number_id: Twilio Phone Number ID
            
        Returns:
            Dictionary representing the HTTP body structure with Make.com variable mappings
        """
        return {
            "agent_id": agent_id,
            "agent_phone_number_id": phone_number_id,
            "to_number": "{{to_number}}",
            "custom_variables": {
                "opener": "{{personalized_opener}}",
                "name": "{{prospect_name}}"
            }
        }
    
    def validate_configuration(self, config: Dict) -> Tuple[bool, List[str]]:
        """
        Validate a complete configuration.
        
        Args:
            config: Dictionary containing configuration values
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Validate API key
        if "elevenlabs_api_key" in config:
            valid, msg = self.validator.validate_api_key(config["elevenlabs_api_key"])
            if not valid:
                errors.append(f"API Key: {msg}")
        else:
            errors.append("Missing required field: elevenlabs_api_key")
        
        # Validate agent ID
        if "agent_id" in config:
            valid, msg = self.validator.validate_agent_id(config["agent_id"])
            if not valid:
                errors.append(f"Agent ID: {msg}")
        else:
            errors.append("Missing required field: agent_id")
        
        # Validate phone number ID
        if "agent_phone_number_id" in config:
            valid, msg = self.validator.validate_agent_id(config["agent_phone_number_id"])
            if not valid:
                errors.append(f"Phone Number ID: {msg}")
        else:
            errors.append("Missing required field: agent_phone_number_id")
        
        return len(errors) == 0, errors
    
    def get_complete_setup_config(self, 
                                   elevenlabs_api_key: str,
                                   agent_id: str,
                                   agent_phone_number_id: str) -> Dict:
        """
        Generate a complete, ready-to-use configuration for the integration.
        
        Args:
            elevenlabs_api_key: ElevenLabs API key
            agent_id: ElevenLabs Agent ID
            agent_phone_number_id: Twilio Phone Number ID
            
        Returns:
            Complete configuration dictionary
        """
        config = {
            "elevenlabs_api_key": elevenlabs_api_key,
            "agent_id": agent_id,
            "agent_phone_number_id": agent_phone_number_id
        }
        
        # Validate configuration
        is_valid, errors = self.validate_configuration(config)
        
        return {
            "status": "valid" if is_valid else "invalid",
            "errors": errors if not is_valid else [],
            "makecom_scenario": {
                "name": "Clay to ElevenLabs Outbound Calls",
                "modules": [
                    {
                        "id": 1,
                        "type": "webhook",
                        "app": "webhooks",
                        "module": "webhook",
                        "name": "Clay Webhook Trigger",
                        "configuration": {
                            "hook_name": "clay_webhook",
                            "method": "POST",
                            "expected_structure": {
                                "to_number": "string (E.164 format)",
                                "personalized_opener": "string",
                                "prospect_name": "string"
                            }
                        }
                    },
                    {
                        "id": 2,
                        "type": "http",
                        "app": "http",
                        "module": "make_request",
                        "name": "Call ElevenLabs API",
                        "configuration": {
                            "url": "https://api.elevenlabs.io/v1/convai/twilio/outbound-call",
                            "method": "POST",
                            "headers": [
                                {"name": "Content-Type", "value": "application/json"},
                                {"name": "xi-api-key", "value": elevenlabs_api_key}
                            ],
                            "body_type": "raw",
                            "body": self.generate_http_body(agent_id, agent_phone_number_id)
                        },
                        "mapper": {
                            "Note": "In Make.com UI, replace placeholders with actual webhook values",
                            "to_number": "Use: 1.to_number (from webhook module)",
                            "custom_variables.opener": "Use: 1.personalized_opener (from webhook module)",
                            "custom_variables.name": "Use: 1.prospect_name (from webhook module)"
                        }
                    }
                ]
            },
            "clay_configuration": {
                "table_columns": ["to_number", "personalized_opener", "prospect_name"],
                "http_api_enrichment": {
                    "method": "POST",
                    "url": "{{WEBHOOK_URL_FROM_MAKECOM}}",
                    "body": {
                        "to_number": "{{to_number}}",
                        "personalized_opener": "{{personalized_opener}}",
                        "prospect_name": "{{prospect_name}}"
                    }
                }
            },
            "testing": {
                "sample_webhook_payload": {
                    "to_number": "+14155551212",
                    "personalized_opener": "I noticed you recently raised Series A funding",
                    "prospect_name": "Jane Doe"
                },
                "expected_api_call": {
                    "url": "https://api.elevenlabs.io/v1/convai/twilio/outbound-call",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json",
                        "xi-api-key": elevenlabs_api_key
                    },
                    "body": {
                        "agent_id": agent_id,
                        "agent_phone_number_id": agent_phone_number_id,
                        "to_number": "+14155551212",
                        "custom_variables": {
                            "opener": "I noticed you recently raised Series A funding",
                            "name": "Jane Doe"
                        }
                    }
                }
            }
        }
    
    def generate_clay_ai_prompt(self) -> str:
        """
        Generate a prompt that can be given to an AI agent in Clay.
        This prompt provides context and instructions for the AI to help set up the integration.
        """
        return """You are a helpful AI assistant guiding a user through setting up an integration between Clay, Make.com, and ElevenLabs for AI-powered outbound calling.

CONTEXT:
The user wants to automate outbound sales calls where:
1. Clay sends prospect data via webhook
2. Make.com receives the webhook and calls the ElevenLabs API
3. ElevenLabs initiates an AI-powered phone call with personalized information

REQUIRED INFORMATION TO COLLECT:
1. ElevenLabs API Key (found in ElevenLabs dashboard under API Keys)
2. ElevenLabs Agent ID (the ID of the conversational AI agent to use)
3. Twilio Phone Number ID (the phone number connected to the ElevenLabs agent)

SETUP PROCESS:

Step 1: Make.com Scenario Setup
- Create a new scenario in Make.com
- Add a "Webhooks > Custom webhook" module as the trigger
- This webhook will receive data from Clay with these fields:
  * to_number: The prospect's phone number (E.164 format, e.g., +14155551212)
  * personalized_opener: AI-generated personalized opener line
  * prospect_name: The prospect's name

Step 2: Configure HTTP Module
- Add an "HTTP > Make a request" module
- Configure it as follows:
  * URL: https://api.elevenlabs.io/v1/convai/twilio/outbound-call
  * Method: POST
  * Headers:
    - Content-Type: application/json
    - xi-api-key: [USER'S_ELEVENLABS_API_KEY]
  * Body (Raw JSON):
    {
      "agent_id": "[USER'S_AGENT_ID]",
      "agent_phone_number_id": "[USER'S_PHONE_NUMBER_ID]",
      "to_number": {{to_number from webhook}},
      "custom_variables": {
        "opener": {{personalized_opener from webhook}},
        "name": {{prospect_name from webhook}}
      }
    }

Step 3: Variable Mapping in Make.com
- Map the webhook outputs to the HTTP request body:
  * to_number → Use the webhook's to_number field
  * custom_variables.opener → Use the webhook's personalized_opener field
  * custom_variables.name → Use the webhook's prospect_name field

Step 4: Clay Configuration
- In Clay, create or use a table with columns: to_number, personalized_opener, prospect_name
- Add an "HTTP API" enrichment
- Set the webhook URL from Make.com
- Configure the POST body with the three required fields

Step 5: Testing
- Test with sample data:
  {
    "to_number": "+14155551212",
    "personalized_opener": "I saw your recent product launch",
    "prospect_name": "Jane Doe"
  }

IMPORTANT NOTES:
- Phone numbers must be in E.164 format (starting with +, country code, then number)
- The ElevenLabs agent must reference the custom variables in its system prompt
- Example prompt: "Hello {{name}}, {{opener}}"
- Make sure the Twilio phone number is properly connected to your ElevenLabs agent

Ask the user for the required credentials and guide them through each step, providing specific instructions based on their responses."""


def interactive_setup():
    """
    Run an interactive setup process for collecting configuration.
    This can be used by developers testing the integration or by AI agents with user interaction.
    """
    helper = AgenticSetupHelper()
    
    print("=" * 70)
    print("Clay + Make.com + ElevenLabs Integration Setup")
    print("=" * 70)
    print()
    print("This helper will guide you through setting up your integration.")
    print("You'll need:")
    print("  1. ElevenLabs API Key")
    print("  2. ElevenLabs Agent ID")
    print("  3. Twilio Phone Number ID (connected to your agent)")
    print()
    
    # Collect credentials
    api_key = input("Enter your ElevenLabs API Key: ").strip()
    agent_id = input("Enter your ElevenLabs Agent ID: ").strip()
    phone_number_id = input("Enter your Twilio Phone Number ID: ").strip()
    
    print("\nValidating configuration...")
    config = {
        "elevenlabs_api_key": api_key,
        "agent_id": agent_id,
        "agent_phone_number_id": phone_number_id
    }
    
    is_valid, errors = helper.validate_configuration(config)
    
    if not is_valid:
        print("\n⚠️  Configuration has issues:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix these issues and try again.")
        return None
    
    print("\n✅ Configuration validated successfully!")
    print("\nGenerating complete setup configuration...")
    
    complete_config = helper.get_complete_setup_config(api_key, agent_id, phone_number_id)
    
    output_file = "/tmp/makecom_elevenlabs_config.json"
    with open(output_file, "w") as f:
        json.dump(complete_config, f, indent=2)
    
    print(f"\n✅ Configuration saved to: {output_file}")
    print("\nYou can now use this configuration to set up your Make.com scenario.")
    print("\nNext steps:")
    print("  1. Open Make.com and create a new scenario")
    print("  2. Follow the configuration in the JSON file")
    print("  3. Test with the sample payload provided")
    
    return complete_config


if __name__ == "__main__":
    # When run directly, execute the interactive setup
    interactive_setup()
