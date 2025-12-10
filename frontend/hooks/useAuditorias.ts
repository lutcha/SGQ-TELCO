"use client";

import { useQuery } from "@tanstack/react-query";
import { AuditoriaApi } from "../lib/api";
import { Auditoria } from "../types/auditorias";

export function useAuditorias(filters: Record<string, unknown>) {
  return useQuery({
    queryKey: ["auditorias", filters],
    queryFn: async (): Promise<Auditoria[]> => {
      const payload = await AuditoriaApi.listarAuditorias(filters);
      return payload.results;
    }
  });
}
