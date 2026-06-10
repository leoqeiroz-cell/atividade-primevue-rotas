# PrimeShop - Aplicacao containerizada com Docker

Projeto desenvolvido para a atividade final de Provimento de Servicos
Computacionais. A proposta simula a criacao e implantacao de uma aplicacao web
containerizada com Docker, relacionando a entrega aos conceitos de computacao em
nuvem, PaaS, escalabilidade, elasticidade e responsabilidade compartilhada.

A aplicacao usada na simulacao e a **PrimeShop**, uma vitrine web criada com Vue
3, PrimeVue, Tailwind CSS, Vue Router, Pinia e Vuelidate.

Nome sugerido para o repositorio: `psc-docker-cloud-primeshop`.
Nome sugerido para esta etapa: `atividade-05-vuelidate-pinia-primeshop`.

## O que o projeto demonstra

- Dockerfile funcional com imagens oficiais `node:20-alpine` e `nginx:1.27-alpine`.
- Aplicacao servida em container com Nginx.
- Simulacao de porta de acesso, rede Docker e volumes persistentes.
- Estrategia de deploy em nuvem usando modelo PaaS.
- Relatorio tecnico com arquitetura, beneficios, desafios e conceitos de nuvem.

## Funcionalidades da aplicacao

- Rotas publicas de consumidor: vitrine, detalhes do produto e checkout.
- Layouts separados para consumidor e admin.
- Autenticacao centralizada em uma `authStore` com Pinia, contendo usuario, token,
  estado autenticado e actions simuladas de login, registro e logout.
- Formulario de login e criacao de conta com PrimeVue, Tailwind CSS, Vuelidate,
  feedback por campo, loading nos botoes e mensagens Toast.
- Guards com `beforeEach` para checkout autenticado e area admin restrita ao papel `ADMIN`.
- Admin com rotas filhas, menu lateral, breadcrumbs dinamicos, DataTable de produtos e relatorios.

## Como executar em desenvolvimento

```bash
npm install
npm run dev
```

Credenciais de teste:

```text
Cliente: cliente@primeshop.com / 123456
Admin: admin@primeshop.com / admin123
```

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

## Arquivos principais da entrega

- `Dockerfile`: build da aplicacao Vue e publicacao com Nginx.
- `docker-compose.yml`: simulacao de porta, rede e volumes persistentes.
- `nginx.conf`: configuracao do servidor web para a SPA.
- `src/store/auth.js`: store Pinia de autenticacao.
- `src/views/LoginView.vue`: formularios de login e registro com Vuelidate.
- `RELATORIO_ATIVIDADE05_AUTH_PINIA_VUELIDATE.md`: relatorio tecnico da Atividade 05.
- `RELATORIO_CLOUD_DOCKER.md`: relatorio tecnico da atividade.
