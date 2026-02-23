import base64

import httpx

from backend.config import OPEN_ROUTER_KEY


async def generate_floorplan_png(prompt: str, filename="plan.png"):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {"Authorization": f"Bearer {OPEN_ROUTER_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": "black-forest-labs/flux.2-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=120) as client:

        # 1) Запрос генерации
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()

        result = resp.json()
        msg = result["choices"][0]["message"]

        # 2) Картинка лежит в msg["images"]
        if "images" not in msg or len(msg["images"]) == 0:
            raise RuntimeError("No images returned")

        data_url = msg["images"][0]["image_url"]["url"]

        # 3) Убираем prefix
        prefix = "data:image/png;base64,"
        if not data_url.startswith(prefix):
            raise RuntimeError("Unexpected image format")

        b64_data = data_url[len(prefix) :]

        # 4) Decode base64 → bytes
        image_bytes = base64.b64decode(b64_data)

        # 5) Save file
        with open(filename, "wb") as f:
            f.write(image_bytes)

        print("Saved:", filename)
        return filename
