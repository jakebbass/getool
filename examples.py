#!/usr/bin/env python3
"""
Example: Using the Clay Agent Helper API

This example demonstrates how to use the AgenticSetupHelper programmatically
to build custom automation tools or AI agents.
"""

from clay_agent_helper import AgenticSetupHelper
import json


def example_generate_agent_instructions():
    """Example: Generate structured instructions for an AI agent."""
    print("=" * 70)
    print("Example 1: Generate Agent Instructions")
    print("=" * 70)
    
    helper = AgenticSetupHelper()
    instructions = helper.generate_agent_instructions()
    
    print("\nGenerated instructions for AI agent:")
    print(json.dumps(instructions, indent=2)[:500] + "...")
    print(f"\nTotal setup steps: {len(instructions['setup_steps'])}")


def example_generate_http_body():
    """Example: Generate HTTP body for Make.com."""
    print("\n" + "=" * 70)
    print("Example 2: Generate HTTP Request Body")
    print("=" * 70)
    
    helper = AgenticSetupHelper()
    
    # Your actual credentials (replace with your own)
    agent_id = "agent_abc123"
    phone_number_id = "phone_xyz789"
    
    http_body = helper.generate_http_body(agent_id, phone_number_id)
    
    print("\nHTTP body for Make.com:")
    print(json.dumps(http_body, indent=2))


def example_validate_configuration():
    """Example: Validate a configuration before using it."""
    print("\n" + "=" * 70)
    print("Example 3: Validate Configuration")
    print("=" * 70)
    
    helper = AgenticSetupHelper()
    
    # Example configuration (replace with actual values)
    config = {
        "elevenlabs_api_key": "sk_test_key_12345678901234567890",
        "agent_id": "agent_abc123",
        "agent_phone_number_id": "phone_xyz789"
    }
    
    is_valid, errors = helper.validate_configuration(config)
    
    if is_valid:
        print("\n✅ Configuration is valid!")
    else:
        print("\n❌ Configuration has errors:")
        for error in errors:
            print(f"  - {error}")


def example_complete_setup():
    """Example: Generate a complete setup configuration."""
    print("\n" + "=" * 70)
    print("Example 4: Generate Complete Setup Configuration")
    print("=" * 70)
    
    helper = AgenticSetupHelper()
    
    # Your actual credentials (replace with your own)
    api_key = "sk_test_key_12345678901234567890"
    agent_id = "agent_abc123"
    phone_number_id = "phone_xyz789"
    
    complete_config = helper.get_complete_setup_config(
        api_key, agent_id, phone_number_id
    )
    
    print(f"\nConfiguration status: {complete_config['status']}")
    print(f"Number of Make.com modules: {len(complete_config['makecom_scenario']['modules'])}")
    print(f"Clay columns required: {complete_config['clay_configuration']['table_columns']}")
    
    # Show sample test payload
    print("\nSample test payload:")
    print(json.dumps(complete_config['testing']['sample_webhook_payload'], indent=2))


def example_ai_prompt():
    """Example: Generate a prompt for an AI agent."""
    print("\n" + "=" * 70)
    print("Example 5: Generate AI Agent Prompt")
    print("=" * 70)
    
    helper = AgenticSetupHelper()
    prompt = helper.generate_clay_ai_prompt()
    
    print("\nAI Agent Prompt (first 500 characters):")
    print(prompt[:500] + "...")
    print(f"\nTotal prompt length: {len(prompt)} characters")


def example_custom_ai_agent():
    """Example: Build a custom AI agent that uses the helper."""
    print("\n" + "=" * 70)
    print("Example 6: Custom AI Agent")
    print("=" * 70)
    
    helper = AgenticSetupHelper()
    
    # Simulate AI agent collecting information
    print("\n[AI Agent] I'll help you set up your integration!")
    print("[AI Agent] I need some information from you...\n")
    
    # Get structured instructions to guide the user
    instructions = helper.generate_agent_instructions()
    
    # Show required information
    print("[AI Agent] Here's what I need:")
    for field_name, field_info in instructions['required_information'].items():
        print(f"  • {field_info['description']}")
        print(f"    Format: {field_info['format']}")
        print()
    
    # Simulate collecting information (in real scenario, this would be interactive)
    user_config = {
        "elevenlabs_api_key": "sk_user_provided_key_example",
        "agent_id": "agent_user_123",
        "agent_phone_number_id": "phone_user_456"
    }
    
    # Validate
    is_valid, errors = helper.validate_configuration(user_config)
    
    if is_valid:
        print("[AI Agent] ✅ Great! Your configuration looks good.")
        print("[AI Agent] Generating your setup configuration...")
        
        config = helper.get_complete_setup_config(
            user_config["elevenlabs_api_key"],
            user_config["agent_id"],
            user_config["agent_phone_number_id"]
        )
        
        print(f"[AI Agent] Done! I've created a configuration with {len(config['makecom_scenario']['modules'])} Make.com modules.")
        print("[AI Agent] Now let me guide you through the setup steps...")
        
        # Show first few steps
        for step in instructions['setup_steps'][:3]:
            print(f"\n[AI Agent] Step {step['step']}: {step['description']}")
    else:
        print("[AI Agent] ❌ I found some issues with the configuration:")
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    # Run all examples
    example_generate_agent_instructions()
    example_generate_http_body()
    example_validate_configuration()
    example_complete_setup()
    example_ai_prompt()
    example_custom_ai_agent()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nFor more information, see CLAY_AGENT_SETUP.md")
