# Reporte actualizado para entrega

[FinanZen-Reporte-Actualizado.docx](FinanZen-Reporte-Actualizado.docx) conserva
los capítulos previos del documento compartido y el capítulo V histórico del
Sprint 1, verificado el 10 de octubre de 2026. La actualización del **26 de
noviembre de 2026** incorpora los apartados **5.3.3.2 Development Evidence,
5.3.3.4 Execution Evidence y 5.3.3.6 Software Deployment Evidence** del Sprint 3.
Incluye tablas, hipervínculos y nueve capturas reales de CMD con Docker y Kafka.

El [capítulo V Markdown](../capitulos/05-implementacion.md) y el
[índice de evidencias](../evidencias/cierre-sprint-1/README.md) contienen los
registros originales, código de pruebas, release y videos relacionados.

El Word conserva los **43 archivos de imagen originales** y añade **9 capturas
de CMD**, para un total de **52 archivos de imagen**. El
[índice de evidencias de Sprint 3](../evidencias/sprint-3/docker/README.md)
contiene las capturas, transcripciones, hashes y resultados originales. El
[registro de validación del Word](../evidencias/sprint-3/docker/validacion-word.json)
verifica la conservación de las imágenes y registra la revisión de redacción
del capítulo V.

Las capturas de terminal se tomaron de CMD local. El índice conserva los comandos,
las transcripciones y los resultados de cada ejecución. Los commits de la cuenta
Darkdren se atribuyen a Rodrigo Oblitas, titular de esa cuenta.

## Manual para la presentación

- [Manual de demostración en PDF](Manual-Demostracion-FinanZen.pdf).
- [Manual editable en Word](Manual-Demostracion-FinanZen.docx).
- [Guion breve para exponer](Guion-Demostracion-FinanZen.txt).
- [Sesión y capturas verificadas](manual-demo/sesion-verificada.json).

La aplicación de esta demo se ejecuta en **http://127.0.0.1:8080**, en la laptop
con Docker Desktop. El manual incluye las cuentas de ensayo y respaldo, los pasos
de la demostración, los importes esperados, Swagger y una explicación de los
cuatro servicios y Kafka. Para crear nuevas cuentas se utiliza
`back/scripts/preparar_demostracion.py`; para iniciar Docker y abrir el panel,
`back/scripts/iniciar_demostracion.cmd`.
