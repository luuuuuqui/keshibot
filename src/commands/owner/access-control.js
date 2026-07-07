import { OWNER_LID, PREFIX } from "../../config.js";
import { DangerError, InvalidParameterError } from "../../errors/index.js";
import {
  addChatAccessEntry,
  clearChatAccessEntries,
  readChatAccessControl,
  removeChatAccessEntry,
  setChatAccessMode,
} from "../../utils/database.js";
import {
  onlyNumbers,
  removeAccentsAndSpecialCharacters,
} from "../../utils/index.js";

const ACTIONS = {
  add: ["add", "adicionar", "incluir"],
  clear: ["clear", "limpar"],
  list: ["list", "listar", "status"],
  mode: ["mode", "modo"],
  remove: ["remove", "remover", "excluir"],
};

const MODES = {
  blacklist: ["blacklist", "black", "bloqueio", "bloquear"],
  whitelist: ["whitelist", "white", "permissao", "permitir"],
};

const TYPES = {
  groups: ["grupo", "grupos", "group", "groups"],
  numbers: ["numero", "numeros", "número", "números", "number", "numbers"],
};

function normalizeWord(word = "") {
  return removeAccentsAndSpecialCharacters(word.toLowerCase().trim());
}

function findKeyByAlias(aliasesByKey, value) {
  const normalizedValue = normalizeWord(value);

  return Object.entries(aliasesByKey).find(([, aliases]) =>
    aliases.map(normalizeWord).includes(normalizedValue),
  )?.[0];
}

function resolveChatType(value) {
  const type = findKeyByAlias(TYPES, value);

  if (!type) {
    throw new InvalidParameterError(
      'Informe o tipo da entrada: "grupo" ou "numero".',
    );
  }

  return type;
}

function resolveMode(value) {
  const mode = findKeyByAlias(MODES, value);

  if (!mode) {
    throw new InvalidParameterError(
      'Informe o modo: "blacklist" ou "whitelist".',
    );
  }

  return mode;
}

function resolveChatJid({ type, value, remoteJid, isGroup }) {
  const normalizedValue = normalizeWord(value);
  const useCurrentChat = ["aqui", "atual", "este", "this"].includes(
    normalizedValue,
  );

  if (useCurrentChat) {
    if (type === "groups" && !isGroup) {
      throw new InvalidParameterError(
        'Use "aqui" para grupo apenas dentro de um grupo.',
      );
    }

    if (type === "numbers" && isGroup) {
      throw new InvalidParameterError(
        'Use "aqui" para número apenas em conversa privada.',
      );
    }

    return remoteJid;
  }

  if (type === "groups") {
    if (!value?.endsWith("@g.us")) {
      throw new InvalidParameterError(
        `Informe o ID completo do grupo. Use ${PREFIX}get-group-id dentro do grupo para descobrir.`,
      );
    }

    return value;
  }

  if (value?.includes("@")) {
    return value;
  }

  const number = onlyNumbers(value || "");

  if (!number) {
    throw new InvalidParameterError("Informe um número válido.");
  }

  return `${number}@s.whatsapp.net`;
}

function formatList(items) {
  if (!items.length) {
    return "_nenhum_";
  }

  return items.map((item, index) => `${index + 1}. ${item}`).join("\n");
}

function buildStatusMessage() {
  const accessControl = readChatAccessControl();
  const modeDescription =
    accessControl.mode === "whitelist"
      ? "responde apenas nos grupos/números listados"
      : "responde em todos os chats, exceto nos grupos/números listados";

  return (
    `*Controle de respostas*\n\n` +
    `*Modo*: ${accessControl.mode}\n` +
    `_${modeDescription}_\n\n` +
    `*Grupos*\n${formatList(accessControl.groups)}\n\n` +
    `*Números*\n${formatList(accessControl.numbers)}`
  );
}

function buildUsage() {
  return [
    `Uso:`,
    `${PREFIX}access-control modo blacklist`,
    `${PREFIX}access-control modo whitelist`,
    `${PREFIX}access-control add grupo aqui`,
    `${PREFIX}access-control add grupo 123@g.us`,
    `${PREFIX}access-control add numero 5584999999999`,
    `${PREFIX}access-control remove grupo 123@g.us`,
    `${PREFIX}access-control limpar numero`,
    `${PREFIX}access-control listar`,
  ].join("\n");
}

export default {
  name: "access-control",
  description: "Controla em quais grupos e números o bot deve responder.",
  commands: [
    "access-control",
    "controle-acesso",
    "controle-respostas",
    "responder-em",
  ],
  usage: `${PREFIX}access-control modo blacklist`,
  handle: async ({
    fullArgs,
    isGroup,
    remoteJid,
    sendReply,
    sendSuccessReply,
    userLid,
  }) => {
    if (userLid !== OWNER_LID) {
      throw new DangerError("Apenas o dono do bot pode usar este comando.");
    }

    const [rawAction, rawTypeOrMode, rawValue] = fullArgs.trim().split(/\s+/);
    const action = findKeyByAlias(ACTIONS, rawAction);

    if (!action) {
      throw new InvalidParameterError(buildUsage());
    }

    if (action === "list") {
      await sendReply(buildStatusMessage());
      return;
    }

    if (action === "mode") {
      const mode = resolveMode(rawTypeOrMode);
      setChatAccessMode(mode);
      await sendSuccessReply(`Modo de controle alterado para "${mode}".`);
      return;
    }

    const type = resolveChatType(rawTypeOrMode);

    if (action === "clear") {
      clearChatAccessEntries(type);
      await sendSuccessReply(
        `Lista de ${type === "groups" ? "grupos" : "números"} limpa.`,
      );
      return;
    }

    const jid = resolveChatJid({
      type,
      value: rawValue,
      remoteJid,
      isGroup,
    });

    if (action === "add") {
      addChatAccessEntry(type, jid);
      await sendSuccessReply(`Entrada adicionada: ${jid}`);
      return;
    }

    if (removeChatAccessEntry(type, jid)) {
      await sendSuccessReply(`Entrada removida: ${jid}`);
      return;
    }

    throw new InvalidParameterError("Esta entrada não está cadastrada.");
  },
};
