from django.db import models
from django.utils import timezone

class FAQ(models.Model):
    """Modelo para Perguntas Frequentes"""
    
    pergunta = models.CharField(
        max_length=500,
        verbose_name="Pergunta",
        help_text="A pergunta frequente"
    )
    
    resposta = models.TextField(
        verbose_name="Resposta",
        help_text="A resposta detalhada para a pergunta"
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Se esta FAQ está visível no site"
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem",
        help_text="Ordem de exibição (menor número aparece primeiro)"
    )
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['ordem', 'criado_em']
        
    def __str__(self):
        return f"FAQ: {self.pergunta[:50]}..."
        
    @property
    def pergunta_resumida(self):
        """Retorna versão resumida da pergunta para admin"""
        if len(self.pergunta) > 60:
            return f"{self.pergunta[:60]}..."
        return self.pergunta
