def make_flux_floorplan_prompt(width: str, length: str, rooms: list[str], prompt: str):
    rooms_text = "\n".join(f"- {r}" for r in rooms)

    return prompt.format(w=width, l=length, r=rooms_text)
