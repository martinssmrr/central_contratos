from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import io

def generate_contract_pdf(contract):
    """Gera o PDF do contrato usando WeasyPrint"""
    try:
        # Selecionar o template baseado no tipo de contrato
        template_name = f'contracts/pdf_templates/{contract.contract_type.slug}.html'
        
        # Contexto para o template
        context = {
            'contract': contract,
            'payment': contract.payment,
            'dados_especificos': contract.dados_especificos,
        }
        
        # Renderizar HTML
        html_string = render_to_string(template_name, context)
        
        # CSS para o PDF
        css_string = """
        @page {
            margin: 2cm;
            size: A4;
        }
        
        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            font-size: 12px;
            line-height: 1.5;
            color: #333;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 15px;
        }
        
        .header h1 {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .section {
            margin-bottom: 20px;
        }
        
        .section h2 {
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-bottom: 10px;
        }
        
        .party-info {
            background-color: #f8f9fa;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
        }
        
        .contract-details {
            background-color: #f1f2f6;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        
        .signature-section {
            margin-top: 50px;
            page-break-inside: avoid;
        }
        
        .signature-box {
            border-top: 1px solid #333;
            width: 300px;
            margin: 30px auto;
            text-align: center;
            padding-top: 5px;
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 10px;
            color: #666;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        
        table td, table th {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }
        
        table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        """
        
        # Gerar PDF
        font_config = FontConfiguration()
        html = HTML(string=html_string)
        css = CSS(string=css_string, font_config=font_config)
        
        pdf_file = html.write_pdf(stylesheets=[css], font_config=font_config)
        
        return pdf_file
        
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None


def format_currency(value):
    """Formata valor para moeda brasileira"""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def format_cpf_cnpj(document):
    """Formata CPF ou CNPJ"""
    document = ''.join(filter(str.isdigit, document))
    
    if len(document) == 11:  # CPF
        return f"{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}"
    elif len(document) == 14:  # CNPJ
        return f"{document[:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[12:]}"
    else:
        return document
