import { http } from "./http";
import type { CalcInputV1, CalcResponseV1 } from "../types/api";

export async function calculate(input: CalcInputV1): Promise<CalcResponseV1> {
  const res = await http.post<CalcResponseV1>("/calc", input);
  return res.data;
}
