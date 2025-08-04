#!/bin/bash

# ========================================
# Script de Deploy Automatizado
# Central de Contratos - PythonAnywhere
# ========================================

echo "🚀 Iniciando deploy do Central de Contratos..."

# Definir variáveis
PROJECT_DIR="/home/martinssmrr/central_contratos"
VENV_DIR="$PROJECT_DIR/.venv"
SETTINGS_MODULE="setup.settings_production"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log com cor
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -d "$PROJECT_DIR" ]; then
    error "Diretório do projeto não encontrado: $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

# 1. Fazer backup do banco atual
log "📦 Fazendo backup do banco de dados..."
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    log "✅ Backup criado com sucesso"
else
    warning "Banco de dados não encontrado - primeiro deploy?"
fi

# 2. Atualizar código do repositório
log "📥 Atualizando código do repositório..."
git fetch origin
git status

# Verificar se há mudanças
if git diff --quiet HEAD origin/main; then
    info "Nenhuma atualização disponível"
else
    log "📥 Baixando atualizações..."
    git pull origin main
    if [ $? -eq 0 ]; then
        log "✅ Código atualizado com sucesso"
    else
        error "Falha ao atualizar código"
        exit 1
    fi
fi

# 3. Ativar ambiente virtual
log "🐍 Ativando ambiente virtual..."
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    log "✅ Ambiente virtual ativado"
else
    error "Ambiente virtual não encontrado: $VENV_DIR"
    exit 1
fi

# 4. Atualizar dependências
log "📚 Verificando dependências..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    log "✅ Dependências atualizadas"
else
    error "Falha ao instalar dependências"
    exit 1
fi

# 5. Executar migrações
log "🗄️ Aplicando migrações do banco..."
python manage.py migrate --settings="$SETTINGS_MODULE" --noinput
if [ $? -eq 0 ]; then
    log "✅ Migrações aplicadas com sucesso"
else
    error "Falha ao aplicar migrações"
    exit 1
fi

# 6. Coletar arquivos estáticos
log "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --settings="$SETTINGS_MODULE" --noinput --clear
if [ $? -eq 0 ]; then
    log "✅ Arquivos estáticos coletados"
else
    error "Falha ao coletar arquivos estáticos"
    exit 1
fi

# 7. Verificar configuração
log "🔍 Verificando configuração..."
python manage.py check --settings="$SETTINGS_MODULE" --deploy
if [ $? -eq 0 ]; then
    log "✅ Configuração verificada"
else
    warning "Alguns avisos de configuração encontrados"
fi

# 8. Verificar se o site está acessível
log "🌐 Verificando se o site está online..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://martinssmrr.pythonanywhere.com)
if [ "$HTTP_STATUS" -eq 200 ]; then
    log "✅ Site está online e acessível"
else
    warning "Site retornou status HTTP: $HTTP_STATUS"
fi

# 9. Limpeza (opcional)
log "🧹 Executando limpeza..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
log "✅ Limpeza concluída"

# 10. Resumo do deploy
echo ""
echo "========================================="
log "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "========================================="
info "📊 Resumo:"
info "   - Projeto: Central de Contratos"
info "   - Ambiente: Produção (PythonAnywhere)"
info "   - URL: https://martinssmrr.pythonanywhere.com"
info "   - Data: $(date +'%Y-%m-%d %H:%M:%S')"
echo ""
info "🔗 Links importantes:"
info "   - Home: https://martinssmrr.pythonanywhere.com"
info "   - Admin: https://martinssmrr.pythonanywhere.com/admin/"
info "   - Catálogo: https://martinssmrr.pythonanywhere.com/contracts/catalog/"
echo ""
warning "⚠️ Lembre-se de:"
warning "   1. Recarregar o Web App no painel do PythonAnywhere"
warning "   2. Testar funcionalidades críticas"
warning "   3. Verificar logs de erro se necessário"
echo ""
log "🚀 Deploy finalizado! Boa sorte com o projeto!"

# Opcional: mostrar últimos commits
echo ""
info "📝 Últimas mudanças:"
git log --oneline -n 5
