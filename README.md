# takeshi bot

bot de whatsapp baseado em baileys, com comandos modulares e persistência local em json.

este repositório foi enxugado para uso próprio, principalmente no termux. ele não inclui `node_modules/`, sessões do whatsapp, banco local, documentação pública de contribuição ou arquivos de publicação.

## sumário

1. [requisitos](#requisitos)
2. [instalação no termux](#instalação-no-termux)
3. [primeira execução](#primeira-execução)
4. [configuração](#configuração)
5. [dados locais](#dados-locais)
6. [comandos](#comandos)
7. [apis externas](#apis-externas)
8. [estrutura do projeto](#estrutura-do-projeto)
9. [personalização](#personalização)
10. [manutenção](#manutenção)
11. [problemas comuns](#problemas-comuns)

## requisitos

- node.js `22.8.0` ou superior.
- npm.
- git.
- ffmpeg.
- whatsapp com acesso a "dispositivos conectados".

no termux, prefira `nodejs-lts`.

## instalação no termux

atualize o termux e instale os pacotes:

```sh
pkg update -y
pkg upgrade -y
pkg install git nodejs-lts ffmpeg -y
```

libere acesso ao armazenamento, se for usar uma pasta do celular:

```sh
termux-setup-storage
```

escolha a pasta onde o bot vai ficar:

```sh
cd ~/storage/shared/
```

clone o repositório:

```sh
git clone <url-do-repositorio>
cd takeshibot
```

instale as dependências:

```sh
npm install
```

## primeira execução

inicie o bot:

```sh
npm start
```

o bot vai pedir o número de telefone. digite apenas números, com ddi e ddd.

depois, abra o whatsapp:

1. vá em "dispositivos conectados";
2. toque em "conectar dispositivo";
3. escolha a opção de conectar com número de telefone;
4. informe o código que apareceu no termux.

quando conectar, pare o bot com `Ctrl + C`, revise `src/config.js` e rode novamente:

```sh
npm start
```

## configuração

as opções principais ficam em `src/config.js`.

| constante | uso |
| --- | --- |
| `PREFIX` | prefixo padrão dos comandos |
| `BOT_EMOJI` | emoji usado em respostas e reações |
| `BOT_NAME` | nome exibido no menu |
| `BOT_LID` | lid do número do bot |
| `OWNER_LID` | lid do dono |
| `ONLY_GROUP_ID` | limita o bot a um grupo específico quando preenchido |
| `DEVELOPER_MODE` | aumenta logs de mensagens recebidas |
| `SPIDER_API_TOKEN` | token da spider api |
| `LINKER_API_KEY` | chave usada pelo comando `gerar-link` |
| `OPENAI_API_KEY` | chave usada pelo comando `suporte` |

para descobrir seu lid, use:

```text
/meu-lid
```

para descobrir o id do grupo, use:

```text
/get-group-id
```

também é possível trocar o token da spider api em runtime:

```text
/set-spider-api-token seu_token
```

## dados locais

a pasta `database/` não entra no git. ela é criada automaticamente em runtime.

arquivos criados conforme o uso:

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

não comite `database/`.

## comandos

o menu do bot é gerado em `src/menu.js`.

### dono

- `/exec`
- `/get-group-id`
- `/off`
- `/on`
- `/set-menu-image`
- `/set-prefix`
- `/set-spider-api-token`

### administração

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

### membros

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

### downloads

- `/facebook`
- `/instagram`
- `/play-audio`
- `/play-video`
- `/pinterest`
- `/tik-tok`
- `/tik-tok-audio`
- `/yt-mp3`
- `/yt-mp4`

### brincadeiras

- `/abracar`
- `/beijar`
- `/dado`
- `/jantar`
- `/lutar`
- `/matar`
- `/socar`
- `/tapa`

### ia

- `/deepseek`
- `/flux`
- `/gemini`
- `/gpt-5-mini`
- `/ia-sticker`

### canvas

- `/blur`
- `/bolsonaro`
- `/cadeia`
- `/contraste`
- `/espelhar`
- `/gray`
- `/inverter`
- `/pixel`
- `/rip`

## apis externas

alguns comandos dependem de api externa.

### spider api

usada por comandos de downloads, ia, stickers de texto, saldo e alguns recursos de imagem.

configure em `src/config.js`:

```js
export const SPIDER_API_TOKEN = "seu_token_aqui";
```

ou via comando:

```text
/set-spider-api-token seu_token
```

### linker

usada pelo comando `/gerar-link`.

```js
export const LINKER_BASE_URL = "https://linker.devgui.dev/api";
export const LINKER_API_KEY = "seu_token_aqui";
```

### openai

usada pelo comando `/suporte`.

```js
export const OPENAI_API_KEY = "sua_chave";
```

se `OPENAI_API_KEY` estiver vazia, o comando `/suporte` responde que o suporte inteligente não está disponível.

## estrutura do projeto

```text
assets/
  auth/              estado de autenticação do whatsapp
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
  connection.js      conexão do baileys
  index.js           entrada do bot
  loader.js          registro dos eventos
  menu.js            texto do menu
  messages.js        mensagens de boas-vindas e saída
```

arquivos ignorados:

- `node_modules/`
- `database/`
- `assets/auth/baileys/`
- `assets/temp/`
- `.vscode/`

## personalização

### menu

edite `src/menu.js`.

### mensagens de entrada e saída

edite `src/messages.js`.

### imagem do menu

troque o arquivo `assets/images/takeshi-bot.png` ou use o comando `/set-menu-image` respondendo a uma imagem.

### novos comandos

crie arquivos em uma das pastas:

- `src/commands/owner/`
- `src/commands/admin/`
- `src/commands/member/`

modelo básico:

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

use os helpers recebidos no `handle()` antes de criar lógica de baixo nível.

### middleware customizado

use `src/middlewares/customMiddleware.js`.

esse é o ponto mais seguro para adicionar regras globais sem mexer no fluxo principal.

## manutenção

instalar dependências:

```sh
npm install
```

rodar o bot:

```sh
npm start
```

resetar sessão do whatsapp:

```sh
bash reset-qr-auth.sh
```

verificar arquivos versionados:

```sh
git status --short
```

subir mudanças:

```sh
git add -A
git commit -m "mensagem em português"
git push
```

## problemas comuns

### o bot não reconhece configuração nova

confira se você está rodando a mesma pasta que editou.

no termux, é comum ter uma cópia em `/sdcard/`, outra em `~/storage/shared/` ou outra em `Downloads/`.

### erro de conexão ou sessão corrompida

rode:

```sh
bash reset-qr-auth.sh
```

depois remova o dispositivo conectado no whatsapp e faça o pareamento novamente.

### `permission denied` ao acessar armazenamento

rode:

```sh
termux-setup-storage
```

aceite a permissão no android e tente novamente.

### `ffmpeg` não encontrado

instale:

```sh
pkg install ffmpeg -y
```

### dependências ausentes

rode:

```sh
npm install
```

### comando não encontrado

confira:

- se o arquivo está em `src/commands/admin/`, `src/commands/member/` ou `src/commands/owner/`;
- se o export default tem `commands: [...]`;
- se o nome digitado no whatsapp está dentro de `commands`;
- se o prefixo do grupo está correto.

## segurança

não compartilhe nem comite:

- tokens de api;
- arquivos de `database/`;
- arquivos de `assets/auth/baileys/`;
- logs com dados sensíveis;
- prints com código de pareamento.

mantenha as configurações locais e sensíveis fora do histórico do git sempre que possível.

## licença

este projeto é licenciado sob a gnu general public license (gpl). consulte o arquivo `LICENSE` para mais detalhes.
