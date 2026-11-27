"""Build the presentation manual from the actual local demo and UI captures."""

from hashlib import sha256
import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "entrega"
LIVE = json.loads((ROOT.parent / "back/reports/presentacion/presentacion.json").read_text(encoding="utf-8"))
BACKUP = json.loads((ROOT.parent / "back/reports/presentacion/respaldo.json").read_text(encoding="utf-8"))
doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Inches(8.5), Inches(11)
section.top_margin = section.bottom_margin = Inches(0.65)
section.left_margin = section.right_margin = Inches(0.8)
normal = doc.styles["Normal"]
normal.font.name, normal.font.size = "Calibri", Pt(10.5)
normal.paragraph_format.space_after = Pt(6)
for name in ("Title", "Heading 1", "Heading 2"):
    doc.styles[name].font.name = "Calibri"
    doc.styles[name].font.color.rgb = RGBColor.from_string("164D3B")
doc.styles["Heading 1"].font.size = Pt(20)
doc.styles["Heading 2"].font.size = Pt(13)
header = section.header.paragraphs[0]
header.text = "FINANZEN  /  GUÍA PARA LA PRESENTACIÓN"
header.runs[0].font.size = Pt(8)
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run("FinanZen · ")
field = OxmlElement("w:fldSimple");field.set(qn("w:instr"), "PAGE");footer._p.append(field)
doc.core_properties.title = "FinanZen — Manual de demostración"
doc.core_properties.author = "Rodrigo Oblitas"


def p(text, bold=False):
    para = doc.add_paragraph()
    para.add_run(text).bold = bold
    return para


def h(text):
    doc.add_heading(text, 2)


def page(title, first=False):
    if not first:
        doc.add_page_break()
    doc.add_heading(title, 1)


def code(text):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.font.name, run.font.size = "Consolas", Pt(8.5)
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after = Pt(8)


def table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.autofit = False
    if len(headers) == 2:
        first = 0.55 if headers[0] == "Paso" else 2.25
        widths = [first, 6.9 - first]
    elif len(headers) == 3:
        widths = [1.3, 3.4, 2.2]
    else:
        widths = [6.9 / len(headers)] * len(headers)
    for column, width in zip(t.columns, widths):
        column.width = Inches(width)
    for c, text in zip(t.rows[0].cells, headers):
        c.text = text
        for run in c.paragraphs[0].runs:
            run.bold = True
    for row in rows:
        for c, text in zip(t.add_row().cells, row):
            c.text = str(text)
    for index, row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        if index == 0:
            row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
        for c, width in zip(row.cells, widths):
            c.width = Inches(width)
            shading = OxmlElement("w:shd")
            shading.set(qn("w:fill"), "164D3B" if index == 0 else "EFF6F2" if index % 2 else "FFFFFF")
            c._tc.get_or_add_tcPr().append(shading)
            for paragraph in c.paragraphs:
                paragraph.paragraph_format.space_after = Pt(3)
                for run in paragraph.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor.from_string("FFFFFF" if index == 0 else "243830")
    doc.add_paragraph()


def picture(name, caption, max_height=3.8):
    path = OUTPUT / "manual-demo/capturas" / (name + ".png")
    with Image.open(path) as im:
        width = min(6.5, max_height * im.width / im.height)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.keep_with_next = True
    para.add_run().add_picture(str(path), width=Inches(width))
    caption_p = p(caption)
    caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_p.runs[0].font.size = Pt(8)


page("FinanZen | Manual de demostración", True)
p("Recorrido de 10 minutos para explicar la aplicación y demostrar los Sprints 2 y 3.", True)
p("Versión de demostración verificada el 26 de noviembre de 2026. Expositor: Rodrigo Oblitas.")
h("Abrir la aplicación")
code(LIVE["url"])
p("Esta dirección abre la aplicación completa en la laptop donde corre Docker Desktop. Los cuatro servicios, Kafka y Nginx se ejecutan localmente. El navegador de otro equipo necesita un despliegue público o una conexión configurada hacia esta laptop.")
table(["Cuenta preparada", "Identificador que debes elegir en Cuenta demo"], [
    ("Exposición en vivo: solo ingreso inicial", LIVE["user_id"]),
    ("Respaldo: recorrido ya terminado", BACKUP["user_id"]),
])
p("Entra con la cuenta de exposición. La cuenta de respaldo sirve para mostrar el resultado final sin repetir operaciones. Las capturas de este manual corresponden al respaldo.")
picture("01-resumen", "Resumen al completar el recorrido: S/ 1,000 de ingresos, S/ 105 de gastos y S/ 895 de balance.", 3.6)

page("1. Preparar la exposición")
p("Abre la carpeta FinanZen/back en VS Code. En una terminal CMD ejecuta:")
code("docker compose up -d --wait --wait-timeout 240\ndocker compose ps")
p("Comprueba seis servicios running/healthy: financial-records, budget-service, notification-service, device-service, kafka y web. kafka-init y kafka-permissions son tareas de arranque y terminan con código 0.")
h("Si quieres una cuenta nueva para ensayar")
code("python scripts/preparar_demostracion.py\npython scripts/preparar_demostracion.py --completa")
p("El primer comando crea una cuenta nueva con S/ 1,000 de ingreso en el mes actual e historial del mes anterior. El segundo crea otra cuenta con el recorrido terminado. Cada ejecución imprime un identificador distinto y conserva los datos de otras cuentas. Los identificadores más recientes están en back/reports/presentacion/.")
p("En la aplicación: Cuenta demo → escribe el identificador → Cambiar cuenta demo. Elige el periodo actual; esta sesión se preparó para " + LIVE["month"] + ". Si expones otro mes, prepara cuentas nuevas.")
table(["Tiempo", "Qué mostrar"], [("0:00–1:00", "Problema que resuelve y Resumen"),
    ("1:00–4:00", "Presupuesto, gastos y alertas"), ("4:00–7:00", "Dispositivo, consumo y reenvío idempotente"),
    ("7:00–8:00", "Reporte semanal y recomendación"), ("8:00–10:00", "Servicios, Docker, Kafka y cierre")])
h("Introducción que puedes decir")
p("“FinanZen ayuda a organizar ingresos y gastos, controlar presupuestos por categoría y entender el consumo de dispositivos. Voy a mostrar cómo un gasto actualiza un presupuesto y genera una alerta, y cómo una lectura de consumo se registra sin cambiar el dinero de la cuenta.”")
p("Deja abiertos el panel y una terminal en back. Para explicar las APIs, prepara también las pestañas Swagger indicadas más adelante.")

page("2. Presupuesto y registro de gastos")
p("La cuenta de exposición empieza con ingreso S/ 1,000, gasto S/ 0 y balance S/ 1,000. La lista del mes tiene un movimiento; el historial de recomendaciones pertenece al mes anterior.")
table(["Paso", "Acción en la aplicación"], [
    ("1", "Presupuestos → Crear presupuesto: Alimentación, límite 100, avisar al 80 % → Guardar presupuesto."),
    ("2", "Resumen → Registrar movimiento: Gasto, 85, Alimentación, fecha actual, descripción Compra de la semana → Guardar movimiento."),
    ("3", "Presupuestos: espera unos segundos. Se muestran S/ 85 de S/ 100, 85 % y Cerca del límite."),
    ("4", "Resumen → Registrar movimiento: otro gasto de 20, Alimentación, Compra adicional. El presupuesto llega a 105 % y muestra Límite alcanzado."),
])
table(["Momento", "Gastos", "Balance", "Uso del presupuesto"], [
    ("Inicial", "S/ 0", "S/ 1,000", "0 %"), ("Después de gastar 85", "S/ 85", "S/ 915", "85 %"),
    ("Después de gastar otros 20", "S/ 105", "S/ 895", "105 %")])
p("Qué decir: “El saldo representa los movimientos confirmados. El presupuesto compara mis gastos de alimentación con el límite que definí para el mes.”")
picture("02-presupuestos", "Presupuesto de Alimentación después de los dos gastos.", 3.2)

page("3. Alertas y comunicación por eventos")
table(["Acción", "Qué comprobar"], [
    ("Abre Alertas después del primer gasto", "Aparece Tu presupuesto se acerca al límite; el aviso corresponde al umbral del 80 %."),
    ("Después del gasto adicional", "Aparece Límite de presupuesto alcanzado; corresponde al umbral del 100 %."),
    ("Pulsa Marcar como leída en una alerta", "Cambia su estado. En el filtro Sin leer deja de aparecer esa alerta."),
    ("Abre Preferencias", "Hay opciones para avisos de presupuestos y consumo. Mantén ambas activadas durante el recorrido."),
])
p("Qué decir: “El servicio financiero registra el gasto y publica TransactionRecorded. Budget procesa el evento y, al cruzar un umbral, publica BudgetThresholdReached. Notification recibe ese evento y entrega el aviso en la bandeja.”")
p("El panel actualiza la información cada cuatro segundos mientras está visible y no hay un formulario abierto. También puedes usar el botón Actualizar información. El aviso puede aparecer unos segundos después del registro porque el flujo es asíncrono.")
picture("03-alertas", "El respaldo incluye dos avisos de presupuesto y, tras la etapa IoT, un aviso de consumo.", 3.9)

page("4. Dispositivo y consumo de energía")
table(["Paso", "Acción y resultado"], [
    ("1", "Dispositivos → Agregar dispositivo: Medidor de casa, Medidor simulado, límite 20 kWh y tarifa 0.75 → Guardar dispositivo."),
    ("2", "Simular lectura: consumo 15000, unidad Wh → Enviar lectura. Se muestran 15 kWh, S/ 11.25 y una lectura única."),
    ("3", "Pulsa Reenviar última lectura. El total sigue en 15 kWh y la tabla conserva una lectura."),
    ("4", "Simular lectura: consumo 10000, unidad Wh. Se acumulan 25 kWh, S/ 18.75 y dos lecturas únicas."),
    ("5", "Abre Alertas: aparece Límite de consumo alcanzado. Vuelve a Resumen: el balance sigue en S/ 895."),
])
p("Qué decir: “El adaptador convierte Wh a kWh. Cada lectura identifica el consumo de un intervalo. Reenviar una lectura no vuelve a sumarla. El costo es una estimación; la lectura IoT no se transforma en una transacción financiera.”")
p("Cálculo: 25 kWh × S/ 0.75 = S/ 18.75. El consumo alcanza 125 % del límite de 20 kWh.")
picture("04-dispositivos", "Resultado del medidor simulado al terminar las dos lecturas.", 3.6)

page("5. Reporte y recomendación")
h("Reporte semanal")
p("Abre Reportes y selecciona la fecha de los movimientos de la demo. Para la semana de esta exposición se observan ingreso S/ 1,000, gastos S/ 105 y balance S/ 895. El reporte de gastos se consulta bajo demanda.")
p("Qué decir: “Esta vista reúne los movimientos de la semana y el estado de los presupuestos para ayudarme a revisar cómo voy.”")
h("Recomendación de presupuesto")
p("En Presupuestos pulsa Ver recomendación. El preparador cargó ingreso S/ 2,000 y gastos de alimentación, transporte y servicios en el mes anterior. La recomendación utiliza meses con ingresos dentro de los tres meses anteriores, reserva 20 % para ahorro y distribuye el resto según el gasto histórico.")
p("En esta cuenta la reserva es S/ 400 y el importe a distribuir es S/ 1,600. Puedes explicar el cálculo mientras consultas la propuesta. Es una recomendación basada en reglas y datos históricos.")
picture("05-reportes", "Reporte semanal de la cuenta de respaldo.", 4.0)

page("6. Cómo explicar la arquitectura")
table(["Componente", "Responsabilidad", "Persistencia en Docker"], [
    ("Nginx / frontend", "Sirve el panel y dirige cada petición a su API.", "Archivos de la imagen web"),
    ("Financial Records", "Registra movimientos, conserva Idempotency-Key y genera eventos.", "financial-data"),
    ("Budget", "Proyecta gastos, compara límites y prepara reportes.", "budget-data"),
    ("Notification", "Procesa avisos y administra su entrega y lectura.", "notification-data"),
    ("Device Integration", "Adapta entradas, normaliza y conserva telemetría.", "telemetry-data"),
    ("Apache Kafka", "Transporta los eventos y mantiene topics y DLQs.", "kafka-data"),
])
h("Flujo que acabas de demostrar")
code("Registro financiero + Outbox\n  -> Kafka: TransactionRecorded\n  -> Budget + Outbox: BudgetThresholdReached\n  -> Kafka -> Notification -> bandeja de alertas\n\nLectura -> adaptador -> Telemetry Store + Outbox\n  -> Kafka: ConsumptionReadingNormalized\n  -> Notification -> aviso de consumo")
p("Outbox: el dato y el evento se guardan en la misma transacción local. Un publicador envía los pendientes al broker y marca su entrega después de la confirmación de Kafka.")
p("Consumidor idempotente: reconoce un evento ya procesado y evita aplicar sus efectos otra vez. Los reintentos atienden fallas transitorias; las DLQs conservan mensajes que agotaron los intentos configurados.")
p("Database per Service: cada API accede a su propia base y volumen. Los demás servicios reciben eventos para mantener sus proyecciones.")
p("Ports & Adapters: explica el adaptador del servicio Device Integration para el simulador y Meter V1. Es el punto donde diferentes formatos externos se traducen al modelo común de consumo.")

page("7. Evidencia técnica para el profesor")
p("En CMD o en la terminal de VS Code, dentro de FinanZen/back:")
code("docker compose ps --all\ndocker compose logs --no-color --tail 10 financial-records budget-service notification-service device-service\ndocker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:19092 --list")
p("Explica los seis contenedores saludables y los inicializadores terminados. En la lista de topics se encuentran transacciones, umbrales de presupuesto, telemetría, resultados de notificación y DLQs.")
table(["Swagger del servicio", "Dirección"], [
    ("Financial Records", LIVE["url"] + "/services/financial/docs"),
    ("Budget", LIVE["url"] + "/services/budgets/docs"),
    ("Notification", LIVE["url"] + "/services/notifications/docs"),
    ("Device Integration", LIVE["url"] + "/services/devices/docs"),
])
h("Health checks")
code("curl.exe http://127.0.0.1:8080/services/financial/health\ncurl.exe http://127.0.0.1:8080/services/budgets/health\ncurl.exe http://127.0.0.1:8080/services/notifications/health\ncurl.exe http://127.0.0.1:8080/services/devices/health")
p("Comprueba status=ok, transport=kafka y workers activos. Los health checks de Docker también comprueban Kafka y Nginx.")
h("Prueba automatizada opcional")
code(".\\.venv\\Scripts\\python.exe scripts\\verify_docker.py")
p("El verificador utiliza una cuenta aislada y produce siete comprobaciones. Incluye flujo financiero, reentregas, telemetría, Outbox, persistencia separada y mensaje inválido enviado a DLQ. Durante la exposición puedes explicar los resultados existentes y reservar su ejecución para las preguntas.")

page("8. Mostrar idempotencia en Swagger")
p("Esta prueba es opcional y usa una identidad distinta para conservar las cifras de la demostración principal.")
p("1. Abre Swagger de Financial Records y despliega POST /api/v1/transactions. Pulsa Try it out.")
p("2. En X-User-Id escribe swagger-demo-1. En Idempotency-Key escribe movimiento-demo-1. Para un nuevo ensayo cambia ambos identificadores.")
code('{\n  "account_id": "cash-account",\n  "type": "expense",\n  "amount": "10.00",\n  "currency": "PEN",\n  "category": "other",\n  "occurred_at": "2026-11-26T15:00:00Z",\n  "description": "Prueba de idempotencia"\n}')
p("3. Pulsa Execute: la primera respuesta es HTTP 201. Guarda el id de la respuesta.")
p("4. Ejecuta exactamente el mismo cuerpo y la misma clave: responde HTTP 200, conserva el id e informa Idempotent-Replayed: true.")
p("5. Cambia únicamente amount a 20.00 y conserva la misma clave: responde HTTP 409 por conflicto.")
p("Qué decir: “Si se pierde una respuesta y el cliente reintenta, la misma clave permite recuperar el resultado original. Si cambia el contenido, el servidor detecta el conflicto.”")
h("Idempotencia de telemetría")
p("La comprobaste con Reenviar última lectura. Device Integration mantiene el reading_id y conserva una sola medición aunque llegue repetida. Kafka también puede redespachar eventos; los consumidores guardan recibos para evitar efectos duplicados.")

page("9. Preguntas que te pueden hacer")
table(["Pregunta", "Respuesta que puedes dar"], [
    ("¿Para qué sirve FinanZen?", "Para organizar movimientos, controlar presupuestos y relacionar hábitos financieros con información de consumo."),
    ("¿Qué demuestra Sprint 2?", "El flujo gasto → presupuesto → alerta con servicios independientes, Kafka, Outbox e idempotencia."),
    ("¿Qué demuestra Sprint 3?", "La recepción simulada de lecturas, adaptación de formato, normalización, deduplicación y almacenamiento de telemetría."),
    ("¿El dispositivo es físico?", "El recorrido usa un simulador funcional. El servicio también admite el contrato Meter V1 por API."),
    ("¿La estimación de energía cobra dinero?", "Se muestra como estimación. Un gasto real se registra mediante una operación financiera explícita."),
    ("¿Las alertas son correos?", "Esta versión entrega avisos dentro de la aplicación y permite configurar preferencias."),
    ("¿Qué es Cuenta demo?", "Es un selector de identidad de demostración para separar datos por X-User-Id. La sesión mostrada usa esa identidad de prueba."),
    ("¿Por qué tardó en salir la alerta?", "El procesamiento por eventos es asíncrono y el panel consulta actualizaciones periódicamente."),
    ("¿Cómo evitan duplicados?", "Idempotency-Key en movimientos, reading_id en lecturas y recibos persistentes en los consumidores."),
    ("¿Se aplicó arquitectura hexagonal?", "Device Integration usa adaptadores para traducir fuentes externas a un modelo interno. Los servicios separan API, reglas y persistencia según sus necesidades."),
    ("¿Qué sucede si falla una entrega?", "Los componentes reintentan las fallas; al agotarse los intentos registran el fallo o envían el mensaje a la DLQ correspondiente."),
])
h("Cierre de la presentación")
p("“Con este recorrido vimos que FinanZen registra gastos, los compara con presupuestos y genera alertas. También integra consumo de dispositivos sin alterar los movimientos financieros. La ejecución usa cuatro servicios con persistencia separada, Kafka y Docker Compose.”")

page("10. Si algo se demora y versión de 5 minutos")
table(["Situación", "Acción durante la exposición"], [
    ("El navegador no abre el panel", "Abre Docker Desktop, ejecuta docker compose up -d --wait --wait-timeout 240 desde back y vuelve a http://127.0.0.1:8080."),
    ("El panel parece vacío", "Revisa Cuenta demo y Periodo. La identidad de respaldo tiene el recorrido completo y los datos del mes indicado al inicio."),
    ("El presupuesto no cambia", "Comprueba que gasto y presupuesto tengan la misma categoría y mes. Espera la actualización o pulsa Actualizar información."),
    ("No aparece una alerta", "Comprueba Preferencias y que se cruzó el umbral. Revisa el estado de Budget, Notification y Kafka con docker compose ps."),
    ("No ves Reenviar última lectura", "Primero envía una lectura desde ese navegador. El panel guarda allí el identificador del último envío."),
    ("El reporte muestra otra semana", "Selecciona la fecha de los movimientos creados en este ensayo."),
    ("Necesitas mostrar el resultado sin repetir pasos", "Cambia a la cuenta de respaldo indicada en la portada. Muestra presupuesto 105 %, tres avisos y medidor de 25 kWh."),
])
h("Recorrido breve")
p("Minuto 1: explica el problema y muestra el balance inicial. Minuto 2: crea el presupuesto de 100 y registra el gasto de 85. Minuto 3: muestra la alerta y explica el flujo de eventos. Minuto 4: envía una lectura, repítela y comprueba que el consumo no se duplica. Minuto 5: muestra los servicios saludables y explica la separación entre telemetría y transacciones.")
h("Preparación final")
p("Conecta el cargador, amplía el navegador si vas a proyectar, confirma el periodo y ensaya una vez con una cuenta nueva. Mantén Docker Desktop abierto. Para pausar después de la presentación puedes ejecutar docker compose stop; al iniciar de nuevo, los volúmenes conservan los datos.")
p("Puedes consultar el guion breve en entrega/Guion-Demostracion-FinanZen.txt.")

OUTPUT.mkdir(parents=True, exist_ok=True)
path = OUTPUT / "Manual-Demostracion-FinanZen.docx"
doc.save(path)
facts = {"verified_at": LIVE["created_at"], "deployment": "local Docker Compose with Kafka", "url": LIVE["url"],
         "live_user": LIVE["user_id"], "backup_user": BACKUP["user_id"], "month": LIVE["month"],
         "backup_summary": BACKUP["summary"], "device_id": BACKUP["device_id"],
         "healthy_services": 6, "api_health_http": 200,
         "browser_acceptance": "Passed against http://127.0.0.1:8080; desktop and mobile; no JavaScript errors"}
facts["application_screenshots"] = [{"path": str(path.relative_to(OUTPUT / "manual-demo")),
    "sha256": sha256(path.read_bytes()).hexdigest(), "source": "Chrome screenshot of the running application"}
    for path in sorted((OUTPUT / "manual-demo/capturas").glob("*.png"))]
(OUTPUT / "manual-demo/sesion-verificada.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
brief = f'''FINANZEN — GUION BREVE PARA LA DEMOSTRACION

Aplicacion local: {LIVE['url']}
Cuenta en vivo: {LIVE['user_id']}
Cuenta de respaldo: {BACKUP['user_id']}
Periodo preparado: {LIVE['month']}

1. PRESENTAR
"FinanZen organiza movimientos, presupuestos, alertas y consumo de dispositivos."
Cuenta demo -> identidad en vivo. Balance inicial S/ 1,000.

2. PRESUPUESTO
Presupuestos -> Crear presupuesto -> Alimentacion, 100, umbral 80 %.

3. GASTO Y ALERTA
Resumen -> Registrar movimiento -> Gasto 85, Alimentacion, Compra de la semana.
Balance 915; presupuesto 85 %. Alertas -> aviso de cercania al limite.
Otro gasto de 20 -> gasto total 105, balance 895, presupuesto 105 %.
"TransactionRecorded llega a Budget; BudgetThresholdReached llega a Notification."

4. DISPOSITIVO
Agregar Medidor de casa, simulado, limite 20 kWh, tarifa 0.75.
Simular 15000 Wh -> 15 kWh, S/ 11.25, una lectura.
Reenviar ultima lectura -> mismo total y misma cantidad de lecturas.
Simular otros 10000 Wh -> 25 kWh, S/ 18.75, dos lecturas.
Alerta de consumo. Volver a Resumen -> balance sigue en 895.
"El costo es una estimacion; una lectura no se convierte sola en gasto."

5. REPORTE
Reportes -> fecha de los movimientos -> ingresos 1,000; gastos 105; balance 895.
Presupuestos -> Ver recomendacion -> ingreso historico 2,000; ahorro 400.

6. ARQUITECTURA
docker compose ps
Cuatro APIs + Kafka + Nginx. Base y volumen distintos por servicio.
Outbox: dato y evento juntos en una transaccion local.
Idempotencia: reintentar no repite efectos. Retry y DLQ atienden fallas.

CIERRE
"El flujo financiero y la telemetria funcionan con servicios separados,
comunicacion asincrona y una ejecucion integrada con Docker."

PARA UN NUEVO ENSAYO, DESDE back:
python scripts/preparar_demostracion.py
python scripts/preparar_demostracion.py --completa
Copiar la nueva identidad desde la terminal a Cuenta demo.
'''
(OUTPUT / "Guion-Demostracion-FinanZen.txt").write_text(brief, encoding="utf-8")
print("Manual DOCX, session metadata and short script generated.")
