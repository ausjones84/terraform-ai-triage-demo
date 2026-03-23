# Sample Outputs

This file shows the exact structured output produced by the triage tool for common error inputs.

---

## Sample 1 — Unsupported Argument

**Input:**
```
Error: Unsupported argument

  on modules/vm/main.tf line 14, in resource "azurerm_linux_virtual_machine" "main":
  14:   availability_zone = var.availability_zone

An argument named "availability_zone" is not expected here. Did you mean "zone"?
```

**Output:**

| Field | Value |
|---|---|
| Category | Terraform Code Issue |
| Confidence | High |
| Title | Unsupported Argument |
| What happened | Terraform encountered an argument not recognised by the resource block |
| Why it happened | Provider upgrade renamed the argument, or a typo in the argument name |
| Next steps | Check provider docs, run terraform providers, search changelog |
| Enterprise context | Check module variables.tf before editing the resource directly |
| Recommended action | Check the Terraform provider documentation for the exact resource type and version |

---

## Sample 2 — Invalid Location on Metric Alert

**Input:**
```
Error: Unsupported argument

  on modules/vm-alerts/main.tf line 8, in resource "azurerm_monitor_metric_alert" "cpu":
  8:   location = var.location

An argument named "location" is not expected here.
```

**Output:**

| Field | Value |
|---|---|
| Category | Provider Schema Issue |
| Confidence | High |
| Title | Invalid location on azurerm_monitor_metric_alert |
| What happened | location argument supplied to a resource that does not accept it — metric alerts are global |
| Why it happened | Copied from a VM template that includes location |
| Next steps | Remove location line, validate, check provider docs |
| Enterprise context | Update shared module, notify all environment consumers |
| Recommended action | Remove the location line from your azurerm_monitor_metric_alert block |

---

## Sample 3 — 403 AuthorizationFailed

**Input:**
```
Error: creating Resource Group: StatusCode=403 Code="AuthorizationFailed"
Message="The client 'a1b2c3d4-...' does not have authorization to perform
action 'Microsoft.Resources/resourceGroups/write'"
```

**Output:**

| Field | Value |
|---|---|
| Category | Azure RBAC / Permission Issue |
| Confidence | High |
| Title | 403 AuthorizationFailed — Insufficient Azure RBAC Permissions |
| What happened | Azure returned 403; identity lacks permission for the operation |
| Why it happened | Required role not assigned to user/SP at correct scope |
| Next steps | Check error for denied action, review IAM in Portal, request role assignment |
| Enterprise context | In enterprise envs, this is EXPECTED — Pipeline SP handles prd/dmz, not local engineers |
| Recommended action | Identify the action being denied — shown in the error message |

---

## Sample 4 — State Blob Locked

**Input:**
```
Error: Error locking state: Error acquiring the state lock:
state blob is already locked
Lock Info:
  ID:        f3e2d1c0-aaaa-bbbb-cccc-123456789abc
  Path:      terraform-state/prd/terraform.tfstate
  Operation: OperationTypePlan
  Who:       pipeline-agent@build-server-01
```

**Output:**

| Field | Value |
|---|---|
| Category | Backend / State Issue |
| Confidence | High |
| Title | Terraform State File is Locked |
| What happened | Terraform could not acquire the lock on the remote state blob |
| Why it happened | Previous operation still running or interrupted without releasing lock |
| Next steps | Verify no active run, retrieve Lock ID, run terraform force-unlock |
| Enterprise context | Co-ordinate with DevOps team before force-unlocking in prd/dmz |
| Recommended action | First, check if another pipeline run or colleague is actively running Terraform |

---

## Sample 5 — action_group_id Missing

**Input:**
```
Error: module.action_group.action_group_id references a resource that does
not exist in the current state.
```

**Output:**

| Field | Value |
|---|---|
| Category | Module Wiring Issue |
| Confidence | High |
| Title | action_group_id Missing — Module Output Not Wired |
| What happened | action_group_id is null — module output not correctly referenced |
| Why it happened | action_group module output not passed to vm-alerts module call |
| Next steps | Wire action_group_id = module.action_group.action_group_id, verify outputs.tf |
| Enterprise context | Classic pattern: action_group output feeds vm-alerts. Never hardcode the ID |
| Recommended action | Ensure the action_group module is declared and its output is referenced |

---

## Sample 6 — Azure CLI Not Installed

**Input:**
```
Error: building AzureRM Client: exec: "az": executable file not found in $PATH
```

**Output:**

| Field | Value |
|---|---|
| Category | Azure CLI / Auth Issue |
| Confidence | High |
| Title | Azure CLI Not Installed or Not in PATH |
| What happened | Terraform cannot find the az binary |
| Why it happened | Azure CLI not installed, or install directory not in PATH |
| Next steps | Install CLI, open new terminal, az --version, az login, set subscription |
| Enterprise context | Pipelines use service principal env vars — local devs need full CLI setup |
| Recommended action | Install the Azure CLI from the Microsoft documentation |
