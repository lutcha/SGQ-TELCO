# SGQ-TELCO

Sistema de Gestão de Qualidade Telco Multitennant.

## Estrutura

- `backend/`: Projeto Django com API REST das auditorias (e apps auxiliares de utilizadores, processos e não conformidades).
- `frontend/`: Aplicação Next.js (App Router) para orquestrar programa anual, execução, relatórios e dashboards.

## Backend

### Configuração

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Principais apps:
- `auditorias`: modelos, serializers, permissões e viewsets de acordo com a especificação.
- `utilizadores`, `processos`, `nonconformidades`: modelos mínimos para suportar relacionamentos e permissões.

Endpoints expostos (prefixo `/api/`):
- Programas: `/auditorias/programas/`
- Auditorias completas + ações: `/auditorias/`
- Sub-recursos: plano, checklists, constatações, relatório, seguimento, estatísticas e dashboards.

## Frontend

### Configuração

```bash
cd frontend
npm install
npm run dev
```

Páginas principais:
- `/auditorias`: lista com filtros, estados e ações rápidas.
- `/auditorias/programa`: gestão do programa anual.
- `/auditorias/nova`: wizard multi-step de criação.
- `/auditorias/[id]/executar`: cockpit de execução, checklists e constatações.
- `/auditorias/[id]/relatorio`: editor estruturado + geração de PDF (placeholder).
- `/auditorias/dashboard`: KPIs e resumos visuais.

Configure o backend na app através da variável `NEXT_PUBLIC_API_BASE_URL`.
