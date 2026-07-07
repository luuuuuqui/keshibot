# Takeshi Bot

Bot privado de WhatsApp baseado em Baileys, com comandos modulares e persistência local em JSON.

Este repositório foi enxugado para uso próprio, principalmente no Termux. Ele não inclui `node_modules/`, sessões do WhatsApp, banco local, documentação pública de contribuição ou arquivos de publicação.

## Sumário

1. [Requisitos](#requisitos)
2. [Instalação no Termux](#instalação-no-termux)
3. [Primeira execução](#primeira-execução)
4. [Configuração](#configuração)
5. [Dados locais](#dados-locais)
6. [Comandos](#comandos)
7. [APIs externas](#apis-externas)
8. [Estrutura do projeto](#estrutura-do-projeto)
9. [Personalização](#personalização)
10. [Manutenção](#manutenção)
11. [Problemas comuns](#problemas-comuns)

## Requisitos

- Node.js `22.8.0` ou superior.
- npm.
- Git.
- FFmpeg.
- WhatsApp com acesso a "dispositivos conectados".

No Termux, prefira `nodejs-lts`.

## Instalação no Termux

Atualize o Termux e instale os pacotes:

```sh
pkg update -y
pkg upgrade -y
pkg install git nodejs-lts ffmpeg -y
```

Libere acesso ao armazenamento, se for usar uma pasta do celular:

```sh
termux-setup-storage
```

Escolha a pasta onde o bot vai ficar:

```sh
cd ~/storage/shared
```

Clone o repositório privado:

```sh
git clone <url-do-repositorio>
cd takeshibot
```

Instale as dependências:

```sh
npm install
```

## Primeira execução

Inicie o bot:

```sh
npm start
```

O bot vai pedir o número de telefone. Digite apenas números, com DDI e DDD.

Depois, abra o WhatsApp:

1. vá em "dispositivos conectados";
2. toque em "conectar dispositivo";
3. escolha a opção de conectar com número de telefone;
4. informe o código que apareceu no Termux.

Quando conectar, pare o bot com `CTRL + C`, revise `src/config.js` e rode novamente:

```sh
npm start
```

## Configuração

As opções principais ficam em `src/config.js`.

| Constante | Uso |
| --- | --- |
| `PREFIX` | prefixo padrão dos comandos |
| `BOT_EMOJI` | emoji usado em respostas e reações |
| `BOT_NAME` | nome exibido no menu |
| `BOT_LID` | LID do número do bot |
| `OWNER_LID` | LID do dono |
| `ONLY_GROUP_ID` | limita o bot a um grupo específico quando preenchido |
| `DEVELOPER_MODE` | aumenta logs de mensagens recebidas |
| `SPIDER_API_TOKEN` | token da Spider API |
| `LINKER_API_KEY` | chave usada pelo comando `gerar-link` |
| `OPENAI_API_KEY` | chave usada pelo comando `suporte` |

Para descobrir seu LID, use:

```text
/meu-lid
```

Para descobrir o ID do grupo, use:

```text
/get-group-id
```

Também é possível trocar o token da Spider API em runtime:

```text
/set-spider-api-token seu_token
```

## Dados locais

A pasta `database/` não entra no Git. Ela é criada automaticamente em runtime.

Arquivos criados conforme o uso:

- `database/config.json`: configurações mutáveis, como token salvo por comando.
- `database/prefix-groups.json`: prefixos por grupo.
- `database/auto-responder.json`: gatilhos e respostas automáticas.
- `database/auto-responder-groups.json`: grupos com auto-responder ativo.
- `database/auto-sticker-groups.json`: grupos com auto-sticker ativo.
- `database/group-restrictions.json`: restrições de mídia por grupo.
- `database/inactive-groups.json`: grupos onde o bot está desativado.
- `database/muted.json`: membros mutados por grupo.
- `database/only-admins.json`: grupos restritos a comandos de admins.
- `database/welcome-groups.json`: grupos com boas-vindas ativa.
- `database/exit-groups.json`: grupos com mensagem de saída ativa.
- `database/warns.json`: advertências.
- `database/afk-groups.json`: membros em modo ausente.

Não comite `database/`.

## Comandos

O menu do bot é gerado em `src/menu.js`.

### Dono

- `/exec`
- `/get-group-id`
- `/off`
- `/on`
- `/set-menu-image`
- `/set-prefix`
- `/set-spider-api-token`

### Administração

- `/abrir`
- `/add-auto-responder`
- `/agendar-mensagem`
- `/anti-audio 1|0`
- `/anti-call 1|0`
- `/anti-document 1|0`
- `/anti-event 1|0`
- `/anti-image 1|0`
- `/anti-link 1|0`
- `/anti-lottie-sticker 1|0`
- `/anti-payment 1|0`
- `/anti-product 1|0`
- `/anti-sticker 1|0`
- `/anti-status-grupo 1|0`
- `/anti-video 1|0`
- `/auto-responder 1|0`
- `/auto-sticker 1|0`
- `/ban`
- `/delete`
- `/delete-auto-responder`
- `/exit 1|0`
- `/fechar`
- `/hidetag`
- `/limpar-chat`
- `/link-grupo`
- `/list-auto-responder`
- `/mute`
- `/only-admin 1|0`
- `/promover`
- `/rebaixar`
- `/revelar`
- `/saldo`
- `/unmute`
- `/welcome 1|0`

### Membros

- `/attp`
- `/brat`
- `/bratvid`
- `/cep`
- `/fake-chat`
- `/gerar-link`
- `/info`
- `/meu-lid`
- `/menu`
- `/perfil`
- `/ping`
- `/rename`
- `/removebg`
- `/sticker`
- `/suporte`
- `/to-gif`
- `/to-image`
- `/to-mp3`
- `/ttp`
- `/yt-search`

### Downloads

- `/facebook`
- `/instagram`
- `/play-audio`
- `/play-video`
- `/pinterest`
- `/tik-tok`
- `/tik-tok-audio`
- `/yt-mp3`
- `/yt-mp4`

### Brincadeiras

- `/abracar`
- `/beijar`
- `/dado`
- `/jantar`
- `/lutar`
- `/matar`
- `/socar`
- `/tapa`

### IA

- `/deepseek`
- `/flux`
- `/gemini`
- `/gpt-5-mini`
- `/ia-sticker`

### Canvas

- `/blur`
- `/bolsonaro`
- `/cadeia`
- `/contraste`
- `/espelhar`
- `/gray`
- `/inverter`
- `/pixel`
- `/rip`

## APIs externas

Alguns comandos dependem de API externa.

### Spider API

Usada por comandos de downloads, IA, stickers de texto, saldo e alguns recursos de imagem.

Configure em `src/config.js`:

```js
export const SPIDER_API_TOKEN = "seu_token_aqui";
```

Ou via comando:

```text
/set-spider-api-token seu_token
```

### Linker

Usada pelo comando `gerar-link`.

```js
export const LINKER_BASE_URL = "https://linker.devgui.dev/api";
export const LINKER_API_KEY = "seu_token_aqui";
```

### OpenAI

Usada pelo comando `suporte`.

```js
export const OPENAI_API_KEY = "sua_chave";
```

Se `OPENAI_API_KEY` estiver vazia, o comando `suporte` responde que o suporte inteligente não está disponível.

## Estrutura do projeto

```text
assets/
  auth/              estado de autenticação do WhatsApp
  images/            imagens usadas pelo bot
  stickers/          stickers locais
  temp/              arquivos temporários
src/
  @types/            tipos e documentação dos helpers
  commands/
    admin/           comandos administrativos
    member/          comandos de membros
    owner/           comandos do dono
  errors/            classes de erro usadas pelo fluxo de comandos
  middlewares/       pipeline de mensagens, grupos e chamadas
  services/          integrações e processamento de mídia
  utils/             helpers e persistência
  config.js          configuração principal
  connection.js      conexão do Baileys
  index.js           entrada do bot
  loader.js          registro dos eventos
  menu.js            texto do menu
  messages.js        mensagens de boas-vindas e saída
```

Arquivos ignorados:

- `node_modules/`
- `database/`
- `assets/auth/baileys/`
- `assets/temp/`
- `.vscode/`

## Personalização

### Menu

Edite:

```text
src/menu.js
```

### Mensagens de entrada e saída

Edite:

```text
src/messages.js
```

### Imagem do menu

Troque o arquivo:

```text
assets/images/takeshi-bot.png
```

Ou use o comando:

```text
/set-menu-image
```

respondendo a uma imagem.

### Novos comandos

Crie arquivos em uma das pastas:

- `src/commands/owner/`
- `src/commands/admin/`
- `src/commands/member/`

Modelo básico:

```js
import { PREFIX } from "../../config.js";
import { InvalidParameterError } from "../../errors/index.js";

export default {
  name: "comando",
  description: "descrição curta",
  commands: ["comando", "alias"],
  usage: `${PREFIX}comando <argumento>`,
  handle: async ({ args, sendReply }) => {
    if (!args[0]) {
      throw new InvalidParameterError("informe um argumento.");
    }

    await sendReply("ok");
  },
};
```

Use os helpers recebidos no `handle()` antes de criar lógica de baixo nível.

### Middleware customizado

Use:

```text
src/middlewares/customMiddleware.js
```

Esse é o ponto mais seguro para adicionar regras globais sem mexer no fluxo principal.

## Manutenção

Instalar dependências:

```sh
npm install
```

Rodar o bot:

```sh
npm start
```

Resetar sessão do WhatsApp:

```sh
bash reset-qr-auth.sh
```

Verificar arquivos versionados:

```sh
git status --short
```

Subir mudanças:

```sh
git add -A
git commit -m "mensagem em português"
git push
```

## Problemas comuns

### O bot não reconhece configuração nova

Confira se você está rodando a mesma pasta que editou.

No Termux, é comum ter uma cópia em `/sdcard`, outra em `~/storage/shared` ou outra em `Download`.

### Erro de conexão ou sessão corrompida

Rode:

```sh
bash reset-qr-auth.sh
```

Depois remova o dispositivo conectado no WhatsApp e faça o pareamento novamente.

### `permission denied` ao acessar armazenamento

Rode:

```sh
termux-setup-storage
```

Aceite a permissão no Android e tente novamente.

### `ffmpeg` não encontrado

Instale:

```sh
pkg install ffmpeg -y
```

### Dependências ausentes

Rode:

```sh
npm install
```

### Comando não encontrado

Confira:

- se o arquivo está em `src/commands/admin/`, `src/commands/member/` ou `src/commands/owner/`;
- se o export default tem `commands: [...]`;
- se o nome digitado no WhatsApp está dentro de `commands`;
- se o prefixo do grupo está correto.

## Segurança

Não compartilhe nem comite:

- tokens de API;
- arquivos de `database/`;
- arquivos de `assets/auth/baileys/`;
- logs com dados sensíveis;
- prints com código de pareamento.

Este é um repositório privado. Mantenha a configuração real fora do histórico do Git sempre que possível.

## Licença

Este projeto usa uma licença privada. Consulte `LICENSE`.
