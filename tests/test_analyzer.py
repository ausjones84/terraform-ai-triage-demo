tests/test_analyzer.py"""
test_analyzer.py — Unit tests for the Terraform AI Triage analyzer.

Run with:
    pytest tests/ -v
"""

import sys
import os

# Ensure the app directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from analyzer import analyze  # noqa: E402


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestEmptyInput:
    def test_empty_string_returns_no_input(self):
        result = analyze("")
        assert result["rule_id"] == "no_input"
        assert result["confidence"] == "N/A"

    def test_whitespace_only_returns_no_input(self):
        result = analyze("   \n  ")
        assert result["rule_id"] == "no_input"


class TestUnsupportedArgument:
    def test_basic_match(self):
        error = 'An argument named "availability_zone" is not expected here.'
        result = analyze(error)
        assert result["rule_id"] == "unsupported_argument"
        assert result["category"] == "Terraform Code Issue"
        assert result["confidence"] in ("High", "Medium")

    def test_case_insensitive(self):
        error = "UNSUPPORTED ARGUMENT: an argument named foo is not expected here"
        result = analyze(error)
        assert result["rule_id"] == "unsupported_argument"


class TestInvalidLocationMetricAlert:
    def test_location_on_metric_alert(self):
        error = (
            'on modules/vm-alerts/main.tf line 8, in resource '
            '"azurerm_monitor_metric_alert" "cpu":\n'
            '  8:   location = var.location\n\n'
            'An argument named "location" is not expected here.'
        )
        result = analyze(error)
        assert result["rule_id"] == "invalid_location_metric_alert"
        assert result["category"] == "Provider Schema Issue"


class TestMissingRequiredArgument:
    def test_missing_argument(self):
        error = 'The argument "resource_group_name" is required, but no definition was found.'
        result = analyze(error)
        assert result["rule_id"] == "missing_required_argument"


class TestAuthorizationFailed:
    def test_403_match(self):
        error = (
            "StatusCode=403 Code=\"AuthorizationFailed\" "
            "Message=\"The client does not have authorization to perform action\""
        )
        result = analyze(error)
        assert result["rule_id"] == "authorization_failed_403"
        assert result["category"] == "Azure RBAC / Permission Issue"

    def test_enterprise_note_present(self):
        error = "authorizationfailed 403"
        result = analyze(error)
        assert len(result["enterprise"]) > 0


class TestStorageBackendAccessDenied:
    def test_storage_backend(self):
        error = (
            "does not have authorization to perform this operation. "
            "Microsoft.Storage/storageAccounts/read denied on backend storage account."
        )
        result = analyze(error)
        assert result["rule_id"] == "storage_backend_access_denied"


class TestStateLocked:
    def test_lock_detection(self):
        error = (
            "Error locking state: Error acquiring the state lock: "
            "state blob is already locked\nLock ID: abc-123"
        )
        result = analyze(error)
        assert result["rule_id"] == "state_blob_locked"
        assert any("force-unlock" in step.lower() for step in result["next_steps"])


class TestActionGroupId:
    def test_action_group_wiring(self):
        error = (
            "module.action_group.action_group_id references a resource "
            "that does not exist in the current state."
        )
        result = analyze(error)
        assert result["rule_id"] == "action_group_id_missing"
        assert result["category"] == "Module Wiring Issue"


class TestAzureCLI:
    def test_cli_not_found(self):
        error = 'exec: "az": executable file not found in $PATH'
        result = analyze(error)
        assert result["rule_id"] == "azure_cli_not_installed"
        assert result["category"] == "Azure CLI / Auth Issue"


class TestGenericFallback:
    def test_unrecognised_error(self):
        error = "something went wrong with terraform in an unspecified way"
        result = analyze(error)
        assert result["rule_id"] == "generic_terraform_error"
        assert result["confidence"] == "Low"


class TestResultStructure:
    """Every result must contain all required keys."""

    REQUIRED_KEYS = [
        "rule_id", "category", "title", "confidence",
        "what", "why", "next_steps", "enterprise", "raw_input"
    ]

    def test_all_keys_present(self):
        result = analyze("Error: unsupported argument is not expected here")
        for key in self.REQUIRED_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_next_steps_is_list(self):
        result = analyze("Error: unsupported argument is not expected here")
        assert isinstance(result["next_steps"], list)
        assert len(result["next_steps"]) > 0
