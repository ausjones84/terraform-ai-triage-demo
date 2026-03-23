# How to Deploy to Azure

## Recommended Azure Service

### Azure Container Apps (Recommended)

- Serverless — scales to zero when not in use (no idle cost)
- Built-in HTTPS with a managed domain
- Easy to connect to Azure Monitor, Log Analytics, and pipelines
- Supports environment variables for secrets (future LLM API keys)
- Managed ingress — no load balancer or Nginx configuration required

### Alternative — Azure App Service

- Simpler to set up if your team already uses App Service
- Better for teams not yet using containers
- More expensive at low traffic (always-on by default)

---

## Architecture

```
Developer / Pipeline
        │
        ▼
  Docker image build
  (FROM python:3.12-slim)
        │
        ▼
  Push to Azure Container Registry (ACR)
        │
        ▼
  Azure Container Apps
  (auto-scaled, HTTPS, managed ingress)
        │
        ▼
  Optional: Azure Front Door / WAF
  (for enterprise traffic management)
```

---

## Step-by-Step Deployment

### 1. Containerise the Application

Create `Dockerfile` in the repo root:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

### 2. Build and Push to Azure Container Registry

```bash
# Create ACR (one-time)
az acr create \
  --resource-group rg-devtools-prd \
  --name acrtriagedemoprd \
  --sku Basic

# Login to ACR
az acr login --name acrtriagedemoprd

# Build and push
docker build -t acrtriagedemoprd.azurecr.io/terraform-ai-triage:latest .
docker push acrtriagedemoprd.azurecr.io/terraform-ai-triage:latest
```

### 3. Create Container Apps Environment

```bash
az containerapp env create \
  --name cae-devtools-prd \
  --resource-group rg-devtools-prd \
  --location uksouth
```

### 4. Deploy the Container App

```bash
az containerapp create \
  --name ca-terraform-triage \
  --resource-group rg-devtools-prd \
  --environment cae-devtools-prd \
  --image acrtriagedemoprd.azurecr.io/terraform-ai-triage:latest \
  --target-port 8501 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 3
```

---

## Why Backend / State RBAC Matters Here

When this tool is extended to call Terraform directly, the Container App managed identity will need:

| Permission | Scope | Why |
|---|---|---|
| `Storage Blob Data Reader` | State storage account | To read .tfstate files for context |
| `Reader` | Target subscription | To enumerate resources for enhanced analysis |

Grant permissions at the **resource group** level to follow the principle of least privilege.

---

## Pipeline Integration

```yaml
# azure-pipelines.yml (partial)
- task: Bash@3
  displayName: 'Run Terraform Plan'
  inputs:
    targetType: 'inline'
    script: terraform plan -out=plan.tfplan 2>&1 | tee plan_output.txt
  continueOnError: true

- task: Bash@3
  displayName: 'Triage Terraform Errors'
  condition: failed()
  inputs:
    targetType: 'inline'
    script: |
      curl -X POST https://ca-terraform-triage.<env>.azurecontainerapps.io/api/analyse \
        -H "Content-Type: application/json" \
        -d "{\"error\": \"$(cat plan_output.txt)\"}"
```

---

## Security Considerations

- Store API keys as **Container Apps secrets**, not environment variables in YAML
- Use **Private ingress** if this tool should only be accessible from your corporate network
- Enable **Managed Identity** on the Container App instead of client secret credentials
- Apply **Azure AD authentication** (Easy Auth) to restrict access to your tenant
