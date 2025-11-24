# 🌍 Multilingual Voice Cloning System

Sistema avanzado de clonación de voz y generación de reels en múltiples idiomas usando modelos locales.

## ✨ Características

### 🎙️ Voice Cloning
- **Modelo:** Coqui TTS XTTS-v2
- **Idiomas soportados:** 16 idiomas
- **Calidad:** Clonación de voz de alta fidelidad
- **Local:** 100% en tu máquina, sin APIs externas

### 🌐 Traducción Automática
- **Modelo:** MarianMT (Helsinki-NLP)
- **Pares de idiomas:** 9 pares principales
- **Precisión:** Traducción de calidad profesional
- **Offline:** Modelos descargables para uso local

### 🎬 Generación de Reels
- **Formato:** Videos verticales 9:16 (1080x1920)
- **Duración:** 20 segundos
- **Idiomas:** Generación simultánea en múltiples idiomas
- **Audio:** Tu voz clonada en cada idioma

## 📋 Idiomas Soportados

| Idioma | Código | Voice Cloning | Traducción |
|--------|--------|---------------|------------|
| English | `en` | ✅ | ✅ |
| Español | `es` | ✅ | ✅ |
| Français | `fr` | ✅ | ✅ |
| Deutsch | `de` | ✅ | ✅ |
| Italiano | `it` | ✅ | ✅ |
| Português | `pt` | ✅ | ✅ |
| Русский | `ru` | ✅ | ✅ |
| 中文 | `zh-cn` | ✅ | ✅ |
| 日本語 | `ja` | ✅ | ✅ |
| العربية | `ar` | ✅ | ✅ |
| Polski | `pl` | ✅ | ❌ |
| Türkçe | `tr` | ✅ | ❌ |
| Nederlands | `nl` | ✅ | ❌ |
| Čeština | `cs` | ✅ | ❌ |
| Magyar | `hu` | ✅ | ❌ |
| 한국어 | `ko` | ✅ | ❌ |

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar PyTorch (con CUDA si tienes GPU)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Instalar Coqui TTS
pip install TTS

# Instalar Transformers para traducción
pip install transformers sentencepiece
```

### 2. Descargar Modelos (Opcional)

Los modelos se descargan automáticamente la primera vez que los usas, pero puedes pre-descargarlos:

```python
from TTS.api import TTS
from transformers import MarianMTModel, MarianTokenizer

# Descargar modelo de voice cloning
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Descargar modelos de traducción
MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-es")
MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
# ... etc
```

## 💻 Uso

### Opción 1: Web UI (Recomendado)

```bash
# 1. Iniciar el backend API
python api/multilingual_api.py

# 2. En otra terminal, iniciar el frontend
cd web
npm install
npm run dev

# 3. Abrir http://localhost:5173
```

#### Pasos en la UI:
1. **Escribir script** (20 segundos, ~50 palabras)
2. **Grabar tu voz** (click en el micrófono)
3. **Seleccionar idiomas** objetivo
4. **Generar reels** (click en el botón)
5. **Descargar videos** generados

### Opción 2: Python Script

```python
from video_generator.voice_cloning import MultilingualReelGenerator

# Configuración
generator = MultilingualReelGenerator(
    reference_audio="path/to/your/voice.wav",
    output_dir="output/audio"
)

# Script
script = """
    Discover this amazing open source project that solves
    a common developer problem. Check it out!
"""

# Generar audio en múltiples idiomas
audio_files = generator.generate_multilingual_audio(
    script=script,
    repo_name="my-project",
    target_languages=["en", "es", "fr", "de"]
)

# Resultado: {'en': 'path/to/en.wav', 'es': 'path/to/es.wav', ...}
```

### Opción 3: Script Demo

```bash
# Editar scripts/demo_multilingual.py con tu audio de referencia
python scripts/demo_multilingual.py
```

## 🎯 Workflow Completo

```
1. Grabar Voz de Referencia
   └─> Tu voz (10-30 segundos)

2. Escribir Script
   └─> Texto en inglés (~50 palabras)

3. Traducción Automática
   └─> MarianMT traduce a idiomas objetivo

4. Voice Cloning
   └─> XTTS-v2 genera audio con tu voz en cada idioma

5. Generación de Video
   └─> MoviePy crea reels de 20s con:
       - Audio clonado
       - Imágenes del proyecto
       - Transiciones suaves
       - Text overlays

6. Resultado
   └─> Videos listos para publicar en múltiples idiomas
```

## 📊 Requisitos del Sistema

### Mínimos
- **CPU:** Intel i5 / AMD Ryzen 5
- **RAM:** 8 GB
- **Almacenamiento:** 10 GB (para modelos)
- **GPU:** Opcional (acelera generación)

### Recomendados
- **CPU:** Intel i7 / AMD Ryzen 7
- **RAM:** 16 GB
- **GPU:** NVIDIA con 6+ GB VRAM
- **Almacenamiento:** 20 GB SSD

## ⚡ Optimización

### Con GPU (CUDA)
```python
# Los modelos detectan automáticamente CUDA
# Aceleración: 5-10x más rápido
```

### Sin GPU (CPU)
```python
# Funciona perfectamente en CPU
# Tiempo: ~30-60 segundos por idioma
```

## 🎨 Personalización

### Cambiar Voz
```python
# Usa diferentes voces de referencia
generator = MultilingualReelGenerator(
    reference_audio="different_voice.wav"
)
```

### Ajustar Velocidad
```python
voice_cloner.clone_voice(
    text=text,
    reference_audio=ref,
    output_path=out,
    language="es",
    # Parámetros adicionales (si el modelo los soporta)
)
```

### Idiomas Personalizados
```python
# Agregar más pares de traducción
translator.language_pairs["en-ko"] = "Helsinki-NLP/opus-mt-en-ko"
```

## 🔧 Troubleshooting

### Error: "CUDA out of memory"
```bash
# Reducir batch size o usar CPU
export CUDA_VISIBLE_DEVICES=""
```

### Error: "Model not found"
```bash
# Descargar manualmente
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### Audio de baja calidad
- Usa un micrófono de mejor calidad
- Graba en un ambiente silencioso
- Habla claramente y naturalmente
- Proporciona 15-30 segundos de referencia

## 📚 Recursos

- [Coqui TTS Documentation](https://github.com/coqui-ai/TTS)
- [XTTS-v2 Paper](https://arxiv.org/abs/2311.13343)
- [MarianMT Models](https://huggingface.co/Helsinki-NLP)
- [Transformers Documentation](https://huggingface.co/docs/transformers)

## 🤝 Contribuir

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para guías de desarrollo.

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE) para detalles.

---

**Hecho con ❤️ usando modelos de código abierto**
