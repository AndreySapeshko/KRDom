from fastapi import HTTPException

from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.core.calc.context import CalcContext, InternalWall, Opening
from backend.db import Material
from backend.repositories.calculation import CalculationRepository


def is_exist_material(material: Material, section_id: str) -> bool:
    if not material:
        raise HTTPException(status_code=400, detail=f"Material {section_id} not found")
    return True


async def build_context_from_input(
    repo: CalculationRepository,
    data: CalcInputV1,
) -> CalcContext:
    wall_section = await repo.get_material_by_section_id(data.wall_section_id)
    is_exist_material(wall_section, data.wall_section_id)

    ground_overlap_section = await repo.get_material_by_section_id(data.ground_overlap_section_id)
    is_exist_material(ground_overlap_section, data.ground_overlap_section_id)

    interfloor_overlap_section = await repo.get_material_by_section_id(data.interfloor_overlap_section_id)
    is_exist_material(interfloor_overlap_section, data.interfloor_overlap_section_id)

    attic_overlap_section = await repo.get_material_by_section_id(data.attic_overlap_section_id)
    is_exist_material(attic_overlap_section, data.attic_overlap_section_id)

    roof_section = await repo.get_material_by_section_id(data.roof_section_id)
    is_exist_material(roof_section, data.roof_section_id)

    lath_section = await repo.get_material_by_section_id(data.lath_section_id)
    is_exist_material(lath_section, data.lath_section_id)

    return CalcContext(
        length=data.length,
        width=data.width,
        wall_height=data.wall_height,
        total_floors=data.total_floors,
        is_fronton_short=data.is_fronton_short,
        stud_spacing=data.stud_spacing,
        joist_spacing=data.joist_spacing,
        rafter_spacing=data.rafter_spacing,
        wall_section=wall_section,
        ground_overlap_section=ground_overlap_section,
        interfloor_overlap_section=interfloor_overlap_section,
        attic_overlap_section=attic_overlap_section,
        roof_section=roof_section,
        lath_section=lath_section,
        waste_factor=data.waste_factor,
        roof_pitch_deg=data.roof_pitch_deg,
        eave_overhang=data.eave_overhang,
        gable_overhang=data.gable_overhang,
        lath_step=data.lath_step,
        has_ground_overlap=data.has_ground_overlap,
        has_interfloor_overlap=data.has_interfloor_overlap,
        has_attic_overlap=data.has_attic_overlap,
        ground_blocking_rows=data.ground_blocking_rows,
        interfloor_blocking_rows=data.interfloor_blocking_rows,
        attic_blocking_rows=data.attic_blocking_rows,
        external_openings=[Opening(**o.dict()) for o in data.external_openings],
        internal_walls=[
            InternalWall(length=w.length, openings=[Opening(**o.dict()) for o in w.openings])
            for w in data.internal_walls
        ],
    )
