# Cierre verificable del Sprint 1

Fecha: 10 de octubre de 2026 (America/Lima). Backend v0.1.1, biblioteca 0.1.0.

| Evidencia | Apartado | Qué acredita |
| --- | --- | --- |
| [pytest.txt](pytest.txt) / [captura](pytest.png) | 5.1.1 | Doce pruebas aprobadas con PostgreSQL 17 real |
| [build](library-build.txt) / [captura](library-build.png) | 5.1.3 | Construcción de wheel y sdist del paquete |
| [BDD local](bdd-local.txt) / [captura](bdd-local.png) | 5.3.1.3 | Seis escenarios y 29 pasos aprobados |
| [BDD público](bdd-public.txt) | 5.3.1.3 | Cinco escenarios públicos; uno local excluido |
| [CI](github-actions.json) / [captura](github-actions.png) | 5.2.2 / 5.3.1.3 | Workflows y commits reales aprobados |
| [PR feature](pr-back-1.json) / [captura](github-feature-pr.png) | 5.2.2 / 5.3.1.2 | Integración de feature a develop |
| [Release](github-release.json) | 5.1.3 / 5.2.2 | SemVer y distribución descargable |
| [C4 Deployment](../../arquitectura/deployment.png) / [DSL](../../arquitectura/deployment.dsl) | 5.2.4 | Diagrama de la infraestructura implementada |
| [Validación DSL](structurizr-validation.txt) / [export](structurizr-export.txt) | 5.2.4 | Modelo validado y exportado mediante Structurizr |
| [Trello](trello-board.json) / [captura](trello-board.png) | 5.3.1.1 / 5.3.1.8 | Board público real: doce tarjetas en DONE |
| [Contribuciones](github-collaboration.json) | 5.3.1.7 | Usuarios y commits reales; solo Darkdren comprobado |
| [Nueva publicación Render](render-release-deploy.json) | 5.3.1.6 | Release 0.1.1 activa en Render Free |
| [Compatibilidad anterior](legacy-idempotency.json) | 5.1.3 / 5.1.4 / 5.3.1.6 | Movimiento sintético previo conservado; replay 200 sin duplicados |
| [Newman](publico/newman.json) / [captura](publico/01-newman.png) | 5.3.1.4 | Colección Postman: ocho solicitudes y once aserciones |
| [HTTP Swagger](publico/swagger-http.json) / [captura](publico/03-swagger-endpoints.png) | 5.3.1.4 / 5.3.1.5 | Operaciones HTTPS reales contra 0.1.1 |
| [OpenAPI](openapi.json) | 5.3.1.5 | Contrato publicado |
| [Video explicado](demostracion-explicada.mp4) / [timing y guion](video-timeline.json) | 5.3.1.4 | Capturas reales con voz sintética identificada |
| [Grabación del navegador](publico/demostracion.webm) | 5.3.1.4 | Interacción real de Swagger; sin narración |
| [Actualización Google Docs](google-doc-update.json) | Capítulo V | Veinte apartados guardados, capítulos anteriores conservados y enlaces de evidencia comprobados |

Las capturas de registros son vistas identificadas de salidas originales; no
se presentan como interfaces de proveedores. Las imágenes Swagger, Trello y
GitHub muestran páginas reales. Las credenciales no forman parte del reporte.
Los montos corresponden exclusivamente a usuarios sintéticos de evidencia.
La participación individual de todos los integrantes y la aceptación docente
del proveedor no se declaran completadas sin evidencia externa.
