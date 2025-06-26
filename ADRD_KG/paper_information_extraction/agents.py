from openai import OpenAI
import json
from openai import AsyncOpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from loguru import logger

price_map = {
    "o3-mini": {"input": 1.1, "output": 4.4},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "gpt-4.1": {"input": 1.2, "output": 8.0},
}
class Agent():
    def __init__(self, model = "o3-mini", async_mode=True):
        # Load API keys from JSON file
        api_key_file = "api_keys.json"  # Update this with your file path
        api_key = self.load_api_keys(api_key_file)["SaraQ"]
        
        # Set OpenAI API key
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        self.price = price_map.get(model, {"input": 0, "output": 0})

        # Monitoring input/output token usage separately
        self.usage = {
            f"Step{i}": {"input": 0, "output": 0} for i in range(7)
        }

    def print_usage(self):
        total_input_tokens = sum(v["input"] for v in self.usage.values())
        total_output_tokens = sum(v["output"] for v in self.usage.values())
        total_tokens = total_input_tokens + total_output_tokens

        if total_tokens == 0:
            print("No token usage recorded.")
            return

        print(f"{'Step':<10} {'Input (M)':<12} {'Output (M)':<12} {'Input Cost ($)':<15} {'Output Cost ($)':<15} {'% of Total':<10}")
        print("-" * 80)

        total_input_cost = 0
        total_output_cost = 0

        for step, tokens in self.usage.items():
            input_tokens = tokens["input"]
            output_tokens = tokens["output"]
            if input_tokens + output_tokens == 0:
                continue

            input_million = input_tokens / 1e6
            output_million = output_tokens / 1e6

            input_cost = input_million * self.price["input"]
            output_cost = output_million * self.price["output"]

            step_cost = input_cost + output_cost
            percentage = ((input_tokens + output_tokens) / total_tokens) * 100

            total_input_cost += input_cost
            total_output_cost += output_cost

            print(f"{step:<10} {input_million:<12.3f} {output_million:<12.3f} {input_cost:<15.4f} {output_cost:<15.4f} {percentage:<10.2f}")

        print("-" * 80)
        total_cost = total_input_cost + total_output_cost
        print(f"{'Total':<10} {total_input_tokens/1e6:<12.3f} {total_output_tokens/1e6:<12.3f} {total_input_cost:<15.4f} {total_output_cost:<15.4f} {100.00:<10.2f}")


    def load_api_keys(self, filepath: str) -> dict:
        """Loads API keys from a JSON file."""
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"API key file '{filepath}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from '{filepath}'. Ensure it is correctly formatted.")
    
    @retry(wait=wait_random_exponential(min=1, max=300, exp_base=5), stop=stop_after_attempt(5))
    async def process(self, prompt, step, response_format = None):
        if response_format == "JSON":
            response_format = { "type": "json_object" }
        response = await self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format=response_format
        )
        try:
            self.usage[f"Step{step}"]["input"] += response.usage.prompt_tokens
            self.usage[f"Step{step}"]["output"] += response.usage.completion_tokens
        except:
            logger.warning(f"Token usage fail")
        return response.choices[0].message.content
    
