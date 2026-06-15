# Takeshi Bot Python Port

This repository now contains an in-progress Python port that keeps the original
JavaScript bot intact.

## Current Architecture

- `takeshi_bot/` is the Python application and command framework.
- `bridge/baileys-sidecar.js` keeps Baileys as the WhatsApp Web transport.
- Python talks to the sidecar through newline-delimited JSON over stdin/stdout.
- Business logic, command routing, permissions and JSON persistence live in Python.
- WhatsApp auth state is still stored in `assets/auth/baileys/`.

## Run

Install Python dependencies:

```sh
python -m pip install -r requirements.txt
```

The sidecar still needs the Node dependencies already used by this repo:

```sh
npm install
```

For containers and Pterodactyl, the runtime must include **Python 3.12+,
Node.js 24+ and FFmpeg**. `Dockerfile.python-port` builds that combined runtime,
and `eggs/pterodactyl-python-port.json` is a Python-first egg for panels that
can use a compatible image.

Start the Python port:

```sh
python -m takeshi_bot
```

Or through npm:

```sh
npm run python:start
```

If there is no saved Baileys session, the Python process asks for the phone
number and prints the pairing code.

## Test

```sh
python -m unittest discover -s tests_python
```

Or:

```sh
npm run python:test
```

## Doctor

Run a preflight check before pairing WhatsApp:

```sh
python -m takeshi_bot.doctor
```

Or:

```sh
npm run python:doctor
```

The doctor checks Python, Node.js, FFmpeg, bridge script, runtime directories,
command registry and JS-to-Python command mapping.

## Implemented So Far

- Python config, logger, custom errors and atomic JSON database access.
- Baileys sidecar bridge for connect, send message, delete message, group
  participant updates, metadata and media download.
- Python message extraction, command context helpers and dynamic command routing.
- Permission model by folder: `owner`, `admin`, `member`.
- Participant lifecycle for welcome/exit messages with profile-image fallback.
- Group restriction moderation for anti-media, anti-payment and anti-status-grupo.
- Stealth anti-payment detection for ciphertext stubs with `stealthMeta.decryptFail=hide`,
  including tracker/cooldown and the same close-remove-clean-reopen flow.
- Progressive warn storage compatible with `database/warns.json`.
- Sticker creation and `rename` use `node-webpmux` through the Baileys sidecar
  for WhatsApp EXIF metadata.
- `ia-sticker` downloads the generated Spider X image and converts it to local
  WebP with FFmpeg before sending, matching the JavaScript sticker workflow more
  closely.
- Python FFmpeg service parity covers the JavaScript canvas filters
  (`blur`, grayscale, mirror, contrast, pixelation and sticker-to-image), plus
  audio extraction, image normalization and video copy helpers used by ported
  commands.
- Every JS command file under `src/commands` now has a Python counterpart under
  `takeshi_bot/commands`. Many example commands now send real text, media,
  document, button, native-flow button, list, carousel card, poll, contact,
  location and reaction payloads through the bridge.
- JavaScript command aliases are covered by the Python registry for all mapped
  command files, with a regression test comparing the JS `commands` arrays to
  the loaded Python aliases.
- Commands currently loaded by the Python registry include:
  - `abrir`
  - `ping`
  - `menu`
  - `meu-lid`
  - `on`
  - `off`
  - `set-prefix`
  - `set-spider-api-token`
  - `anti-link`
  - `anti-image`
  - `anti-video`
  - `anti-audio`
  - `anti-sticker`
  - `anti-document`
  - `anti-payment`
  - `anti-status-grupo`
  - `auto-responder`
  - `auto-sticker`
  - `add-auto-responder`
  - `ban`
  - `attp`
  - `ttp`
  - `brat`
  - `bratvid`
  - `blur`
  - `bolsonaro`
  - `cadeia`
  - `cep`
  - `contraste`
  - `delete`
  - `delete-auto-responder`
  - `exec`
  - `espelhar`
  - `fake-chat`
  - `flux`
  - `gerar-link`
  - `get-group-id`
  - `hide-tag`
  - `info`
  - `exit`
  - `facebook`
  - `fechar`
  - `instagram`
  - `inverter`
  - `limpar-chat`
  - `link-grupo`
  - `list-auto-responder`
  - `mute`
  - `only-admin`
  - `play-audio`
  - `perfil`
  - `pinterest`
  - `play-video`
  - `pixel`
  - `promover`
  - `rebaixar`
  - `removebg`
  - `rename`
  - `rip`
  - `saldo`
  - `revelar`
  - `set-menu-image`
  - `set-name`
  - `set-proxy`
  - `sticker`
  - `toimage`
  - `to-mp3`
  - `togif`
  - `unmute`
  - `unwarn`
  - `warn`
  - `warn-reactivate`
  - `welcome`
  - `yt-mp3`
  - `yt-mp4`
  - `tik-tok`
  - `tik-tok-audio`
  - `yt-search`
  - `gemini`
  - `gpt-5-mini`
  - `deepseek`
  - `ia-sticker`
  - plus the `member/exemplos/*` example commands and their main JS aliases.

## Still To Port

- Runtime validation for the advanced card/carousel/native-flow examples against
  a real WhatsApp account.
- Remaining sticker edge cases around animated EXIF and unusual WebP inputs.
- Runtime validation with a real paired WhatsApp account.
- Publishing a real container image for the Python-first Pterodactyl egg.
