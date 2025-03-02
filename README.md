# Order Manager
Esse projeto tem como objetivo desenvolver um sistema simples que permite gerir pedidos de forma generica assim como, alem disso também disponibiliza uma API para identificar a vogal em uma string seguindo parãmetros especificos

## Tabela de Conteúdos

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Rodando a Aplicação](#uso)
- [Estrutura Banco dados](#tabela)
- [Estrutura do Projeto](#estrutura)
- [Infraestrutura](#infraestrutura)



<div id='sobre'/>

 ## Sobre

Esse software foi desenvolvido visando poder realizar as tarefas simples de gerar pedidos atualizar esses pedidos e realizar o cadastro e remoção dos clientes e produtos que serão utilizados nos pedidos.

<div id='tecnologias'/>

## Tecnologias
<div style="display: flex">

 <img img align="center" alt="Django-Rest" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/djangorest/djangorest-original.svg" />

 <img align="center" alt="Python" height="50" width="100"  width="80" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg" />
 <img  align="center" alt="Docker" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" />
 <img align="center" alt="PostgreSQL" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original-wordmark.svg" />
 <img align="center" alt="HTML" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original-wordmark.svg" />
 <img align="center" alt="CSS" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original.svg" />
 <img  align="center" alt="Javascript" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" />
 <img align="center" alt="Actions" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/githubactions/githubactions-original.svg"/>
 <img  align="center" alt="bootstrap" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bootstrap/bootstrap-original.svg" />
 <img  align="center" alt="nginx" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg" />
 <img  align="center" alt="nginx" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ssh/ssh-original-wordmark.svg" />
 <img align="center" alt="nginx" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ubuntu/ubuntu-original.svg" />
          


          
          
          
</div>


<div id='requisitos'/>
 
## Requisitos
<ul>
  <li>Git</li>
  <li>Deve possuir o <a href="https://docs.docker.com/engine/install/">Docker</a> e também o <a href="https://docs.docker.com/compose/install/">Docker-compose</a> instalados em sua máquina.
</ul>

<div id='uso'/>

## Rodando a Aplicação
Instruções para iniciar a aplicação.

```sh
# Clone o repositório
git clone https://github.com/Gileno29/orderManager.git

# Navegue até o diretório do projeto
cd ordermanager 
```
vai ser preciso criar dois arquivos de váriaveis ".env" um na raiz do projeto onde encontra-se o docker compose e outro dentro de ```app/ordermanager```

o primeiro arquivo:

```sh
vim .env
```

```yml
POSTGRES_USER=userorder
POSTGRES_PASSWORD=orderpass
POSTGRES_DB=order

```

o segundo navegue até o diretorio  ```app/ordermanager``` e crie o arquivo ".env"

```yml
    SECRET_KEY='django-insecure-nj=w6(caq-bzxcb_0xiw^7@s7oxvfn@k7f&)+bple_8qiw%@pr'
    DB_USER='userorder'
    DB_HOST='db'
    DB_PASSS='orderpass'
    DB_NAME='order'
```

retorne para a raiz do projeto e rode

```sh
docker-compose up --build

  OU 

docker-compose up -d  --build #rodar em backgroud
```
*Obs:* Verifique se já possui serviços funcionando em sua máquina nas portas da aplicação, caso haja desative.

Seguindo a ordem corretamente o sistema deve iniciar e está acessivel no endereço: http://localhost:8080/

## Utilizaçao

O sistema consite em um software que vai gerenciar pedidos, antes de poder criar um pedido vai ser preciso realizar o cadastro de um cliente e o cadastro dos produtos que poderão ser vendidos pelo software.



### interface sistema

<img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/Imagem_tela_inicial.png"/>

- Opção de cadatro do cliente:
  funcionalidade para cadastro simples de um cliente. (Nome, Telefone, descricao do endereco e cpf/cnpj)
 <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/cadastrar_clientes.png"/>

 Formulario de Cadastro:
 <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/CadastroCliente.png"/>

- Opção de cadastro de produtos: 
  funcionalidade para cadastro simples de um produto. (Nome, descricao, valor)
  <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/tela_cadstro_produtos.png"/>

 formlario de produtos
  <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/formulario_de_cadastro_de_produtos.png"/>
 
- Opção de cadastro de usuario:

  <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/cadstro_de_usuarios.png"/>

  formulario para cadastro de usuarios:

  <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/formulario_de_cadastro_de_usuarios.png"/>
  
- Opção de relatorios detalhados:
  Permite a extração de relatórios  em csv com filtros especificos.

<img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/relatorios_detalhamento.png"/>

- Opção de relatorios de vendas:
  permite o usuario visualizar dados gerais sobre as vendas.

  <img src="https://github.com/Gileno29/orderManager/blob/main/ordermanager/doc/imagens/relatorio_vendas.png"/>


o sistema vai abrir na tela inicial onde ficam os pedidos cadastrados na últimas 24 horas.



<div id='tabela'/>

## Estrutura do Database

 Abaixo segue um resumo dos models atuais do sistema que geram o banco de dados.

```bash
  order=# \d
                         List of relations
 Schema |               Name                |   Type   |   Owner   
--------+-----------------------------------+----------+-----------
 public | auth_group                        | table    | userorder
 public | auth_group_id_seq                 | sequence | userorder
 public | auth_group_permissions            | table    | userorder
 public | auth_group_permissions_id_seq     | sequence | userorder
 public | auth_permission                   | table    | userorder
 public | auth_permission_id_seq            | sequence | userorder
 public | auth_user                         | table    | userorder
 public | auth_user_groups                  | table    | userorder
 public | auth_user_groups_id_seq           | sequence | userorder
 public | auth_user_id_seq                  | sequence | userorder
 public | auth_user_user_permissions        | table    | userorder
 public | auth_user_user_permissions_id_seq | sequence | userorder
 public | django_admin_log                  | table    | userorder
 public | django_admin_log_id_seq           | sequence | userorder
 public | django_content_type               | table    | userorder
 public | django_content_type_id_seq        | sequence | userorder
 public | django_migrations                 | table    | userorder
 public | django_migrations_id_seq          | sequence | userorder
 public | django_session                    | table    | userorder
 public | orders_cliente                    | table    | userorder
 public | orders_cliente_id_seq             | sequence | userorder
 public | orders_itempedido                 | table    | userorder
 public | orders_itempedido_id_seq          | sequence | userorder
 public | orders_pedido                     | table    | userorder
 public | orders_pedido_id_seq              | sequence | userorder
 public | orders_produto                    | table    | userorder
 public | orders_produto_id_seq             | sequence | userorde
```
Classe Venda:

```py

from django.db import models
from django.db.models import Sum
from django.shortcuts import render, redirect
from decimal import Decimal
from .constants import STATUS_CHOICES
# Create your models here.

class Cliente(models.Model):

    nome = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    cpfcnpj = models.CharField(max_length=20, blank=False, null=False, verbose_name="CPF/CNPJ")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"




class Produto(models.Model):
    
    nome = models.CharField(max_length=100, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"



class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='itens', verbose_name="Pedido")

    def __str__(self):
         return f"{self.quantidade} x {self.produto.nome if self.produto else 'Produto Removido'}"

    def preco_item(self):
        return Decimal(self.quantidade) * Decimal(self.produto.preco)

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_andamento',  null=True, blank=True,verbose_name="Status")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total")

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

    def preco_total(self):
        total = self.itens.aggregate(total=Sum(models.F('quantidade') * models.F('produto__preco')))['total']
        return Decimal(total) if total is not None else Decimal(0)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def atualizar_valor_total(self):

        self.valor_total = self.preco_total()
        self.save(update_fields=['valor_total'])

```




<div id='estrutura'/>

## Estrutura do projeto
O projeto possui a seguinte estrutura:

```sh
  .
├── app
│   ├── create_user.py
│   ├── db.sqlite3
│   ├── manage.py
│   ├── ordermanager
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── orders
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── constants.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── middleware.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── views_api.py
│   │   └── views.py
│   └── templates
│       ├── cad-clientes.html
│       ├── cad-produtos.html
│       ├── criar-usuario.html
│       ├── editar-cliente.html
│       ├── editar-pedido.html
│       ├── editar-produto.html
│       ├── editar-usuario.html
│       ├── list-clientes.html
│       ├── list-produtos.html
│       ├── list-usuarios.html
│       ├── logged_out.html
│       ├── login.html
│       ├── main.html
│       ├── model-footer.html
│       ├── model-header.html
│       ├── model-page.html
│       ├── relatorio-pedidos.html
│       ├── relatorios.html
│       └── restante.html
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── nginx
│   ├── Dockerfile
│   └── nginx.conf
└── requirements.txt
```
O core do aplicativo encontra-se no diretorio ``app`` nesse diretorio pode ser encontrado as configurações principais do sistema dentro do diretorio ``ordermanager``. E também o APP ``orders`` que possui os models do sistema e as views para acesso.
Externamente pode ser encontrado o arquivo de docker compose e os arquivos de cnfiguração do proxy reverso do nginx.

Ainda nesse nível encontra-se os arquivos para deploy e configuração da infraestrutura da aplicação.

<div id='infraestrutura'/>

## Infraestrutura
A infraestrutura para deploy consiste em 3 partes:

- Aplicação: se trata do sistema em si, que é conteinerizado dentro de um container do Python
- Banco de dados: container à parte com o database do sistema
- Proxy Reverso: container com o serviço do NGINX que vai ser responsável por receber as requisições e encaminhar ao serviço

Diagrama da Estrutura::
  
  <div yle="display: flex">
    <img src=https://github.com/Gileno29/file_loader/blob/main/doc/img/diagrama_estrutural.png/>
  </div>

### Docker file

```sh
  FROM python:3.9-slim

  WORKDIR /app

  COPY requirements.txt requirements.txt
  RUN pip install -r requirements.txt


  COPY . .


  EXPOSE 5000


  CMD ["gunicorn","--timeout" ,"800", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]


```
O Dockerfile consiste em uma imagem criada a partir da imagem python:3.9-slim. Ele vai:

- criar o workdir da aplicação
- enviar o arquivo de requirements e instalar os mesmos
- copiar os arquivos da aplicação e enviar para o container
- expor a porta da aplicação
- Por último, vai chamar o Gunicorn para subir o serviço.

*OBS*: caso seja alterado algo do código da aplicação, da forma que está, esse container precisará ser buildado novamente. Execute:
   ``` docker-compose down -v```
   ```docker-compose up --build```


### Docker compose file
```yml
  version: '3.8'

  services:
    web:
      build: .
      ports:
        - "5000:5000"
      depends_on:
        - db
      networks:
        - webnet
        - database

    db:
      image: postgres:13
      command: -c 'max_connections=5000'
      environment:
        POSTGRES_USER: uservendas
        POSTGRES_PASSWORD: passvendas
        POSTGRES_DB: venda
      volumes:
        - postgres_data:/var/lib/postgresql/data
      networks:
        - database
    nginx:
      image: nginx:latest
      ports:
        - "80:80"
      depends_on:
        - web
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
      networks:
        - webnet

  volumes:
    postgres_data:

  networks:
    webnet:
    database:

  ```
O docker-compose vai definir 3 serviços em sua estrutura, web(aplicacao) db(database) e nginx(proxy).
Os serviço web está tanto na rede do database quando na do proxy devido a necessidade de comunicação com ambos os serviços, enquando o proxy e o database encontran-se em suas respectivas redes apenas.

### Proxy web:
 ```sh
  events {
      worker_connections 1024;
  }

  http {
      upstream web {
          server web:5000;
      }

      server {
          listen 80;

          location / {
              proxy_pass http://web;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
              proxy_connect_timeout 3600s;
              proxy_send_timeout 3600s;
              proxy_read_timeout 3600s;
              send_timeout 3600s;
          }

          # Ajuste para tamanhos de upload
          client_max_body_size 16M;
      }
  }
```
O arquvo de configuração do NGINX define uma configuração de proxy simples, o timeout pode ser ajustado para menos, dependendo da situação, caso o arquivo enviado seja muito grande e demore a carregar demais a aplicação pode dar timeout.

## Testes

Foram implementados tests para validacao de funcionalidades do sistema, eles se encontram na raiz do projeto dentro do diretorio ``tests``:

```sh
  tests/
  ├── test_vendas.py
  └── test_views.py
```
Para execução dos testes do projeto vá até a raiz e execute: 
```python3 -m unittest discover -s tests```

A arquivo test_vendas.py possui os testes da classe Vendas do modulo etl, já o arquivo test_views.py executa alguns testes basicos nas rotas do sistema que se encontram no arquivo main.py.
