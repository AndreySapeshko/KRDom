from backend.api.v1.schemas.calc_input import OpeningIn, OpeningTypes


def opening_to_dict(opening: OpeningIn) -> dict:
    return {"type": opening.type, "width": opening.width, "height": opening.height, "quantity": opening.quantity}


def get_dict_grouped_openings(openings: list[OpeningIn]) -> dict:
    windows = []
    doors = []
    portals = []
    for opening in openings:
        if opening.type == OpeningTypes.WINDOW:
            windows.append(opening)
            continue
        if opening.type == OpeningTypes.DOOR:
            doors.append(opening)
            continue
        if opening.type == OpeningTypes.PORTAL:
            portals.append(opening)
            continue
    result = {}
    if windows:
        result[OpeningTypes.WINDOW] = windows
    if doors:
        result[OpeningTypes.DOOR] = doors
    if portals:
        result[OpeningTypes.PORTAL] = portals

    return result
