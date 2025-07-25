// JavaScript para o formulário de compra e venda de imóvel
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contratoForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    // Campos condicionais para cônjuge
    const proprietarioEstadoCivil = document.getElementById('id_proprietario_estado_civil');
    const compradorEstadoCivil = document.getElementById('id_comprador_estado_civil');
    const proprietarioConjugeFields = document.getElementById('proprietario-conjuge-fields');
    const compradorConjugeFields = document.getElementById('comprador-conjuge-fields');
    
    // Campos condicionais para parcelamento
    const formaPagamento = document.getElementById('id_forma_pagamento');
    const parceladoFields = document.getElementById('parcelado-fields');
    const quantidadeParcelas = document.getElementById('id_quantidade_parcelas');
    const addParcelaBtn = document.getElementById('add-parcela');
    const parcelasContainer = document.getElementById('parcelas-container');
    
    let parcelaCount = 0;
    
    // Função para mostrar/ocultar campos do cônjuge
    function toggleConjugeFields() {
        // Proprietário
        if (proprietarioEstadoCivil.value === 'casado') {
            proprietarioConjugeFields.classList.add('show');
            // Tornar campos obrigatórios
            const requiredFields = proprietarioConjugeFields.querySelectorAll('input');
            requiredFields.forEach(field => field.required = true);
        } else {
            proprietarioConjugeFields.classList.remove('show');
            // Remover obrigatoriedade
            const requiredFields = proprietarioConjugeFields.querySelectorAll('input');
            requiredFields.forEach(field => {
                field.required = false;
                field.value = '';
            });
        }
        
        // Comprador
        if (compradorEstadoCivil.value === 'casado') {
            compradorConjugeFields.classList.add('show');
            const requiredFields = compradorConjugeFields.querySelectorAll('input');
            requiredFields.forEach(field => field.required = true);
        } else {
            compradorConjugeFields.classList.remove('show');
            const requiredFields = compradorConjugeFields.querySelectorAll('input');
            requiredFields.forEach(field => {
                field.required = false;
                field.value = '';
            });
        }
    }
    
    // Função para mostrar/ocultar campos de parcelamento
    function toggleParceladoFields() {
        if (formaPagamento.value === 'parcelado') {
            parceladoFields.classList.add('show');
            quantidadeParcelas.required = true;
        } else {
            parceladoFields.classList.remove('show');
            quantidadeParcelas.required = false;
            quantidadeParcelas.value = '';
            clearParcelas();
        }
    }
    
    // Função para adicionar campo de parcela
    function addParcelaField() {
        parcelaCount++;
        const parcelaDiv = document.createElement('div');
        parcelaDiv.className = 'parcela-item';
        parcelaDiv.innerHTML = `
            <label class="form-label">Parcela ${parcelaCount}:</label>
            <input type="date" class="form-control" name="data_parcela_${parcelaCount}" required>
            <button type="button" class="remove-parcela" onclick="removeParcela(this)">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        parcelasContainer.insertBefore(parcelaDiv, addParcelaBtn);
    }
    
    // Função para remover campo de parcela
    window.removeParcela = function(button) {
        button.closest('.parcela-item').remove();
        updateParcelaLabels();
    }
    
    // Função para atualizar labels das parcelas
    function updateParcelaLabels() {
        const parcelas = parcelasContainer.querySelectorAll('.parcela-item');
        parcelas.forEach((parcela, index) => {
            const label = parcela.querySelector('label');
            const input = parcela.querySelector('input');
            label.textContent = `Parcela ${index + 1}:`;
            input.name = `data_parcela_${index + 1}`;
        });
        parcelaCount = parcelas.length;
    }
    
    // Função para limpar campos de parcelas
    function clearParcelas() {
        const parcelas = parcelasContainer.querySelectorAll('.parcela-item');
        parcelas.forEach(parcela => parcela.remove());
        parcelaCount = 0;
    }
    
    // Função para gerar parcelas automaticamente baseado na quantidade
    function generateParcelas() {
        const quantidade = parseInt(quantidadeParcelas.value);
        if (quantidade > 0) {
            clearParcelas();
            for (let i = 0; i < quantidade; i++) {
                addParcelaField();
            }
        }
    }
    
    // Event listeners
    if (proprietarioEstadoCivil) {
        proprietarioEstadoCivil.addEventListener('change', toggleConjugeFields);
        toggleConjugeFields(); // Executa na inicialização
    }
    
    if (compradorEstadoCivil) {
        compradorEstadoCivil.addEventListener('change', toggleConjugeFields);
        toggleConjugeFields(); // Executa na inicialização
    }
    
    if (formaPagamento) {
        formaPagamento.addEventListener('change', toggleParceladoFields);
        toggleParceladoFields(); // Executa na inicialização
    }
    
    if (addParcelaBtn) {
        addParcelaBtn.addEventListener('click', addParcelaField);
    }
    
    if (quantidadeParcelas) {
        quantidadeParcelas.addEventListener('change', generateParcelas);
    }
    
    // Máscaras para CPF
    const cpfInputs = document.querySelectorAll('.cpf-mask');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    });
    
    // Máscara para CEP
    const cepInputs = document.querySelectorAll('input[name*="_cep"]');
    cepInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        });
    });
    
    // Formatação automática do valor em extenso
    const valorInput = document.getElementById('id_valor_total');
    const valorExtensoInput = document.getElementById('id_valor_extenso');
    
    if (valorInput && valorExtensoInput) {
        valorInput.addEventListener('blur', function() {
            const valor = parseFloat(this.value);
            if (valor > 0) {
                // Aqui você pode implementar uma função para converter número em extenso
                // Por simplicidade, vou deixar um placeholder
                valorExtensoInput.placeholder = `Ex: ${numeroParaExtenso(valor)}`;
            }
        });
    }
    
    // Função simples para conversão numérica (implementação básica)
    function numeroParaExtenso(numero) {
        if (numero === 100000) return "cem mil reais";
        if (numero === 200000) return "duzentos mil reais";
        if (numero === 500000) return "quinhentos mil reais";
        return "Escreva o valor por extenso";
    }
    
    // Validação do formulário
    form.addEventListener('submit', function(e) {
        // Mostrar estado de carregamento
        submitBtn.classList.add('loading');
        btnText.classList.add('d-none');
        btnLoading.classList.remove('d-none');
        
        // Validação básica
        const requiredFields = form.querySelectorAll('[required]');
        let hasErrors = false;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                hasErrors = true;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        // Validação específica para campos condicionais
        if (proprietarioEstadoCivil.value === 'casado') {
            const conjugeFields = proprietarioConjugeFields.querySelectorAll('[required]');
            conjugeFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    hasErrors = true;
                }
            });
        }
        
        if (compradorEstadoCivil.value === 'casado') {
            const conjugeFields = compradorConjugeFields.querySelectorAll('[required]');
            conjugeFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    hasErrors = true;
                }
            });
        }
        
        if (formaPagamento.value === 'parcelado') {
            const parcelaInputs = parcelasContainer.querySelectorAll('input[type="date"]');
            if (parcelaInputs.length === 0) {
                hasErrors = true;
                alert('Adicione pelo menos uma data de parcela para pagamento parcelado.');
            }
        }
        
        if (hasErrors) {
            e.preventDefault();
            // Resetar estado do botão
            submitBtn.classList.remove('loading');
            btnText.classList.remove('d-none');
            btnLoading.classList.add('d-none');
            
            // Mostrar mensagem de erro
            const errorAlert = document.createElement('div');
            errorAlert.className = 'alert alert-danger alert-dismissible fade show';
            errorAlert.innerHTML = `
                <i class="fas fa-exclamation-circle me-2"></i>
                Por favor, preencha todos os campos obrigatórios.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            form.insertBefore(errorAlert, form.firstChild);
            
            // Scroll para o topo
            form.scrollIntoView({ behavior: 'smooth' });
        }
    });
    
    // Validação em tempo real
    const inputs = form.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });
    
    // Preenchimento automático de endereço por CEP (implementação futura)
    cepInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const cep = this.value.replace(/\D/g, '');
            if (cep.length === 8) {
                // Aqui você pode implementar consulta à API de CEP
                // consultarCEP(cep, this);
            }
        });
    });
});
