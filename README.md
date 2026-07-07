# Takeshi Bot

Bot privado de WhatsApp baseado em Baileys, organizado por comandos modulares.

## Uso no Termux

Instale os pacotes principais:

```sh
pkg update -y
pkg upgrade -y
pkg install git nodejs-lts ffmpeg -y
```

Clone o repositório privado e entre na pasta:

```sh
git clone <url-do-repositorio>
cd takeshibot
```

Instale as dependências:

```sh
npm install
```

Configure `src/config.js`:

```js
export const PREFIX = "/";
export const BOT_NAME = "Takeshi Bot";
export const BOT_LID = "12345678901234567890@lid";
export const OWNER_LID = "12345678901234567890@lid";
```

Inicie o bot:

```sh
npm start
```

Depois de parear no WhatsApp, pare com `CTRL + C`, revise as configurações e rode novamente.

## Estrutura

- `src/commands/admin/`: comandos de administração de grupo.
- `src/commands/member/`: comandos disponíveis para membros.
- `src/commands/owner/`: comandos do dono do bot.
- `src/middlewares/`: processamento de mensagens, chamadas e eventos.
- `src/services/`: integrações e processamento de mídia.
- `src/utils/`: helpers, persistência e lógica compartilhada.
- `assets/`: imagens, stickers e arquivos temporários.
- `database/`: dados criados automaticamente em runtime. não entra no git.

## Configuração

As principais opções ficam em `src/config.js`.

Tokens sensíveis não devem ser commitados:

- `OPENAI_API_KEY`
- `LINKER_API_KEY`
- `SPIDER_API_TOKEN`

O comando `/set-spider-api-token` também pode salvar o token da Spider API em runtime dentro de `database/config.json`.

## Persistência

O bot cria os JSONs de `database/` automaticamente quando precisa deles.

Não adicione `database/`, `assets/auth/baileys/`, `assets/temp/` ou `node_modules/` ao repositório.

## Comandos úteis

```sh
npm install
npm start
bash reset-qr-auth.sh
```

## Observações

Este repositório é privado e mantém apenas a documentação necessária para uso e manutenção do bot.
