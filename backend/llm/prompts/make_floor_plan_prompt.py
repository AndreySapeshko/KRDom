def make_prompt_to_image(width: str, length: str, rooms: list[str]):
    rooms_text = "\n".join(f"- {r}" for r in rooms)

    return f"""
Нарисуй план одноэтажного дома размером {width}×{length} метров.

Помещения:
{rooms_text}

Требования:
- хорошее зонирование (дневная/ночная зона)
- подписи комнат на русском
- внешний размер дома указан
- стиль как интерьерный план (цветной)

Формат: top-down floor plan.
"""
