import { http } from "./http";

export async function exportPdf(calcId: string): Promise<Blob> {
  const res = await http.get(`/calc/${calcId}/export/pdf`, {
    responseType: "blob", // 🔑 КЛЮЧ
  });

  return res.data;
}
