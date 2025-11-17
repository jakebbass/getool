#!/usr/bin/env python3
"""Tests for getool."""

import unittest
import json
import sys
from io import StringIO
from getool import (
    generate_clay_webhook_input,
    generate_makecom_http_output,
    generate_makecom_config,
    generate_full_blueprint,
    main
)


class TestGetool(unittest.TestCase):
    """Test cases for getool functions."""

    def test_generate_clay_webhook_input(self):
        """Test Clay webhook input generation."""
        result = generate_clay_webhook_input()
        self.assertIsInstance(result, dict)
        self.assertIn("to_number", result)
        self.assertIn("personalized_opener", result)
        self.assertIn("prospect_name", result)
        self.assertEqual(result["to_number"], "+14155551212")
        self.assertEqual(result["personalized_opener"], "just saw you raised your Series A last week")
        self.assertEqual(result["prospect_name"], "Jane Doe")

    def test_generate_makecom_http_output(self):
        """Test Make.com HTTP output generation."""
        result = generate_makecom_http_output()
        self.assertIsInstance(result, dict)
        self.assertIn("agent_id", result)
        self.assertIn("agent_phone_number_id", result)
        self.assertIn("to_number", result)
        self.assertIn("custom_variables", result)
        
        # Check custom_variables structure
        custom_vars = result["custom_variables"]
        self.assertIn("opener", custom_vars)
        self.assertIn("name", custom_vars)
        
        # Check placeholders
        self.assertEqual(result["to_number"], "{{to_number}}")
        self.assertEqual(custom_vars["opener"], "{{personalized_opener}}")
        self.assertEqual(custom_vars["name"], "{{prospect_name}}")

    def test_generate_makecom_config(self):
        """Test Make.com configuration generation."""
        result = generate_makecom_config()
        self.assertIsInstance(result, dict)
        self.assertIn("method", result)
        self.assertIn("url", result)
        self.assertIn("headers", result)
        self.assertIn("body", result)
        
        # Check HTTP method
        self.assertEqual(result["method"], "POST")
        
        # Check URL
        self.assertEqual(result["url"], "https://api.elevenlabs.io/v1/convai/twilio/outbound-call")
        
        # Check headers
        headers = result["headers"]
        self.assertIn("Content-Type", headers)
        self.assertIn("xi-api-key", headers)
        self.assertEqual(headers["Content-Type"], "application/json")
        
        # Check body structure
        body = result["body"]
        self.assertIn("agent_id", body)
        self.assertIn("custom_variables", body)

    def test_generate_full_blueprint(self):
        """Test full blueprint generation."""
        result = generate_full_blueprint()
        self.assertIsInstance(result, dict)
        self.assertIn("blueprint", result)
        
        blueprint = result["blueprint"]
        self.assertIn("description", blueprint)
        self.assertIn("modules", blueprint)
        self.assertIn("variable_mapping", blueprint)
        self.assertIn("setup_instructions", blueprint)
        
        # Check modules
        modules = blueprint["modules"]
        self.assertIn("webhook", modules)
        self.assertIn("http", modules)
        
        # Check webhook module
        webhook = modules["webhook"]
        self.assertEqual(webhook["type"], "trigger")
        self.assertIn("expected_input", webhook)
        
        # Check HTTP module
        http = modules["http"]
        self.assertEqual(http["type"], "action")
        self.assertIn("configuration", http)
        
        # Check setup instructions
        instructions = blueprint["setup_instructions"]
        self.assertIsInstance(instructions, list)
        self.assertGreater(len(instructions), 0)

    def test_json_serializable(self):
        """Test that all outputs are JSON serializable."""
        outputs = [
            generate_clay_webhook_input(),
            generate_makecom_http_output(),
            generate_makecom_config(),
            generate_full_blueprint()
        ]
        
        for output in outputs:
            try:
                json_str = json.dumps(output)
                self.assertIsInstance(json_str, str)
            except (TypeError, ValueError) as e:
                self.fail(f"Output is not JSON serializable: {e}")

    def test_cli_input_option(self):
        """Test CLI with --input option."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        old_argv = sys.argv
        sys.argv = ['getool', '--input']
        
        try:
            result = main()
            output = sys.stdout.getvalue()
            self.assertEqual(result, 0)
            
            # Parse JSON output
            data = json.loads(output)
            self.assertIn("to_number", data)
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv

    def test_cli_output_option(self):
        """Test CLI with --output option."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        old_argv = sys.argv
        sys.argv = ['getool', '--output']
        
        try:
            result = main()
            output = sys.stdout.getvalue()
            self.assertEqual(result, 0)
            
            # Parse JSON output
            data = json.loads(output)
            self.assertIn("agent_id", data)
            self.assertIn("custom_variables", data)
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv

    def test_cli_config_option(self):
        """Test CLI with --config option."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        old_argv = sys.argv
        sys.argv = ['getool', '--config']
        
        try:
            result = main()
            output = sys.stdout.getvalue()
            self.assertEqual(result, 0)
            
            # Parse JSON output
            data = json.loads(output)
            self.assertIn("method", data)
            self.assertIn("url", data)
            self.assertIn("headers", data)
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv

    def test_cli_default_full_option(self):
        """Test CLI default (full blueprint)."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        old_argv = sys.argv
        sys.argv = ['getool']
        
        try:
            result = main()
            output = sys.stdout.getvalue()
            self.assertEqual(result, 0)
            
            # Parse JSON output
            data = json.loads(output)
            self.assertIn("blueprint", data)
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv

    def test_cli_agent_setup_option(self):
        """Test CLI with --agent-setup option."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        old_argv = sys.argv
        sys.argv = ['getool', '--agent-setup']
        
        try:
            result = main()
            output = sys.stdout.getvalue()
            self.assertEqual(result, 0)
            
            # Parse JSON output
            data = json.loads(output)
            self.assertIn("setup_type", data)
            self.assertIn("required_information", data)
            self.assertIn("setup_steps", data)
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv

    def test_cli_agent_prompt_option(self):
        """Test CLI with --agent-prompt option."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        old_argv = sys.argv
        sys.argv = ['getool', '--agent-prompt']
        
        try:
            result = main()
            output = sys.stdout.getvalue()
            self.assertEqual(result, 0)
            
            # Check for text output (not JSON)
            self.assertIn("Clay", output)
            self.assertIn("Make.com", output)
            self.assertIn("ElevenLabs", output)
        finally:
            sys.stdout = old_stdout
            sys.argv = old_argv


if __name__ == '__main__':
    unittest.main()
