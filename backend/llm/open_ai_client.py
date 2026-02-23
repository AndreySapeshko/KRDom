import asyncio
import json
import time
from typing import Any, Dict

import openai
from openai import AsyncOpenAI

from backend.config import OPEN_AI_KEY
from backend.llm.base_client import BaseLLMClient

client = AsyncOpenAI(api_key=OPEN_AI_KEY)


class OpenAILLMClient(BaseLLMClient):
    client_id = "open_ai"

    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4.1-mini", min_interval: float = 15.0):
        self.client = client
        self.model = model
        self.min_interval = min_interval
        self._last_call = 0
        self._lock = asyncio.Lock()

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
        for attempt in range(5):
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
                raise RuntimeError("LLM returned invalid JSON")

            except openai.RateLimitError as e:
                print(f"openai.RateLimitError: {e}")
                await asyncio.sleep(31)

            except openai.APIError as e:
                print(f"openai.APIError: {e}")
                await asyncio.sleep(2)

        raise RuntimeError("LLM rate limit retry failed")


def get_open_ai_client() -> OpenAILLMClient:
    return OpenAILLMClient(client)
