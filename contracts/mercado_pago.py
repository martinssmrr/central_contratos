"""
Serviço de integração com Mercado Pago
"""
import mercadopago
from django.conf import settings
from django.urls import reverse
import logging

sdk = mercadopago.SDK

logger = logging.getLogger(__name__)

class MercadoPagoService:
    """Serviço para integração com Mercado Pago"""
    
    def __init__(self):
        """Inicializa o SDK do Mercado Pago"""
        self.sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        self.public_key = settings.MERCADO_PAGO_PUBLIC_KEY
    
    def create_preference(self, payment, request=None):
        """
        Cria uma preferência de pagamento no Mercado Pago
        
        Args:
            payment: Instância do modelo Payment
            request: Request HTTP para construir URLs absolutas
            
        Returns:
            dict: Dados da preferência criada
        """
        try:
            # Obter o contrato através do pagamento
            contract = payment.contract
            
            # URLs de retorno
            base_url = "https://centralcontratos.pythonanywhere.com/"  # URL temporária para teste
            if request:
                base_url = f"{request.scheme}://{request.get_host()}"
            elif hasattr(settings, 'BASE_URL') and settings.BASE_URL:
                base_url = settings.BASE_URL
            
            # URLs de retorno configuradas para auto_return funcionar (SEM placeholders)
            back_urls = {
                "success": f"{base_url}/contracts/payment-success/?contract_id={contract.id}",
                "failure": f"{base_url}/pagamento/erro/?contract_id={contract.id}",
                "pending": f"{base_url}/contracts/payment-pending/?contract_id={contract.id}"
            }
            
            # Auto-return funciona apenas em produção (URLs HTTPS)
            # Em desenvolvimento (localhost), o Mercado Pago não permite auto_return
            enable_auto_return = not ('localhost' in base_url or '127.0.0.1' in base_url or ':8000' in base_url)
            
            # Dados da preferência
            preference_data = {
                "items": [
                    {
                        "title": f"Contrato: {contract.contract_type.name}",
                        "description": f"Contrato personalizado - {contract.contract_type.description[:100]}",
                        "quantity": 1,
                        "currency_id": "BRL",
                        "unit_price": float(payment.amount)
                    }
                ],
                "payer": {
                    "name": contract.user.first_name or contract.user.username,
                    "surname": contract.user.last_name or "",
                    "email": contract.user.email,
                },
                "back_urls": back_urls,
                "external_reference": str(contract.id),
                "metadata": {
                    "contract_id": contract.id,
                    "user_id": contract.user.id,
                    "contract_type": contract.contract_type.name
                }

            }
            
            # Adicionar auto_return apenas se não for localhost (produção)
            if enable_auto_return:
                preference_data["auto_return"] = "approved"
                logger.info(f"Auto-return habilitado para produção")
            else:
                logger.info(f"Auto-return desabilitado para desenvolvimento (localhost)")
            
            # Criar preferência
            preference_response = self.sdk.preference().create(preference_data)
            
            if preference_response["status"] == 201:
                preference = preference_response["response"]
                
                # Atualizar o pagamento recebido como parâmetro
                payment.preference_id = preference['id']
                payment.external_reference = str(contract.id)
                payment.save()
                
                logger.info(f"Preferência criada com sucesso: {preference['id']} para contrato {contract.id}")
                
                return {
                    'success': True,
                    'preference_id': preference['id'],
                    'init_point': preference['init_point'],
                    'sandbox_init_point': preference['sandbox_init_point'],
                    'response': preference
                }
            else:
                logger.error(f"Erro ao criar preferência: {preference_response}")
                return {
                    'success': False,
                    'error': 'Erro ao processar pagamento. Tente novamente.'
                }
                
        except Exception as e:
            logger.error(f"Erro ao criar preferência do Mercado Pago: {str(e)}")
            return {
                'success': False,
                'error': 'Erro interno. Tente novamente.'
            }
    
    def get_payment_info(self, payment_id):
        """
        Busca informações de um pagamento pelo ID
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
            
        Returns:
            dict: Dados do pagamento
        """
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] == 200:
                return {
                    'success': True,
                    'payment': payment_response["response"]
                }
            else:
                logger.error(f"Erro ao buscar pagamento {payment_id}: {payment_response}")
                return {
                    'success': False,
                    'error': 'Pagamento não encontrado'
                }
                
        except Exception as e:
            logger.error(f"Erro ao buscar pagamento {payment_id}: {str(e)}")
            return {
                'success': False,
                'error': 'Erro ao buscar informações do pagamento'
            }
    
    def process_webhook(self, request):
        """
        Processa webhook de notificação do Mercado Pago
        
        Args:
            request: Request HTTP com dados do webhook
            
        Returns:
            dict: Resultado do processamento
        """
        try:
            # Dados do webhook
            data = request.GET
            payment_id = data.get('data.id') or data.get('id')
            topic = data.get('topic') or data.get('type')
            
            logger.info(f"Webhook recebido - Topic: {topic}, Payment ID: {payment_id}")
            
            if topic == 'payment' and payment_id:
                # Buscar informações do pagamento
                payment_info = self.get_payment_info(payment_id)
                
                if payment_info['success']:
                    payment_data = payment_info['payment']
                    external_reference = payment_data.get('external_reference')
                    
                    if external_reference:
                        # Buscar contrato e pagamento
                        from .models import Contract, Payment
                        
                        try:
                            contract = Contract.objects.get(id=int(external_reference))
                            payment, created = Payment.objects.get_or_create(
                                contract=contract,
                                defaults={
                                    'amount': contract.contract_type.price,
                                    'status': 'pending'
                                }
                            )
                            
                            # Atualizar dados do pagamento
                            payment.update_from_mercadopago(payment_data)
                            
                            logger.info(f"Pagamento atualizado: {payment.id} - Status: {payment.status}")
                            
                            return {
                                'success': True,
                                'message': 'Webhook processado com sucesso'
                            }
                            
                        except Contract.DoesNotExist:
                            logger.error(f"Contrato não encontrado: {external_reference}")
                            return {
                                'success': False,
                                'error': 'Contrato não encontrado'
                            }
            
            return {
                'success': True,
                'message': 'Webhook ignorado'
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {str(e)}")
            return {
                'success': False,
                'error': 'Erro ao processar notificação'
            }
    
    def _get_expiration_date(self, created_at):
        """Calcula data de expiração (24 horas após criação)"""
        from datetime import timedelta
        return created_at + timedelta(hours=24)

# Instância singleton do serviço
mercado_pago_service = MercadoPagoService()
