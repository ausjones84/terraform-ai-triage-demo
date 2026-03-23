"""
rules.py — Pattern-matching rules for Terraform/Azure error classification.

Each rule is a dictionary with:
  - id:          unique rule identifier
  - category:    high-level error category
  - patterns:    list of substrings to match (case-insensitive)
  - title:       short display title
  - what:        plain-English "what happened"
  - why:         plain-English "why it happened"
  - next_steps:  list of recommended actions
  - enterprise:  enterprise-specific context note
  - confidence:  default confidence level (High / Medium / Low)
"""

RULES = [
    # ------------------------------------------------------------------
    # 1. Unsupported argument
    # ------------------------------------------------------------------
    {
        "id": "unsupported_argument",
        "category": "Terraform Code Issue",
        "patterns": ["unsupported argument", "an argument named", "is not expected here"],
        "title": "Unsupported Argument",
        "what": (
            "Terraform encountered an argument in your configuration that is not "
            "recognised by the resource or module block it was placed in."
        ),
        "why": (
            "This usually happens when: (1) a provider version was upgraded and an "
            "argument was renamed or removed, (2) the argument belongs to a different "
            "resource type, or (3) there is a typo in the argument name."
        ),
        "next_steps": [
            "Check the Terraform provider documentation for the exact resource type and version you are using.",
            "Run `terraform providers` to confirm which provider version is locked.",
            "Search for the argument name in the relevant provider changelog — it may have been renamed.",
            "If the argument was added in a newer version, update your version constraint in `required_providers`.",
        ],
        "enterprise": (
            "In enterprise module repositories, argument names sometimes differ between "
            "module wrapper variables and the underlying resource. Check the module's "
            "variable definitions in `modules/<name>/variables.tf` first before editing "
            "the resource directly."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 2. Invalid provider argument — location on metric alert
    # ------------------------------------------------------------------
    {
        "id": "invalid_location_metric_alert",
        "category": "Provider Schema Issue",
        "patterns": [
            "monitor_metric_alert",
            "azurerm_monitor_metric_alert",
            "location",
            "is not expected here",
        ],
        "title": "Invalid location on azurerm_monitor_metric_alert",
        "what": (
            "The `location` argument was supplied to `azurerm_monitor_metric_alert`, "
            "but this resource does not accept a location — Azure Monitor metric alerts "
            "are global resources."
        ),
        "why": (
            "Engineers often copy a resource block from a VM or storage account template "
            "that includes `location`. Metric alert resources in the AzureRM provider do "
            "not have a `location` field because they are not region-scoped."
        ),
        "next_steps": [
            "Remove the `location` line from your `azurerm_monitor_metric_alert` block.",
            "Verify the resource schema at: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_metric_alert",
            "Run `terraform validate` after removing the argument.",
        ],
        "enterprise": (
            "If this alert is defined inside a shared `vm-alerts` module, update the "
            "module main.tf and remove `location` from the resource. Notify consumers "
            "of the module so they remove the input variable too. This is a common issue "
            "when the module was originally written against an older provider."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 3. Missing required argument
    # ------------------------------------------------------------------
    {
        "id": "missing_required_argument",
        "category": "Terraform Code Issue",
        "patterns": ["missing required argument", "the argument", "is required"],
        "title": "Missing Required Argument",
        "what": (
            "A required argument was not supplied to a resource, data source, or module."
        ),
        "why": (
            "Every resource has mandatory fields that must be set. When a field is added "
            "as required in a newer provider version, or when a module variable has no "
            "default, Terraform will fail at plan time."
        ),
        "next_steps": [
            "Read the error message carefully — it will name the resource and missing argument.",
            "Add the missing argument to the relevant .tf file.",
            "If this is a module call, check modules/<name>/variables.tf for required variables with no default value.",
            "Run `terraform validate` to confirm all required arguments are now present.",
        ],
        "enterprise": (
            "In enterprise pipelines, missing arguments often surface when a shared module "
            "is updated centrally and a new required variable is added. Ensure module "
            "changelogs are communicated to all environment teams (dev, prd, dmz) so they "
            "can update their terraform.tfvars accordingly."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 4. Variable type mismatch — object vs string
    # ------------------------------------------------------------------
    {
        "id": "variable_type_mismatch",
        "category": "Variable / Input Format Issue",
        "patterns": [
            "variable",
            "object",
            "string",
            "type constraint",
            "invalid value for",
            "expected type",
        ],
        "title": "Variable Type Mismatch (object expected, string received)",
        "what": (
            "A Terraform variable is declared with a complex type (such as object or "
            "map) but the caller passed a plain string."
        ),
        "why": (
            "This happens when a tfvars file or module call passes a quoted string "
            "where the variable block expects structured data. It can also occur when "
            "environment-specific overrides are applied incorrectly."
        ),
        "next_steps": [
            "Open the variables.tf file for the relevant module and check the type constraint.",
            "Update the calling terraform.tfvars or module block to pass the correct structure.",
            "Example: if type = object({ name = string, rg = string }), pass: { name = \"myapp\", rg = \"rg-prod\" }",
            "Run `terraform validate` after fixing.",
        ],
        "enterprise": (
            "In multi-environment setups (dev/prd/dmz), each environment folder should have "
            "its own terraform.tfvars. A common mistake is copying a string value from a "
            "simpler environment config into one that expects an object. Always validate "
            "variable shapes before promoting configs across environments."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 5. Azure CLI not installed / not found
    # ------------------------------------------------------------------
    {
        "id": "azure_cli_not_installed",
        "category": "Azure CLI / Auth Issue",
        "patterns": [
            "az command not found",
            "azure cli",
            "az login",
            "executable file not found",
            "no such file or directory",
            "az: command not found",
        ],
        "title": "Azure CLI Not Installed or Not in PATH",
        "what": (
            "Terraform cannot find the Azure CLI (az) binary. This is required when "
            "using the AzureCliCredential authentication method."
        ),
        "why": (
            "The Azure CLI is not installed on this machine, or its installation directory "
            "is not included in the system PATH variable."
        ),
        "next_steps": [
            "Install the Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli",
            "After installation, open a new terminal and run: az --version",
            "Authenticate with: az login",
            "Then set your subscription: az account set --subscription <subscription-id>",
            "Re-run `terraform init` and `terraform plan`.",
        ],
        "enterprise": (
            "In enterprise pipelines, the Azure CLI is typically pre-installed on build "
            "agents and authentication is handled via service principal environment "
            "variables (ARM_CLIENT_ID, ARM_CLIENT_SECRET, ARM_TENANT_ID). If you are "
            "running locally, ensure you have completed `az login` and selected the "
            "correct subscription."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 6. 403 AuthorizationFailed
    # ------------------------------------------------------------------
    {
        "id": "authorization_failed_403",
        "category": "Azure RBAC / Permission Issue",
        "patterns": [
            "authorizationfailed",
            "403",
            "the client does not have authorization",
            "does not have authorization to perform action",
            "authorization failed",
        ],
        "title": "403 AuthorizationFailed — Insufficient Azure RBAC Permissions",
        "what": (
            "Azure returned a 403 AuthorizationFailed error. The identity used by "
            "Terraform (your user account or the service principal) does not have "
            "permission to perform the requested operation."
        ),
        "why": (
            "Azure Role-Based Access Control (RBAC) is blocking the action. The required "
            "role assignment (e.g., Contributor, Owner, or a custom role) has not been "
            "granted to the identity at the correct scope."
        ),
        "next_steps": [
            "Identify the action being denied — it is shown in the error message.",
            "In the Azure Portal, go to the target resource > Access control (IAM) > Check access.",
            "Ask your Azure administrator to assign the required role to your user or service principal.",
            "If using a service principal, verify ARM_CLIENT_ID is set to the correct SP.",
            "Do NOT attempt to work around RBAC — it exists for security reasons.",
        ],
        "enterprise": (
            "IMPORTANT: In enterprise environments, 403 errors on certain resources are "
            "EXPECTED and BY DESIGN. Engineers typically do not have write access to "
            "production subscriptions. Terraform plans for prd/ and dmz/ environments "
            "should be executed by a pipeline service principal with scoped permissions. "
            "If you are seeing this locally, confirm whether you should be running against "
            "this environment at all."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 7. Microsoft.Storage/storageAccounts/read denied (backend access)
    # ------------------------------------------------------------------
    {
        "id": "storage_backend_access_denied",
        "category": "Backend / State Issue",
        "patterns": [
            "microsoft.storage/storageaccounts/read",
            "storageaccounts",
            "does not have authorization",
            "storage account",
            "backend",
        ],
        "title": "Access Denied to Azure Storage Backend",
        "what": (
            "Terraform cannot read from (or write to) the Azure Storage Account used as "
            "the remote state backend. The Microsoft.Storage/storageAccounts/read "
            "operation was denied."
        ),
        "why": (
            "The identity running Terraform does not have the Storage Blob Data "
            "Contributor (or equivalent) role on the storage account or container "
            "where state files are stored."
        ),
        "next_steps": [
            "Confirm the backend configuration in your backend.tf (storage account name, container, key).",
            "Ask your Azure administrator to grant Storage Blob Data Contributor on the state storage account.",
            "If you are a developer without state access, you may need to run plans through the pipeline instead.",
            "Check if a SAS token or access key is required — some enterprise configs use key-based auth for the backend.",
        ],
        "enterprise": (
            "EXPECTED BEHAVIOUR in enterprise setups: Engineers typically do NOT have "
            "direct access to the Terraform state storage account. The azurerm backend "
            "is managed by a pipeline service principal. If you need to inspect state, "
            "ask your platform/DevOps team to run `terraform state list` via pipeline, "
            "or request read-only access to the container for your user."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 8. State blob already locked
    # ------------------------------------------------------------------
    {
        "id": "state_blob_locked",
        "category": "Backend / State Issue",
        "patterns": [
            "state blob is already locked",
            "blob is already locked",
            "error locking state",
            "lock id",
            "state lock",
            "leased",
        ],
        "title": "Terraform State File is Locked",
        "what": (
            "Terraform attempted to acquire a lock on the remote state file in Azure "
            "Blob Storage, but the blob is already locked by another process."
        ),
        "why": (
            "A previous Terraform operation (plan, apply, or destroy) either is still "
            "running in another terminal or pipeline, or it was interrupted without "
            "releasing the lock. Azure Blob Storage uses lease-based locking."
        ),
        "next_steps": [
            "First, check if another pipeline run or colleague is actively running Terraform against this environment.",
            "If the lock is stale (the process is definitely not running), retrieve the Lock ID from the error message.",
            "Run: terraform force-unlock <LOCK_ID>",
            "WARNING: Only force-unlock if you are 100% certain no other process is running.",
            "After unlocking, re-run your intended Terraform command.",
        ],
        "enterprise": (
            "In CI/CD pipelines, locks should be released automatically when a job "
            "completes. If a pipeline was cancelled mid-apply, the lock may persist. "
            "Co-ordinate with your DevOps team before force-unlocking in shared "
            "environments (prd/dmz). Never force-unlock without confirmation that no "
            "pipeline is actively writing to state."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 9. action_group_id missing / module output wiring
    # ------------------------------------------------------------------
    {
        "id": "action_group_id_missing",
        "category": "Module Wiring Issue",
        "patterns": [
            "action_group_id",
            "action group",
            "module output",
            "output value",
            "references a resource that does not exist",
        ],
        "title": "action_group_id Missing — Module Output Not Wired",
        "what": (
            "A resource (typically azurerm_monitor_metric_alert) requires an "
            "action_group_id, but the value is either null, empty, or references a "
            "module output that has not been correctly wired."
        ),
        "why": (
            "In enterprise Terraform, the action group is usually created by a shared "
            "action_group module. Its output must be passed to the vm-alerts module "
            "(or similar). If the output reference is missing or the module "
            "dependency is not declared, the value will be null at plan time."
        ),
        "next_steps": [
            "In the calling module or root main.tf, ensure the action_group module is declared and its output is referenced.",
            "Example: action_group_id = module.action_group.action_group_id",
            "Verify the output is defined in modules/action_group/outputs.tf",
            "Confirm the module call appears before the vm-alerts module (or use depends_on).",
            "Run `terraform plan` to verify the reference resolves correctly.",
        ],
        "enterprise": (
            "This is the most common module wiring issue in enterprise Terraform repos. "
            "The pattern is: modules/action_group creates the alert action group and its "
            "id output is passed into modules/vm-alerts as action_group_id. If these "
            "modules are in separate state files, you will need a terraform_remote_state "
            "data source or pass the value via a shared variable. Never hardcode the "
            "action group resource ID."
        ),
        "confidence": "High",
    },

    # ------------------------------------------------------------------
    # 10. Generic / fallback
    # ------------------------------------------------------------------
    {
        "id": "generic_terraform_error",
        "category": "Terraform Code Issue",
        "patterns": ["error", "failed", "terraform"],
        "title": "General Terraform Error",
        "what": (
            "A Terraform error was detected, but it did not match any specific known "
            "pattern in the triage database."
        ),
        "why": (
            "The error may be related to provider configuration, HCL syntax, resource "
            "lifecycle issues, or a dependency ordering problem."
        ),
        "next_steps": [
            "Read the full error message carefully — Terraform error output is usually very descriptive.",
            "Run `terraform validate` to catch syntax and type issues.",
            "Run `terraform plan` with the -refresh=false flag to isolate plan vs refresh errors.",
            "Check the Terraform and provider documentation for the specific resource mentioned.",
            "Search the HashiCorp discuss forums or GitHub issues for the exact error string.",
        ],
        "enterprise": (
            "If this error appeared during a pipeline run, download the full pipeline log "
            "and search for the first occurrence of Error: — there may be an earlier "
            "error that caused this one. Always triage the root cause, not just the last "
            "error in the output."
        ),
        "confidence": "Low",
    },
]
