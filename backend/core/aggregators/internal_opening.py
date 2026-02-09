from backend.api.v1.schemas.calc_input import InternalWallIn
from backend.core.aggregators.grouped_openings import get_dict_grouped_openings


def append_dict_by_type(indict: dict, outdict: dict) -> dict:
    for key_in in indict.keys():
        if not outdict.get(key_in):
            outdict[key_in] = indict[key_in]
            continue
        outdict[key_in] += indict[key_in]
    return outdict


def get_grouped_internal_openings(internal_walls: list[InternalWallIn]) -> dict:
    result = {}
    for i_wall in internal_walls:
        openings = get_dict_grouped_openings(i_wall.openings)
        result = append_dict_by_type(openings, result)
    return result
