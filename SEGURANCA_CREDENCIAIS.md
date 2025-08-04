# 🔐 SEGURANÇA DAS CREDENCIAIS - GOOGLE OAUTH

## ⚠️ IMPORTANTE: SEGURANÇA EM PRIMEIRO LUGAR

Este projeto foi configurado seguindo as **melhores práticas de segurança**:

### ✅ O QUE ESTÁ SEGURO:

1. **Nenhuma credencial hardcoded** nos arquivos de código
2. **Arquivo .env protegido** pelo .gitignore
3. **Configuração via variáveis de ambiente**
4. **Script de configuração seguro**

### 🔒 COMO AS CREDENCIAIS SÃO GERENCIADAS:

```
📁 Desenvolvimento Local:
   └── .env (não versionado)
       ├── GOOGLE_CLIENT_ID=sua-credencial-real
       └── GOOGLE_CLIENT_SECRET=sua-credencial-real

📁 Produção:
   └── Variáveis de ambiente do servidor
       ├── GOOGLE_CLIENT_ID
       └── GOOGLE_CLIENT_SECRET

📁 Código Fonte (GitHub):
   └── .env.example (apenas templates)
       ├── GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
       └── GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 📋 INSTRUÇÕES PARA CONFIGURAR:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/martinssmrr/central_contratos.git
   cd central_contratos
   ```

2. **Configure as credenciais**:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais reais
   ```

3. **Execute a configuração segura**:
   ```bash
   python configure_oauth_secure.py
   ```

### 🛡️ CREDENCIAIS NECESSÁRIAS:

```env
# Arquivo .env (local apenas)

```

### 🌐 URIs DE CALLBACK CONFIGURADAS:

No Google Cloud Console, adicione estas URIs:
```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
http://centralcontratos.pythonanywhere.com/accounts/google/login/callback/
```

### 🚨 NUNCA FAÇA:

- ❌ Commitar arquivos .env
- ❌ Expor credenciais em código
- ❌ Compartilhar Client Secrets publicamente
- ❌ Usar credenciais de produção em desenvolvimento

### ✅ SEMPRE FAÇA:

- ✅ Use variáveis de ambiente
- ✅ Mantenha .env no .gitignore
- ✅ Use credenciais diferentes para dev/prod
- ✅ Rotacione credenciais periodicamente

---

**Status Atual**: ✅ **SEGURO** - Nenhuma credencial exposta no código fonte
