# Atividade PrimeVue Rotas

Aplicacao Vue 3 com PrimeVue, Tailwind e Vue Router demonstrando:

- Rotas publicas de consumidor: vitrine, detalhes do produto e checkout.
- Layouts separados para consumidor e admin.
- Guards com `beforeEach` para checkout autenticado e area admin restrita ao papel `ADMIN`.
- Admin com rotas filhas, menu lateral, breadcrumbs dinamicos, DataTable de produtos e relatorios.

## Como executar

```bash
npm install
npm run dev
```

Use os botoes da tela de login para simular um usuario consumidor ou admin.

## Como executar com Docker

Esta versao tambem simula a entrega da aplicacao em container, usando Docker,
Docker Compose e Nginx.

```bash
docker compose up --build
```

Depois acesse:

```text
http://localhost:8080
```

Para parar a aplicacao:

```bash
docker compose down
```

O arquivo `docker-compose.yml` publica a porta `8080:80`, cria a rede
`primeshop-net` e configura volumes persistentes para cache e logs do Nginx.
