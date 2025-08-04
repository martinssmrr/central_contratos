# 🏆 Central de Contratos - Sistema de Venda de Contratos Jurídicos

## 📋 Descrição

Sistema completo em Django para venda automatizada de contratos jurídicos personalizados. Plataforma e-commerce com integração Mercado Pago, geração de documentos e painel administrativo completo.

## 🚀 Tecnologias Principais

- **Backend:** Django 4.2.11 (Python)
- **Frontend:** Bootstrap 5.3.0 + Font Awesome 6.0.0
- **Pagamentos:** Mercado Pago SDK 2.2.3
- **PDF:** WeasyPrint 63.1
- **Deploy:** PythonAnywhere
- **Database:** SQLite (dev) / MySQL (prod)

## 🌟 Funcionalidades Implementadas

### 🏠 Página Inicial
- Apresentação do serviço com design moderno
- Destaque dos principais tipos de contratos
- Chamada para ação clara
- Layout responsivo otimizado

### 📚 Catálogo de Contratos
Tipos de contratos disponíveis:
- **Prestação de Serviços** - R$ 49,90
- **Locação Residencial** - R$ 79,90
- **Locação Comercial** - R$ 89,90
- **Compra e Venda** - R$ 69,90
- **Confissão de Dívida** - R$ 39,90
- **Freelancer** - R$ 59,90
- **Contrato de Teste MP** - R$ 1,00 (para testes)

### 💳 Sistema de Pagamento Completo
- **Mercado Pago integrado** (PIX, Cartão, Boleto)
- **Auto-return inteligente** (prod/dev)
- **Webhooks configurados** para notificações
- **Status em tempo real** de pagamentos
- **Histórico completo** de transações

### � Sistema de Usuários
- Autenticação completa (Login/Register)
- **Google OAuth** integrado
- Perfil personalizável com avatar
- Histórico de contratos e pagamentos
- Re-download de documentos

### 🔧 Painel Administrativo
- **Dashboard executivo** com métricas
- Gerenciamento de contratos e categorias
- **Sistema de FAQ** completo
- Relatórios de vendas e usuários
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

## 🌐 Deploy no PythonAnywhere

### 📋 Pré-requisitos
- Conta no PythonAnywhere
- Repositório Git configurado
- Arquivos `.gitignore` e `.gitattributes` criados

### 🚀 Passo a Passo

#### 1. Preparar o Repositório
```bash
# Commit todas as mudanças
git add .
git commit -m "Preparando para deploy no PythonAnywhere"
git push origin main
```

#### 2. Configurar no PythonAnywhere Console
```bash
# Acessar console Bash no PythonAnywhere
# Clone o repositório
cd ~
git clone https://github.com/martinssmrr/central_contratos.git
cd central_contratos

# Criar ambiente virtual
python3.10 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

#### 3. Configurar WSGI
Editar `/var/www/martinssmrr_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

# Adicionar projeto ao path
path = '/home/martinssmrr/central_contratos'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'setup.settings_production'

# Variáveis de ambiente para produção
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', 'martinssmrr.pythonanywhere.com')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 4. Configurar Web App (Interface Web)
- **Source code:** `/home/martinssmrr/central_contratos`
- **Working directory:** `/home/martinssmrr/central_contratos`
- **Virtualenv:** `/home/martinssmrr/central_contratos/.venv`

**Static files:**
- **URL:** `/static/`
- **Directory:** `/home/martinssmrr/central_contratos/staticfiles/`

**Media files:**
- **URL:** `/media/`
- **Directory:** `/home/martinssmrr/central_contratos/media/`

#### 5. Configurar Variáveis de Ambiente
Criar arquivo `.env` no diretório do projeto:
```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura-aqui
MERCADO_PAGO_ACCESS_TOKEN=seu-token-producao
MERCADO_PAGO_PUBLIC_KEY=sua-chave-publica-producao
EMAIL_HOST_USER=seuemail@gmail.com
EMAIL_HOST_PASSWORD=senha-app-gmail
DEFAULT_FROM_EMAIL=noreply@centraldecontratos.com
CONTACT_EMAIL=contato@centraldecontratos.com
BASE_URL=https://martinssmrr.pythonanywhere.com
```

#### 6. Executar Comandos Finais
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Aplicar migrações
python manage.py migrate --settings=setup.settings_production

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=setup.settings_production

# Criar superusuário (opcional)
python manage.py createsuperuser --settings=setup.settings_production

# Popular banco com dados iniciais
python populate_db.py
```

#### 7. Recarregar Web App
- Acessar aba **Web** no PythonAnywhere
- Clicar em **Reload martinssmrr.pythonanywhere.com**

### ✅ Verificação do Deploy

#### URLs para Testar:
- **Home:** https://martinssmrr.pythonanywhere.com
- **Admin:** https://martinssmrr.pythonanywhere.com/admin/
- **Catálogo:** https://martinssmrr.pythonanywhere.com/contracts/catalog/
- **Login:** https://martinssmrr.pythonanywhere.com/users/login/

#### Checklist Pós-Deploy:
- [ ] Site carregando corretamente
- [ ] Static files sendo servidos
- [ ] Admin panel acessível
- [ ] Login funcionando
- [ ] Mercado Pago testado
- [ ] Formulários de contato operacionais

### 🔧 Troubleshooting

#### Problemas Comuns:

**1. Erro 500 - Internal Server Error**
```bash
# Verificar logs
tail -f /var/log/martinssmrr.pythonanywhere.com.error.log
```

**2. Static files não carregando**
```bash
# Re-executar collectstatic
python manage.py collectstatic --noinput --clear
```

**3. Erro de importação**
```bash
# Verificar PYTHONPATH no WSGI
import sys
print(sys.path)
```

**4. Erro de database**
```bash
# Aplicar migrações novamente
python manage.py migrate --settings=setup.settings_production
```

### 🔄 Atualizações

Para atualizar o projeto em produção:
```bash
# No console PythonAnywhere
cd ~/central_contratos
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=setup.settings_production
python manage.py collectstatic --noinput --settings=setup.settings_production
# Recarregar web app via interface
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
