# guia do agente

este repositório é uma cópia privada do Takeshi Bot para uso próprio.

## objetivo do projeto

manter um bot de WhatsApp funcional, enxuto e fácil de rodar no termux.

prioridades:

- preservar o runtime do bot;
- evitar arquivos locais ou sensíveis no git;
- manter comandos simples e organizados por permissão;
- preferir mudanças pequenas e fáceis de revisar.

## stack

- Node.js 22.8 ou superior;
- Baileys;
- FFmpeg;
- JSON local para persistência em runtime.

script principal:

```sh
npm start
```

não rode `npm start` automaticamente neste repositório.

## estrutura importante

- `src/index.js`: entrada principal do bot;
- `src/connection.js`: conexão com WhatsApp e estado do Baileys;
- `src/loader.js`: registro dos eventos;
- `src/middlewares/onMesssagesUpsert.js`: pipeline principal de mensagens;
- `src/utils/dynamicCommand.js`: resolução e execução de comandos;
- `src/utils/loadCommonFunctions.js`: helpers injetados nos comandos;
- `src/utils/database.js`: persistência JSON;
- `src/services/`: integrações, mídia, stickers e APIs;
- `src/commands/owner/`: comandos do dono;
- `src/commands/admin/`: comandos administrativos;
- `src/commands/member/`: comandos de membros.

## arquivos que não entram no git

nunca versionar:

- `node_modules/`;
- `database/`;
- `assets/auth/baileys/`;
- `assets/temp/`;
- `.vscode/`;
- tokens, chaves, sessões e arquivos gerados em runtime.

`database/` deve ser criado automaticamente pelo código quando necessário.

## regras de alteração

- leia o código ao redor antes de alterar;
- preserve mudanças existentes do usuário;
- não reverta trabalho que você não fez;
- não crie abstrações sem necessidade;
- use helpers existentes antes de criar novos;
- em comandos, use os helpers recebidos no `handle()`;
- para persistência, use `src/utils/database.js`;
- ao mexer em mídia, confira `src/services/` e `src/utils/loadCommonFunctions.js`;
- ao mexer em mensagens de grupo, confira middlewares e `src/messages.js`.

## segurança

nunca exponha:

- `OPENAI_API_KEY`;
- `LINKER_API_KEY`;
- `SPIDER_API_TOKEN`;
- arquivos de `assets/auth/baileys/`;
- dados reais de `database/`.

não modifique manualmente `assets/auth/`.

## commits e push

sempre faça commit quando terminar uma tarefa neste repositório, desde que a alteração esteja coerente e verificável.

depois do commit, sempre faça push para o remote da branch atual.

antes de commitar:

1. veja `git status --short`;
2. confira o diff relevante;
3. valide o que for possível sem iniciar o bot;
4. use uma mensagem curta em português.

depois de commitar:

1. veja `git status --short`;
2. confira `git log -1 --oneline`;
3. rode `git push` ou `git push -u origin <branch>` se a branch ainda não tiver upstream.

estilo das mensagens:

- sem prefixos como `feat:` ou `fix:`;
- verbo no presente;
- letras minúsculas;
- crase para arquivos, diretórios e identificadores.

exemplos:

```text
remove documentação pública do projeto original
ignora dados locais de `database/`
ajusta leitura de contexto do suporte
```

## validação

não rode `npm start` automaticamente.

pode rodar validações estáticas como:

```sh
node --check src/index.js
node --check src/utils/database.js
```

se `node_modules/` não existir, não tente importar dependências externas só para validar.

## comunicação

responda de forma direta, em português, com foco no que foi feito e no que precisa de atenção.
