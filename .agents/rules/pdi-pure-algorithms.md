# Regra P0: Pureza Algorítmica em PDI (Zero OpenCV / Zero SciPy)

> **DIRETRIZ OBRIGATÓRIA E PERMANENTE**: No escopo dos algoritmos de Processamento Digital de Imagens deste projeto, é terminantemente proibido o uso de pacotes de alto nível para processamento de imagens.

---

## 🚫 1. Proibições Específicas
1. **OpenCV (`cv2`)**: É estritamente proibido importar ou utilizar OpenCV para qualquer cálculo, filtro, transformação ou inspeção.
2. **SciPy ndimage (`scipy.ndimage`)**: Proibido utilizar rotinas prontas de convolução ou interpolação do SciPy.
3. **Pillow ImageFilter (`PIL.ImageFilter`)**: Proibido aplicar filtros automáticos do PIL (ex: `BLUR`, `SHARPEN`, `CONTOUR`).
4. **Skimage (`scikit-image`)**: Proibido.

---

## ✅ 2. O que é Permitido e Exigido
1. **Formulação Matemática Pura**:
   - Todo operador deve ser escrito com loops, comprensões de lista ou funções matemáticas elementares (`math.log`, `math.exp`, `math.sqrt`).
   - Convoluções espaciais devem iterar manualmente os índices dos pixels respeitando as bordas (extensão de borda, espelhamento ou preenchimento zero).
   - Cálculos de moda, mediana, mínimo e máximo devem operar sobre listas de vizinhança.
2. **Pillow (PIL) Restrito**:
   - O uso de `PIL.Image` é estritamente limitado à conversão de Base64 para matriz de inteiros e de matriz de inteiros para PNG/Base64 em `backend/pdi/utils.py`.
3. **Clamping [0, 255] Obrigatório**:
   - Toda operação matemática que produza valores fora do intervalo $[0, 255]$ deve aplicar clamping:
     ```python
     def clamp(valor: float) -> int:
         return max(0, min(255, round(valor)))
     ```
