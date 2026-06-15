# TAKESHI BOT AGENT GUIDE

This file is the single source of truth for agents and contributors who need fast,
reliable project context.

Use it as the primary documentation for:

- architecture and runtime flow
- command authoring rules
- Python port work
- configuration and persistence rules
- service boundaries
- supported hosting context
- AI-agent operating rules and local skills

For installation walkthroughs and end-user tutorials, see `README.md`.

## PROJECT_OVERVIEW

**Takeshi Bot** is a modular WhatsApp bot framework originally built on the
Baileys ecosystem.

The repository currently keeps two implementations:

- the original JavaScript bot under `src/`
- an in-progress Python port under `takeshi_bot/`

The Python port is the active modernization path, but the JavaScript code remains
important as the reference implementation for behavior, command parity, and the
Baileys WhatsApp transport.

This fork is intentionally AI-assisted. Multiple AI coding agents may contribute
implementation, documentation, tests, and migration work. Treat AI-written code
as welcome in this fork when it is readable, reviewed, tested where practical,
and consistent with the project architecture.

Core principles:

- file-oriented command architecture instead of giant switch/case handlers
- clear separation of permissions by folder
- simple JSON persistence
- reusable services and middleware
- code optimized for readability and maintenance
- preserve behavior parity while moving bot logic to Python
- use AI assistance openly and pragmatically while keeping technical ownership
  with the repository maintainer

Permission model:

- `src/commands/owner` and `takeshi_bot/commands/owner` -> bot owner features
- `src/commands/admin` and `takeshi_bot/commands/admin` -> group administration features
- `src/commands/member` and `takeshi_bot/commands/member` -> regular member features

The project philosophy is simple: code for humans first.

## PYTHON_PORT

The Python port is documented in `PYTHON_PORT.md`. Treat that file as the main
status document for the port.

Current Python-port architecture:

1. `takeshi_bot/` contains the Python application, command framework, routing,
   permissions, middleware-like processing, services, and JSON persistence.
2. `bridge/baileys-sidecar.js` keeps Baileys as the WhatsApp Web transport.
3. Python communicates with the sidecar through newline-delimited JSON over
   stdin/stdout.
4. WhatsApp auth state remains in `assets/auth/baileys/`.
5. JavaScript command files under `src/commands` are the behavior reference for
   Python counterparts under `takeshi_bot/commands`.

Python-port goals:

- keep the JavaScript bot intact while Python reaches parity
- move business logic, command routing, permissions, persistence, and services to Python
- preserve existing command names, aliases, permissions, and user-facing behavior
- reuse the sidecar for WhatsApp features that still depend on Baileys
- keep Pterodactyl/container support practical for a mixed Python + Node runtime

Useful Python-port commands:

```sh
python -m takeshi_bot
python -m takeshi_bot.doctor
python -m unittest discover -s tests_python
npm run python:start
npm run python:doctor
npm run python:test
```

Runtime requirements for the Python port:

- Python 3.12+
- Node.js 24+
- FFmpeg
- Node dependencies from `package.json`
- Python dependencies from `requirements.txt`

Container and panel support:

- `Dockerfile.python-port` builds the combined Python + Node + FFmpeg runtime.
- `eggs/pterodactyl-python-port.json` is the Python-first Pterodactyl egg.

When porting or fixing Python behavior:

- compare the matching JavaScript command/service first
- keep folder-based permissions instead of duplicating checks inside commands
- use the Python database utilities instead of reading JSON files directly
- prefer parity and small safe steps over broad rewrites
- update `PYTHON_PORT.md` when implementation status materially changes

## JAVASCRIPT_ARCHITECTURE

Main JavaScript runtime flow:

1. `index.js` or `src/index.js` boots the bot.
2. `src/connection.js` opens the WhatsApp connection, loads auth state, handles
   pairing, and reconnects when needed.
3. `src/loader.js` registers listeners and wraps event execution with safe error
   handling.
4. `src/middlewares/onMesssagesUpsert.js` receives messages, filters stale events,
   handles muted users and participant events, and injects common functions.
5. `src/utils/dynamicCommand.js` validates prefix, permission, group state, and
   dispatches the selected command.
6. `src/services/*` and `src/utils/*` provide integrations, media processing,
   database access, and helpers.

High-value architectural notes:

- the bot stores its WhatsApp auth state in `assets/auth/baileys/`
- `TIMEOUT_IN_MILLISECONDS_BY_EVENT` throttles event handling to reduce spam-ban risk
- `badMacHandler` is part of the self-healing strategy for session issues
- `loadCommonFunctions.js` is the main injection layer for JavaScript command helpers

## CORE_FILES

| Path | Responsibility |
| --- | --- |
| `index.js` | Root entrypoint for hosts that expect a root `index.js`. |
| `src/index.js` | Main JavaScript source entrypoint. |
| `src/config.js` | JavaScript runtime configuration, tokens, directories, flags, and platform settings. |
| `src/connection.js` | WhatsApp socket setup, pairing, session persistence, reconnection logic. |
| `src/loader.js` | JavaScript event registration and safe wrapper logic. |
| `src/middlewares/onMesssagesUpsert.js` | Main JavaScript inbound message processing pipeline. |
| `src/middlewares/customMiddleware.js` | Official JavaScript extension point for custom global logic. |
| `src/utils/dynamicCommand.js` | JavaScript prefix validation, permission enforcement, and command dispatch. |
| `src/utils/loadCommonFunctions.js` | Injected JavaScript helper functions used by command handlers. |
| `src/utils/database.js` | Safe JavaScript access layer for JSON persistence. |
| `src/@types/index.d.ts` | Typing and documentation for JavaScript command and middleware props. |
| `src/services/spider-x-api.js` | Spider X integration for downloads, AI, Pinterest, Brat, and related endpoints. |
| `src/services/sticker.js` | JavaScript sticker processing and EXIF handling. |
| `src/services/ffmpeg.js` | JavaScript media conversion and audio/video processing. |
| `takeshi_bot/` | Python application, command framework, services, and runtime. |
| `bridge/baileys-sidecar.js` | Node/Baileys sidecar used by the Python port. |
| `tests_python/` | Python port tests. |
| `PYTHON_PORT.md` | Current Python port status, run instructions, and remaining work. |
| `Dockerfile.python-port` | Combined runtime image for the Python port. |
| `eggs/pterodactyl-python-port.json` | Python-first Pterodactyl egg. |

## COMMAND_GUIDE

JavaScript command template:

```javascript
import { PREFIX } from "../../config.js";
import { InvalidParameterError } from "../../errors/index.js";

export default {
  name: "command",
  description: "What it does",
  commands: ["alias1", "alias2"],
  usage: `${PREFIX}command <args>`,
  handle: async ({ sendReply, args }) => {
    if (!args[0]) throw new InvalidParameterError("Missing arguments!");
    await sendReply("Success!");
  },
};
```

Command authoring rules:

- always use injected helpers from `handle()` before introducing new low-level logic
- never manually enforce owner/admin/member permission inside the command if folder
  placement already defines it
- use custom errors for automatic user-facing responses
- keep commands focused and readable
- prefer existing helpers and services over duplicating code
- if a command needs persistence, go through the project database utility layer

## TYPING_AND_MIDDLEWARE

JavaScript typing lives in `src/@types/index.d.ts`.

Important interfaces:

- `CommandHandleProps`
- `CustomMiddlewareProps`

Useful JavaScript `handle()` capabilities:

- media flags: `isImage`, `isVideo`, `isAudio`, `isSticker`
- send helpers: `sendReply()`, `sendSuccessReply()`, `sendReact()`,
  `sendImageFromURL()`, `sendStickerFromFile()`
- download helpers: `downloadImage()`, `downloadVideo()`, `downloadAudio()`,
  `downloadSticker()`
- context values: `args`, `fullArgs`, `fullMessage`, `remoteJid`, `replyText`,
  `userLid`

Custom JavaScript global logic should go into `src/middlewares/customMiddleware.js`.

Use it for:

- custom logs
- extra validations
- automatic reactions
- per-group behavior
- custom participant hooks

Do not modify core middleware flow unless there is a real architectural need.

## DATA_RULES

The bot uses JSON files in `database/` for persistence.

Important files:

| File | Role |
| --- | --- |
| `config.json` | runtime values such as tokens and mutable settings |
| `prefix-groups.json` | custom prefixes per group |
| `auto-responder.json` | trigger/answer entries |
| `muted.json` | muted users by group |
| `inactive-groups.json` | groups where the bot is disabled |
| `group-restrictions.json` | restrictions by message type |

Mandatory rule:

- never read these files directly inside command code
- always use the appropriate database utility layer for the implementation being edited

This keeps persistence behavior consistent and avoids duplicated parsing logic.

## SERVICES

### Spider X API

`src/services/spider-x-api.js` powers:

- downloads from TikTok, YouTube, Instagram, Facebook, Pinterest
- AI endpoints such as Gemini, GPT-5 Mini, Flux
- sticker endpoints such as `attp`, `ttp`, and `brat`
- utility endpoints used by several commands

It depends on `SPIDER_API_TOKEN`, which can come from:

- `src/config.js`
- runtime database config through `/set-spider-api-token`

### Media Services

`src/services/ffmpeg.js` handles media conversion, including audio normalization
and voice-note friendly formats.

`src/services/sticker.js` handles:

- static sticker processing
- animated sticker workflows
- EXIF metadata
- WebP packaging

The Python port has corresponding service code under `takeshi_bot/` where parity
has already been implemented or is in progress.

## STACK

Runtime and dependency snapshot lives in:

- `package.json`
- `requirements.txt`
- `pyproject.toml`

Project-level scripts include:

- `npm start`
- `npm test`
- `npm run test:all`
- `npm run python:start`
- `npm run python:test`
- `npm run python:doctor`

## HOSTING_AND_PTERODACTYL

The project README currently highlights the supported hosts in its installation
section. Treat `README.md` as the source of truth for host names and links.

Installation tutorials stay in `README.md`.

If the topic is about hosting, VPS setup, startup configuration, schedules, SFTP,
Pterodactyl panel usage, or backup flow, agents should also load:

- `.skills/pterodactyl-specialist/SKILL.md`

That skill is the specialized source for Pterodactyl guidance.

## STABILITY_AND_ERRORS

Stability mechanisms:

- `DEVELOPER_MODE` in `src/config.js` increases logging
- runtime logs are stored in `assets/temp/wa-logs.txt`
- `src/utils/badMacHandler.js` helps recover from repeated session failures
- `TIMEOUT_IN_MILLISECONDS_BY_EVENT` throttles event execution

Use these custom error classes in JavaScript:

- `InvalidParameterError`
- `WarningError`
- `DangerError`

Use the corresponding Python custom errors when working in `takeshi_bot/`.

These are expected by the bot flow and produce cleaner automatic replies.

## AGENT_RULES

Agents working in this repository should follow these rules:

- prefer `AGENTS.md` as the primary project context source
- use `README.md` for installation and end-user tutorials
- use `PYTHON_PORT.md` for Python-port status and remaining work
- understand that this fork welcomes code written with help from multiple AI agents
- treat the repository as modular and file-oriented
- compare JavaScript and Python implementations when working on port parity
- avoid manual JSON reads from `database/` in command code
- prefer existing helpers and services before adding new primitives
- never modify `assets/auth/` manually
- never expose the values of `OPENAI_API_KEY`, `LINKER_API_KEY`, or `SPIDER_API_TOKEN`
- keep changes focused, but do not be afraid to touch every file needed for a real fix
- update docs when the behavior, runtime, or port status changes

## COMMIT_POLICY

The repository owner explicitly allows agents to make commits as needed.

Agents may:

- create as many commits as useful for the task
- choose commit boundaries that make review and rollback easier
- commit documentation, implementation, tests, and cleanup separately or together
- use their own judgment for commit messages and sequencing

Do not wait for special permission before committing when a task naturally calls
for commits. Still avoid committing unrelated local changes that were not made
for the current task.

## LOCAL_SKILLS

This repository uses a local skills pattern to help AI agents load specialized
context only when needed.

Current local skill directory:

- `.skills/pterodactyl-specialist/`

Current local skill:

- `pterodactyl-specialist` -> focused instructions for Pterodactyl panel usage,
  hosting workflows, files, databases, backups, schedules, bots, and APIs

Skill usage rule:

- if the topic is about hosting or **Pterodactyl**, load `.skills/pterodactyl-specialist/SKILL.md`

This keeps support and agent workflows selective instead of forcing every answer
to carry all hosting knowledge by default.

## DO_NOT_RUN

Do not run these commands in this repository unless the user explicitly changes
this rule:

- `npm test`
- `npm run test:all`
- `npm start`

Prefer Python-port checks only when relevant, such as:

- `python -m unittest discover -s tests_python`
- `python -m takeshi_bot.doctor`
- `npm run python:test`
- `npm run python:doctor`
