from django.urls import path
from .views import (
    homepage, loja, minhaconta, ver_produto, login, carrinho, checkout,
    adicionar_carrinho, atualizar_carrinho, remover_do_carrinho,
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("loja/", loja, name="loja"),
    path("loja/<str:nome_categoria>/", loja, name="loja_categoria"),
    path("minhaconta/", minhaconta, name="minhaconta"),
    path("produto/<int:id_produto>/", ver_produto, name="ver_produto"),
    path("login/", login, name="login"),
    path("carrinho/", carrinho, name="carrinho"),
    path("carrinho/adicionar/", adicionar_carrinho, name="adicionar_carrinho"),
    path("carrinho/atualizar/<int:item_id>/", atualizar_carrinho, name="atualizar_carrinho"),
    path("carrinho/remover/<int:item_id>/", remover_do_carrinho, name="remover_do_carrinho"),
    path("checkout/", checkout, name="checkout"),
]
