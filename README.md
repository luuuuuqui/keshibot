# keshi bot

[![versão do bot (v8.10.0)](https://img.shields.io/badge/versão-8.10.0-blue)](https://github.com/luuuuuqui/keshibot)
[![node (>=v22.8.0)](https://img.shields.io/badge/node.js-%3E%3D22.8.0-green)](https://nodejs.org)
[![licença (GPL-3.0)](https://img.shields.io/badge/licença-GPL--3.0-orange)](LICENSE)

> [!WARNING]
> o projeto possui algumas funcionalidades dependentes de APIs externas.

fork enxuto do [takeshi-bot](https://github.com/guiireal/takeshi-bot), de [guiireal](https://github.com/guiireal), adaptado pra uso próprio via whatsapp/baileys.

bot de whatsapp com comandos modulares, persistência local em json e suporte a mídia. roda no termux, pc ou qualquer lugar com node.js e ffmpeg.

## o que faz

- **administração de grupo**: ban, mute, anti-link, anti-mídia, boas-vindas, etc.
- **downloads**: youtube, tiktok, instagram, facebook, pinterest.
- **stickers e canvas**: cria stickers, aplica filtros de imagem, attp, ttp, brat.
- **auto-responder e auto-sticker**: respostas automáticas por gatilho e conversão automática de imagens em sticker.
- **utilitários**: busca de cep, busca no youtube, gerador de link, perfil, ping.
- **suporte com ia**: integração com openai para respostas inteligentes.

## sumário

1. [requisitos](#requisitos)
2. [instalação](#instalação)
3. [primeira execução](#primeira-execução)
4. [configuração](#configuração)
5. [dados locais](#dados-locais)
6. [comandos](#comandos)
7. [apis externas](#apis-externas)
8. [estrutura do projeto](#estrutura-do-projeto)
9. [personalização](#personalização)
10. [desenvolvimento](#desenvolvimento)
11. [atualização](#atualização)
12. [problemas comuns](#problemas-comuns)
13. [segurança](#segurança)
14. [licença](#licença)

## requisitos

- node.js `22.8.0` ou superior.
- npm.
- git.
- ffmpeg.
- whatsapp com acesso a "dispositivos conectados".

no termux, prefira `nodejs-lts`.

## instalação

### instalação das ferramentas do sistema

#### termux (android)

```sh
pkg update -y && pkg upgrade -y
pkg install git nodejs-lts ffmpeg -y
```

libere acesso ao armazenamento, se for usar uma pasta do celular:

```sh
termux-setup-storage
```

#### ubuntu / debian

```sh
sudo apt update
sudo apt install -y nodejs npm git ffmpeg
```

#### windows

1. instale o node.js em <https://nodejs.org/pt-br/download>.
2. instale o git em <https://git-scm.com/install/windows>.
3. instale o ffmpeg em <https://ffmpeg.org/download.html>.
4. adicione `node`, `npm`, `git` e `ffmpeg` ao `PATH` durante a instalação ou nas configurações de sistema.

#### verificação

```sh
node -v
npm -v
git --version
ffmpeg -version
```

### baixar o projeto

antes de clonar, entre na pasta onde quer que o bot fique:

```sh
# termux
cd ~/storage/shared/

# linux / windows
mkdir -p ~/projetos
cd ~/projetos
```

clone o repositório pelo git:

```sh
git clone https://github.com/luuuuuqui/keshibot.git
```

ou pelo github cli:

```sh
gh repo clone luuuuuqui/keshibot
```

e entre no diretório:

```sh
cd keshibot
```

### instalar dependências do node

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
4. informe o código que apareceu no terminal.

> [!TIP]
> a pasta `assets/auth/` será criada automaticamente e armazenará a sessão do whatsapp.

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

### apis

| constante | uso |
| --- | --- |
| `SPIDER_API_TOKEN` | token da spider x api |
| `LINKER_API_KEY` | chave usada pelo comando `gerar-link` |
| `OPENAI_API_KEY` | chave usada pelo comando `suporte` |

### comportamento

para descobrir seu lid, use:

```text
/meu-lid
```

para descobrir o id do grupo, use:

```text
/get-group-id
```

também é possível trocar o token da spider x api em runtime:

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

| comando | permissão | descrição |
| --- | --- | --- |
| `/access-control` | owner | controla a quais grupos e números o bot responde |
| `/exec` | owner | executa comandos de terminal pelo bot |
| `/get-group-id` | owner | mostra o id completo do grupo no formato jid |
| `/off` | owner | desativa o bot no grupo |
| `/on` | owner | ativa o bot no grupo |
| `/set-menu-image` | owner | altera a imagem do menu |
| `/set-prefix` | owner | muda o prefixo dos comandos |
| `/set-spider-api-token` | owner | atualiza o token da spider x api |

### administração

| comando | permissão | descrição |
| --- | --- | --- |
| `/abrir` | admin | abre o grupo |
| `/add-auto-responder` | admin | adiciona um termo ao auto-responder |
| `/afk` | admin | informa que você está ausente e registra o motivo |
| `/agendar-mensagem` | admin | agenda uma mensagem para ser enviada depois |
| `/anti-audio 1\|0` | admin | ativa ou desativa bloqueio de áudio |
| `/anti-call 1\|0` | admin | ativa ou desativa bloqueio de chamadas |
| `/anti-document 1\|0` | admin | ativa ou desativa bloqueio de documentos |
| `/anti-event 1\|0` | admin | ativa ou desativa bloqueio de eventos |
| `/anti-image 1\|0` | admin | ativa ou desativa bloqueio de imagens |
| `/anti-link 1\|0` | admin | ativa ou desativa bloqueio de links |
| `/anti-lottie-sticker 1\|0` | admin | ativa ou desativa bloqueio de stickers animados |
| `/anti-payment 1\|0` | admin | ativa ou desativa bloqueio de pagamentos |
| `/anti-product 1\|0` | admin | ativa ou desativa bloqueio de produtos |
| `/anti-status-grupo 1\|0` | admin | ativa ou desativa bloqueio de marcação de status |
| `/anti-sticker 1\|0` | admin | ativa ou desativa bloqueio de stickers |
| `/anti-video 1\|0` | admin | ativa ou desativa bloqueio de vídeos |
| `/auto-responder 1\|0` | admin | ativa ou desativa respostas automáticas |
| `/auto-sticker 1\|0` | admin | ativa ou desativa conversão automática de sticker |
| `/ban` | admin | remove um membro do grupo |
| `/block-wpp` | admin | bloqueia um número no whatsapp do bot |
| `/delete` | admin | apaga mensagens do bot |
| `/delete-auto-responder` | admin | remove um termo do auto-responder pelo id |
| `/exit 1\|0` | admin | ativa ou desativa mensagem de saída do grupo |
| `/fechar` | admin | fecha o grupo |
| `/hidetag` | admin | marca todos do grupo invisivelmente |
| `/limpar-chat` | admin | limpa o histórico de mensagens do grupo |
| `/link-grupo` | admin | envia o link de convite do grupo |
| `/list-auto-responder` | admin | lista todos os termos do auto-responder |
| `/mute` | admin | silencia um membro no grupo |
| `/only-admin 1\|0` | admin | restringe comandos a administradores |
| `/promover` | admin | promove um usuário a administrador |
| `/rebaixar` | admin | rebaixa um administrador a membro |
| `/revelar` | admin | revela imagem ou vídeo de visualização única |
| `/saldo` | admin | consulta o saldo de requests da spider x api |
| `/set-name` | admin | altera o nome do grupo |
| `/unmute` | admin | remove o silêncio de um membro |
| `/unwarn` | admin | remove ou lista advertências |
| `/warn` | admin | aplica advertência a um membro |
| `/warn-reactivate` | admin | reativa uma advertência inválida |
| `/welcome 1\|0` | admin | ativa ou desativa mensagem de boas-vindas |

### membros

| comando | permissão | descrição |
| --- | --- | --- |
| `/attp` | member | cria sticker animado de texto |
| `/brat` | member | gera imagem no estilo brat |
| `/bratvid` | member | gera sticker animado no estilo brat |
| `/cep` | member | consulta endereço por cep |
| `/fake-chat` | member | cria uma citação falsa mencionando um usuário |
| `/gerar-link` | member | faz upload de imagem e gera link |
| `/info` | member | exibe informações de um comando |
| `/meu-lid` | member | retorna o lid do usuário |
| `/menu` | member | exibe o menu de comandos |
| `/perfil` | member | mostra informações de um usuário |
| `/ping` | member | verifica se o bot está online, latência e uptime |
| `/rename` | member | adiciona metadados à figurinha |
| `/removebg` | member | remove o fundo de imagens e figurinhas |
| `/sticker` | member | cria figurinha de imagem, gif ou vídeo |
| `/suporte` | member | suporte inteligente com ia |
| `/to-gif` | member | converte figurinha animada em gif |
| `/to-image` | member | extrai imagem de figurinha estática |
| `/to-mp3` | member | extrai áudio de vídeo em mp3 |
| `/ttp` | member | cria sticker de texto |
| `/yt-search` | member | busca vídeos no youtube |

### downloads

| comando | permissão | descrição |
| --- | --- | --- |
| `/facebook` | member | baixa vídeo do facebook |
| `/instagram` | member | baixa vídeo/reel do instagram |
| `/play-audio` | member | busca e baixa música |
| `/play-video` | member | busca e baixa vídeo |
| `/pinterest` | member | busca imagens no pinterest |
| `/tik-tok` | member | baixa vídeo do tiktok |
| `/tik-tok-audio` | member | baixa áudio de vídeo do tiktok |
| `/yt-mp3` | member | baixa áudio do youtube pelo link |
| `/yt-mp4` | member | baixa vídeo do youtube pelo link |

### brincadeiras

| comando | permissão | descrição |
| --- | --- | --- |
| `/abracar` | member | abraça um usuário |
| `/beijar` | member | beija um usuário |
| `/dado` | member | joga um dado d6 |
| `/jantar` | member | convida um usuário para jantar |
| `/lutar` | member | luta com um usuário |
| `/matar` | member | mata um usuário |
| `/socar` | member | dá um soco em um usuário |
| `/tapa` | member | dá um tapa em alguém |

### canvas

| comando | permissão | descrição |
| --- | --- | --- |
| `/blur` | member | aplica desfoque na imagem |
| `/bolsonaro` | member | meme do bolsonaro com a imagem |
| `/cadeia` | member | meme de cadeia com a imagem |
| `/contraste` | member | ajusta o contraste da imagem |
| `/espelhar` | member | espelha a imagem |
| `/gray` | member | converte a imagem para preto e branco |
| `/inverter` | member | inverte as cores da imagem |
| `/pixel` | member | aplica efeito pixel-art na imagem |
| `/rip` | member | meme de lápide com a imagem |

## apis externas

alguns comandos dependem de serviços externos.

### spider x api

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

se a api do linker não estiver configurada, alguns comandos podem usar a spider x api como fallback.

### openai

usada pelo comando `/suporte`.

```js
export const OPENAI_API_KEY = "sua_chave";
```

se `OPENAI_API_KEY` estiver vazia, o comando `/suporte` responde que o suporte inteligente não está disponível.

## estrutura do projeto

```text
./
├─ assets/
│  ├─ auth/               estado de autenticação do whatsapp
│  ├─ images/             imagens usadas pelo bot
│  ├─ stickers/           stickers locais
│  └─ temp/               arquivos temporários
├─ src/
│  ├─ commands/
│  │  ├─ admin/           comandos administrativos
│  │  ├─ member/          comandos de membros
│  │  └─ owner/           comandos do dono
│  ├─ errors/             classes de erro usadas pelo fluxo de comandos
│  ├─ middlewares/        pipeline de mensagens, grupos e chamadas
│  ├─ services/           integrações e processamento de mídia
│  ├─ utils/              helpers e persistência
│  ├─ config.js           configuração principal
│  ├─ connection.js       conexão do baileys
│  ├─ index.js            entrada do bot
│  ├─ loader.js           registro dos eventos
│  ├─ menu.js             texto do menu
│  └─ messages.js         mensagens de boas-vindas e saída
├─ package.json
├─ package-lock.json
├─ README.md
└─ LICENSE
```

arquivos ignorados:

- `node_modules/`: dependências do npm.
- `database/`: arquivos de persistência local.
- `assets/auth/baileys/`: estado de autenticação do whatsapp.
- `assets/temp/`: arquivos temporários de mídia.
- `.vscode/`: configurações do vscode.

## personalização

### menu

edite `src/menu.js`.

### mensagens de entrada e saída

edite `src/messages.js`.

### imagem do menu

troque o arquivo `assets/images/keshi-bot.png` ou use o comando `/set-menu-image` respondendo a uma imagem.

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

## desenvolvimento

instalar ou atualizar dependências:

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

## atualização

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

no termux, por exemplo, é comum ter uma cópia em `/sdcard/`, outra em `~/storage/shared/` ou outra em `Downloads/`.

### erro de conexão ou sessão corrompida

rode:

```sh
bash reset-qr-auth.sh
```

depois remova o dispositivo conectado no whatsapp e faça o pareamento novamente.

### `permission denied` ao acessar armazenamento (termux)

rode:

```sh
termux-setup-storage
```

aceite a permissão no android e tente novamente.

### `ffmpeg` não encontrado

instale o ffmpeg:

#### para termux

```sh
pkg install ffmpeg -y
```

#### para ubuntu/debian

```sh
sudo apt install ffmpeg -y
```

#### para windows

baixe em <https://ffmpeg.org/download.html> ou use chocolatey/winget e adicione `ffmpeg` ao `PATH`.

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

distribuído sob a GPL-3.0.
veja [`LICENSE`](LICENSE) para mais informações.

---

baseado no projeto [takeshi-bot](https://github.com/guiireal/takeshi-bot), de [Guilherme França](https://devgui.dev/).

mantido por [Lucas Duarte](https://github.com/luuuuuqui).
