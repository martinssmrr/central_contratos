# Central de Contratos - Sistema de Venda de Contratos Jurídicos

## 📋 Descrição

Sistema completo em Django para venda automatizada de contratos jurídicos personalizados em PDF. O sistema permite que usuários escolham tipos de contratos, preencham dados específicos, realizem pagamentos e baixem contratos profissionais automaticamente.

## 🚀 Funcionalidades

### 🏠 Página Inicial
- Apresentação do serviço com design moderno
- Destaque dos principais tipos de contratos
- Chamada para ação clara
- Layout responsivo com Bootstrap 5

### 📚 Catálogo de Contratos
Tipos de contratos disponíveis:
- **Prestação de Serviços** - R$ 49,90
- **Locação Residencial** - R$ 79,90
- **Locação Comercial** - R$ 89,90
- **Compra e Venda** - R$ 69,90
- **Confissão de Dívida** - R$ 39,90
- **Freelancer** - R$ 59,90

### 📝 Formulários Personalizados
- Formulários específicos para cada tipo de contrato
- Validação completa dos dados
- Interface intuitiva com Crispy Forms
- Campos obrigatórios e opcionais claramente identificados

### 💳 Sistema de Pagamento
- Múltiplos métodos: Cartão, PIX, Boleto
- Simulação de processamento automático
- Status de pagamento em tempo real
- Histórico de transações

### 📄 Geração de PDF
- Contratos profissionais automatizados
- Layout juridicamente válido
- Dados personalizados inseridos automaticamente
- Download instantâneo após pagamento

### 👤 Área do Cliente
- Sistema completo de autenticação
- Perfil personalizável com avatar
- Histórico de contratos gerados
- Re-download de PDFs anteriores

### 🔧 Painel Administrativo
- Dashboard com estatísticas
- Relatórios de contratos e pagamentos
- Gerenciamento de usuários
- Analytics de vendas por período

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.3** - Framework web principal
- **Python 3.12** - Linguagem de programação
- **SQLite** - Banco de dados (configurável para PostgreSQL)
- **WeasyPrint** - Geração de PDFs (requer dependências específicas)

### Frontend
- **Bootstrap 5.3** - Framework CSS responsivo
- **Font Awesome 6.0** - Ícones
- **Crispy Forms** - Formulários estilizados
- **JavaScript ES6** - Interatividade

### Dependências Python
```
Django==5.2.3
Pillow==11.1.0
WeasyPrint==63.1
django-crispy-forms==2.3
crispy-bootstrap5==2025.2
python-decouple==3.8
```

## 📁 Estrutura do Projeto

```
Central_Contratos/
├── setup/                 # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                  # App das páginas públicas
│   ├── views.py          # Página inicial, sobre, contato
│   └── urls.py
├── contracts/             # App principal dos contratos
│   ├── models.py         # ContractType, Contract, Payment
│   ├── forms.py          # Formulários específicos por tipo
│   ├── views.py          # Lógica de criação e pagamento
│   ├── admin.py          # Interface administrativa
│   └── utils.py          # Geração de PDFs
├── users/                 # App de usuários
│   ├── models.py         # UserProfile
│   ├── forms.py          # Login, registro, perfil
│   ├── views.py          # Autenticação e perfil
│   └── admin.py
├── adminpanel/           # App do painel administrativo
│   ├── views.py          # Dashboard e relatórios
│   └── urls.py
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── core/            # Templates das páginas públicas
│   ├── contracts/       # Templates dos contratos
│   │   └── pdf/         # Templates para PDFs
│   └── users/           # Templates de usuário
├── static/              # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── media/               # Uploads de usuários
├── requirements.txt     # Dependências
├── manage.py           # Script de gerenciamento Django
└── populate_db.py      # Script para dados iniciais
```

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório
```bash
cd C:\Users\teste\OneDrive\Desktop\Central_Conrtatos
```

### 2. Criar Ambiente Virtual
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# ou
.\.venv\Scripts\activate.bat  # Command Prompt
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar Dados Iniciais
```bash
python populate_db.py
```

### 6. Executar Servidor
```bash
python manage.py runserver
```

## 👥 Usuários de Teste

O script `populate_db.py` cria automaticamente:

### Administrador
- **Username:** admin
- **Password:** admin123
- **Email:** admin@centralcontratos.com
- **Acesso:** Painel administrativo completo

### Usuário Demo
- **Username:** demo
- **Password:** demo123
- **Email:** demo@centralcontratos.com
- **Acesso:** Funcionalidades de cliente

## 🌐 URLs Principais

- **Home:** http://127.0.0.1:8000/
- **Catálogo:** http://127.0.0.1:8000/contracts/catalog/
- **Login:** http://127.0.0.1:8000/users/login/
- **Registro:** http://127.0.0.1:8000/users/register/
- **Admin Django:** http://127.0.0.1:8000/admin/
- **Painel Admin:** http://127.0.0.1:8000/adminpanel/

## 📊 Modelos de Dados

### ContractType
- Tipos de contratos disponíveis
- Preços e descrições
- Status ativo/inativo

### Contract
- Contratos gerados pelos usuários
- Dados das partes contratantes
- Informações específicas por tipo
- Status e arquivos PDF

### Payment
- Registros de pagamentos
- Métodos e status
- Histórico de transações

### UserProfile
- Perfis estendidos dos usuários
- Informações adicionais
- Configurações pessoais

## 🎨 Design e UX

### Cores Principais
- **Primária:** #f4623a (Laranja Vibrante)
- **Sucesso:** #198754 (Green)
- **Aviso:** #ffc107 (Yellow)
- **Erro:** #dc3545 (Red)

### Responsividade
- Mobile-first design
- Breakpoints do Bootstrap 5
- Componentes adaptativos
- Menu colapsável

### Acessibilidade
- Contraste adequado
- Navegação por teclado
- Textos alternativos
- Estrutura semântica

## 🔧 Funcionalidades Avançadas

### Validação de Formulários
- CPF/CNPJ com máscara automática
- Validação de e-mail
- Campos obrigatórios
- Mensagens de erro claras

### Sistema de Pagamento
- Simulação de gateway
- Múltiplos métodos
- Feedback em tempo real
- Histórico completo

### Geração de PDFs
- Templates profissionais
- Dados dinâmicos
- Layout juridicamente válido
- Download seguro

### Painel Administrativo
- Estatísticas em tempo real
- Filtros e buscas
- Exportação de dados
- Gráficos interativos

## 🚧 Próximas Funcionalidades

- [ ] Integração com gateway real (PagSeguro/Stripe)
- [ ] Sistema de cupons de desconto
- [ ] Assinatura digital de contratos
- [ ] Notificações por email
- [ ] API REST para integrações
- [ ] App mobile
- [ ] Sistema de afiliados

## 🐛 Solução de Problemas

### WeasyPrint no Windows
Se houver problemas com WeasyPrint:
```bash
# Instalar dependências GTK3
# https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows
```

### Erro de Migração
```bash
python manage.py migrate --run-syncdb
```

### Problemas de Estáticos
```bash
python manage.py collectstatic
```

## 📝 Licença

Este projeto é desenvolvido para fins educacionais e de demonstração.

## 👨‍💻 Desenvolvimento

Desenvolvido com Django seguindo as melhores práticas:
- Clean Code
- DRY (Don't Repeat Yourself)
- Separation of Concerns
- Security First
- Performance Optimization

---

**Central de Contratos** - Sua solução completa para contratos jurídicos automatizados! 🚀
