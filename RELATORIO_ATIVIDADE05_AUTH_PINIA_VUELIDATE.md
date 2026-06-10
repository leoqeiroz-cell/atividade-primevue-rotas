# Relatorio Tecnico - Atividade 05: Autenticacao Segura com Pinia, Vuelidate e PrimeVue

## 1. Identificacao da entrega

**Projeto:** PrimeShop - Atividade 05  
**Tema:** Autenticacao segura, gerenciamento de estado e validacao reativa  
**Tecnologias principais:** Vue 3, Vue Router, Pinia, Vuelidate, PrimeVue e Tailwind CSS  
**Nome recomendado para publicacao:** `atividade-05-vuelidate-pinia-primeshop`

## 2. Objetivo

Esta atividade teve como objetivo evoluir a aplicacao PrimeShop com um fluxo de
autenticacao mais organizado e profissional. A implementacao substitui estados
locais ou soltos por uma store centralizada, aplica validacao reativa antes das
submissoes e integra a experiencia de login, cadastro, logout e protecao de
rotas com a navegacao da aplicacao.

## 3. Gerenciamento de estado com Pinia

A autenticacao foi centralizada em `src/store/auth.js`, usando Pinia como fonte
unica da verdade. A store controla:

- `user`: dados publicos do usuario autenticado.
- `token`: token simulado para representar a sessao ativa.
- `isAuthenticated`: getter que deriva o status autenticado a partir de `user`
  e `token`.
- `isLoading`: estado usado pelos botoes de submissao enquanto as actions
  simulam processamento assincrono.
- `registeredUsers`: lista em memoria para permitir cadastro e login posterior
  durante a sessao.

As actions implementadas foram:

- `login(credentials)`: valida credenciais simuladas, cria sessao e retorna o
  usuario autenticado.
- `register(account)`: valida duplicidade de e-mail, registra um usuario cliente
  e inicia a sessao automaticamente.
- `logout()`: limpa usuario e token.

Com isso, componentes como `AppHeader`, `AdminLayout`, `CheckoutView` e os
guards de rota passam a consumir os dados da mesma store, garantindo
consistencia entre interface, navegacao e regra de acesso.

## 4. Interface com PrimeVue e Tailwind CSS

A tela `src/views/LoginView.vue` foi reconstruida com componentes PrimeVue:

- `Card` como conteiner central.
- `InputText` para nome e e-mail.
- `Password` com `toggleMask` para senha e confirmacao.
- `Button` com `loading` durante as actions.
- `Toast` para feedback de sucesso e erro.

O layout usa Tailwind CSS para espacamento, responsividade, textos auxiliares,
bordas de erro e organizacao visual. A tela possui alternancia entre Login e
Criar conta, permitindo duas visualizacoes distintas dentro da mesma rota.

## 5. Validacao com Vuelidate

O Vuelidate foi aplicado antes de qualquer chamada as actions da store.

No login, as regras implementadas foram:

- E-mail obrigatorio.
- Formato de e-mail valido.
- Senha obrigatoria.

No cadastro, as regras implementadas foram:

- Nome obrigatorio.
- E-mail obrigatorio e em formato valido.
- Senha obrigatoria com minimo de 6 caracteres.
- Confirmacao de senha obrigatoria e coincidente com a senha principal.

Quando um campo falha, a interface exibe mensagem logo abaixo do input em texto
vermelho, como "Informe um e-mail valido", "A senha deve ter no minimo 6
caracteres" e "As senhas nao coincidem". O envio tambem e bloqueado enquanto o
formulario estiver invalido.

## 6. Experiencia do usuario e feedback

A experiencia foi aprimorada com:

- Mensagens Toast de sucesso para login e cadastro.
- Mensagens Toast de erro para credenciais invalidas, e-mail duplicado ou
  formulario incompleto.
- Loading visual nos botoes enquanto a action assincrona esta em andamento.
- Redirecionamento automatico apos login para a rota de origem, como Checkout,
  quando o usuario foi enviado ao login por um guard.
- Logout com limpeza de sessao e retorno para a tela de Login.

## 7. Integracao com Vue Router

Os guards continuam protegendo as rotas com `meta.requiresAuth` e
`meta.requiresRole`. O checkout exige autenticacao e a area administrativa exige
papel `ADMIN`. Quando um visitante tenta acessar uma rota protegida, ele e
redirecionado para Login com a query `redirect`, preservando o destino original.

Fluxos validados:

- Visitante acessa `/checkout`: e enviado para `/login?redirect=/checkout`.
- Cliente autenticado acessa checkout: rota liberada.
- Cliente comum acessa admin: retorno para Home.
- Admin autenticado acessa admin: rota liberada.
- Logout: usuario e token sao removidos e a aplicacao volta para Login.

## 8. Credenciais de demonstracao

```text
Cliente: cliente@primeshop.com / 123456
Admin: admin@primeshop.com / admin123
```

Usuarios cadastrados pela tela de registro sao mantidos em memoria durante a
sessao do navegador e recebem papel `CUSTOMER`.

## 9. Criterios de entrega atendidos

- Estado centralizado em Pinia como unica fonte da verdade.
- Validacao reativa com Vuelidate antes das actions.
- Erros claros por campo com destaque visual.
- Uso coeso de PrimeVue e Tailwind CSS.
- Feedback visual com Toast e loading.
- Integracao com Vue Router e guards.
- Redirecionamento apos login e limpeza de estado no logout.

## 10. Conclusao

A entrega cumpre a proposta da Atividade 05 ao aplicar boas praticas de
organizacao de estado, validacao de formulario e experiencia de usuario em uma
SPA Vue. A separacao entre store, view e guards torna a solucao mais
manutenivel, testavel e adequada para evolucoes futuras, como persistencia real
de token, integracao com API e politicas de autorizacao mais granulares.
