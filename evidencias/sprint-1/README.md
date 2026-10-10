# Sprint 1 — Evidencias disponibles y por agregar

[Volver al capítulo V](../../capitulos/05-implementacion.md).

Actualización: **10 de octubre de 2026**, America/Lima.
Referencia: statement `Trabajo Final_1ASI0657_202620.docx`.
Los nombres sugeridos del checklist inicial no son rutas a archivos existentes.

**Actualización:** ya se incorporaron [13 capturas, logs y una grabación real](../deployment/README.md)
de Swagger, pytest, Newman, persistencia local y GitHub. La tabla de nombres
sugeridos de abajo conserva el checklist inicial; consultar el nuevo índice
para los archivos que ya existen. La publicación cloud espera las cuentas conectadas.

## Evidencias disponibles

| Archivo o referencia | Qué demuestra | Apartado |
| --- | --- | --- |
| [pytest.txt](pytest.txt) | Ejecución real: cuatro pruebas aprobadas sobre `6ff8141` | 5.1.1 y 5.3.1.3 |
| [respuestas-api.json](respuestas-api.json) | Ocho peticiones reales por TestClient con SQLite temporal y datos de muestra | 5.3.1.4 y 5.3.1.5 |
| [OpenAPI](../openapi.json) | Contrato del servicio actual | 5.3.1.5 |
| [Commit back](https://github.com/1ASI0657-2620-9199/back/commit/6ff8141000371271d8b91ebc8d0b7ed5fdea1906) | Incorporación de API, modelos, Repository y tests | 5.1.2 y 5.3.1.2 |
| [Commit front](https://github.com/1ASI0657-2620-9199/front/commit/e0b1ac5b272004863300c2a8a4eb2c5222a58111) | Incorporación del panel y comprobación de integración | 5.3.1.2 |
| Diagrama del capítulo V | Clientes, proceso Uvicorn/FastAPI, panel opcional y SQLite | 5.2.4 |

La [colección Postman preparada](FinanZen-Sprint1.postman_collection.json)
se ejecutó con Newman: ocho peticiones y once aserciones, sin fallos. Los logs
están en el nuevo índice; no se presenta esa ejecución como Postman Desktop.

## Preparar la demostración

Desde `back`, iniciar un servidor con una base separada para las evidencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:FINANZEN_DB_PATH = 'data/sprint1-evidence.db'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Importar la colección en Postman y mantener `baseUrl` en
`http://127.0.0.1:8000`. Ejecutar **01 a 08 en orden**. La petición 01 genera
un identificador nuevo para el usuario de muestra; así se pueden repetir las
corridas sin mezclar sus movimientos. Los POST fijan su fecha en octubre de 2026.
La colección comprueba los códigos HTTP, repetición del ID, dos movimientos
y saldo de PEN 874.50. Para reiniciar, volver a ejecutar 01.

Para capturar Swagger, usar el mismo `X-User-Id` de la colección (`evidence-`
seguido del valor `evidenceRunId`). Abrir `/docs`, seleccionar **Try it out**,
completar los datos y ejecutar. Si se crea otro movimiento, usar una clave
nueva y explicar el cambio de totales.

El frontend usa `demo-user`: no muestra automáticamente los movimientos del
usuario de Postman. Para capturar el panel, registrar datos desde la interfaz
y explicar que corresponden a otra demostración.

## Checklist inicial de capturas

Este checklist conserva los objetivos originales. Health, ingreso, repetición,
conflicto, listado, resumen, Swagger, arranque, pytest y commit ya tienen
evidencia en el [índice actualizado](../deployment/README.md), con nombres distintos.
Contribuciones, Kanban y los demás objetivos sin correspondencia siguen pendientes.
Para futuras figuras, añadir explicación, fecha, entorno y resultado.

| Nombre sugerido | Qué debe mostrar | Apartado |
| --- | --- | --- |
| `01-entorno.png` | Versiones, dependencias instaladas y herramienta usada | 5.2.1 |
| `02-pytest.png` | Comando y resultado completo de las ocho pruebas actuales | 5.1.1 / 5.3.1.3 |
| `03-repository.png` | Repository y endpoint que delega en él, con explicación | 5.1.2 |
| `04-commits.png` | Historial/diff de los commits reales de back/front | 5.3.1.2 |
| `05-health.png` | GET `/health`, URL, HTTP 200 y cuerpo | 5.3.1.4 |
| `06-create-income.png` | POST de ingreso, cabeceras, cuerpo y HTTP 201 | 5.3.1.4 |
| `07-idempotent-replay.png` | POST repetido, HTTP 200, mismo ID y `Idempotent-Replayed` | 5.3.1.4 |
| `08-idempotency-conflict.png` | Misma clave con otro importe y HTTP 409 | 5.3.1.4 |
| `09-create-expense.png` | POST de gasto y HTTP 201 | 5.3.1.4 |
| `10-list-transactions.png` | GET de movimientos y los dos registros del usuario | 5.3.1.4 |
| `11-monthly-summary.png` | Mes/moneda, ingresos 1000.00, gastos 125.50 y saldo 874.50 | 5.3.1.4 |
| `12-validation-error.png` | Mes `2026-13` y HTTP 422 | 5.3.1.4 |
| `13-swagger-endpoints.png` | Nombre/versión de API y operaciones en `/docs` | 5.3.1.5 |
| `14-swagger-execution.png` | Parámetros, ejecución y respuesta de una operación en Swagger | 5.3.1.5 |
| `15-local-startup.png` | Comando Uvicorn, arranque y URL local | 5.3.1.6 |
| `16-team-contributions.png` | Analíticas de contribuciones/commits reales de los integrantes | 5.3.1.7 |
| `17-sprint1-kanban.png` | Board con tareas, responsables y estados del Sprint 1 | 5.3.1.1 / 5.3.1.8 |

## Video de ejecución

Ya se adjunta una [grabación de Swagger y registros locales](../deployment/local/demostracion.webm),
sin narración. Para completar el formato explicativo de la entrega:

Grabar una demostración que explique el alcance y muestre health, creación de
ingreso/gasto, repetición idempotente, conflicto, listado, resumen y Swagger.
Publicar el video, comprobar acceso para el docente y agregar su enlace en
**5.3.1.4**, acompañado de descripción y marcas de tiempo reales.
Duración sugerida: 3–5 minutos; no es una duración exigida por el statement.

## Evidencias que necesitan trabajo adicional

- **BDD/Gherkin (5.3.1.3):** implementar/ejecutar archivos `.feature`, relacionar
  escenarios con historias y enlazar commits y resultados. La suite actual no los incluye.
- **Kanban (5.3.1.1 y 5.3.1.8):** URL pública y captura del board. Validar con
  el equipo tareas, responsables, estimaciones y estados; distinguir el backlog histórico.
- **Colaboración (5.3.1.7):** explicar trabajo real e incluir analíticas de GitHub,
  PR o revisiones que efectivamente existan.
- **Refactorización (5.1.4):** cambio de patrón real, código antes/después,
  commits y pruebas. Ya se añadió la separación de conexión SQLite/PostgreSQL
  en `f218113`; el capítulo V documenta ese cambio y los patrones aún pendientes.
- **Librería propia (5.1.3):** paquete reutilizable, patrones, consumo y pruebas.
  `finanzen_common` sigue siendo una propuesta.
- **Deployment:** pasos realizados durante el sprint. Añadir recursos, URL y
  capturas cloud cuando existan; el índice reserva el despliegue cloud completo para TF1.

## Reproducir los archivos de evidencia

Con `back` y `report` clonados como carpetas vecinas y las dependencias del
backend instaladas en el intérprete utilizado, ejecutar desde `report`:

```powershell
python scripts/capturar_evidencia_api.py
```

El script usa una base temporal, ejecuta la suite existente y actualiza el
JSON, log y colección. Cada ejecución tiene sus tiempos e identificadores;
si cambian los resultados, actualizar también el texto del informe.
