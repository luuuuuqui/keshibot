import { PREFIX } from "../../config.js";
import { DangerError, WarningError } from "../../errors/index.js";
import { checkIfMemberIsMuted, unmuteMember } from "../../utils/database.js";
import { onlyNumbers } from "../../utils/index.js";

export default {
  name: "unmute",
  description: "Desativa o mute de um membro do grupo",
  commands: ["unmute", "desmutar"],
  usage: `${PREFIX}unmute @usuario ou responda à mensagem do usuário`,
  handle: async ({ remoteJid, sendSuccessReply, args, isGroup, replyLid }) => {
    if (!isGroup) {
      throw new DangerError("Este comando só pode ser usado em grupos.");
    }

    if (!args.length && !replyLid) {
      throw new DangerError(
        `Você precisa mencionar um usuário ou responder à mensagem do usuário que deseja desmutar.\n\nExemplo: ${PREFIX}unmute @fulano`,
      );
    }

    if (!replyLid && !args[0]?.includes("@")) {
      throw new DangerError('Use "@" ao mencionar um usuário.');
    }

    const targetNumber = replyLid ? "" : onlyNumbers(args[0]);
    const userId = replyLid
      ? replyLid
      : targetNumber
        ? `${targetNumber}@lid`
        : null;

    if (!userId) {
      throw new DangerError("Membro inválido!");
    }

    if (!checkIfMemberIsMuted(remoteJid, userId)) {
      throw new WarningError("Este usuário não está silenciado!");
    }
    unmuteMember(remoteJid, userId);
    await sendSuccessReply("Usuário desmutado com sucesso!");
  },
};
