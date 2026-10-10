# Validación — Repositorios independientes de FinanZen

Fecha de organización: **10 de octubre de 2026**, America/Lima.
Entorno local: Windows, Python 3.11.9 y Node.js 24.14.1.

## Repositorios

[Enlace común de la organización](https://github.com/orgs/1ASI0657-2620-9199/repositories).

| Repositorio | Contenido | Validación |
| --- | --- | --- |
| [back](https://github.com/1ASI0657-2620-9199/back) | API y pruebas | pytest, ejecutable sin otros repositorios |
| [front](https://github.com/1ASI0657-2620-9199/front) | Panel y script de integración | Sintaxis JavaScript e integración con back |
| [report](https://github.com/1ASI0657-2620-9199/report) | Informe, fuentes, diagramas y evidencias | Enlaces internos e integridad del PDF |
| [landing](https://github.com/1ASI0657-2620-9199/landing) | README y configuración inicial | Pendiente de código, según indicación del usuario |
| [mobile](https://github.com/1ASI0657-2620-9199/mobile) | README y configuración inicial | Pendiente de código, según indicación del usuario |

Cada repositorio contiene su propio historial Git. Los enlaces entre proyectos
apuntan a GitHub; los enlaces relativos del informe se resuelven dentro de report.

## Suite del backend

La validación vigente para la preparación cloud está en
[deployment](deployment/README.md): **8 passed in 1.43s** con SQLite/PostgreSQL,
8 peticiones y 11 aserciones Newman sin fallos, capturas de Swagger y reinicio
del proceso Uvicorn conservando IDs. Los registros siguientes preservan las
comprobaciones anteriores a la incorporación de PostgreSQL.

El [workflow del backend](https://github.com/1ASI0657-2620-9199/back/actions/runs/38037169861)
también terminó con éxito sobre `f218113`. Se adjuntan
[captura real de GitHub](deployment/local/12-github-actions.png) y
[estado consultado por API](deployment/local/github-actions.json).

Dentro del repositorio `back`, con sus dependencias instaladas:

```powershell
python -m pytest -q -p no:cacheprovider
```

Las cuatro pruebas usan bases temporales y comprueban:

- Creación idempotente y conflicto al reutilizar una clave con otro cuerpo.
- Resumen mensual y filtrado de movimientos por identificador de usuario.
- Entrega de un frontend configurado por variable de entorno.
- Ejecución de la API sin un frontend disponible.

Resultado observado: **4 passed in 1.00s**.

En la ampliación del capítulo V se volvió a ejecutar la misma suite el
10 de octubre de 2026: **4 passed in 0.77s**. La [salida capturada](sprint-1/pytest.txt)
identifica el commit y la hora de ejecución en America/Lima. Se conservaron
[ocho respuestas reales](sprint-1/respuestas-api.json) obtenidas con TestClient,
SQLite temporal y datos de muestra. La [guía del Sprint 1](sprint-1/README.md)
conserva el checklist original. Las nuevas capturas técnicas se incorporaron
en deployment; colaboración, Kanban y la publicación cloud siguen pendientes.

## Frontend e integración

Clonar `back` y `front` en un mismo directorio padre. Dentro de `front`:

```powershell
node --check app.js
python scripts/verificar_integracion.py
```

Se comprueban HTML, CSS y JavaScript servidos desde el repositorio vecino,
health, Swagger, OpenAPI, registro, consulta y resumen mediante una base temporal.

Sintaxis JavaScript: correcta. Resultado de integración:

```text
Independent front/back integration OK.
```

## Reporte

Dentro de este repositorio:

```powershell
python scripts/verificar_documentacion.py
```

Se verifican los enlaces internos y la integridad del PDF original de 109 páginas.
El [contrato OpenAPI](openapi.json) corresponde al servicio incorporado y se
conserva la transcripción completa de la fuente.

SHA-256 del PDF:

```text
b81f72f9f9c03d0c70d0dcd8934043ee67e3286bf2df98885a912e1040bbdc58
```

Resultado observado:

```text
Report: 58 internal links OK; original PDF checksum OK.
```

Después de ampliar el capítulo V y agregar la guía del Sprint 1, el verificador
reporta **73 enlaces internos correctos** y mantiene intacto el checksum del PDF.
La colección preparada contiene ocho peticiones; sus scripts JavaScript pasan
la comprobación de sintaxis de Node. Posteriormente se ejecutó con Newman y
se capturó Swagger; consultar el índice de deployment. No se presenta como
una ejecución de la interfaz de Postman Desktop.

## Integración continua y límites

Los repositorios back, front y report tienen workflows independientes. Sus
resultados remotos deben consultarse en GitHub Actions. Las capturas de Postman
y del repositorio platform son evidencia histórica del PDF.

Las pruebas locales no demuestran autenticación real, despliegue cloud,
rendimiento con 50 usuarios, IoT, proyecciones ni auditoría. Landing y mobile
continúan preparados sin implementación.
