# LAB-VALIDEZ IA V1.0 — RED CTII.AI

Aplicación web funcional con 13 secciones de navegación, fundamentación y simulación de juicio de expertos, V de Aiken, Lawshe, prueba binomial y Kappa de Cohen; lectura de PDF/DOCX/TXT/CSV, revisión editable de ítems, fichas de validación, carga CSV de valoraciones reales, cálculo del lado del servidor y exportaciones CSV/DOCX/PDF.

**Autor y titular de derechos:** © 2026 Prof. Dr. Pablo José Guerrero, PhD. RED CTII.AI. Todos los derechos reservados.

## Instalación

```bash
python -m pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000
```

Abrir http://127.0.0.1:8000 . Los datos de los documentos se procesan sin persistencia en el prototipo; no existe base de datos multiusuario ni autenticación. **No subir datos personales sensibles a un servidor público sin implementar seguridad.**

## Publicación

Incluye `render.yaml` y `Procfile` para despliegue en servicios compatibles con FastAPI. La URL definitiva se obtiene solamente al desplegar la aplicación en la cuenta y dominio del titular. Un enlace de ejemplo no implica que la web esté publicada.

## Formato de los datos de expertos

CSV UTF-8, encabezados **item,criterion,expert,value**. Cada experto emite una valoración por cada combinación ítem/criterio, sin duplicados. Para Aiken se esperan enteros entre 1 y 5; Lawshe usa `esencial`, `útil` o `no necesaria`; la prueba binomial usa `sí` o `no`. Los datos de ejemplo están expresamente identificados como simulados.

## Límites metodológicos y de esta versión

- El reconocimiento de ítems de PDF/DOCX es heurístico y **siempre requiere revisión manual**; no es todavía un agente semántico conectado a un LLM.
- El cuadro de categorización se extrae para revisión; no se infiere con garantía de precisión el mapeo de categorías e indicadores.
- PDF escaneado (solo imagen) requiere OCR previo; carga XLSX debe exportarse a CSV UTF-8.
- El módulo de estructura interna explica KMO/Bartlett y bloquea su uso incorrecto sobre preguntas abiertas; el motor factorial para escalas estructuradas no está implementado en esta versión.
- Los reportes no certifican automáticamente validez; requieren interpretación académica y revisión humana.
- La ficha DOC compatible con Word se genera en HTML; informe final se exporta como DOCX y PDF reales.

Referencia: Sánchez Espejo, F. G. (2020). *Estadística para tesis y uso del SPSS*. Centrum Legalis.

## Acceso al código fuente y citación académica

- **Código fuente:** https://github.com/pablojoseguerrero/LAB-VALIDEZ-IA_V01
- **Citas académicas:** revisar [CITACION.md](CITACION.md) y la sección **13 · Cómo citar** de la interfaz (APA 7.ª, APA 6.ª, IEEE y Vancouver).
- **Acceso público a la aplicación:** pendiente de despliegue externo del servidor FastAPI; GitHub Pages por sí solo no ejecuta el backend Python.

> **Repositorio independiente:** `pablojoseguerrero/LAB-VALIDEZ-IA_V01`. No corresponde al proyecto `PARV-LAB-GPT_V01`, que es exclusivo del taller de educación parvularia.