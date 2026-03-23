"""
sample_inputs.py — Pre-loaded error samples for demo purposes.

Each entry is a dict with:
  label:   display name shown in the dropdown
  text:    the raw error text to pre-fill the input box
"""

SAMPLES = [
    {
        "label": "— Select a sample error —",
        "text": "",
    },
    {
        "label": "1 · Unsupported argument (typo in resource block)",
        "text": (
            "Error: Unsupported argument\n\n"
            "  on modules/vm/main.tf line 14, in resource \"azurerm_linux_virtual_machine\" \"main\":\n"
            "  14:   availability_zone = var.availability_zone\n\n"
            "An argument named \"availability_zone\" is not expected here. Did you mean \"zone\"?\n"
        ),
    },
    {
        "label": "2 · Invalid location on azurerm_monitor_metric_alert",
        "text": (
            "Error: Unsupported argument\n\n"
            "  on modules/vm-alerts/main.tf line 8, in resource \"azurerm_monitor_metric_alert\" \"cpu\":\n"
            "  8:   location = var.location\n\n"
            "An argument named \"location\" is not expected here.\n"
        ),
    },
    {
        "label": "3 · Missing required argument",
        "text": (
            "Error: Missing required argument\n\n"
            "  on terraform-scripts/dev/main.tf line 22, in module \"vm\":\n"
            "  22: module \"vm\" {\n\n"
            "The argument \"resource_group_name\" is required, but no definition was found.\n"
        ),
    },
    {
        "label": "4 · Variable type mismatch (object vs string)",
        "text": (
            "Error: Invalid value for input variable\n\n"
            "  on terraform-scripts/prd/terraform.tfvars line 5:\n"
            "  5: tags = \"env=production\"\n\n"
            "The given value is not suitable for var.tags declared in\n"
            "modules/vm/variables.tf: object required, got string.\n"
        ),
    },
    {
        "label": "5 · Azure CLI not installed",
        "text": (
            "Error: building AzureRM Client: obtain subscription() from Azure CLI: "
            "parsing json result from the Azure CLI: waiting for the Azure CLI: "
            "exec: \"az\": executable file not found in $PATH\n"
        ),
    },
    {
        "label": "6 · 403 AuthorizationFailed",
        "text": (
            "Error: creating Resource Group: resources.GroupsClient#CreateOrUpdate:\n"
            "Failure responding to request: StatusCode=403 -- Original Error:\n"
            "autorest/azure: Service returned an error.\n"
            "Status=403 Code=\"AuthorizationFailed\"\n"
            "Message=\"The client 'a1b2c3d4-xxxx-xxxx-xxxx-000000000000' with object id\n"
            "'a1b2c3d4-xxxx-xxxx-xxxx-000000000000' does not have authorization to perform\n"
            "action 'Microsoft.Resources/resourceGroups/write' over scope\n"
            "'/subscriptions/00000000-0000-0000-0000-000000000000'.\n"
            "If access was recently granted, please refresh your credentials.\"\n"
        ),
    },
    {
        "label": "7 · Storage backend access denied",
        "text": (
            "Error: Failed to get existing workspaces: storage: service returned error:\n"
            "StatusCode=403, ErrorCode=AuthorizationFailure,\n"
            "ErrorMessage=This request is not authorized to perform this operation.\n\n"
            "The identity does not have Microsoft.Storage/storageAccounts/read permission\n"
            "on the backend storage account 'stterraformstateprd001'.\n"
        ),
    },
    {
        "label": "8 · State blob already locked",
        "text": (
            "Error: Error locking state: Error acquiring the state lock:\n"
            "state blob is already locked\n"
            "Lock Info:\n"
            "  ID:        f3e2d1c0-aaaa-bbbb-cccc-123456789abc\n"
            "  Path:      terraform-state/prd/terraform.tfstate\n"
            "  Operation: OperationTypePlan\n"
            "  Who:       pipeline-agent@build-server-01\n"
            "  Version:   1.5.7\n"
            "  Created:   2024-01-15 09:23:11.456 +0000 UTC\n"
        ),
    },
    {
        "label": "9 · action_group_id missing (module wiring)",
        "text": (
            "Error: Invalid value for input variable\n\n"
            "  on terraform-scripts/dev/main.tf line 45, in module \"vm_alerts\":\n"
            "  45:   action_group_id = module.action_group.action_group_id\n\n"
            "The given value is not suitable for var.action_group_id declared in\n"
            "modules/vm-alerts/variables.tf: string required.\n\n"
            "Error: module.action_group.action_group_id references a resource that does\n"
            "not exist in the current state. Ensure the action_group module has been\n"
            "applied before referencing its outputs.\n"
        ),
    },
]
