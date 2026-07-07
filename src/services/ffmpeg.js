/**
 * Serviços de processamento de imagens usando ffmpeg.
 *
 */
import { exec } from "child_process";
import webp from "node-webpmux";
import fs from "node:fs";
import path from "node:path";
import { TEMP_DIR } from "../config.js";
import { getRandomNumber, removeFileIfExists } from "../utils/index.js";
import { errorLog } from "../utils/logger.js";

class Ffmpeg {
  constructor() {
    this.tempDir = TEMP_DIR;
  }

  async _executeCommand(command) {
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          errorLog(`Command error: ${stderr}`);
          return reject(error);
        }
        resolve(stdout);
      });
    });
  }

  async _createTempFilePath(extension = "png") {
    return path.join(
      this.tempDir,
      `${getRandomNumber(10_000, 99_999)}.${extension}`,
    );
  }

  async _extractFirstAnimatedWebpFrame(inputPath) {
    const image = new webp.Image();
    await image.load(inputPath);

    if (!image.hasAnim) {
      return null;
    }

    const [firstFrameBuffer] = await image.demux({
      buffers: true,
      frame: 0,
    });

    if (!firstFrameBuffer) {
      throw new Error("Nao foi possivel extrair o primeiro frame da figurinha.");
    }

    const firstFramePath = await this._createTempFilePath("webp");
    await fs.promises.writeFile(firstFramePath, firstFrameBuffer);

    return firstFramePath;
  }

  async applyBlur(inputPath, intensity = "7:5") {
    const outputPath = await this._createTempFilePath();
    const command = `ffmpeg -i ${inputPath} -vf boxblur=${intensity} ${outputPath}`;
    await this._executeCommand(command);
    return outputPath;
  }

  async convertToGrayscale(inputPath) {
    const outputPath = await this._createTempFilePath();
    const command = `ffmpeg -i ${inputPath} -vf format=gray ${outputPath}`;
    await this._executeCommand(command);
    return outputPath;
  }

  async mirrorImage(inputPath) {
    const outputPath = await this._createTempFilePath();
    const command = `ffmpeg -i ${inputPath} -vf hflip ${outputPath}`;
    await this._executeCommand(command);
    return outputPath;
  }

  async adjustContrast(inputPath, contrast = 1.2) {
    const outputPath = await this._createTempFilePath();
    const command = `ffmpeg -i ${inputPath} -vf eq=contrast=${contrast} ${outputPath}`;
    await this._executeCommand(command);
    return outputPath;
  }

  async applyPixelation(inputPath) {
    const outputPath = await this._createTempFilePath();
    const command = `ffmpeg -i ${inputPath} -vf 'scale=iw/6:ih/6, scale=iw*10:ih*10:flags=neighbor' ${outputPath}`;
    await this._executeCommand(command);
    return outputPath;
  }

  async convertStickerToImage(inputPath) {
    const outputPath = await this._createTempFilePath();
    let firstFramePath = null;

    try {
      firstFramePath = await this._extractFirstAnimatedWebpFrame(inputPath);

      const sourcePath = firstFramePath || inputPath;
      const command = `ffmpeg -y -i "${sourcePath}" "${outputPath}"`;
      await this._executeCommand(command);
    } finally {
      removeFileIfExists(firstFramePath);
    }

    return outputPath;
  }

  async cleanup(filePath) {
    removeFileIfExists(filePath);
  }
}

export { Ffmpeg };
