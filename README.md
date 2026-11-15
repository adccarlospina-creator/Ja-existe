# JÁ EXISTE?! — projeto pronto para publicar

Este projeto contém um site estático de demonstração (`index.html`) e um recolhedor de sugestões de notícias (`descobrir.py`). **Não está online até o proprietário publicar num serviço de alojamento.**

## Publicação gratuita com GitHub Pages

1. Criar conta em https://github.com/signup (requer ação do proprietário).
2. Criar repositório **público** com nome `ja-existe` (ou outro).
3. Carregar os ficheiros **da raiz desta pasta** para a raiz do repositório, incluindo a pasta oculta `.github/workflows/` (mais fácil num computador ou via Git).
4. Abrir **Settings → Pages → Build and deployment → Source → GitHub Actions**.
5. Abrir **Actions**, autorizar a execução se solicitado, e executar `Publicar site no GitHub Pages` (ou aguardar execução automática).
6. Depois de publicado, o endereço será semelhante a `https://UTILIZADOR.github.io/ja-existe/`.

## Novidades automáticas

O workflow `Descobrir novidades para revisão` executa diariamente o script Python e atualiza `sugestoes.json` com **sugestões não verificadas**. Não as publica no site. Os RSS podem falhar, e o GitHub pode atrasar ou suspender execuções agendadas. Para publicar uma novidade, confirmar fonte oficial, data de lançamento e disponibilidade e editar o catálogo em `index.html`.

## Custos e limites

O GitHub tem opções gratuitas para repositórios públicos, GitHub Pages e GitHub Actions sujeitas às respetivas condições e limites. Não existe neste projeto pagamento, conta de utilizador, métricas de audiência, ligação a anunciantes, nem IA paga. Não prometer receita automática ou conteúdos atualizados sem revisão.
