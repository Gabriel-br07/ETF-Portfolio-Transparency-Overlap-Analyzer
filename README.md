# ETF-Portfolio-Transparency-Overlap-Analyzer

Guia rápido para rodar o projeto localmente.

Requisitos
- Node.js 20
- pnpm 9
- Python 3.13
- Poetry 2.2

Frontend (ui/)
1. Instale dependências (a partir da raiz do monorepo):

```
cd ui
pnpm install --frozen-lockfile
```

2. Rodar em modo de desenvolvimento (monorepo):

```
pnpm dev
```

3. Para rodar apenas o app `v4`:

```
cd apps/v4
pnpm dev
```

Backend (backend/)
1. Instale dependências de runtime:

```
cd backend
poetry install --only main --no-root --no-interaction --no-ansi
```

2. Entrar no ambiente virtual (opcional):

```
poetry shell
```

3. Executar comandos Python conforme o projeto (ex.: servidor ou scripts). Exemplo genérico:

```
poetry run python -m my_module
```

Observações
- O CI do repositório foi temporariamente desativado durante o desenvolvimento inicial.
- O app `ui/apps/v4` usa `fumadocs-mdx` no `postinstall`; se houver erros, verifique o `postinstall` em `ui/apps/v4/package.json`.

Problemas / contribuição
- Abra uma issue descrevendo passos para reproduzir e logs.
