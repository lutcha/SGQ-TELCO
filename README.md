# SGQ-TELCO - Sistema de Gestão de Qualidade Telco

Sistema completo de Gestão de Qualidade multi-tenant para empresas de telecomunicações, com foco em conformidade com ISO 9001 e requisitos específicos do setor.

## 📋 Sobre o Projeto

O SGQ-TELCO é uma plataforma robusta para gerenciamento de qualidade que inclui módulos para auditorias, não conformidades, ações corretivas, gestão de documentos, e muito mais.

Este repositório contém o **Módulo de Auditorias**, um sistema completo para:

- ✅ Planejamento e execução de auditorias
- ✅ Registro e acompanhamento de constatações
- ✅ Gestão de ações corretivas e preventivas
- ✅ Dashboard com indicadores e métricas
- ✅ Sistema multi-tenant
- ✅ Rastreabilidade completa
- ✅ Conformidade com ISO 9001 e ISO 19011

## 🏗️ Arquitetura

O sistema é dividido em duas partes principais:

### Backend (Django REST Framework)
- **Localização**: `/workspace/backend/`
- **Tecnologia**: Django 4.2+, Django REST Framework
- **Banco de Dados**: PostgreSQL
- **API**: RESTful com autenticação JWT
- **Documentação**: [Backend README](./backend/README.md)

### Frontend (Next.js)
- **Localização**: `/workspace/frontend/`
- **Tecnologia**: Next.js 14, React 18, TypeScript
- **Estilização**: Tailwind CSS
- **State Management**: React Query, Zustand
- **Documentação**: [Frontend README](./frontend/README.md)

## 🚀 Quick Start

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- PostgreSQL 13+
- Git

### Instalação Rápida

1. **Clone o repositório**
```bash
git clone <repository-url>
cd sgq-telco
```

2. **Configure o Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate no Windows

pip install -r requirements.txt

# Configure o .env
cp .env.example .env
# Edite .env com suas configurações

# Execute migrations
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

3. **Configure o Frontend**
```bash
cd ../frontend
npm install

# Configure o .env
cp .env.example .env
# Edite .env com a URL do backend

# Inicie o servidor de desenvolvimento
npm run dev
```

4. **Acesse o sistema**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin Django: http://localhost:8000/admin/

## 📁 Estrutura do Projeto

```
sgq-telco/
├── backend/                    # Backend Django
│   ├── auditorias/            # Módulo de Auditorias
│   │   ├── models.py          # Modelos de dados
│   │   ├── serializers.py     # Serializers DRF
│   │   ├── views.py           # Views e ViewSets
│   │   ├── urls.py            # Rotas da API
│   │   ├── admin.py           # Admin do Django
│   │   ├── permissions.py     # Permissões
│   │   ├── filters.py         # Filtros customizados
│   │   ├── signals.py         # Signals
│   │   └── tests.py           # Testes
│   ├── requirements.txt       # Dependências Python
│   └── README.md              # Documentação do backend
│
├── frontend/                   # Frontend Next.js
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   │   ├── ui/           # Componentes base
│   │   │   └── auditorias/   # Componentes específicos
│   │   ├── pages/            # Páginas Next.js
│   │   ├── services/         # Serviços de API
│   │   ├── types/            # Tipos TypeScript
│   │   ├── lib/              # Utilitários
│   │   └── styles/           # Estilos globais
│   ├── package.json          # Dependências Node
│   └── README.md             # Documentação do frontend
│
├── AUDITORIA_ESPECIFICACAO.md # Especificação completa
└── README.md                  # Este arquivo
```

## 📚 Documentação

- **[Especificação do Módulo](./AUDITORIA_ESPECIFICACAO.md)** - Documentação completa com requisitos e funcionalidades
- **[Backend README](./backend/README.md)** - Guia do backend Django
- **[Frontend README](./frontend/README.md)** - Guia do frontend Next.js

## 🎯 Funcionalidades Principais

### Gestão de Auditorias
- Planejamento com definição de equipe e processos
- Execução com controle de status
- Geração de relatórios consolidados
- Dashboard com indicadores

### Gestão de Constatações
- Registro de achados com classificação por severidade
- Análise de causa raiz
- Acompanhamento de prazos
- Alertas automáticos

### Gestão de Ações Corretivas
- Plano de ações (Imediata, Corretiva, Preventiva)
- Controle de execução
- Verificação de eficácia
- Indicadores de performance

### Dashboard e Indicadores
- Visão geral de auditorias
- Estatísticas de constatações
- Taxa de fechamento
- Ações atrasadas
- Gráficos e visualizações

### Sistema Multi-Tenant
- Isolamento total de dados por organização
- Configurações independentes
- Usuários por tenant

## 🔐 Segurança

- Autenticação JWT
- Isolamento de dados por tenant
- Permissões granulares
- Validação de entrada
- Proteção CSRF
- CORS configurado
- Logs de auditoria

## 🧪 Testes

### Backend
```bash
cd backend
pytest
# ou
python manage.py test
```

### Frontend
```bash
cd frontend
npm run test
```

## 📦 Deploy

### Backend (Django)

**Opção 1: Docker**
```bash
cd backend
docker build -t sgq-backend .
docker run -p 8000:8000 sgq-backend
```

**Opção 2: Manual**
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (Next.js)

**Opção 1: Vercel (Recomendado)**
```bash
cd frontend
vercel
```

**Opção 2: Build Manual**
```bash
npm run build
npm run start
```

## 🔧 Configuração de Ambiente

### Backend (.env)
```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-segura
DATABASE_URL=postgresql://user:password@localhost:5432/sgq_telco
ALLOWED_HOSTS=seu-dominio.com
CORS_ALLOWED_ORIGINS=https://seu-frontend.com
EMAIL_NOTIFICATIONS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha
```

### Frontend (.env)
```env
API_URL=https://api.seu-dominio.com
NEXT_PUBLIC_APP_NAME=SGQ Telco - Auditorias
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📊 Tecnologias Utilizadas

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Pillow (processamento de imagens)
- pytest (testes)

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios
- React Hook Form
- React Query
- Lucide React (ícones)
- Recharts (gráficos)

## 🗺️ Roadmap

- [ ] Módulo de Gestão de Documentos
- [ ] Módulo de Não Conformidades
- [ ] Módulo de Calibração de Equipamentos
- [ ] Integração com Active Directory
- [ ] App Mobile (React Native)
- [ ] Relatórios avançados com BI
- [ ] Notificações push
- [ ] API pública para integrações

## 📝 Licença

Propriedade da SGQ Telco - Todos os direitos reservados.

## 👥 Equipe

- **Desenvolvimento**: Equipe SGQ Telco
- **Contato**: suporte@sgqtelco.com

## 🆘 Suporte

Para suporte técnico:
- Email: suporte@sgqtelco.com
- Documentação: Ver READMEs específicos
- Issues: Use o sistema de issues do repositório

---

**Desenvolvido com ❤️ para o setor de Telecomunicações**
