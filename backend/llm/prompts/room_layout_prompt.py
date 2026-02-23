ROOM_LAYOUT_PROMPT = """
You are an architect.

Task:
Generate RoomLayoutV1 JSON for a one-storey residential house.
Generate a rectangular room layout.
inside the given building footprint.

House context:
- Family of 4
- One floor
- Footprint is fixed

Rooms required:
- living_room (main central space)
- kitchen (adjacent to living_room)
- 3 bedrooms (private zone)
- 2 bathrooms (non-adjacent)

Entrance and circulation rules (IMPORTANT):
- The entrance from outside MUST go through a vestibule (tambour).
- The vestibule must be placed inside the building footprint.
- Vestibule must connect to a hall or living_room.
- Bedrooms must NOT open directly into the kitchen or outside.
- Bedrooms must be accessed only from a hall/corridor or living_room.
- If needed, add a hall/corridor space to connect rooms logically.

Planning rules:
- living_room should be near the entrance zone
- kitchen must share a wall with living_room
- bedrooms should be grouped in a private zone
- bathrooms should be near bedrooms
- Rectangles must not overlap
- All rectangles must stay inside the footprint
- Layout must look like a real house plan, not random packing

Return JSON строго по формату (RoomLayoutV1):

{
  "version": "1.0",
  "rooms": [
    {"id": "...", "role": "...", "rect": [x1,y1,x2,y2]}
  ],
  "assumptions": []
}

Do NOT generate walls or openings.
Only rooms as rectangles.

"""
