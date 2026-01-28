import { http } from "./http";
import type { Material } from "../types/api";

export async function fetchMaterials(): Promise<Material[]> {
  const res = await http.get<Material[]>("/materials");
  return res.data;
}
