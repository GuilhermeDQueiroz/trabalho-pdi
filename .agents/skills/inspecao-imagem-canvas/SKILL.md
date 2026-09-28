---
name: inspecao-imagem-canvas
description: Manipulação de pixels no HTML5 Canvas, conversão Base64 para matriz 2D e inspeção de coordenadas na Ponta de Prova.
---

# Skill: Inspeção de Imagem e HTML5 Canvas

Esta skill cobre os procedimentos de manipulação da imagem no cliente (Canvas) e inspeção via Ponta de Prova.

---

## 1. Conversão Base64 <-> Matriz 2D
No frontend (`src/utils/imageUtils.ts`):
- **Base64 para Matriz**:
  1. Carrega a string em um objeto `Image()`.
  2. Desenha a imagem no Canvas com dimensões nativas (`canvas.width = image.width`).
  3. Extrai os dados brutos com `context.getImageData(0, 0, width, height).data`.
  4. Converte cada pixel RGBA em intensidade de nível de cinza:
     $$\text{intensity} = \text{round}\left(\frac{R + G + B}{3}\right)$$
  5. Agrupa em linhas e adiciona ao array bidimensional com `row.push(intensity)`.
- **Matriz para Base64**:
  1. Cria `imageData = context.createImageData(width, height)`.
  2. Preenche os canais $R, G, B$ com o valor de cinza da matriz e define $A = 255$.
  3. Executa `context.putImageData(imageData, 0, 0)`.
  4. Retorna `canvas.toDataURL('image/png')`.

---

## 2. Ponta de Prova: Coordenadas Nativas vs Tela
Ao inspecionar o pixel sob o cursor do mouse:
1. Obtenha a posição do cursor relativa ao elemento visual do Canvas:
   ```typescript
   const rect = canvas.getBoundingClientRect()
   const visualX = event.clientX - rect.left
   const visualY = event.clientY - rect.top
   ```
2. Mapeie para as coordenadas nativas da imagem:
   ```typescript
   const nativeX = Math.floor(visualX * (canvas.width / rect.width))
   const nativeY = Math.floor(visualY * (canvas.height / rect.height))
   ```
3. Consulte o Nível de Cinza ($NC$) diretamente na matriz `matriz[nativeY][nativeX]`.
