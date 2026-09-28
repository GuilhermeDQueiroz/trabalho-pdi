/**
 * Utilitários no front-end para conversão rápida de imagem Base64 em matriz 2D e vice-versa via HTML5 Canvas.
 */

export async function base64ToMatriz(pImagem: string): Promise<number[][]> {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.src = pImagem

    image.onload = () => {
      const canvas = document.createElement('canvas')
      const context = canvas.getContext('2d')

      if (!context) {
        reject(new Error('Contexto do canvas não disponível'))
        return
      }

      canvas.width = image.width
      canvas.height = image.height
      context.drawImage(image, 0, 0)

      const imageData = context.getImageData(0, 0, image.width, image.height)
      const pixels = imageData.data
      const matrizPixels: number[][] = []

      for (let y = 0; y < image.height; y++) {
        const row: number[] = []
        for (let x = 0; x < image.width; x++) {
          const index = (y * image.width + x) * 4
          const r = pixels[index]
          const g = pixels[index + 1]
          const b = pixels[index + 2]
          const intensity = Math.round((r + g + b) / 3.0)
          row.push(intensity)
        }
        matrizPixels.push(row)
      }

      resolve(matrizPixels)
    }

    image.onerror = () => {
      reject(new Error('Falha ao carregar a imagem'))
    }
  })
}

export async function matrizToBase64(matriz: number[][]): Promise<string> {
  return new Promise((resolve, reject) => {
    const height = matriz.length
    if (height === 0) {
      resolve('')
      return
    }
    const width = matriz[0].length

    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')

    if (!context) {
      reject(new Error('Contexto do canvas não disponível'))
      return
    }

    canvas.width = width
    canvas.height = height

    const imageData = context.createImageData(width, height)

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const intensity = Math.max(0, Math.min(255, Math.round(matriz[y][x])))
        const index = (y * width + x) * 4
        imageData.data[index] = intensity
        imageData.data[index + 1] = intensity
        imageData.data[index + 2] = intensity
        imageData.data[index + 3] = 255
      }
    }

    context.putImageData(imageData, 0, 0)
    resolve(canvas.toDataURL('image/png'))
  })
}
