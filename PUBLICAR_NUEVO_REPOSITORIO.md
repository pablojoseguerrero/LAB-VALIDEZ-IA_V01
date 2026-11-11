# Publicación independiente en GitHub

## Repositorio

- Nombre del proyecto: **LAB-VALIDEZ IA_V01**.
- Nombre recomendado para GitHub (sin espacios): **LAB-VALIDEZ-IA_V01**.
- Propietario: **pablojoseguerrero**.
- Dirección prevista tras crearlo: https://github.com/pablojoseguerrero/LAB-VALIDEZ-IA_V01
- Visibilidad sugerida: pública, **solo para el código**, nunca para instrumentos con datos privados.

## Instrucciones de publicación

1. En GitHub, crea un repositorio vacío con el nombre `LAB-VALIDEZ-IA_V01`, sin inicializarlo con README ni LICENSE.
2. En una terminal situada dentro de esta carpeta ejecuta:

```bash
git init
git branch -M main
git add .
git commit -m "Publicar LAB-VALIDEZ IA V01 como proyecto independiente"
git remote add origin https://github.com/pablojoseguerrero/LAB-VALIDEZ-IA_V01.git
git push -u origin main
```

3. Comprueba que el repositorio contiene `app.py`, `engine.py`, `static/index.html`, `static/logo.png`, `CITACION.md` y `README.md`.
4. El README y la aplicación incluyen las cuatro normas de citación. El enlace bibliográfico definitivo es válido después de la publicación.
5. Para el acceso a la **aplicación ejecutable**, configura un hosting compatible con FastAPI usando `render.yaml`. GitHub Pages no ejecuta Python.

## Conservación del proyecto anterior

`PARV-LAB-GPT_V01` está reservado al taller de Skills en educación parvularia. No copies allí archivos de este proyecto. La rama `main` del repositorio anterior conservó su contenido. Una rama adicional llamada `lab-validez-ia` se restableció a `main` y puede eliminarse desde GitHub (Settings > Branches o desde el selector de ramas) cuando ya no se necesite.

© 2026 Prof. Dr. Pablo José Guerrero, PhD. RED CTII.AI.