export type OpeningType = "DOOR" | "WINDOW" | "PORTAL";

export type OpeningIn = {
  type: OpeningType;
  width: number;
  height: number;
  quantity: number;
};

export type InternalWallIn = {
  length: number;
  openings: OpeningIn[];
};

export type CalcInputV1 = {
  length: number;
  width: number;
  wall_height: number;
  total_floors: number;
  is_fronton_short: boolean;

  stud_spacing: number;
  joist_spacing: number;
  rafter_spacing: number;

  wall_section_id: string;
  ground_overlap_section_id: string;
  interfloor_overlap_section_id: string;
  attic_overlap_section_id: string;
  roof_section_id: string;
  lath_section_id: string;
  counter_lath_section_id: string;

  waste_factor: number;

  roof_pitch_deg: number;
  eave_overhang: number;
  gable_overhang: number;
  lath_step: number;
  ties_enabled: boolean;

  has_ground_overlap: boolean;
  has_interfloor_overlap: boolean;
  has_attic_overlap: boolean;

  ground_blocking_rows: number;
  interfloor_blocking_rows: number;
  attic_blocking_rows: number;

  external_openings: OpeningIn[];
  internal_walls: InternalWallIn[];
};

export type Material = {
  id: string;
  section_id: string;
  width_mm: number;
  height_mm: number;
  length_mm: number | null;
  kind: string;
  is_active: boolean;
};

export type SectionTotal = {
  section_id: string;
  lm: number;
  lm_with_waste: number;
  volume_m3: number;
};

export type GroupTotal = {
  group: string;
  totals_by_section: SectionTotal[];
};

export type CalcSummary = {
  waste_factor: number;
  total_usable_area_of_board: number;
  volume_total_without_waste_m3: number;
  volume_total_m3: number;
  volume_waste_m3: number;
  total_volume_insulation: number;

  total_roof_area: number;
  total_overhang_area: number;
  total_roof_perimeter: number;
  total_length_ridge: number;
  total_length_gable: number;
  total_length_eave: number;

  total_external_walls_area: number;
  total_internal_walls_area: number;
  total_ceilings_area: number;
  total_floors_area: number;
  width_building: number;
  length_building: number;
  height_building: number;
  roof_pitch_deg: number;
};

export type GroupEnum =
  | "EXTERNAL_WALLS"
  | "INTERNAL_WALLS"
  | "GROUND_OVERLAP"
  | "INTERFLOOR_OVERLAP"
  | "ATTIC_OVERLAP"
  | "ROOF_STRUCT";

export type ElementEnum =
  | "STUDS"
  | "PLATES_BOTTOM"
  | "PLATES_TOP"
  | "OPENING_FRAME"
  | "JOISTS"
  | "RIM"
  | "BLOCKING"
  | "RAFTERS"
  | "RIDGE"
  | "TIES"
  | "LATH"
  | "COUNTER_LATH";

  export type CalcItem = {
  group: GroupEnum;
  element: ElementEnum;
  section_id: string;

  lm: number;
  lm_with_waste: number;
  volume_m3: number;
};

export type PlanningRequirementsV1 = {
  version: string;
  building: Record<string, unknown>;
  structural_params: Record<string, unknown>;
  planning_requirements: Record<string, unknown>;
  assumptions: string[];
};

export type CalcResultV1 = {
  items: CalcItem[];
  totals_by_section: SectionTotal[];
  totals_by_group: GroupTotal[];
  external_openings: Record<OpeningType, OpeningIn[]>;
  internal_openings: Record<OpeningType, OpeningIn[]>;
  summary: CalcSummary;
};

export type CalcResponseV1 = {
  calc_version: string;
  calc_id: string;
  calc_result: CalcResultV1;
  planning_requirements: PlanningRequirementsV1;
};
// for git
