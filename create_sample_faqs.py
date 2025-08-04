#!/usr/bin/env python
"""
Script para criar FAQs de exemplo para o sistema
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from core.models import FAQ

def create_sample_faqs():
    """Criar FAQs de exemplo"""
    
    # Limpar FAQs existentes
    FAQ.objects.all().delete()
    print("🗑️ FAQs existentes removidas")
    
    faqs_data = [
        {
            'pergunta': 'Como funciona a personalização de contratos?',
            'resposta': '''Nossa plataforma permite que você customize contratos de acordo com suas necessidades específicas. 

Após selecionar um tipo de contrato, você pode:

• Preencher campos personalizados
• Adicionar cláusulas específicas
• Ajustar valores e datas
• Incluir informações das partes envolvidas

O processo é guiado e intuitivo, garantindo que seu contrato esteja completo e juridicamente válido.''',
            'ordem': 1
        },
        {
            'pergunta': 'Quais são os métodos de pagamento aceitos?',
            'resposta': '''Aceitamos diversos métodos de pagamento para sua comodidade:

**Cartões de Crédito:**
• Visa, Mastercard, American Express
• Parcelamento em até 12x sem juros

**PIX:**
• Pagamento instantâneo
• Disponível 24h por dia
• Desconto de 5% para pagamentos via PIX

**Boleto Bancário:**
• Vencimento em 3 dias úteis
• Aceito em qualquer banco

Todos os pagamentos são processados de forma segura com criptografia SSL.''',
            'ordem': 2
        },
        {
            'pergunta': 'Os contratos têm validade jurídica?',
            'resposta': '''Sim! Todos os nossos contratos são elaborados por advogados especialistas e seguem a legislação brasileira vigente.

**Características dos nossos contratos:**
• Baseados no Código Civil Brasileiro
• Revisados por equipe jurídica especializada
• Atualizados conforme mudanças na legislação
• Válidos em todo território nacional

**Importante:** Recomendamos sempre a revisão por um advogado de sua confiança antes da assinatura, especialmente em contratos de alto valor.''',
            'ordem': 3
        },
        {
            'pergunta': 'Posso editar um contrato após a compra?',
            'resposta': '''Sim, você pode editar seus contratos dentro de certas condições:

**Período de Edição:**
• Até 30 dias após a compra
• Antes da primeira assinatura digital
• Máximo de 5 edições por contrato

**O que pode ser editado:**
• Dados das partes (nomes, documentos, endereços)
• Valores e datas
• Cláusulas opcionais
• Condições específicas

**O que NÃO pode ser editado:**
• Estrutura base do contrato
• Cláusulas obrigatórias por lei
• Tipo de contrato

Para editar, acesse "Meus Contratos" no seu perfil.''',
            'ordem': 4
        },
        {
            'pergunta': 'Como funciona o suporte técnico?',
            'resposta': '''Oferecemos suporte completo para garantir sua melhor experiência:

**Canais de Atendimento:**
• Chat online (horário comercial)
• Email: suporte@centralcontratos.com.br
• WhatsApp: (11) 99999-9999
• Central de ajuda online

**Horários:**
• Segunda a Sexta: 8h às 18h
• Sábado: 8h às 12h
• Resposta em até 4 horas úteis

**Tipos de Suporte:**
• Dúvidas sobre personalização
• Problemas técnicos
• Orientação jurídica básica
• Ajuda com pagamentos

Nossa equipe está sempre pronta para ajudar!''',
            'ordem': 5
        },
        {
            'pergunta': 'Existe garantia de satisfação?',
            'resposta': '''Sim! Oferecemos garantia total de satisfação:

**Garantia de 30 dias:**
• Reembolso integral em caso de insatisfação
• Sem perguntas, sem burocracia
• Válida para contratos não utilizados

**O que está coberto:**
• Problemas técnicos na plataforma
• Contratos que não atendam suas expectativas
• Dificuldades na personalização
• Qualquer insatisfação com o serviço

**Como solicitar:**
1. Entre em contato pelo suporte
2. Informe o motivo da solicitação
3. Reembolso processado em até 5 dias úteis

Sua satisfação é nossa prioridade!''',
            'ordem': 6
        },
        {
            'pergunta': 'Preciso ser advogado para usar a plataforma?',
            'resposta': '''Não! Nossa plataforma foi desenvolvida para ser acessível a todos:

**Para Pessoas Físicas:**
• Interface intuitiva e simples
• Linguagem clara e objetiva
• Processo guiado passo a passo
• Explicações detalhadas de cada campo

**Para Empresários:**
• Contratos comerciais simplificados
• Templates adequados para diferentes setores
• Orientações específicas para cada tipo de negócio

**Para Profissionais do Direito:**
• Ferramentas avançadas de customização
• Biblioteca jurídica completa
• Modelos atualizados conforme legislação

**Dica importante:** Mesmo sendo fácil de usar, sempre recomendamos consultar um advogado em contratos complexos ou de alto valor.''',
            'ordem': 7
        },
        {
            'pergunta': 'Como posso acessar meus contratos comprados?',
            'resposta': '''Você pode acessar seus contratos de várias formas:

**No seu perfil:**
• Faça login na plataforma
• Acesse "Meus Contratos"
• Visualize todos os contratos adquiridos
• Baixe em PDF quando necessário

**Por email:**
• Receba cópia automática no seu email
• Links diretos para download
• Notificações de atualizações

**Armazenamento:**
• Contratos salvos permanentemente
• Backup em nuvem segura
• Acesso ilimitado
• Histórico de versões

**Formatos disponíveis:**
• PDF para impressão
• Word para edição (quando aplicável)
• Versão online para consulta

Seus contratos ficam sempre disponíveis no seu painel pessoal.''',
            'ordem': 8
        }
    ]
    
    # Criar as FAQs
    for i, faq_data in enumerate(faqs_data, 1):
        faq = FAQ.objects.create(**faq_data)
        print(f"✅ FAQ {i}: {faq.pergunta[:50]}...")
    
    print(f"\n🎉 {len(faqs_data)} FAQs criadas com sucesso!")
    print("\n📋 Resumo das FAQs criadas:")
    for faq in FAQ.objects.all().order_by('ordem'):
        status = "🟢 Ativa" if faq.ativa else "🔴 Inativa"
        print(f"   {faq.ordem}. {faq.pergunta[:60]}... ({status})")

if __name__ == '__main__':
    print("🚀 Criando FAQs de exemplo...")
    create_sample_faqs()
    print("\n✨ Processo concluído!")
