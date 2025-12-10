# SGQ Telco - Módulo de Auditorias (Frontend)

Frontend Next.js para o Módulo de Auditorias do Sistema de Gestão de Qualidade Telco.

## 🚀 Tecnologias

- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS
- **Axios** - Cliente HTTP
- **React Hook Form** - Gerenciamento de formulários
- **React Query** - Gerenciamento de estado do servidor
- **Lucide React** - Ícones
- **Recharts** - Gráficos e visualizações

## 📋 Pré-requisitos

- Node.js 18+ 
- npm ou yarn
- Backend Django rodando

## 🔧 Instalação

1. Instalar dependências:
```bash
npm install
# ou
yarn install
```

2. Configurar variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:
```
API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=SGQ Telco - Auditorias
```

## 🏃 Executando

### Modo de desenvolvimento
```bash
npm run dev
# ou
yarn dev
```

Acesse [http://localhost:3000](http://localhost:3000)

### Build de produção
```bash
npm run build
npm run start
# ou
yarn build
yarn start
```

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── components/         # Componentes React
│   │   ├── ui/            # Componentes base (Button, Input, etc)
│   │   └── auditorias/    # Componentes específicos do módulo
│   ├── lib/               # Utilitários e configurações
│   ├── pages/             # Páginas Next.js
│   ├── services/          # Serviços de API
│   ├── styles/            # Estilos globais
│   └── types/             # Tipos TypeScript
├── public/                # Arquivos estáticos
├── next.config.js         # Configuração do Next.js
├── tailwind.config.js     # Configuração do Tailwind
└── tsconfig.json          # Configuração do TypeScript
```

## 🎨 Funcionalidades

### Dashboard
- Visão geral de auditorias
- Estatísticas e indicadores
- Acesso rápido às funcionalidades

### Auditorias
- Listagem com filtros e busca
- Criação e edição de auditorias
- Visualização detalhada
- Gerenciamento de status (Iniciar, Concluir)
- Grid e visualização em tabela

### Constatações
- Registro de achados de auditoria
- Classificação por tipo e severidade
- Acompanhamento de prazos
- Gestão de status

### Ações Corretivas
- Plano de ações corretivas e preventivas
- Acompanhamento de execução
- Verificação de eficácia
- Controle de prazos

## 🔐 Autenticação

O sistema utiliza JWT (JSON Web Tokens) para autenticação. O token é armazenado no localStorage e incluído automaticamente em todas as requisições.

## 🎯 Componentes Principais

### UI Components
- `Button` - Botão com variantes e estados
- `Card` - Container de conteúdo
- `Badge` - Indicador de status
- `Input` - Campo de entrada de texto
- `Select` - Seletor dropdown
- `Textarea` - Área de texto

### Auditoria Components
- `AuditoriaCard` - Card de auditoria
- `AuditoriaTable` - Tabela de auditorias
- `Dashboard` - Dashboard de estatísticas
- `ConstatacaoCard` - Card de constatação

## 🔌 Integração com API

Os serviços de API estão em `src/services/auditoriaService.ts` e incluem:

- `auditoriaService` - Operações de auditorias
- `constatacaoService` - Operações de constatações
- `acaoCorretivaService` - Operações de ações corretivas
- `tipoAuditoriaService` - Gerenciamento de tipos
- `tipoConstatacaoService` - Gerenciamento de tipos de constatação
- `processoService` - Gerenciamento de processos
- `documentoService` - Upload e gestão de documentos
- `comentarioService` - Comentários e discussões

## 📱 Responsividade

O sistema é totalmente responsivo e otimizado para:
- Desktop (1920px+)
- Laptop (1024px+)
- Tablet (768px+)
- Mobile (320px+)

## 🧪 Testes

```bash
npm run test
# ou
yarn test
```

## 📝 Lint

```bash
npm run lint
# ou
yarn lint
```

## 🚢 Deploy

### Vercel (Recomendado)
```bash
vercel
```

### Build Manual
```bash
npm run build
npm run start
```

## 📄 Licença

Propriedade da SGQ Telco - Todos os direitos reservados.

## 👥 Suporte

Para suporte, entre em contato com a equipe de desenvolvimento.
