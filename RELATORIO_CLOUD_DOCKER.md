# Relatorio tecnico - Aplicacao containerizada em nuvem

**Nome completo do aluno:** Leo Queiroz de Lima  
**Projeto:** PrimeShop - vitrine web com area administrativa simulada  
**Entrega:** Atividade final obrigatoria - Docker e modelos de servico em nuvem

## 1. Apresentacao do projeto

Este projeto simula a entrega de uma aplicacao web simples para um cliente que precisa de uma solucao segura, escalavel, hospedada em nuvem e baseada em containers. A aplicacao escolhida foi a **PrimeShop**, uma loja demonstrativa criada em Vue 3, com vitrine de produtos, carrinho, checkout protegido por login simulado e area administrativa restrita ao perfil de administrador.

A escolha dessa aplicacao torna a simulacao mais proxima de um caso real: o cliente nao receberia apenas uma pagina estatica, mas um pequeno sistema web com rotas, separacao entre area publica e area interna, build de producao e publicacao em servidor web Nginx dentro de um container Docker.

## 2. Modelo de servico escolhido

O modelo escolhido foi **PaaS (Platform as a Service)**, usando como referencia uma plataforma como **Azure App Service for Containers**, **AWS Elastic Beanstalk com Docker** ou **Google Cloud Run**.

Esse modelo foi escolhido porque reduz a responsabilidade operacional da equipe. Em vez de administrar manualmente servidores, sistema operacional, patches, balanceador de carga e parte da infraestrutura, a equipe entrega uma imagem Docker pronta e a plataforma cuida de boa parte da execucao. Assim, o foco fica no codigo da aplicacao, na configuracao do container e nas regras de seguranca.

Mesmo assim, a solucao tambem poderia ser implantada em IaaS, por exemplo em uma VM EC2 da AWS. Nesse caso, haveria mais controle, mas tambem mais manutencao. Para este projeto, o PaaS oferece um equilibrio melhor entre simplicidade, escalabilidade e seguranca.

## 3. Componentes utilizados

- **Vue 3 e Vite:** desenvolvimento e empacotamento da interface web.
- **PrimeVue e Tailwind CSS:** componentes visuais, layout e responsividade.
- **Docker:** empacotamento da aplicacao em container.
- **Node.js 20 Alpine:** imagem oficial usada na etapa de build.
- **Nginx Alpine:** imagem oficial usada para servir os arquivos estaticos em producao.
- **Docker Compose:** simulacao local de porta, rede e volumes.
- **Rede Docker `primeshop-net`:** isolamento logico do container.
- **Volumes `primeshop-nginx-cache` e `primeshop-nginx-logs`:** persistencia simulada de cache e logs do servidor.

## 4. Preparacao do ambiente com Docker

Foi criado um **Dockerfile multi-stage**. Na primeira etapa, a imagem oficial `node:20-alpine` instala as dependencias e executa o build da aplicacao. Na segunda etapa, a imagem oficial `nginx:1.27-alpine` recebe apenas os arquivos finais da pasta `dist`, deixando a imagem final mais leve e adequada para producao.

A aplicacao e servida internamente na porta **80** do container. No ambiente local, o Docker Compose publica essa porta como **8080**, permitindo acesso em:

```text
http://localhost:8080
```

A rede `primeshop-net` simula o isolamento da aplicacao dentro de uma arquitetura maior, onde futuramente poderiam existir outros servicos, como API, banco de dados ou observabilidade. Os volumes persistentes simulam a manutencao de cache e logs do Nginx mesmo se o container for recriado.

## 5. Diagrama simplificado da arquitetura

```text
Usuario
  |
  | HTTPS
  v
Plataforma PaaS em nuvem
  |
  | executa imagem Docker
  v
Container PrimeShop
  |
  | Nginx - porta 80
  v
Arquivos estaticos Vue/Vite
  |
  +-- Volume de logs
  +-- Volume de cache
  +-- Rede Docker isolada
```

## 6. Simulacao de deploy

A estrategia de entrega proposta e **automatizada com CI/CD**. Em um fluxo real, cada alteracao enviada para o repositorio GitHub poderia iniciar um pipeline com as seguintes etapas:

1. Instalar dependencias com `npm ci`.
2. Executar testes ou verificacoes do projeto.
3. Gerar o build com `npm run build`.
4. Construir a imagem Docker.
5. Publicar a imagem em um registry, como Docker Hub, Amazon ECR, Azure Container Registry ou Google Artifact Registry.
6. Atualizar o servico na plataforma PaaS.

Em uma implantacao na **Azure App Service for Containers**, por exemplo, a plataforma buscaria a imagem no registry e executaria o container. O servico poderia ser configurado com HTTPS, variaveis de ambiente, logs, monitoramento e aumento de instancias conforme a demanda.

Para uma entrega mais controlada, tambem seria possivel usar deploy escalonado: primeiro publicar em ambiente de homologacao, validar a aplicacao e depois promover a mesma imagem para producao. Isso reduz risco, porque a imagem testada e exatamente a mesma imagem entregue ao cliente.

## 7. Escalabilidade

A escalabilidade aparece na possibilidade de executar mais de uma instancia do mesmo container. Como a aplicacao web e estatica e nao guarda estado de usuario dentro do container, ela pode ser replicada com facilidade atras de um balanceador de carga.

Em uma plataforma de nuvem, se muitos usuarios acessarem a PrimeShop ao mesmo tempo, novas instancias podem ser adicionadas para dividir as requisicoes. O container continua igual; o que muda e a quantidade de copias rodando.

## 8. Elasticidade

Elasticidade e a capacidade de aumentar ou reduzir recursos conforme a necessidade. Neste projeto, a elasticidade poderia ser configurada por metricas como uso de CPU, memoria ou numero de requisicoes.

Em horarios de pico, a plataforma subiria mais instancias do container. Quando o movimento diminuisse, reduziria a quantidade de instancias para economizar recursos. Isso evita pagar por capacidade ociosa e mantem a aplicacao disponivel quando a demanda cresce.

## 9. Seguranca e responsabilidade compartilhada

Na nuvem, a seguranca e dividida entre provedor e cliente. O provedor fica responsavel por datacenters, energia, rede fisica, infraestrutura base e parte da plataforma gerenciada. A equipe do projeto fica responsavel pela imagem Docker, codigo da aplicacao, configuracoes de acesso, variaveis sensiveis, permissoes e boas praticas de publicacao.

Neste projeto, algumas medidas foram consideradas:

- Uso de imagens oficiais e pequenas, reduzindo superficie de ataque.
- Separacao entre etapa de build e etapa de execucao.
- Publicacao apenas da porta necessaria.
- Healthcheck no container para facilitar monitoramento.
- Logs persistidos para auditoria e diagnostico.
- Controle de acesso simulado na aplicacao, com checkout protegido e area administrativa restrita.

## 10. Beneficios e desafios da solucao

Os principais beneficios sao portabilidade, padronizacao do ambiente, facilidade de escalar e menor diferenca entre desenvolvimento e producao. Com Docker, a aplicacao passa a ser entregue como uma unidade previsivel, facilitando a implantacao em diferentes provedores.

Os desafios estao na necessidade de manter imagens atualizadas, configurar bem o pipeline, proteger credenciais, acompanhar logs e definir limites de recursos. Tambem e importante lembrar que containerizar nao torna uma aplicacao automaticamente segura; a seguranca depende de configuracao, atualizacao e monitoramento continuo.

## 11. Como executar localmente

Com Docker instalado, executar:

```bash
docker compose up --build
```

Depois acessar:

```text
http://localhost:8080
```

Para parar a aplicacao:

```bash
docker compose down
```

## 12. Conclusao

A solucao proposta atende aos requisitos da atividade porque apresenta uma aplicacao real empacotada com Docker, usando imagens oficiais, porta de acesso, rede isolada, volumes persistentes e estrategia de deploy em nuvem. O modelo PaaS foi escolhido por oferecer boa escalabilidade com menor carga operacional.

Com essa arquitetura, a PrimeShop poderia sair do ambiente local e ser publicada em uma plataforma de nuvem com um processo organizado, seguro e facil de evoluir. A atividade tambem demonstra, de forma pratica, os conceitos de escalabilidade, elasticidade e responsabilidade compartilhada, que sao essenciais em projetos modernos de computacao em nuvem.
