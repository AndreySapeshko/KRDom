import asyncio
import base64
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from backend.config import OPEN_ROUTER_KEY, OPEN_ROUTER_URL
from backend.llm.make_flux_floorplan_prompt import make_flux_floorplan_prompt
from backend.llm.prompts.flux_clean_plan_prompt import FLUX_CLEAN_PLAN_PROMPT
from backend.llm.prompts.flux_tamplate_plan_prompt import FLUX_TAMPLATE_PLAN_PROMPT

DATA_URL_PREFIX_PNG = "data:image/png;base64,"


def file_to_data_url_png(path: str | Path) -> str:
    """Read PNG bytes and convert to data URL (base64)."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return DATA_URL_PREFIX_PNG + b64


def data_url_to_png_bytes(data_url: str) -> bytes:
    """Decode data:image/png;base64,... to raw PNG bytes."""
    if not data_url.startswith(DATA_URL_PREFIX_PNG):
        raise ValueError(f"Unexpected data URL format (expected PNG base64). Got prefix: {data_url[:32]!r}")
    b64 = data_url[len(DATA_URL_PREFIX_PNG) :]
    return base64.b64decode(b64)


def extract_image_data_url_from_openrouter(resp_json: Dict[str, Any]) -> str:
    """
    OpenRouter image responses often come in:
      choices[0].message.images[0].image_url.url = data:image/png;base64,....
    Sometimes other shapes exist, so we check a few possibilities.
    """
    try:
        msg = resp_json["choices"][0]["message"]
    except Exception as e:
        raise RuntimeError(
            f"Unexpected OpenRouter response shape, missing choices/message: {e}. Keys: {list(resp_json.keys())}"
        )

    # Preferred: message.images
    images = msg.get("images")
    if isinstance(images, list) and images:
        img0 = images[0]
        # e.g. {"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}
        if isinstance(img0, dict):
            image_url_obj = img0.get("image_url")
            if isinstance(image_url_obj, dict) and "url" in image_url_obj:
                return image_url_obj["url"]

    # Some providers may embed in content blocks (less common)
    content = msg.get("content")
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "image_url":
                image_url_obj = item.get("image_url", {})
                if isinstance(image_url_obj, dict) and "url" in image_url_obj:
                    return image_url_obj["url"]

    # Or content is directly a URL/data-url string
    if isinstance(content, str) and content:
        if content.startswith("http") or content.startswith("data:image/"):
            return content

    raise RuntimeError(
        f"No image found in OpenRouter response. message keys={list(msg.keys())}, content type={type(content)}"
    )


@dataclass
class OpenRouterImageToImageConfig:
    api_key: str = OPEN_ROUTER_KEY
    model: str = "black-forest-labs/flux.2-pro"
    base_url: str = OPEN_ROUTER_URL
    timeout_s: float = 240.0
    min_interval_s: float = 2.0  # throttle between calls
    retries: int = 2  # retries per request
    backoff_s: float = 2.0  # base backoff


class OpenRouterImageToImageClient:
    """
    Async client for OpenRouter multimodal image-to-image:
      - Sends template image as reference
      - Receives generated image as data URL base64
      - Saves PNG
    """

    def __init__(self, config: OpenRouterImageToImageConfig):
        self.cfg = config
        self._lock = asyncio.Lock()
        self._last_call = 0.0

    async def _throttle(self):
        async with self._lock:
            now = time.time()
            delta = now - self._last_call
            if delta < self.cfg.min_interval_s:
                await asyncio.sleep(self.cfg.min_interval_s - delta)
            self._last_call = time.time()

    def _headers(self) -> Dict[str, str]:
        # OpenRouter supports optional headers like HTTP-Referer / X-Title.
        # If you have a website/app name, it's worth setting for rate-limit fairness.
        return {
            "Authorization": f"Bearer {self.cfg.api_key}",
            "Content-Type": "application/json",
        }

    def _endpoint(self) -> str:
        return f"{self.cfg.base_url.rstrip('/')}/chat/completions"

    async def generate_from_template(
        self,
        template_png_path: str,
        instruction_text: str,
        out_png_path: str,
        *,
        extra_negative: Optional[str] = None,
    ) -> str:
        """
        Image-to-image generation:
          - template_png_path: your rendered outer-wall template png
          - instruction_text: prompt that tells model how to fill the template
          - out_png_path: where to save output PNG
        """

        template_data_url = file_to_data_url_png(template_png_path)

        prompt = instruction_text.strip()
        if extra_negative:
            prompt = prompt + "\n\nNegative:\n" + extra_negative.strip()

        payload = {
            "model": self.cfg.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": template_data_url}},
                    ],
                }
            ],
        }

        async with httpx.AsyncClient(timeout=self.cfg.timeout_s) as http:
            for attempt in range(self.cfg.retries + 1):
                await self._throttle()
                try:
                    r = await http.post(self._endpoint(), headers=self._headers(), json=payload)
                    r.raise_for_status()
                    data = r.json()

                    data_url = extract_image_data_url_from_openrouter(data)
                    png_bytes = data_url_to_png_bytes(data_url)

                    with open(out_png_path, "wb") as f:
                        f.write(png_bytes)

                    return out_png_path

                except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                    # For debugging: include body snippet if available
                    body = ""
                    try:
                        body = e.response.text[:500] if hasattr(e, "response") and e.response is not None else ""
                    except Exception:
                        pass

                    if attempt >= self.cfg.retries:
                        raise RuntimeError(f"OpenRouter request failed after retries: {e}. Body: {body}") from e

                    await asyncio.sleep(self.cfg.backoff_s * (attempt + 1))

                except Exception:
                    if attempt >= self.cfg.retries:
                        raise
                    await asyncio.sleep(self.cfg.backoff_s * (attempt + 1))

        raise RuntimeError("Unreachable: generation loop exited unexpectedly")

    # --- Convenience prompts ---

    async def fill_template(
        self,
        template_png_path: str | Path,
        out_png_path: str,
        *,
        house_width: str = "8",
        house_length: str = "10",
        rooms: Optional[List[str]] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Fills the template with a plan. Keeps outer walls unchanged, draws interior partitions inside.
        """
        if rooms is None:
            rooms = [
                "1. Living room 25+ m² with panoramic windows",
                "2. Kitchen 13+ m²",
                "3. Bedroom 1 (12+ m²)",
                "4. Bedroom 2 (12+ m²)",
                "5. Bathroom 1 (4+ m²)",
                "6. Bathroom 2 (4+ m²)",
                "7. Entrance hall (5+ m²)",
            ]

        instruction = make_flux_floorplan_prompt(house_width, house_length, rooms, FLUX_TAMPLATE_PLAN_PROMPT).strip()

        if notes:
            instruction += "\n\nAdditional notes:\n" + notes.strip()

        negatives = (
            "no 3D, no perspective, no isometric, no furniture icons, " "no shadows, no exterior view, no decorations"
        )

        return await self.generate_from_template(
            template_png_path=template_png_path,
            instruction_text=instruction,
            out_png_path=out_png_path,
            extra_negative=negatives,
        )

    async def cleanup_walls_only(
        self,
        noisy_plan_png_path: str,
        out_png_path: str,
    ) -> str:
        """
        Second-pass cleanup: remove furniture/textures, keep only walls.
        Useful before OpenCV extraction.
        """
        noisy_data_url = file_to_data_url_png(noisy_plan_png_path)

        instruction = FLUX_CLEAN_PLAN_PROMPT.strip()

        payload = {
            "model": self.cfg.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction},
                        {"type": "image_url", "image_url": {"url": noisy_data_url}},
                    ],
                }
            ],
        }

        async with httpx.AsyncClient(timeout=self.cfg.timeout_s) as http:
            for attempt in range(self.cfg.retries + 1):
                await self._throttle()
                try:
                    r = await http.post(self._endpoint(), headers=self._headers(), json=payload)
                    r.raise_for_status()
                    data = r.json()

                    data_url = extract_image_data_url_from_openrouter(data)
                    png_bytes = data_url_to_png_bytes(data_url)

                    with open(out_png_path, "wb") as f:
                        f.write(png_bytes)

                    return out_png_path

                except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                    body = ""
                    try:
                        body = e.response.text[:500] if hasattr(e, "response") and e.response is not None else ""
                    except Exception:
                        pass

                    if attempt >= self.cfg.retries:
                        raise RuntimeError(f"OpenRouter cleanup failed after retries: {e}. Body: {body}") from e

                    await asyncio.sleep(self.cfg.backoff_s * (attempt + 1))

                except Exception:
                    if attempt >= self.cfg.retries:
                        raise
                    await asyncio.sleep(self.cfg.backoff_s * (attempt + 1))

        raise RuntimeError("Unreachable: cleanup loop exited unexpectedly")


# -------------------------
# Example usage
# -------------------------


async def _demo():
    cfg = OpenRouterImageToImageConfig(
        api_key=OPEN_ROUTER_KEY,
        model="black-forest-labs/flux.2-pro",
        min_interval_s=2.0,
        retries=2,
    )
    client = OpenRouterImageToImageClient(cfg)

    # 1) Fill template
    await client.fill_template(
        template_png_path="house_template.png",
        out_png_path="plan_raw.png",
        house_width="8",
        house_length="10",
        notes="Entrance at the bottom side; living room on the left.",
    )

    # 2) Cleanup walls only
    await client.cleanup_walls_only(noisy_plan_png_path="plan_raw.png", out_png_path="plan_walls_only.png")

    print("Done: plan_raw.png, plan_walls_only.png")


if __name__ == "__main__":
    asyncio.run(_demo())
