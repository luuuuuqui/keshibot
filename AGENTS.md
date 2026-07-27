# guia do agente

este repositório é uma cópia do takeshi bot para uso próprio.

este guia complementa o `AGENTS.md` global do usuário com regras específicas deste projeto.

## objetivo do projeto

manter um bot de whatsapp funcional, enxuto e fácil de rodar no termux.

este repositório foi simplificado para uso próprio. ele não deve depender de arquivos locais versionados, sessões do whatsapp, bancos de dados persistidos ou outros artefatos gerados em runtime.

prioridades:

- preservar o runtime do bot;
- evitar arquivos locais ou sensíveis no git;
- manter comandos simples e organizados por permissão;
- preferir mudanças pequenas e fáceis de revisar.

## stack

- node.js 22.8 ou superior;
- baileys;
- ffmpeg;
- json local para persistência em runtime.

script principal:

```sh
npm start
```

não rode `npm start` automaticamente neste repositório.

## configuração

as opções principais ficam em `src/config.js`.

ao adicionar novas configurações:

- preserve a organização existente;
- utilize nomes consistentes com as demais constantes;
- mantenha comentários e descrições quando fizer sentido.

tokens e credenciais devem permanecer apenas na configuração local. nunca escreva valores reais no código.

## estrutura importante

- `src/index.js`: entrada principal do bot;
- `src/connection.js`: conexão com whatsapp e estado do baileys;
- `src/loader.js`: registro dos eventos;
- `src/middlewares/onMesssagesUpsert.js`: pipeline principal de mensagens;
- `src/utils/dynamicCommand.js`: resolução e execução de comandos;
- `src/utils/loadCommonFunctions.js`: helpers injetados nos comandos;
- `src/utils/database.js`: persistência local;
- `src/services/`: integrações, mídia, stickers e apis;
- `src/commands/owner/`: comandos do dono;
- `src/commands/admin/`: comandos administrativos;
- `src/commands/member/`: comandos de membros.

## comandos

novos comandos devem seguir o mesmo padrão utilizado pelos existentes.

antes de criar novas abstrações:

- reutilize os helpers disponíveis;
- utilize os helpers recebidos no `handle()`;
- mantenha a organização por permissão;
- preserve o estilo dos comandos já existentes.

## persistência

toda persistência local deve passar por `src/utils/database.js`.

o diretório `database/` é criado automaticamente em runtime e nunca faz parte do código-fonte.

ao adicionar novos arquivos de persistência:

- utilize json;
- mantenha um arquivo por responsabilidade;
- preserve compatibilidade com instalações existentes;
- não exija criação manual da pasta.

## arquivos que não entram no git

nunca versionar:

- `node_modules/`;
- `database/`;
- `assets/auth/baileys/`;
- `assets/temp/`;
- `.vscode/`;
- tokens, chaves, sessões e arquivos gerados em runtime.

## regras de alteração

antes de alterar qualquer arquivo:

- leia o código ao redor;
- preserve mudanças existentes do usuário;
- não reverta trabalho que você não fez;
- prefira mudanças pequenas;
- evite criar abstrações sem necessidade.

também observe:

- utilize `src/utils/database.js` para persistência;
- confira `src/services/` antes de alterar integrações;
- ao mexer em mídia, confira `src/utils/loadCommonFunctions.js`;
- ao mexer em mensagens de grupo, confira os middlewares e `src/messages.js`;
- preserve compatibilidade com a estrutura atual do projeto.

## serviços externos

alguns comandos dependem de serviços externos.

ao alterar essas integrações:

- preserve a compatibilidade com `src/config.js`;
- nunca exponha tokens;
- trate falhas de forma amigável para o usuário;
- evite alterar contratos existentes sem necessidade.

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
- letras minúsculas fora de aspas e crases;
- crase para arquivos, diretórios e identificadores.

exemplos:

```text
remove documentação pública do projeto original
ignora dados locais de `database/`
ajusta leitura de contexto do suporte
```

## validação

não rode `npm start` automaticamente.

antes de considerar uma alteração concluída:

- confira se o código continua consistente;
- valide arquivos modificados com `node --check` quando possível;
- não altere dados de runtime apenas para facilitar testes.

validações recomendadas:

```sh
node --check src/index.js
node --check src/utils/database.js
```

se `node_modules/` não existir, não tente importar dependências externas apenas para validar.

## comunicação

responda de forma direta com foco no que foi feito, no que mudou e no que precisa de atenção.
