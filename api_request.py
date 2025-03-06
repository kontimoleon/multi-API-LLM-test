import os
import yaml
import logging

from datetime import datetime
from openai import OpenAI, AzureOpenAI

def load_yaml(file_path):
    with open(file_path) as f:
        config = yaml.safe_load(f)
    return config


def append_to_txt_file(data, file_path):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(data)


def create_entry_for_model(provider, model, prompt, response):
    entry = (
        f"API call to {provider} using model {model} with prompt: {prompt}\n"
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        "\n"
        "Response:\n"
        f"{response}\n"
        "\n"
    )
    return entry


def request_response(provider, model_name, prompt):
    if provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    elif provider == "gpustack":
        client = OpenAI(
            base_url="https://gpu.gess-k8s.ethz.ch/v1-openai", 
            api_key=os.getenv("GPUSTACK_API_KEY")
        )
    elif provider == "azure":
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-05-01-preview",
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # make request to client to retrieve chat completion response
    response = client.chat.completions.create(
        model=model_name,
        store=False,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Logging set up
    log_file_path = './logs'
    os.makedirs(log_file_path, exist_ok=True)
    log_filename = f"{log_file_path}/api_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=log_filename,
        filemode="w"
    )
    # Reduce logging level for API-related libraries
    logging.getLogger("openai").setLevel(logging.WARNING)  # Suppresses OpenAI logs below WARNING
    logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppresses HTTPX logs below WARNING

    # Load config
    logging.info("Loading config file...")
    config = load_yaml("config.yaml")
    providers = config["providers"]
    prompt = config["prompt"]

    output_file = f"data/api_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    os.makedirs("data", exist_ok=True)  # Ensure the directory exists
    with open(output_file, "w") as file:
        file.write("")
    logging.info(f"Output file created: {output_file}")

    # Loop through models and providers
    for provider_name, provider_data in providers.items():
        if provider_data["include"]:
            logging.info(f"Using provider: {provider_name}")
            models = provider_data["models"]
            for model in models:
                logging.info(f"Requesting response from {provider_name} using model {model}")
                try:
                    response = request_response(provider_name, model, prompt)
                    data = create_entry_for_model(provider_name, model, prompt, response)
                    append_to_txt_file(data, output_file)
                    logging.info(f"Response from {provider_name} using model {model} written to file.")
                except Exception as e:
                    logging.error(f"Error while querying {provider_name} with model {model}: {e}")
