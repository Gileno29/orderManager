document.addEventListener('DOMContentLoaded', function () {
    // Adiciona o evento de change aos campos de produto existentes
    document.querySelectorAll('.product-select').forEach(select => {
        select.addEventListener('change', function () {
            const selectedOption = this.options[this.selectedIndex];
            const price = selectedOption.getAttribute('data-price');
            const priceInput = this.closest('.product-entry').querySelector('.product-price');
            if (priceInput) {
                priceInput.value = price || '';
            }
        });
    });

    // Função para adicionar mais campos de produto
    window.addProductField = function () {
        const productsContainer = document.getElementById('products-container');
        if (!productsContainer) return; // Verifica se o container existe

        const productEntry = productsContainer.querySelector('.product-entry');
        if (!productEntry) return; // Verifica se o campo de produto existe

        const newProductEntry = productEntry.cloneNode(true);

        // Limpa os valores do novo campo
        const selects = newProductEntry.querySelectorAll('select');
        const inputs = newProductEntry.querySelectorAll('input');

        selects.forEach(select => {
            select.selectedIndex = 0;
        });

        inputs.forEach(input => {
            input.value = '';
        });

        // Atualiza o título do novo campo
        const productCount = productsContainer.querySelectorAll('.product-entry').length + 1;
        newProductEntry.querySelector('h6').textContent = `Produto ${productCount}`;

        // Adiciona o novo campo ao container
        productsContainer.appendChild(newProductEntry);

        // Adiciona o evento de change ao novo campo de produto
        const newProductSelect = newProductEntry.querySelector('.product-select');
        const newProductPrice = newProductEntry.querySelector('.product-price');
        if (newProductSelect && newProductPrice) {
            newProductSelect.addEventListener('change', function () {
                const selectedOption = this.options[this.selectedIndex];
                const price = selectedOption.getAttribute('data-price');
                newProductPrice.value = price || '';
            });
        }
    };
});document.addEventListener('DOMContentLoaded', function () {
    // Adiciona o evento de change aos campos de produto existentes
    document.querySelectorAll('.product-select').forEach(select => {
        select.addEventListener('change', function () {
            const selectedOption = this.options[this.selectedIndex];
            const price = selectedOption.getAttribute('data-price');
            const priceInput = this.closest('.product-entry').querySelector('.product-price');
            if (priceInput) {
                priceInput.value = price || '';
            }
        });
    });

    // Função para adicionar mais campos de produto
    window.addProductField = function () {
        const productsContainer = document.getElementById('products-container');
        if (!productsContainer) return; // Verifica se o container existe

        const productEntry = productsContainer.querySelector('.product-entry');
        if (!productEntry) return; // Verifica se o campo de produto existe

        const newProductEntry = productEntry.cloneNode(true);

        // Limpa os valores do novo campo
        const selects = newProductEntry.querySelectorAll('select');
        const inputs = newProductEntry.querySelectorAll('input');

        selects.forEach(select => {
            select.selectedIndex = 0;
        });

        inputs.forEach(input => {
            input.value = '';
        });

        // Atualiza o título do novo campo
        const productCount = productsContainer.querySelectorAll('.product-entry').length + 1;
        newProductEntry.querySelector('h6').textContent = `Produto ${productCount}`;

        // Adiciona o novo campo ao container
        productsContainer.appendChild(newProductEntry);

        // Adiciona o evento de change ao novo campo de produto
        const newProductSelect = newProductEntry.querySelector('.product-select');
        const newProductPrice = newProductEntry.querySelector('.product-price');
        if (newProductSelect && newProductPrice) {
            newProductSelect.addEventListener('change', function () {
                const selectedOption = this.options[this.selectedIndex];
                const price = selectedOption.getAttribute('data-price');
                newProductPrice.value = price || '';
            });
        }
    };
});