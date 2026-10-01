# Textos prontos para o LinkedIn e passo a passo para o GitHub

## 1. Como subir cada projeto no GitHub

Faça isto para **cada pasta** (`gerenciador-tarefas-c` e `servidor-http-c`):

1. No GitHub, clique em **New repository**, use o mesmo nome da pasta, deixe **público** e **não** marque "Add a README" (o projeto já tem).
2. No terminal, dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Versão inicial"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
git push -u origin main
```

3. Antes do push, troque nos arquivos:
   - `README.md`: `SEU-USUARIO`, `Seu Nome` e `SEU-PERFIL`
   - `LICENSE`: `Seu Nome`
4. No repositório, em **About** (engrenagem à direita), adicione uma descrição curta e os tópicos:
   `c`, `c11`, `linux`, `makefile`, `valgrind` (+ `http-server`, `sockets` no servidor / `cli` no gerenciador).
5. Depois do push, confira a aba **Actions**: o CI vai compilar e rodar os testes sozinho. ✅ verde no repositório passa uma ótima impressão.
6. No seu perfil do GitHub, **fixe** (Pin) os dois repositórios.

---

## 2. LinkedIn: seção "Projetos"

Perfil → **Adicionar seção** → **Recomendado** → **Adicionar projetos**.

### Projeto 1

**Nome:** Gerenciador de Tarefas em C (CLI)

**Descrição:**
> Aplicação de linha de comando em C11 para gerenciar tarefas com prioridade, status e persistência em arquivo.
>
> • Estrutura de dados própria (vetor dinâmico com realloc) e código organizado em módulos
> • Persistência com gravação atômica, evitando perda de dados em falhas
> • Validação completa de entradas do usuário e do arquivo
> • 12 testes unitários, zero vazamentos de memória (Valgrind) e build com AddressSanitizer
> • CI com GitHub Actions a cada push
>
> Tecnologias: C, Make, Valgrind, GCC, Git, GitHub Actions

**Competências:** Linguagem C · Estruturas de dados · Gerenciamento de memória · Testes de software · Git

**Link:** URL do repositório no GitHub

### Projeto 2

**Nome:** Servidor HTTP em C

**Descrição:**
> Servidor web de arquivos estáticos construído do zero em C, usando apenas a API de sockets POSIX.
>
> • Implementação do parsing de requisições HTTP/1.1 (GET e HEAD) e respostas com os códigos corretos (200, 301, 400, 403, 404, 405…)
> • Detecção de Content-Type, redirecionamento de diretórios e log de acessos
> • Proteção contra path traversal (inclusive codificado) e fuga por symlink
> • Encerramento limpo via sinais (SIGINT/SIGTERM) e timeout para clientes lentos
> • Testes unitários + testes de integração com requisições reais, Valgrind e CI no GitHub Actions
>
> Tecnologias: C, Sockets POSIX, HTTP, Linux, Make, Valgrind, Bash, GitHub Actions

**Competências:** Linguagem C · Redes de computadores · Protocolo HTTP · Linux · Segurança da informação

**Link:** URL do repositório no GitHub

---

## 3. Post opcional para divulgar

> Nas últimas semanas estive aprofundando meus estudos em C e publiquei dois projetos no GitHub 🚀
>
> 🌐 **Servidor HTTP em C**: um servidor web escrito do zero com sockets POSIX. Entendi na prática o que acontece quando o navegador acessa um site: conexão TCP, parsing do protocolo HTTP, envio de arquivos e cuidados de segurança como bloqueio de path traversal.
>
> 📝 **Gerenciador de Tarefas (CLI)**: aplicação de terminal com vetor dinâmico, persistência em arquivo e gravação atômica.
>
> Nos dois, busquei ir além do "funciona": testes automatizados, checagem de memória com Valgrind, compilação sem nenhum warning e CI com GitHub Actions.
>
> Os links estão nos comentários. Feedbacks são muito bem-vindos! 🙌
>
> #linguagemC #programacao #desenvolvimento #linux #github #desenvolvedorjunior

**Dica:** coloque os links dos repositórios no primeiro comentário, não no texto do post; o LinkedIn tende a entregar menos posts com links externos.

---

## 4. Prepare-se para a entrevista

Recrutadores técnicos costumam perguntar sobre os projetos. Garanta que você sabe explicar:

- Por que usar `realloc` dobrando a capacidade, e não aumentando de 1 em 1?
- O que é *path traversal* e como o servidor impede?
- Por que `send()` precisa de um laço (`send_all`)?
- O que o Valgrind e o AddressSanitizer detectam?
- Qual a limitação do servidor atender uma conexão por vez, e como você resolveria?

Ler o código com calma e conseguir responder isso é o que transforma o projeto de portfólio em ponto a favor na entrevista.
