from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Banner, Produto, ItemEstoque, Categoria

def _cart_data(request):
    """Transforma o carrinho da sessão em linhas com produto, quantidade e subtotal."""
    cart = request.session.get("carrinho", {})
    linhas = []
    total = Decimal("0.00")
    for item_id, quantidade in cart.items():
        try:
            item = ItemEstoque.objects.select_related("produto", "cor").get(
                pk=int(item_id), produto__ativo=True
            )
            quantidade = max(1, int(quantidade))
        except (ItemEstoque.DoesNotExist, ValueError, TypeError):
            continue
        if not item.produto:
            continue
        subtotal = item.produto.preco * quantidade
        linhas.append({
            "item": item,
            "produto": item.produto,
            "quantidade": quantidade,
            "subtotal": subtotal,
        })
        total += subtotal
    return linhas, total

def _contexto_carrinho(request):
    linhas, total = _cart_data(request)
    return {
        "linhas_carrinho": linhas,
        "total_carrinho": total,
        "quantidade_carrinho": sum(linha["quantidade"] for linha in linhas),
        "whatsapp_number": getattr(settings, "WHATSAPP_NUMBER", ""),
    }

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    produtos = Produto.objects.filter(ativo=True).order_by("-id")[:8]
    context = {
        "banners": banners,
        "produtos": produtos,
        **_contexto_carrinho(request),
    }
    return render(request, "homepage.html", context)

def loja(request, nome_categoria=None):
    produtos = Produto.objects.filter(ativo=True).select_related("categoria", "tipo").order_by("nome")
    if nome_categoria:
        produtos = produtos.filter(categoria__nome=nome_categoria)
    context = {
        "produtos": produtos,
        "categorias": Categoria.objects.all().order_by("nome"),
        "categoria_atual": nome_categoria,
        **_contexto_carrinho(request),
    }
    return render(request, "loja.html", context)

def ver_produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto, ativo=True)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0).select_related("cor")
    context = {
        "produto": produto,
        "itens_estoque": itens_estoque,
        "tem_estoque": itens_estoque.exists(),
        **_contexto_carrinho(request),
    }
    return render(request, "ver_produto.html", context)

@require_POST
def adicionar_carrinho(request):
    item_id = request.POST.get("item_estoque")
    quantidade = request.POST.get("quantidade", "1")
    item = get_object_or_404(ItemEstoque, pk=item_id, produto__ativo=True, quantidade__gt=0)
    try:
        quantidade = max(1, int(quantidade))
    except (ValueError, TypeError):
        quantidade = 1
    cart = request.session.get("carrinho", {})
    key = str(item.pk)
    atual = int(cart.get(key, 0))
    cart[key] = min(atual + quantidade, item.quantidade)
    request.session["carrinho"] = cart
    request.session.modified = True
    messages.success(request, f"{item.produto.nome} foi adicionado ao carrinho.")
    return redirect("carrinho")

@require_POST
def atualizar_carrinho(request, item_id):
    cart = request.session.get("carrinho", {})
    key = str(item_id)
    item = get_object_or_404(ItemEstoque, pk=item_id, produto__ativo=True)
    try:
        quantidade = int(request.POST.get("quantidade", "1"))
    except (ValueError, TypeError):
        quantidade = 1
    if quantidade <= 0:
        cart.pop(key, None)
    else:
        cart[key] = min(quantidade, max(item.quantidade, 1))
    request.session["carrinho"] = cart
    request.session.modified = True
    return redirect("carrinho")

@require_POST
def remover_do_carrinho(request, item_id):
    cart = request.session.get("carrinho", {})
    cart.pop(str(item_id), None)
    request.session["carrinho"] = cart
    request.session.modified = True
    messages.info(request, "Produto removido do carrinho.")
    return redirect("carrinho")

def carrinho(request):
    return render(request, "carrinho.html", _contexto_carrinho(request))

def checkout(request):
    return render(request, "checkout.html", _contexto_carrinho(request))

def minhaconta(request):
    return render(request, "usuario/minhaconta.html", _contexto_carrinho(request))

def login(request):
    return render(request, "usuario/login.html", _contexto_carrinho(request))
