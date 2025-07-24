# Página de Contato - Central de Contratos

## Visão Geral
A página de contato foi criada para facilitar a comunicação entre usuários e a Central de Contratos, oferecendo múltiplos canais de atendimento e um formulário funcional com validações completas.

## Estrutura da Página

### 1. Hero Section
- **Apresentação**: Destaque da proposta de atendimento
- **Highlights**: 3 destaques principais (Resposta rápida, Suporte especializado, Atendimento seguro)
- **Grid de Ícones**: Representação visual dos canais de contato

### 2. Seção do Formulário de Contato
- **Formulário Funcional**: Implementado com Django Forms
- **Validações**: Frontend e backend completas
- **Campos**:
  - Nome Completo (validação de nome e sobrenome)
  - E-mail (validação de formato)
  - Assunto (seleção categorizada)
  - Mensagem (mínimo 10 caracteres, máximo 1000)

### 3. Informações de Contato
- **E-mail**: contato@centraldecontratos.com
- **Telefone**: (11) 9 9999-9999
- **WhatsApp**: Link direto para conversação
- **Endereço**: Localização física do escritório

### 4. Redes Sociais
- **Links**: LinkedIn, Instagram, Facebook, Twitter, YouTube
- **Design**: Ícones responsivos com hover effects

### 5. FAQ Rápido
- **3 Perguntas Frequentes** sobre funcionamento dos contratos
- **CTA**: Direcionamento para catálogo

## Funcionalidades Técnicas

### Formulário Django (core/forms.py)
```python
class ContactForm(forms.Form):
    # Campos com validações customizadas
    # Método send_email() integrado
    # Validações específicas para nome e mensagem
```

### Validações Implementadas
- **Nome Completo**: Deve ter nome + sobrenome, apenas letras
- **E-mail**: Formato válido obrigatório
- **Assunto**: Categorias predefinidas
- **Mensagem**: Mínimo 3 palavras, máximo 1000 caracteres

### Sistema de E-mail
- **Desenvolvimento**: Console backend (e-mails aparecem no terminal)
- **Produção**: Configuração SMTP comentada para facilitar setup
- **E-mail Duplo**: Confirmação para usuário + notificação para empresa

### Tratamento de Erros
- **Validação Frontend**: Bootstrap styling + JavaScript
- **Validação Backend**: Django forms validation
- **Mensagens**: Success/error messages com Django messages framework

## Características de Design

### CSS Personalizado (+300 linhas)
- **Animações**: fadeInUp, fadeInLeft com delays progressivos
- **Cards Responsivos**: Hover effects e transitions
- **Formulário Moderno**: Bordas arredondadas, focus states
- **Grid Adaptativo**: Layout responsivo completo

### Responsividade
- **Desktop**: Layout em 2 colunas, animações completas
- **Tablet**: Adaptação de grids e espaçamentos
- **Mobile**: Layout em coluna única, formulário otimizado

### Acessibilidade
- **Semântica HTML5**: Estrutura adequada
- **Labels**: Todos os campos devidamente rotulados
- **Cores**: Contraste adequado
- **Links**: rel="noopener" para segurança

## URLs e Navegação
- **URL**: `/contact/`
- **View**: `contact_view` com GET/POST handling
- **Template**: `templates/core/contact.html`
- **Integração**: Link presente na navbar

## Configuração de E-mail

### Desenvolvimento
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@centraldecontratos.com'
CONTACT_EMAIL = 'contato@centraldecontratos.com'
```

### Produção (configurar quando necessário)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Estados do Formulário

### Sucesso
- **Mensagem**: Verde com confirmação
- **Redirect**: Limpa formulário
- **E-mails**: Enviados para empresa e usuário

### Erro
- **Validação**: Campos destacados em vermelho
- **Mensagens**: Específicas para cada erro
- **Preservação**: Dados válidos mantidos no formulário

## Melhorias Futuras Sugeridas

1. **Captcha**: Implementar proteção anti-spam
2. **Ajax**: Submissão sem reload da página
3. **Upload**: Permitir anexos no formulário
4. **Chat**: Integração com sistema de chat ao vivo
5. **Localização**: Mapa interativo do escritório
6. **Horários**: Sistema dinâmico de disponibilidade
7. **FAQ Expandido**: Seção completa de perguntas frequentes

## Monitoramento

### Métricas Importantes
- Taxa de conversão do formulário
- Tempo de resposta aos contatos
- Canais mais utilizados
- Tipos de assunto mais comuns

### Logs
- E-mails enviados registrados no console (desenvolvimento)
- Erros de validação podem ser monitorados
- Submissões do formulário trackeable via Django admin

## Manutenção

### Atualizações Regulares
- **Informações de Contato**: Telefones, endereços, horários
- **FAQ**: Adicionar novas perguntas frequentes
- **Validações**: Ajustar conforme necessário
- **Design**: Manter consistência com outras páginas

### Backup e Segurança
- **LGPD**: Dados protegidos conforme legislação
- **Validação**: Previne injeção de código
- **Rate Limiting**: Considerar implementar para produção
