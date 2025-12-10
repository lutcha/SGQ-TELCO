# SGQ Telco - Módulo de Auditorias (Backend)

Backend Django REST Framework para o Módulo de Auditorias do Sistema de Gestão de Qualidade Telco.

## 🚀 Tecnologias

- **Django 4.2+** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados
- **Django CORS Headers** - Suporte a CORS
- **Django Filter** - Filtros avançados
- **Pillow** - Processamento de imagens
- **pytest** - Testes

## 📋 Pré-requisitos

- Python 3.10+
- PostgreSQL 13+
- pip e virtualenv

## 🔧 Instalação

1. Criar e ativar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:
```
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost:5432/sgq_telco
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

4. Executar migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Criar superusuário:
```bash
python manage.py createsuperuser
```

## 🏃 Executando

### Modo de desenvolvimento
```bash
python manage.py runserver
```

Acesse:
- API: [http://localhost:8000/api/](http://localhost:8000/api/)
- Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Documentação: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

## 📁 Estrutura do Módulo

```
auditorias/
├── __init__.py
├── admin.py              # Configuração do Django Admin
├── apps.py               # Configuração da aplicação
├── filters.py            # Filtros customizados
├── models.py             # Modelos de dados
├── permissions.py        # Permissões customizadas
├── serializers.py        # Serializers DRF
├── signals.py            # Sinais Django
├── tests.py              # Testes unitários
├── urls.py               # Rotas da API
└── views.py              # Views e ViewSets
```

## 📊 Modelos de Dados

### Tenant
Suporte multi-tenant para isolamento de dados por organização.

### TipoAuditoria
Categorização de auditorias (Interna, Externa, Fornecedor, etc).

### Processo
Processos da organização que podem ser auditados.

### Auditoria
Registro principal de auditoria com:
- Informações básicas (código, título, tipo)
- Datas planejadas e reais
- Equipe de auditores
- Status (Planejada, Em Andamento, Concluída, Cancelada)
- Processos auditados

### TipoConstatacao
Classificação de constatações por severidade:
- Baixa (1)
- Média (2)
- Alta (3)
- Crítica (4)

### Constatacao
Achados de auditoria (findings):
- Descrição e evidências
- Processo relacionado
- Responsável pelo tratamento
- Prazos e status
- Análise de causa raiz

### AcaoCorretiva
Plano de ações para tratar constatações:
- Tipo (Imediata, Corretiva, Preventiva)
- Responsável e prazos
- Status de execução
- Verificação de eficácia

### DocumentoAuditoria
Anexos e evidências documentais.

### Comentario
Sistema de comentários para auditorias e constatações.

### IndicadorAuditoria
Indicadores e métricas de performance.

## 🔌 Endpoints da API

### Auditorias
- `GET /api/auditorias/auditorias/` - Listar auditorias
- `POST /api/auditorias/auditorias/` - Criar auditoria
- `GET /api/auditorias/auditorias/{id}/` - Detalhar auditoria
- `PATCH /api/auditorias/auditorias/{id}/` - Atualizar auditoria
- `DELETE /api/auditorias/auditorias/{id}/` - Deletar auditoria
- `POST /api/auditorias/auditorias/{id}/iniciar/` - Iniciar auditoria
- `POST /api/auditorias/auditorias/{id}/concluir/` - Concluir auditoria
- `GET /api/auditorias/auditorias/{id}/relatorio/` - Gerar relatório
- `GET /api/auditorias/auditorias/estatisticas/` - Estatísticas gerais

### Constatações
- `GET /api/auditorias/constatacoes/` - Listar constatações
- `POST /api/auditorias/constatacoes/` - Criar constatação
- `GET /api/auditorias/constatacoes/{id}/` - Detalhar constatação
- `PATCH /api/auditorias/constatacoes/{id}/` - Atualizar constatação
- `DELETE /api/auditorias/constatacoes/{id}/` - Deletar constatação
- `POST /api/auditorias/constatacoes/{id}/iniciar_tratamento/` - Iniciar tratamento
- `POST /api/auditorias/constatacoes/{id}/solicitar_validacao/` - Solicitar validação
- `POST /api/auditorias/constatacoes/{id}/fechar/` - Fechar constatação

### Ações Corretivas
- `GET /api/auditorias/acoes-corretivas/` - Listar ações
- `POST /api/auditorias/acoes-corretivas/` - Criar ação
- `GET /api/auditorias/acoes-corretivas/{id}/` - Detalhar ação
- `PATCH /api/auditorias/acoes-corretivas/{id}/` - Atualizar ação
- `DELETE /api/auditorias/acoes-corretivas/{id}/` - Deletar ação
- `POST /api/auditorias/acoes-corretivas/{id}/iniciar/` - Iniciar ação
- `POST /api/auditorias/acoes-corretivas/{id}/concluir/` - Concluir ação
- `POST /api/auditorias/acoes-corretivas/{id}/verificar/` - Verificar eficácia

### Outros Endpoints
- `/api/auditorias/tipos-auditoria/` - Tipos de auditoria
- `/api/auditorias/tipos-constatacao/` - Tipos de constatação
- `/api/auditorias/processos/` - Processos
- `/api/auditorias/documentos/` - Documentos
- `/api/auditorias/comentarios/` - Comentários
- `/api/auditorias/indicadores/` - Indicadores

## 🔐 Autenticação

O sistema utiliza JWT (JSON Web Tokens) para autenticação:

```python
# Obter token
POST /api/token/
{
  "username": "usuario",
  "password": "senha"
}

# Resposta
{
  "access": "token_jwt",
  "refresh": "refresh_token"
}

# Usar token
Headers: {
  "Authorization": "Bearer token_jwt"
}
```

## 🎯 Permissões

### IsTenantUser
Verifica se o usuário pertence ao tenant dos dados acessados.

### IsAuditorLider
Verifica se o usuário é o auditor líder da auditoria.

### IsResponsavel
Verifica se o usuário é o responsável pelo item.

### CanEditAuditoria
Permite edição apenas para auditor líder e equipe.

## 📧 Notificações

O sistema envia notificações automáticas via signals para:
- Nova constatação criada → Notifica responsável
- Nova ação corretiva → Notifica responsável

Configure `EMAIL_NOTIFICATIONS=True` no `.env` para habilitar.

## 🧪 Testes

Executar testes:
```bash
pytest
# ou
python manage.py test
```

Com coverage:
```bash
pytest --cov=auditorias
```

## 📝 Migrations

Criar migrations:
```bash
python manage.py makemigrations auditorias
```

Aplicar migrations:
```bash
python manage.py migrate
```

## 🔍 Filtros Disponíveis

### Auditorias
- `status` - Filtrar por status
- `tipo` - Filtrar por tipo
- `auditor_lider` - Filtrar por auditor líder
- `ano` - Filtrar por ano
- `mes` - Filtrar por mês
- `search` - Busca em código, título, descrição

### Constatações
- `status` - Filtrar por status
- `tipo` - Filtrar por tipo
- `processo` - Filtrar por processo
- `auditoria` - Filtrar por auditoria
- `responsavel` - Filtrar por responsável
- `severidade` - Filtrar por severidade
- `prazo_vencido` - Constatações com prazo vencido

### Ações Corretivas
- `status` - Filtrar por status
- `tipo` - Filtrar por tipo
- `constatacao` - Filtrar por constatação
- `responsavel` - Filtrar por responsável
- `eficaz` - Filtrar por eficácia
- `atrasada` - Ações atrasadas

## 🚀 Deploy

### Preparação
```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Desabilitar DEBUG
DEBUG=False
```

### Docker (Recomendado)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📊 Admin Django

Acesse `/admin/` para gerenciar dados via interface administrativa.

Recursos:
- Gestão completa de auditorias
- Visualização de estatísticas inline
- Filtros e busca avançada
- Ações em lote
- Visualização colorida de status

## 📄 Licença

Propriedade da SGQ Telco - Todos os direitos reservados.

## 👥 Suporte

Para suporte, entre em contato com a equipe de desenvolvimento.
