# Outlet Virtual — versão com carrinho e pedido por WhatsApp

## O que foi implementado
- Layout responsivo para celular e computador.
- Página inicial e catálogo com cartões de produtos.
- Filtro por categoria.
- Página individual do produto com seleção de variação/tamanho disponível.
- Carrinho baseado na sessão do Django, com alteração de quantidade e remoção de itens.
- Resumo do pedido com subtotais e total.
- Botão para abrir o WhatsApp com a lista de produtos, variações, quantidades e total preenchidos na mensagem.
- Arquivos Python e CSS organizados sem a pasta `.venv`.

## Configurar o WhatsApp da loja
Abra `ecomerce/ecomerce/settings.py` e localize no final:

```python
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "")
```

Troque por seu número, usando código do país + DDD + número, somente dígitos. Exemplo fictício:

```python
WHATSAPP_NUMBER = "5531999999999"
```

Substitua o exemplo pelo número real que receberá os pedidos. Não coloque `+`, espaços, parênteses ou hífens.

## Executar no Windows / VS Code
Abra o terminal na pasta que contém `requirements.txt` e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ecomerce
py manage.py migrate
py manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador.

Se precisar criar um usuário para o painel administrativo:

```powershell
py manage.py createsuperuser
```

Depois acesse `http://127.0.0.1:8000/admin/`.

## Observações
- Os produtos e suas opções de estoque continuam sendo gerenciados pelo Django Admin.
- Para aparecer como opção de compra, o produto precisa estar ativo e ter pelo menos um registro de estoque com quantidade maior que zero.
- O botão do WhatsApp apenas prepara e abre a mensagem; não processa pagamento nem confirma automaticamente o estoque.
- Antes de publicar em produção, configure `DEBUG = False`, `ALLOWED_HOSTS`, `SECRET_KEY`, HTTPS e os arquivos estáticos conforme o ambiente do servidor.
"# outletv" 
"# lojavirtual" 
"# lojavirtual" 
