import { BOT_LID, OWNER_LID } from "../../config.js";
import { DangerError, InvalidParameterError } from "../../errors/index.js";
import { onlyNumbers } from "../../utils/index.js";
import {
  getAllWarns,
  removeLastWarn,
  revokeWarnByIndex,
} from "../../utils/warnSystem.js";

export default {
  name: "unwarn",
  description: "Remove ou lista advertências válidas.",
  commands: [
    "unwarn",
    "perdoaradvertência",
    "perdoaradvt",
    "removeradvertencia",
    "advtremove",
  ],
  handle: async ({ args, isReply, replyLid, remoteJid, sendReply }) => {
    if (!args.length && !isReply) {
      throw new InvalidParameterError(
        "Mencione um usuário ou responda a uma mensagem.",
      );
    }

    if (!isReply && !args[0]?.includes("@")) {
      throw new InvalidParameterError('Use "@" ao mencionar um usuário.');
    }

    const targetNumber = isReply ? "" : onlyNumbers(args[0]);
    const targetLid = isReply ? replyLid : `${targetNumber}@lid`;

    if (!targetLid || targetLid === "@lid") {
      throw new InvalidParameterError("Membro inválido!");
    }

    if (targetLid === BOT_LID || targetLid === OWNER_LID) {
      throw new DangerError(
        "Não é possível alterar advertências deste usuário.",
      );
    }

    const actionIndex = isReply ? 0 : 1;
    const action = args[actionIndex]?.toLowerCase();
    const allWarns = getAllWarns(remoteJid, targetLid);
    const validWarns = allWarns.filter((w) => w.valid);

    if (validWarns.length === 0) {
      return sendReply("Usuário não tem advertências válidas.");
    }

    if (action === "list") {
      let msg = `📋 *Advertências válidas de @${targetLid.split("@")[0]}:*\n\n`;
      validWarns.forEach((w, i) => {
        const date = new Date(w.timestamp).toLocaleDateString("pt-BR");
        msg += `${i + 1}. "${w.reason}" (${date})\n`;
      });

      return sendReply(msg, [targetLid]);
    }

    if (action && /^\d+$/.test(action)) {
      const index = parseInt(action, 10) - 1;
      if (index >= 0 && index < validWarns.length) {
        revokeWarnByIndex(remoteJid, targetLid, index);
        return sendReply(`✅ Advertência #${index + 1} removida.`);
      }

      throw new InvalidParameterError(
        "Informe um número de advertência válido.",
      );
    }

    if (action) {
      throw new InvalidParameterError('Use "list" ou o número da advertência.');
    }

    removeLastWarn(remoteJid, targetLid);
    await sendReply(`✅ Última advertência removida.`);
  },
};
