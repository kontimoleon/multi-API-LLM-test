# Multi-API LLM Tests

This guide explains how to set up the necessary API keys as environment variables and configure the provider settings for this project.

## Setting Up API Keys

Before running the script, you must define the required API keys as environment variables. This ensures secure access to the necessary services.

### Required Environment Variables
- `OPENAI_API_KEY` - API key for OpenAI services.
- `GPUSTACK_API_KEY` - API key for GPUStack services.

### How to Set Environment Variables

#### Linux / macOS
```sh
export OPENAI_API_KEY="your-openai-api-key"
export GPUSTACK_API_KEY="your-gpustack-api-key"
export AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
export AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint"
```

To make these changes permanent, add them to your `~/.bashrc` or `~/.zshrc` file:
```sh
echo 'export OPENAI_API_KEY="your-openai-api-key"' >> ~/.bashrc
echo 'export GPUSTACK_API_KEY="your-gpustack-api-key"' >> ~/.bashrc
echo 'export AZURE_OPENAI_API_KEY="your-azure-openai-api-key"' >> ~/.bashrc
echo 'export AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
$env:GPUSTACK_API_KEY="your-gpustack-api-key"
$env:AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
$env:AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint"
```
To make them persistent, add them to your user environment variables:
```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-openai-api-key", "User")
[Environment]::SetEnvironmentVariable("GPUSTACK_API_KEY", "your-gpustack-api-key", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY", "your-azure-openai-api-key", "User")
[Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT", "your-azure-openai-endpoint", "User")
```

## Configuration File
The script also relies on a configuration file to specify which API providers to use and which models to include.

### Example Configuration File
```yaml
providers:
  openai:
    include: true
    models:
      - "gpt-4"
      - "gpt-4o-mini"
  
  gpustack:
    include: true
    models:
      - "llama-3.3b"

  azure:
    include: false
    models:
      - "gpt-4"

prompt: "Hi, tell me a joke!"
```

### Configuration Options
- **`providers`**: Specifies available API providers.
  - **`include`**: Set to `true` to enable the provider, `false` to disable it.
  - **`models`**: List of models to use from the provider. If `null`, no models are specified.
- **`prompt`**: The input prompt for the model.

Ensure that the providers you enable match the API keys you have configured.

## Running the Script
Once the API keys are set and the configuration file is ready, you can execute the `api_request.py` script without additional setup.

#TODO: add info on script output.

