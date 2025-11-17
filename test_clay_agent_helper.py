#!/usr/bin/env python3
"""Tests for clay_agent_helper."""

import unittest
import json
from clay_agent_helper import (
    SetupValidator,
    AgenticSetupHelper
)


class TestSetupValidator(unittest.TestCase):
    """Test cases for SetupValidator class."""
    
    def setUp(self):
        self.validator = SetupValidator()
    
    def test_valid_phone_number(self):
        """Test validation of valid phone numbers."""
        valid_numbers = [
            "+14155551212",
            "+442071234567",
            "+33123456789",
            "+12125551234"
        ]
        for number in valid_numbers:
            valid, msg = self.validator.validate_phone_number(number)
            self.assertTrue(valid, f"Phone number {number} should be valid")
    
    def test_invalid_phone_number(self):
        """Test validation of invalid phone numbers."""
        invalid_numbers = [
            "14155551212",      # Missing +
            "",                 # Empty
            "1-415-555-1212",   # Wrong format
            "+0123456789"       # Invalid country code (starts with 0)
        ]
        for number in invalid_numbers:
            valid, msg = self.validator.validate_phone_number(number)
            self.assertFalse(valid, f"Phone number {number} should be invalid")
    
    def test_valid_api_key(self):
        """Test validation of valid API keys."""
        valid_keys = [
            "sk_abc123xyz456def789",
            "a" * 32,  # Long enough
            "test_api_key_12345"
        ]
        for key in valid_keys:
            valid, msg = self.validator.validate_api_key(key)
            self.assertTrue(valid, f"API key should be valid")
    
    def test_invalid_api_key(self):
        """Test validation of invalid API keys."""
        invalid_keys = [
            "",                         # Empty
            "short",                    # Too short
            "[YOUR_API_KEY]",          # Placeholder
            "[PLACEHOLDER]"            # Placeholder
        ]
        for key in invalid_keys:
            valid, msg = self.validator.validate_api_key(key)
            self.assertFalse(valid, f"API key '{key}' should be invalid")
    
    def test_valid_agent_id(self):
        """Test validation of valid agent IDs."""
        valid_ids = [
            "agent_abc123",
            "ag_xyz789",
            "test_agent_id"
        ]
        for agent_id in valid_ids:
            valid, msg = self.validator.validate_agent_id(agent_id)
            self.assertTrue(valid, f"Agent ID should be valid")
    
    def test_invalid_agent_id(self):
        """Test validation of invalid agent IDs."""
        invalid_ids = [
            "",                     # Empty
            "[YOUR_AGENT_ID]",     # Placeholder
            "[PLACEHOLDER]"        # Placeholder
        ]
        for agent_id in invalid_ids:
            valid, msg = self.validator.validate_agent_id(agent_id)
            self.assertFalse(valid, f"Agent ID '{agent_id}' should be invalid")


class TestAgenticSetupHelper(unittest.TestCase):
    """Test cases for AgenticSetupHelper class."""
    
    def setUp(self):
        self.helper = AgenticSetupHelper()
    
    def test_generate_agent_instructions(self):
        """Test generation of agent instructions."""
        instructions = self.helper.generate_agent_instructions()
        
        # Check structure
        self.assertIsInstance(instructions, dict)
        self.assertIn("setup_type", instructions)
        self.assertIn("required_information", instructions)
        self.assertIn("setup_steps", instructions)
        self.assertIn("helper_methods", instructions)
        
        # Check required information
        req_info = instructions["required_information"]
        self.assertIn("elevenlabs_api_key", req_info)
        self.assertIn("agent_id", req_info)
        self.assertIn("agent_phone_number_id", req_info)
        
        # Check setup steps
        steps = instructions["setup_steps"]
        self.assertIsInstance(steps, list)
        self.assertGreater(len(steps), 0)
        
        # Verify first step structure
        first_step = steps[0]
        self.assertIn("step", first_step)
        self.assertIn("action", first_step)
        self.assertIn("description", first_step)
    
    def test_generate_http_body(self):
        """Test HTTP body generation."""
        agent_id = "test_agent_123"
        phone_id = "test_phone_456"
        
        body = self.helper.generate_http_body(agent_id, phone_id)
        
        # Check structure
        self.assertIsInstance(body, dict)
        self.assertEqual(body["agent_id"], agent_id)
        self.assertEqual(body["agent_phone_number_id"], phone_id)
        self.assertEqual(body["to_number"], "{{to_number}}")
        
        # Check custom variables
        self.assertIn("custom_variables", body)
        custom_vars = body["custom_variables"]
        self.assertEqual(custom_vars["opener"], "{{personalized_opener}}")
        self.assertEqual(custom_vars["name"], "{{prospect_name}}")
    
    def test_validate_configuration_valid(self):
        """Test validation of valid configuration."""
        config = {
            "elevenlabs_api_key": "sk_test_key_12345678901234567890",
            "agent_id": "agent_test_123",
            "agent_phone_number_id": "phone_test_456"
        }
        
        is_valid, errors = self.helper.validate_configuration(config)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_configuration_missing_fields(self):
        """Test validation with missing fields."""
        config = {
            "elevenlabs_api_key": "sk_test_key_12345678901234567890"
        }
        
        is_valid, errors = self.helper.validate_configuration(config)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check for specific missing fields
        error_text = " ".join(errors)
        self.assertIn("agent_id", error_text)
        self.assertIn("agent_phone_number_id", error_text)
    
    def test_validate_configuration_invalid_values(self):
        """Test validation with invalid values."""
        config = {
            "elevenlabs_api_key": "short",  # Too short
            "agent_id": "[YOUR_AGENT_ID]",  # Placeholder
            "agent_phone_number_id": ""     # Empty
        }
        
        is_valid, errors = self.helper.validate_configuration(config)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_get_complete_setup_config(self):
        """Test generation of complete setup configuration."""
        api_key = "sk_test_key_12345678901234567890"
        agent_id = "agent_test_123"
        phone_id = "phone_test_456"
        
        config = self.helper.get_complete_setup_config(api_key, agent_id, phone_id)
        
        # Check structure
        self.assertIsInstance(config, dict)
        self.assertIn("status", config)
        self.assertIn("makecom_scenario", config)
        self.assertIn("clay_configuration", config)
        self.assertIn("testing", config)
        
        # Check status
        self.assertEqual(config["status"], "valid")
        
        # Check Make.com scenario
        scenario = config["makecom_scenario"]
        self.assertIn("modules", scenario)
        modules = scenario["modules"]
        self.assertEqual(len(modules), 2)
        
        # Check webhook module
        webhook = modules[0]
        self.assertEqual(webhook["type"], "webhook")
        self.assertIn("configuration", webhook)
        
        # Check HTTP module
        http_module = modules[1]
        self.assertEqual(http_module["type"], "http")
        http_config = http_module["configuration"]
        self.assertEqual(http_config["method"], "POST")
        self.assertIn("xi-api-key", str(http_config["headers"]))
        
        # Check Clay configuration
        clay_config = config["clay_configuration"]
        self.assertIn("table_columns", clay_config)
        self.assertIn("http_api_enrichment", clay_config)
        
        # Check testing section
        testing = config["testing"]
        self.assertIn("sample_webhook_payload", testing)
        self.assertIn("expected_api_call", testing)
    
    def test_get_complete_setup_config_invalid(self):
        """Test complete setup with invalid configuration."""
        api_key = "short"  # Invalid
        agent_id = "[PLACEHOLDER]"  # Invalid
        phone_id = ""  # Invalid
        
        config = self.helper.get_complete_setup_config(api_key, agent_id, phone_id)
        
        # Should still return a structure but with invalid status
        self.assertEqual(config["status"], "invalid")
        self.assertGreater(len(config["errors"]), 0)
    
    def test_generate_clay_ai_prompt(self):
        """Test generation of Clay AI prompt."""
        prompt = self.helper.generate_clay_ai_prompt()
        
        # Check that prompt is a non-empty string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
        
        # Check for key content
        self.assertIn("Clay", prompt)
        self.assertIn("Make.com", prompt)
        self.assertIn("ElevenLabs", prompt)
        self.assertIn("webhook", prompt.lower())
        self.assertIn("api", prompt.lower())
        
        # Check for step-by-step structure
        self.assertIn("Step 1", prompt)
        self.assertIn("Step 2", prompt)
    
    def test_json_serializable(self):
        """Test that all outputs are JSON serializable."""
        outputs = [
            self.helper.generate_agent_instructions(),
            self.helper.generate_http_body("test_agent", "test_phone"),
            self.helper.get_complete_setup_config(
                "sk_test_12345678901234567890",
                "agent_test",
                "phone_test"
            )
        ]
        
        for output in outputs:
            try:
                json_str = json.dumps(output)
                self.assertIsInstance(json_str, str)
            except (TypeError, ValueError) as e:
                self.fail(f"Output is not JSON serializable: {e}")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_complete_workflow(self):
        """Test the complete setup workflow."""
        helper = AgenticSetupHelper()
        
        # Step 1: Get agent instructions
        instructions = helper.generate_agent_instructions()
        self.assertIn("setup_steps", instructions)
        
        # Step 2: Collect configuration
        config = {
            "elevenlabs_api_key": "sk_test_key_12345678901234567890",
            "agent_id": "agent_test_123",
            "agent_phone_number_id": "phone_test_456"
        }
        
        # Step 3: Validate configuration
        is_valid, errors = helper.validate_configuration(config)
        self.assertTrue(is_valid, f"Configuration should be valid, errors: {errors}")
        
        # Step 4: Generate complete setup
        complete_config = helper.get_complete_setup_config(
            config["elevenlabs_api_key"],
            config["agent_id"],
            config["agent_phone_number_id"]
        )
        
        # Verify the complete configuration
        self.assertEqual(complete_config["status"], "valid")
        self.assertEqual(len(complete_config["errors"]), 0)
        
        # Verify Make.com scenario structure
        scenario = complete_config["makecom_scenario"]
        self.assertEqual(len(scenario["modules"]), 2)
        
        # Verify HTTP module has correct configuration
        http_module = scenario["modules"][1]
        http_config = http_module["configuration"]
        self.assertEqual(
            http_config["url"],
            "https://api.elevenlabs.io/v1/convai/twilio/outbound-call"
        )
        
        # Verify testing payload is complete
        test_payload = complete_config["testing"]["sample_webhook_payload"]
        self.assertIn("to_number", test_payload)
        self.assertIn("personalized_opener", test_payload)
        self.assertIn("prospect_name", test_payload)


if __name__ == '__main__':
    unittest.main()
