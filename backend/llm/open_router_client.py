import asyncio
import base64
import json
import time
from typing import Any, Dict

import openai
from openai import AsyncOpenAI

from backend.config import OPEN_ROUTER_KEY, OPEN_ROUTER_URL
from backend.llm.base_client import BaseLLMClient
from backend.llm.prompts.make_floor_plan_prompt import make_prompt_to_image

client = AsyncOpenAI(api_key=OPEN_ROUTER_KEY, base_url=OPEN_ROUTER_URL)


class OpenRouterLLMClient(BaseLLMClient):
    client_id = "open_router"

    def __init__(
        self,
        client: AsyncOpenAI,
        models: list[str] = ["black-forest-labs/flux.2-pro", "mistralai/mistral-medium-3.1"],
        min_interval: float = 31.0,
        retries_per_model: int = 2,
    ):
        self.client = client
        self.models = models
        self.model = ""
        self.min_interval = min_interval
        self._last_call = 0
        self._lock = asyncio.Lock()
        self.retries_per_model = retries_per_model

    async def _throttled(self):
        async with self._lock:
            now = time.time()
            delta = now - self._last_call

            if delta < self.min_interval:
                await asyncio.sleep(self.min_interval - delta)

            self._last_call = time.time()

    async def llm_complete_json(self, prompt: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(input_data, ensure_ascii=False)},
        ]
        for model in self.models:
            self.model = model
            for attempt in range(self.retries_per_model):
                await self._throttled()
                try:
                    resp = await self.client.chat.completions.create(
                        model=self.model, messages=messages, response_format={"type": "json_object"}
                    )

                    content = resp.choices[0].message.content

                    if not content:
                        print(f"if not content: {content}")
                        raise RuntimeError("Empty LLM response")

                    return json.loads(content)

                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    # raise RuntimeError("LLM returned invalid JSON")

                except openai.RateLimitError as e:
                    print(f"openai.RateLimitError: {e}")
                    await asyncio.sleep(31)

                except openai.APIError as e:
                    print(f"openai.APIError: {e}")
                    await asyncio.sleep(2)

        raise RuntimeError("All models failed")

    async def llm_complete_images(self, width: str, length: str, rooms: list[str]):
        prompt = make_prompt_to_image(width, length, rooms)
        for model in self.models:
            self.model = model
            for attempt in range(self.retries_per_model):
                await self._throttled()
                try:
                    result = await client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024")

                    # Картинка приходит в base64
                    image_base64 = result.data[0].b64_json

                    if not image_base64:
                        print(f"if not content: {image_base64}")
                        raise RuntimeError("Empty LLM response")

                    image_bytes = base64.b64decode(image_base64)

                    # Сохраняем в файл
                    with open("floorplan.png", "wb") as f:
                        f.write(image_bytes)

                except openai.RateLimitError as e:
                    print(f"openai.RateLimitError: {e}")
                    await asyncio.sleep(31)

                except openai.APIError as e:
                    print(f"openai.APIError: {e}")
                    await asyncio.sleep(2)

        raise RuntimeError("All models failed")


def get_open_router_client() -> OpenRouterLLMClient:
    return OpenRouterLLMClient(client)
