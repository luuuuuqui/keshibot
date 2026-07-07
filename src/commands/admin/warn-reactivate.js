import { BOT_LID, OWNER_LID } from "../../config.js";
import { DangerError, InvalidParameterError } from "../../errors/index.js";
import { onlyNumbers } from "../../utils/index.js";
import { getAllWarns, reactivateWarnByIndex } from "../../utils/warnSystem.js";

export default {
  name: "warn-reactivate",
  description: "Reativa uma advertência inválida.",
  commands: [
    "warn-reactivate",
    "reativarwarn",
    "reativaradvertencia",
    "reativaradvt",
  ],
  handle: async ({ args, isReply, replyLid, remoteJid, sendReply }) => {
    let targetLid = null;

    if (isReply && replyLid) {
      targetLid = replyLid;
    } else if (args[0]?.includes("@")) {
      const targetNumber = onlyNumbers(args[0]);
      targetLid = targetNumber ? `${targetNumber}@lid` : null;
    } else {
      throw new InvalidParameterError(
        "Mencione um usuário ou responda a uma mensagem.",
      );
    }

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
    const invalidWarns = allWarns.filter((w) => !w.valid);

    if (invalidWarns.length === 0) {
      return sendReply("Usuário não tem advertências inválidas.");
    }

    if (action === "list") {
      let msg = `📋 *Advertências inválidas de @${targetLid.split("@")[0]}:*\n\n`;
      invalidWarns.forEach((w, i) => {
        const date = new Date(w.timestamp).toLocaleDateString("pt-BR");
        msg += `${i + 1}. "${w.reason}" (${date})\n`;
      });
      return sendReply(msg, [targetLid]);
    }

    if (action && /^\d+$/.test(action)) {
      const index = parseInt(action, 10) - 1;
      if (index >= 0 && index < invalidWarns.length) {
        if (reactivateWarnByIndex(remoteJid, targetLid, index)) {
          return sendReply(`✅ Advertência #${index + 1} reativada.`);
        }
      }

      throw new InvalidParameterError(
        "Informe um número de advertência válido.",
      );
    }

    if (action) {
      throw new InvalidParameterError('Use "list" ou o número da advertência.');
    }

    const lastIndex = invalidWarns.length - 1;

    if (reactivateWarnByIndex(remoteJid, targetLid, lastIndex)) {
      await sendReply(`✅ Última advertência inválida reativada.`);
    } else {
      await sendReply("❌ Falha ao reativar advertência.");
    }
  },
};
