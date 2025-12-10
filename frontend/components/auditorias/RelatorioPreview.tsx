interface Props {
  resumo?: string;
  conclusoes?: string;
  anexos?: Array<{ nome: string }>;
}

export function RelatorioPreview({ resumo, conclusoes, anexos = [] }: Props) {
  return (
    <section className="border border-slate-200 rounded-lg p-4 bg-white space-y-3">
      <div>
        <h3 className="text-sm font-semibold text-slate-600">Resumo Executivo</h3>
        <p className="text-sm text-slate-700 whitespace-pre-line">{resumo ?? "Ainda sem conteúdo"}</p>
      </div>
      <div>
        <h3 className="text-sm font-semibold text-slate-600">Conclusões</h3>
        <p className="text-sm text-slate-700 whitespace-pre-line">{conclusoes ?? "Adicione as conclusões"}</p>
      </div>
      <div>
        <h3 className="text-sm font-semibold text-slate-600">Anexos</h3>
        {anexos.length === 0 && <p className="text-sm text-slate-500">Sem anexos</p>}
        <ul className="text-sm text-slate-700">
          {anexos.map((anexo) => (
            <li key={anexo.nome}>• {anexo.nome}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
