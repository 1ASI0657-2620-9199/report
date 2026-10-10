# Deployment público de FinanZen

[Capítulo V](../../../capitulos/05-implementacion.md) · [Índice de evidencias](../README.md).

Publicado y verificado el **10 de octubre de 2026**, America/Lima.
El deploy inicial terminó a las **03:43:30** y la API se reinició durante la
comprobación de persistencia; el nuevo arranque figura a las **03:46:03**.
Los archivos originales conservan sus fechas UTC.

| Recurso | Valor comprobado |
| --- | --- |
| API pública | https://finanzen-financial-records.onrender.com |
| Health | https://finanzen-financial-records.onrender.com/health — HTTP 200 |
| Swagger | https://finanzen-financial-records.onrender.com/docs — HTTP 200 |
| OpenAPI | https://finanzen-financial-records.onrender.com/openapi.json — HTTP 200 |
| Render | `srv-db4vl25ckfvc738e4hp0`, Web Service, **Free**, Virginia, Python 3.11.9 |
| Deploy inicial | `dep-db4vl2tckfvc738e4j60`, **live** |
| Commit publicado | [525ac3f](https://github.com/1ASI0657-2620-9199/back/commit/525ac3fd678b72340aaec689f444301b5afe073c) |
| Neon | Proyecto `dawn-bird-07958545`, PostgreSQL 17, `aws-us-east-1`, organización **Free** |
| Compute PostgreSQL | Mínimo y máximo 0.25 CU; sin cambio de plan |
| Persistencia | `DATABASE_URL` privada en Render; datos en Neon, sin disco local de pago |

## Actividades y resultados

1. Se inspeccionaron los recursos existentes y se verificó Neon Free.
2. Se creó PostgreSQL 17 con Neon CLI y autorización del usuario.
3. Se creó Render Free por su API oficial, con repo `back/main`, build pip,
   arranque Uvicorn y health `/health`. La conexión PostgreSQL se configuró como
   variable privada con TLS verificado.
4. Render completó el build y el deploy quedó `live`.
5. Health, Swagger y OpenAPI respondieron HTTP 200. Newman ejecutó **8 peticiones,
   11 aserciones y 0 fallos** contra la URL HTTPS real.
6. Se creó un usuario sintético con ingreso PEN 105.00 y gasto PEN 12.34.
   Se solicitó el reinicio de Render por su API y se verificó el nuevo arranque
   en los logs. Después se conservaron los dos IDs, saldo **PEN 92.66** y
   repetición idempotente HTTP 200, sin duplicar el ingreso.

La prueba de persistencia usa otro usuario que la demostración Swagger/Newman;
por eso su saldo 92.66 difiere del saldo 874.50 de aquella demostración.

## Evidencias por apartado

| Archivo | Qué demuestra | Apartado |
| --- | --- | --- |
| [01-newman.png](01-newman.png) | Vista del registro real de la colección Postman ejecutada con Newman contra HTTPS | 5.3.1.3 / 5.3.1.4 |
| [03-swagger-endpoints.png](03-swagger-endpoints.png) | Operaciones y contrato público de Swagger | 5.3.1.5 |
| [04-health.png](04-health.png) | GET health público, HTTP 200 | 5.3.1.4 |
| [05-create-income.png](05-create-income.png) | POST público, HTTP 201 | 5.3.1.4 |
| [06-list.png](06-list.png) | Listado público con dos movimientos | 5.3.1.4 |
| [07-summary.png](07-summary.png) | Resumen público, saldo PEN 874.50 | 5.3.1.4 |
| [08-replay.png](08-replay.png) | Repetición pública, HTTP 200 y mismo ID | 5.3.1.4 |
| [09-conflict.png](09-conflict.png) | Conflicto público, HTTP 409 | 5.3.1.4 |
| [12-render-live.png](12-render-live.png) | Vista de respuestas reales de Render: plan, URL, deploy live y commit | 5.2.4 / 5.3.1.6 |
| [13-neon-free.png](13-neon-free.png) | Vista de respuestas reales de Neon: organización Free y PostgreSQL | 5.2.4 / 5.3.1.6 |
| [14-render-build.png](14-render-build.png) | Vista del log real de build successful e instalación | 5.3.1.6 |
| [15-render-runtime.png](15-render-runtime.png) | Vista del log real de arranque, peticiones y nuevo arranque | 5.3.1.6 |
| [16-persistence.png](16-persistence.png) | IDs y saldo conservados después del reinicio remoto | 5.3.1.6 |
| [demostracion.webm](demostracion.webm) | Grabación real de Swagger contra la URL pública, sin narración | 5.3.1.4 |

Las vistas de respuestas/logs de los proveedores están identificadas como tales;
no imitan los dashboards de Render/Neon ni Postman Desktop. Las capturas de
Swagger muestran peticiones reales al servicio público.

## Registros originales

- [Servicio y configuración Render](render-service.json), con nombres de variables, sin valores privados.
- [Deploys y commit](render-deploys.json).
- [Recursos y plan Neon](neon-resources.json).
- [Build](render-build-logs.json) y [runtime](render-runtime-logs.json).
- [Solicitud de reinicio](reinicio-solicitud.json) y [persistencia verificada](persistencia.json).
- [Endpoints HTTP 200](public-endpoints.json) y [OpenAPI publicado](openapi.json).
- [Newman: log](newman.txt), [reporte JSON](newman.json) y [operaciones Swagger](swagger-http.json).
- [Fecha, URL y commit de la captura](metadata.json).

Los registros contienen solo datos de demostración y configuración publicable.
Las claves de acceso y la conexión PostgreSQL no se incluyen en estas evidencias.
