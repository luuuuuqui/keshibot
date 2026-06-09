import makeWASocket, {
  DisconnectReason,
  downloadContentFromMessage,
  fetchLatestBaileysVersion,
  isJidBroadcast,
  isJidNewsletter,
  isJidStatusBroadcast,
  useMultiFileAuthState,
} from "baileys";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";
import webp from "node-webpmux";
import pino from "pino";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "..");
const tempDir = path.join(projectRoot, "assets", "temp");
const authDir = path.join(projectRoot, "assets", "auth", "baileys");

fs.mkdirSync(tempDir, { recursive: true });
fs.mkdirSync(authDir, { recursive: true });

let socket = null;
let saveCreds = null;

const logger = pino(
  { timestamp: () => `,"time":"${new Date().toJSON()}"` },
  pino.destination(path.join(tempDir, "wa-logs-python-sidecar.txt")),
);
logger.level = "error";

function emit(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function emitEvent(type, payload) {
  emit({ kind: "event", type, payload });
}

function respond(id, ok, dataOrError) {
  emit({
    kind: "response",
    id,
    ok,
    ...(ok ? { data: dataOrError ?? null } : { error: String(dataOrError) }),
  });
}

function serializeError(error) {
  return {
    message: error?.message || String(error),
    stack: error?.stack || null,
    statusCode: error?.output?.statusCode || null,
  };
}

function formatPairingCode(code) {
  return code?.match(/.{1,4}/g)?.join("-") || code;
}

async function connect() {
  const auth = await useMultiFileAuthState(authDir);
  saveCreds = auth.saveCreds;
  const { version } = await fetchLatestBaileysVersion();

  socket = makeWASocket({
    version,
    logger,
    auth: auth.state,
    defaultQueryTimeoutMs: undefined,
    retryRequestDelayMs: 5000,
    shouldIgnoreJid: (jid) =>
      isJidBroadcast(jid) || isJidStatusBroadcast(jid) || isJidNewsletter(jid),
    connectTimeoutMs: 20_000,
    keepAliveIntervalMs: 30_000,
    maxMsgRetryCount: 5,
    markOnlineOnConnect: true,
    syncFullHistory: false,
    emitOwnEvents: false,
    shouldSyncHistoryMessage: () => false,
  });

  socket.ev.on("connection.update", async (update) => {
    emitEvent("connection.update", {
      ...update,
      lastDisconnect: update.lastDisconnect
        ? {
            ...update.lastDisconnect,
            error: serializeError(update.lastDisconnect.error),
          }
        : null,
      version,
      registered: socket?.authState?.creds?.registered || false,
    });

    if (update.connection === "close") {
      const statusCode = update.lastDisconnect?.error?.output?.statusCode;
      if (statusCode !== DisconnectReason.loggedOut) {
        setTimeout(() => {
          connect().catch((error) =>
            emitEvent("sidecar.error", serializeError(error)),
          );
        }, 5000);
      }
    }
  });

  socket.ev.on("messages.upsert", (data) => {
    emitEvent("messages.upsert", data);
  });

  socket.ev.on("creds.update", saveCreds);

  emitEvent("sidecar.ready", {
    version,
    registered: socket.authState.creds.registered,
  });
}

function getNestedMessage(webMessage, context) {
  return (
    webMessage?.message?.[`${context}Message`] ||
    webMessage?.message?.extendedTextMessage?.contextInfo?.quotedMessage?.[
      `${context}Message`
    ] ||
    webMessage?.message?.viewOnceMessage?.message?.[`${context}Message`] ||
    webMessage?.message?.extendedTextMessage?.contextInfo?.quotedMessage
      ?.viewOnceMessage?.message?.[`${context}Message`] ||
    webMessage?.message?.viewOnceMessageV2?.message?.[`${context}Message`] ||
    webMessage?.message?.extendedTextMessage?.contextInfo?.quotedMessage
      ?.viewOnceMessageV2?.message?.[`${context}Message`]
  );
}

async function downloadMedia({ webMessage, context, fileName, extension }) {
  const content = getNestedMessage(webMessage, context);
  if (!content) return null;

  const stream = await downloadContentFromMessage(content, context);
  let buffer = Buffer.from([]);
  for await (const chunk of stream) {
    buffer = Buffer.concat([buffer, chunk]);
  }

  const outputPath = path.resolve(tempDir, `${fileName}.${extension}`);
  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

async function addStickerMetadata({ inputPath, outputPath, metadata = {} }) {
  const img = new webp.Image();
  await img.load(inputPath);

  const json = {
    "sticker-pack-id": String(metadata.packId || Date.now()),
    "sticker-pack-name": metadata.packName || metadata.username || "Takeshi",
    "sticker-pack-publisher":
      metadata.packPublisher || metadata.botName || "Takeshi Bot",
    emojis: metadata.emojis || metadata.categories || [""],
  };

  const exifAttr = Buffer.from([
    0x49, 0x49, 0x2a, 0x00, 0x08, 0x00, 0x00, 0x00, 0x01, 0x00, 0x41, 0x57,
    0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00,
  ]);
  const jsonBuff = Buffer.from(JSON.stringify(json), "utf-8");
  const exif = Buffer.concat([exifAttr, jsonBuff]);
  exif.writeUIntLE(jsonBuff.length, 14, 4);

  img.exif = exif;
  await img.save(outputPath);
  return outputPath;
}

async function handleCommand(command) {
  const { id, action, payload = {} } = command;

  try {
    if (!socket && action !== "connect") {
      throw new Error("Sidecar ainda nao conectou o socket.");
    }

    switch (action) {
      case "connect":
        await connect();
        respond(id, true, { connected: true });
        break;
      case "request_pairing_code": {
        const code = await socket.requestPairingCode(
          String(payload.phoneNumber || "").replace(/[^0-9]/g, ""),
        );
        respond(id, true, { code, formattedCode: formatPairingCode(code) });
        break;
      }
      case "send_message": {
        const result = await socket.sendMessage(
          payload.remoteJid,
          payload.content,
          payload.options || {},
        );
        respond(id, true, result);
        break;
      }
      case "send_file_message": {
        const fileBuffer = fs.readFileSync(payload.filePath);
        const content = {
          ...payload.content,
        };
        if (payload.mediaKey) {
          content[payload.mediaKey] = fileBuffer;
        }
        const result = await socket.sendMessage(
          payload.remoteJid,
          content,
          payload.options || {},
        );
        respond(id, true, result);
        break;
      }
      case "send_presence": {
        await socket.sendPresenceUpdate(payload.presence, payload.remoteJid);
        respond(id, true, null);
        break;
      }
      case "delete_message": {
        const result = await socket.sendMessage(payload.remoteJid, {
          delete: payload.key,
        });
        respond(id, true, result);
        break;
      }
      case "group_participants_update": {
        const result = await socket.groupParticipantsUpdate(
          payload.remoteJid,
          payload.participants,
          payload.operation,
        );
        respond(id, true, result);
        break;
      }
      case "group_metadata": {
        const result = await socket.groupMetadata(payload.remoteJid);
        respond(id, true, result);
        break;
      }
      case "group_setting_update": {
        const result = await socket.groupSettingUpdate(
          payload.remoteJid,
          payload.setting,
        );
        respond(id, true, result);
        break;
      }
      case "group_invite_code": {
        const result = await socket.groupInviteCode(payload.remoteJid);
        respond(id, true, result);
        break;
      }
      case "group_update_subject": {
        const result = await socket.groupUpdateSubject(
          payload.remoteJid,
          payload.subject,
        );
        respond(id, true, result);
        break;
      }
      case "update_profile_name": {
        const result = await socket.updateProfileName(payload.name);
        respond(id, true, result);
        break;
      }
      case "update_block_status": {
        const result = await socket.updateBlockStatus(payload.jid, payload.status);
        respond(id, true, result);
        break;
      }
      case "profile_picture_url": {
        const result = await socket.profilePictureUrl(
          payload.jid,
          payload.type || "image",
        );
        respond(id, true, result);
        break;
      }
      case "download_media": {
        const result = await downloadMedia(payload);
        respond(id, true, result);
        break;
      }
      case "add_sticker_metadata": {
        const outputPath =
          payload.outputPath ||
          path.resolve(tempDir, `sticker-metadata-${Date.now()}.webp`);
        const result = await addStickerMetadata({
          ...payload,
          outputPath,
        });
        respond(id, true, result);
        break;
      }
      case "relay_raw": {
        const fn = socket[payload.method];
        if (typeof fn !== "function") {
          throw new Error(`Metodo Baileys indisponivel: ${payload.method}`);
        }
        const result = await fn.apply(socket, payload.args || []);
        respond(id, true, result);
        break;
      }
      default:
        throw new Error(`Acao desconhecida: ${action}`);
    }
  } catch (error) {
    respond(id, false, error?.message || error);
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  crlfDelay: Infinity,
});

rl.on("line", (line) => {
  if (!line.trim()) return;
  try {
    handleCommand(JSON.parse(line));
  } catch (error) {
    emitEvent("sidecar.error", serializeError(error));
  }
});

process.on("uncaughtException", (error) => {
  emitEvent("sidecar.error", serializeError(error));
});

process.on("unhandledRejection", (reason) => {
  emitEvent("sidecar.error", serializeError(reason));
});

connect().catch((error) => emitEvent("sidecar.error", serializeError(error)));
