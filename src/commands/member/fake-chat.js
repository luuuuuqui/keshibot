import { PREFIX } from "../../config.js";
import { InvalidParameterError } from "../../errors/index.js";
import { onlyNumbers } from "../../utils/index.js";

export default {
  name: "fake-chat",
  description: "Cria uma citação falsa mencionando um usuário",
  commands: ["fake-chat", "fq", "fake-quote", "f-quote", "fk"],
  usage: `${PREFIX}fake-chat @usuário / texto citado / mensagem que será enviada`,
  handle: async ({ remoteJid, socket, args }) => {
    if (args.length !== 3) {
      throw new InvalidParameterError(
        `Uso incorreto do comando. Exemplo: ${PREFIX}fake-chat @usuário / texto citado / mensagem que será enviada`
      );
    }

    const quotedText = args[1];
    const responseText = args[2];

    const mentionedNumber = onlyNumbers(args[0]);
    const mentionedLid = mentionedNumber ? `${mentionedNumber}@lid` : null;

    if (!mentionedLid) {
      throw new InvalidParameterError("Mencione um usuário válido.");
    }

    if (quotedText.length < 2) {
      throw new InvalidParameterError(
        "O texto citado deve ter pelo menos 2 caracteres."
      );
    }

    if (responseText.length < 2) {
      throw new InvalidParameterError(
        "A mensagem de resposta deve ter pelo menos 2 caracteres."
      );
    }

    const fakeQuoted = {
      key: {
        fromMe: false,
        participant: mentionedLid,
        remoteJid,
      },
      message: {
        extendedTextMessage: {
          text: quotedText,
          contextInfo: {
            mentionedJid: [mentionedLid],
          },
        },
      },
    };

    await socket.sendMessage(
      remoteJid,
      { text: responseText },
      { quoted: fakeQuoted }
    );
  },
};
