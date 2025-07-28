# Configuração do Google OAuth2

## Passos para configurar o login com Google:

### 1. Configurar no Google Cloud Console

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Vá para "APIs & Services" > "Credentials"
4. Clique em "Create Credentials" > "OAuth 2.0 Client IDs"
5. Configure o tipo de aplicação como "Web application"
6. Adicione as seguintes URLs autorizadas:

**Authorized JavaScript origins:**
```
http://localhost:8000
http://127.0.0.1:8000
```

**Authorized redirect URIs:**
```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
```

7. Copie o Client ID e Client Secret gerados

### 2. Configurar variáveis de ambiente

1. Abra o arquivo `.env` na raiz do projeto
2. Substitua os valores das variáveis:

```env
GOOGLE_CLIENT_ID=seu_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
```

### 3. Configurar no Django Admin

1. Acesse o Django Admin: http://localhost:8000/admin/
2. Vá para "Sites" > "Sites"
3. Edite o site padrão:
   - Domain name: `localhost:8000` ou `127.0.0.1:8000`
   - Display name: `Central de Contratos`

4. Vá para "Social Applications" > "Add Social Application"
5. Configure:
   - Provider: Google
   - Name: Google OAuth
   - Client id: (cole o Client ID do Google)
   - Secret key: (cole o Client Secret do Google)
   - Sites: Selecione o site criado acima

### 4. Testar a integração

1. Acesse a página de login: http://localhost:8000/users/login/
2. Clique no botão "Continuar com Google"
3. Faça login com sua conta Google
4. Confirme que o usuário foi criado automaticamente no sistema

## Segurança em Produção

Para produção, certifique-se de:

1. Usar HTTPS em todas as URLs
2. Configurar as URLs de redirect corretas no Google Cloud Console
3. Usar variáveis de ambiente seguras
4. Ativar verificação de email (`ACCOUNT_EMAIL_VERIFICATION = 'mandatory'`)
5. Configurar domínios corretos no Django Sites framework

## URLs importantes

- Login: `/users/login/`
- Registro: `/users/register/`
- Logout: `/accounts/logout/`
- Callback do Google: `/accounts/google/login/callback/`
- Admin: `/admin/`
