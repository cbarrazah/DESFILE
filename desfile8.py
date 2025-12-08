import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage  # pip install Pillow
import os
import textwrap

# ====================== RUTAS ======================
EXCEL_RUTA = r"C:\Users\cbarrazah\Documents\DESFILE\LISTADO.xlsx"
CARPETA_SALIDA = r"C:\Users\cbarrazah\Documents\DESFILE\resoluciones"
FIRMAS_DIR = r"C:\Users\cbarrazah\Documents\DESFILE\firmas"
ENCABEZADO_IMG = r"C:\Users\cbarrazah\Documents\DESFILE\bannerTop.png"
PIE_IMG = r"C:\Users\cbarrazah\Documents\DESFILE\BannerFin.png"
FIRMA_FINAL = r"C:\Users\cbarrazah\Documents\DESFILE\FirmaNelson.png"

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Verificar archivos
for ruta, nombre in [(ENCABEZADO_IMG, "bannerTop.png"), (PIE_IMG, "BannerFin.png"), (FIRMA_FINAL, "FirmaNelson.png")]:
    if not os.path.exists(ruta):
        print(f"ERROR: No se encontró {nombre}")
        exit()

# Leer Excel
try:
    df = pd.read_excel(EXCEL_RUTA)
    print(f"Archivo leído: {len(df)} filas.")
except Exception as e:
    print(f"Error al leer Excel: {e}")
    exit()

columnas = ['ASOCIADO', 'CEDULA', 'EVENTO', 'DIRECCION', 'CANT. DE SILLAS', 'ASOCIACIÓN']
if not all(col in df.columns for col in columnas):
    print("Faltan columnas en el Excel.")
    exit()

# ====================== FUNCIONES ======================
def draw_wrapped_paragraph(c, text, x, y, max_width, font="Helvetica", size=9.5, leading=11, bold=False):
    c.setFont(f"{font}-Bold" if bold else font, size)
    words = text.split()
    line = ""
    for word in words:
        test_line = line + (" " + word if line else word)
        if c.stringWidth(test_line, f"{font}-Bold" if bold else font, size) <= max_width:
            line = test_line
        else:
            if y < 50: return y
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y

def draw_centered_title(c, title, y, max_width, font_size=10.5, leading=13):
    c.setFont("Helvetica-Bold", font_size)
    lines = textwrap.wrap(title, width=85)
    for line in lines:
        line_width = c.stringWidth(line, "Helvetica-Bold", font_size)
        x_centered = left + (max_width - line_width) / 2
        c.drawString(x_centered, y, line)
        y -= leading
    return y - 5

# ====================== GENERAR PDF ======================
width, height = A4
ANCHO_HOJA = width
MARGEN_LATERAL = 50
MARGEN_SUPERIOR_ENC = 100
MARGEN_INFERIOR_PIE = 80

for index, fila in df.iterrows():
    consecutivo = str(fila['CONSECUTIVO']).strip()
    asociado = str(fila['ASOCIADO']).strip()
    cedula = str(fila['CEDULA']).strip()
    evento = str(fila['EVENTO']).strip().upper()
    direccion = str(fila['DIRECCION']).strip()
    sillas = str(fila['CANT. DE SILLAS']).strip()
    asociacion = str(fila['ASOCIACIÓN']).strip()

    nombre_pdf = f"RESOLUCION_{asociado.replace(' ', '_')}_{cedula}.pdf"
    ruta_pdf = os.path.join(CARPETA_SALIDA, nombre_pdf)
    c = canvas.Canvas(ruta_pdf, pagesize=A4)

    # === ENCABEZADO Y PIE ===
    c.drawImage(ImageReader(ENCABEZADO_IMG), 0, height - MARGEN_SUPERIOR_ENC, width=ANCHO_HOJA, preserveAspectRatio=True)
    c.drawImage(ImageReader(PIE_IMG), 0, 0, width=ANCHO_HOJA, height=MARGEN_INFERIOR_PIE, preserveAspectRatio=True)

    # === ÁREA DE TEXTO ===
    left = MARGEN_LATERAL
    right = width - MARGEN_LATERAL
    top = height - MARGEN_SUPERIOR_ENC - 10
    max_width = right - left
    y = top

    # === DATOS DEL ASOCIADO ===

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left, y, "CONSECUTIVO:")
    c.setFont("Helvetica", 10)
    c.drawString(left + 90, y, consecutivo)
    y -= 16

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left, y, "ASOCIACIÓN:")
    c.setFont("Helvetica", 10)
    c.drawString(left + 90, y, asociacion)
    y -= 16

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left, y, "ASOCIADO:")
    c.setFont("Helvetica", 10)
    c.drawString(left + 90, y, asociado)
    y -= 16

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left, y, "IDENTIFICACIÓN:")
    c.setFont("Helvetica", 10)
    c.drawString(left + 90, y, cedula)
    y -= 25

    # === TEXTO LEGAL ===
    texto_legal = (
        "Que de conformidad con el Decreto No. 0801 de 07 de diciembre de 2020, la oficina de Gestión urbanística podrá "
        "“Adelantar las acciones técnicas necesarias, previas a la suscripción y/o adopción del instrumento de gestión "
        "correspondiente para el aprovechamiento económico del espacio público, así como la verificación de su posterior cumplimiento.”\n\n"
        "Así las cosas, luego de realizar las verificaciones técnicas correspondientes en el marco de la normatividad vigente, "
        "se avala lo que a continuación se describe:"
    )
    y = draw_wrapped_paragraph(c, texto_legal, left, y, max_width, size=9.5, leading=11)
    y -= 15

    # === ESPACIO PÚBLICO ===
    y = draw_centered_title(c, "ESPACIO PÚBLICO OBJETO DE APROVECHAMIENTO", y, max_width)
    tabla = [
        ("Elemento Constitutivo del espacio público", "Natural"),
        ("Tipo de espacio público", "No efectivo"),
        ("", "Zona Amoblamiento Urbano"),
        ("Ubicación y Tramo", direccion),
        ("Número de sillas permitidas", sillas),
        ("Plazo Máximo", "1 día"),
    ]
    for label, value in tabla:
        c.setFont("Helvetica", 8.5)
        if label:
            c.drawString(left, y, f"{label}:")
        c.setFont("Helvetica-Bold", 8.5)
        y = draw_wrapped_paragraph(c, value, left + 170, y, max_width - 170, size=8.5, leading=11)
        y -= 3
    y -= 10

    # === ACTIVIDAD PERMITIDA ===
    titulo_actividad = "ACTIVIDAD PERMITIDA EN EL EJERCICIO DEL APROVECHAMIENTO ECONÓMICO TEMPORAL DEL ESPACIO PÚBLICO"
    y = draw_centered_title(c, titulo_actividad, y, max_width, font_size=10.2, leading=12)

    actividad = (
        "Actividad: Actividades de aprovechamiento económico relacionados con Desfiles culturales.\n"
        "Descripción: Actividades enmarcadas en las actividades de desarrollo de desfiles culturales.\n"
        f"Actividad Solicitada: Ocupación temporal del espacio público, en la zona de amoblamiento urbano con {sillas} sillas para el desfile denominado "
        "GRAN PARADA DE LA LUZ"
    )
    y = draw_wrapped_paragraph(c, actividad, left, y, max_width, size=9.3, leading=10.8)
    y -= 12

    # === CONDICIONES ===
    y = draw_centered_title(c, "CONDICIONES MÍNIMAS PARA SALVAGUARDAR LA INTEGRIDAD DEL ESPACIO PÚBLICO:", y, max_width, font_size=9.8)

    condiciones = [
        "1. Acatar la Constitución, la ley, las normas legales y procedimientos establecidos por el Gobierno Nacional y Distrital, y demás disposiciones vigentes.",
        "2. Reportar de manera inmediata cualquier novedad o anomalía, a la Secretaría Distrital de Control urbano y Espacio Público.",
        "3. No impedir a la ciudadanía el uso, goce, disfrute visual y libre tránsito del espacio público.",
        "4. Mantener el área de espacio público objeto de aprovechamiento económico y su entorno inmediato definido en la propuesta, en las condiciones adecuadas de aseo y limpieza.",
        "5. Entregar el espacio público objeto del aprovechamiento en igual o mejores condiciones que las recibidas.",
        "6. El presente permiso podrá ser revocado por este despacho en los casos que puedan generar riesgo para la realización del evento en especial cuando se ubiquen sillas obstruyendo rutas de evacuación (Bocacalles)."
    ]
    c.setFont("Helvetica", 8.5)
    for cond in condiciones:
        y = draw_wrapped_paragraph(c, cond, left + 15, y, max_width - 15, size=8.5, leading=10.2)
        y -= 1
    y -= 8

    # === VERIFICACIÓN ===
    y = draw_centered_title(c, "VERIFICACIÓN DE CUMPLIMIENTO", y, max_width, font_size=9.5)

    verif = (
        "El aprovechador deberá presentar este documento al momento de realizar la ocupación temporal, con la finalidad de garantizar "
        "el cumplimiento de las condiciones técnicas, para lo cual deberá exhibirlo junto con su documento de identidad ante funcionarios "
        "de la Secretaría Distrital de Control Urbano y Espacio Público."
    )
    y = draw_wrapped_paragraph(c, verif, left, y, max_width, size=8.8, leading=10.5)
    y -= 20
    # === CIERRE FINAL: FECHA + FIRMA + CARGO ===
    c.setFont("Helvetica", 9)
    c.drawString(left, y, "Dado en Barranquilla D.E.I.P., a los 5 días del mes de diciembre de 2025")
    y -= 90  # Espacio limpio entre fecha y firma

    # ─────── FIRMA DIGITAL (ENCIMA DEL NOMBRE) ───────
    firma_path = FIRMA_FINAL  # Ya está definida al inicio como FirmaNelson.png
    
    if os.path.exists(firma_path):
        try:
            # Cargar y limpiar fondo transparente (si lo tiene)
            img = PILImage.open(firma_path).convert("RGBA")
            # Fondo blanco forzoso para que no quede negro al imprimir
            background = PILImage.new("RGBA", img.size, (255, 255, 255, 255))
            img = PILImage.alpha_composite(background, img).convert("RGB")
            
            # Tamaño deseado de la firma (ajusta si quieres más grande/más pequeña)
            ancho_firma = 220          # píxeles (aumenta o reduce según tu imagen)
            alto_firma  = 70           # mantiene proporción automáticamente
            
            # Centrar horizontalmente
            x_firma = (width - ancho_firma) / 2
            
            # Posicionar justo encima del nombre (el nombre estará ~10 puntos más abajo)
            y_firma = y + 10
            
            c.drawImage(
                ImageReader(img),
                x_firma, y_firma,
                width=ancho_firma,
                height=alto_firma,
                preserveAspectRatio=True,
                mask='auto'  # ayuda con transparencias
            )
            
            # Ajustar y para que el nombre quede debajo de la firma
            y = y_firma - 15
            
        except Exception as e:
            print(f"Error al cargar la firma {firma_path}: {e}")
            y -= 40  # fallback si falla la imagen
    else:
        print(f"No se encontró la firma: {firma_path}")
        y -= 40

    # ─────── NOMBRE Y CARGO (DEBajo de la firma) ───────
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, y, "NELSON ENRIQUE PATRON PÉREZ")
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, "SECRETARIO DE CONTROL URBANO Y ESPACIO PÚBLICO")


    c.showPage()
    c.save()
    print(f"Generada: {nombre_pdf}")

print(f"\n¡TODAS LAS RESOLUCIONES GENERADAS!\nCarpeta: {CARPETA_SALIDA}")