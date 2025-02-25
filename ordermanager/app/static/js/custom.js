function buscarProdutos(termo, callback) {
    fetch(`/buscar-produtos/?termo=${termo}`)
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => console.error('Erro ao buscar produtos:', error));
}

// Função para inicializar o autocomplete
function inicializarAutocomplete(input) {
    input.addEventListener('input', function () {
        const termo = this.value;
        if (termo.length >= 2) { // Busca apenas após 2 caracteres
            buscarProdutos(termo, function (produtos) {
                const datalist = document.createElement('datalist');
                datalist.id = 'produtos-lista';
                produtos.forEach(produto => {
                    const option = document.createElement('option');
                    option.value = produto.nome;
                    option.setAttribute('data-id', produto.id);
                    option.setAttribute('data-preco', produto.preco);
                    datalist.appendChild(option);
                });
                // Remove a lista anterior (se existir)
                const listaAnterior = document.getElementById('produtos-lista');
                if (listaAnterior) listaAnterior.remove();
                // Adiciona a nova lista
                document.body.appendChild(datalist);
                input.setAttribute('list', 'produtos-lista');
            });
        }
    });

    // Preenche o preço ao selecionar um produto
    input.addEventListener('change', function () {
        const selectedOption = document.querySelector(`#produtos-lista option[value="${this.value}"]`);
        if (selectedOption) {
            const preco = selectedOption.getAttribute('data-preco');
            const quantidadeInput = this.closest('.row').querySelector('.product-quantity');
            const precoInput = this.closest('.row').querySelector('.product-price');
            precoInput.value = preco;
            quantidadeInput.focus(); // Foca no campo de quantidade
        }
    });
}

// Função para adicionar novos campos de produto
function addProductField() {
    const productsContainer = document.getElementById('products-container');
    const productCount = productsContainer.children.length + 1;

    const newProductField = `
        <div class="product-entry mb-3">
            <h6>Produto ${productCount}</h6>
            <div class="row">
                <div class="col">
                    <label class="form-label">Nome</label>
                    <input type="text" class="form-control product-name" required data-autocomplete-url="{% url 'buscar_produtos' %}">
                </div>
                <div class="col">
                    <label class="form-label">Quantidade</label>
                    <input type="number" class="form-control product-quantity" min="1" required>
                </div>
                <div class="col">
                    <label class="form-label">Preço</label>
                    <input type="number" class="form-control product-price" min="0" step="0.01" required>
                </div>
            </div>
        </div>
    `;

    productsContainer.insertAdjacentHTML('beforeend', newProductField);

    // Inicializa o autocomplete para o novo campo
    const newInput = productsContainer.lastElementChild.querySelector('.product-name');
    inicializarAutocomplete(newInput);
}

// Inicializa o autocomplete para os campos existentes
document.querySelectorAll('.product-name').forEach(input => {
    inicializarAutocomplete(input);
});