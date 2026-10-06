import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

pdf_path = "public/libretos/noche-de-apagon-acto-1.pdf"
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=50,
    leftMargin=50,
    topMargin=45,
    bottomMargin=45
)

styles = getSampleStyleSheet()

# Typography and Hierarchy
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    alignment=1, # Center
    textColor=colors.HexColor('#091224')
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    alignment=1,
    textColor=colors.HexColor('#d97706') # Theater Gold
)

meta_style = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    alignment=1,
    textColor=colors.HexColor('#475569')
)

h1_style = ParagraphStyle(
    'ActHeading',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    spaceBefore=14,
    spaceAfter=6,
    textColor=colors.HexColor('#091224')
)

char_style = ParagraphStyle(
    'CharacterName',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#991b1b'),
    spaceBefore=7,
    spaceAfter=1
)

dialogue_style = ParagraphStyle(
    'Dialogue',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    leftIndent=14,
    spaceAfter=3,
    textColor=colors.HexColor('#1e293b')
)

stage_dir_style = ParagraphStyle(
    'StageDir',
    parent=styles['Italic'],
    fontName='Helvetica-Oblique',
    fontSize=8.5,
    leading=11.5,
    leftIndent=14,
    spaceBefore=3,
    spaceAfter=3,
    textColor=colors.HexColor('#475569')
)

cue_style = ParagraphStyle(
    'TechCue',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    leftIndent=14,
    spaceBefore=2,
    spaceAfter=2,
    textColor=colors.HexColor('#0284c7')
)

story = []

# Title & Cover Header
story.append(Spacer(1, 10))
story.append(Paragraph("NOCHE DE APAGÓN", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("Obra Teatral Original en Tres Actos — LIBRETO DEFINITIVO DEL ACTO 1", subtitle_style))
story.append(Spacer(1, 6))
story.append(Paragraph("Creación Dramatúrgica Original • Elenco de Teatro COAR Amazonas<br/>Tiempo escénico estimado: 15 a 18 min • 8 Personajes • Escenario: SUM Internado", meta_style))
story.append(Spacer(1, 12))

# Cast & Vocal Score Table
cast_data = [
    [Paragraph("<b>Personaje</b>", meta_style), Paragraph("<b>Rol & Partitura Vocal</b>", meta_style)],
    [Paragraph("<b>MATEO</b>", char_style), Paragraph("<b>El Brigadier:</b> Frases cortas, verbos en imperativo/futuro dictatorial. Tensión maxilar constante. Se aferra al manual para no volver a su pueblo.", dialogue_style)],
    [Paragraph("<b>SOFÍA</b>", char_style), Paragraph("<b>La Excelencia:</b> Respiración clavicular cortada. Habla a tropezones, repite frases. Canaliza el pánico en la obsesión histérica por un error milimétrico.", dialogue_style)],
    [Paragraph("<b>LUCAS</b>", char_style), Paragraph("<b>El Sarcasmo:</b> Arrastra vocales, ritmo sincopado. Responde con preguntas cínicas para ocultar el abandono de su familia.", dialogue_style)],
    [Paragraph("<b>VALERIA</b>", char_style), Paragraph("<b>La Fricción:</b> Voz física, cortante e invasiva. Postura reclinada o de ataque. Corta los diálogos ajenos. Desprecia las jerarquías institucionales.", dialogue_style)],
    [Paragraph("<b>DANTE</b>", char_style), Paragraph("<b>El Fantasma:</b> Voz pasiva y murmullos hacia adentro (<i>'se cayó'</i>, <i>'estaba abierto'</i>). Habla hacia el piso, abrazando su mochila.", dialogue_style)],
    [Paragraph("<b>ISABEL</b>", char_style), Paragraph("<b>La Raíz:</b> Tempo lentísimo (Largo), graves profundos. Sus pausas pesan más que las palabras. Conectada al pulso del río con crudeza pragmática.", dialogue_style)],
    [Paragraph("<b>JOAQUÍN</b>", char_style), Paragraph("<b>El Cálculo:</b> Ametralladora matemática. Porcentajes exactos, estadísticas frías. Cree que los números lo protegerán del colapso.", dialogue_style)],
    [Paragraph("<b>CAMILA</b>", char_style), Paragraph("<b>El Pegamento:</b> Tono suplicante y conciliador. Plurales inclusivos (<i>'chicos'</i>, <i>'vamos'</i>). Sonrisa agotada que busca frenar la desintegración del grupo.", dialogue_style)],
]
t = Table(cast_data, colWidths=[110, 400])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
]))
story.append(t)
story.append(Spacer(1, 10))

# Technical Staging Note
tech_data = [
    [Paragraph("<b>PAUTA TÉCNICA ESCOLAR</b>", meta_style)],
    [Paragraph("<b>Espacio:</b> Sala de estudio (SUM) en ceja de selva (Amazonas). Mesas apiñadas al centro con libros y laptops.<br/>"
               "<b>Iluminación:</b> Tubo fluorescente blanco clínico &rarr; Apagón súbito &rarr; Círculo claustrofóbico de 3 velas de sebo (ámbar tenue) &rarr; Relámpagos azul frío.<br/>"
               "<b>Efectos de Sonido:</b> [AUDIO 01 - LLUVIA_TORRENCIAL], [AUDIO 02 - TRUENO_SECO_APAGÓN_BRUTAL], [AUDIO 03 - TRUENO_SECO_CERCANO].", stage_dir_style)]
]
t_tech = Table(tech_data, colWidths=[510])
t_tech.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fef3c7')),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#d97706')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_tech)
story.append(Spacer(1, 10))

# GUION ACTO 1
story.append(Paragraph("ACTO I: LA CUENTA REGRESIVA Y EL ANILLO DE FUEGO", h1_style))
story.append(Paragraph("(El escenario es una caldera a punto de estallar. Los ocho estudiantes están apiñados alrededor de las tres mesas. JOAQUÍN teclea mirando obsesivamente su reloj. SOFÍA tiene los ojos desorbitados pegados a la pantalla, borrando y reescribiendo. LUCAS hace girar un lapicero. VALERIA está despatarrada con zapatillas sobre un diccionario. DANTE, en el suelo, abraza su mochila con nudillos blancos. ISABEL mira fijamente el cristal de la ventana. Suena [AUDIO 01 - LLUVIA_TORRENCIAL] pesada y continua).", stage_dir_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("Cero coma cinco de margen de error. Cuarenta y tres minutos para el cierre de la plataforma. Si el servidor no colapsa, enviamos.", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("(Borrando frenética, voz entrecortada). Cero coma cinco... Cero coma cinco no sirve. No sirve. El manual dice cero coma dos. El manual dice...", dialogue_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("El manual es una guía, Sofía. Cincuenta y dos páginas escritas, no las vamos a deshacer por tres décimas. Envío a las once en punto.", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("No. No, no, no. La línea tres de la página doce. Hay una coma mal puesta. Hay una coma...", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("(Con la cabeza hacia atrás, bostezando con desdén). Envíalo ya, Joaquín. Me aburro.", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("(Voz rígida, militar). Valeria. Bajamos los pies de la mesa. El mobiliario es propiedad del Estado.", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("¿El Estado? Qué tierno. ¿Le vas a mandar una carta al presidente si rayo la fórmica?", dialogue_style))

story.append(Paragraph("LUCAS", char_style))
story.append(Paragraph("(Arrastrando las vocales, sonriendo). ¿A qué presidente? ¿Al que está preso o al que va a entrar?", dialogue_style))

story.append(Paragraph("CAMILA", char_style))
story.append(Paragraph("Chicos, por favor, vamos a concentrarnos, ¿sí? Ya casi terminamos la semana. Un esfuercito más y...", dialogue_style))

story.append(Paragraph("ISABEL", char_style))
story.append(Paragraph("(Sin darse vuelta, voz grave y pausada). El agua está raspando la piedra grande del río.", dialogue_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("Veintinueve minutos. Sofía, deja de borrar. Vas a malograr el formato.", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("¡Tengo que leer la línea tres! ¡Si el revisor la lee y no tiene sentido... me van a anular la monografía! Me la anulan y...", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("Cállense. Cállense todos. Hay un protocolo de silencio a partir de las diez y media.", dialogue_style))

story.append(Paragraph("LUCAS", char_style))
story.append(Paragraph("¿Y la lluvia leyó tu protocolo, brigadier? Porque suena bastante fuerte allá afuera, ¿no crees?", dialogue_style))

story.append(Paragraph("DANTE", char_style))
story.append(Paragraph("(Desde el rincón, con la voz pegada a las rodillas). Deberíamos irnos a los cuartos. Ya.", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("Nadie sale del SUM hasta la ronda del monitor. Esperaremos en nuestros sitios.", dialogue_style))

story.append(Paragraph("(Un relámpago violento tiñe la gran ventana de un azul eléctrico cegador).", stage_dir_style))
story.append(Paragraph("[SONIDO]: [AUDIO 02 - TRUENO_SECO_APAGÓN_BRUTAL] — Estruendo sísmico que sacude el piso.", cue_style))
story.append(Paragraph("[ILUMINACIÓN]: APAGÓN TOTAL DE GOLPE. OSCURIDAD ABSOLUTA.", cue_style))

story.append(Paragraph("(En la negrura, la lluvia cobra una presencia colosal. Sonido de sillas arrastradas y respiraciones cortas).", stage_dir_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("(Un grito ahogado en la oscuridad). La pantalla... Mi pantalla se apagó. ¡Joaquín! ¡La pantalla se apagó!", dialogue_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("Sin red. Sin servidor local. Ochenta y dos por ciento de batería, pero sin señal no hay subida. Estamos fuera.", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("Nos quedamos quietos. Nadie respira. Nadie camina.", dialogue_style))

story.append(Paragraph("LUCAS", char_style))
story.append(Paragraph("¿Cómo hacemos para no respirar, Mateo? Explícanos tu técnica ninja.", dialogue_style))

story.append(Paragraph("CAMILA", char_style))
story.append(Paragraph("Chicos, tranquilos, de repente es solo el fusible del piso. ¿Alguien tiene el celular a la mano?", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("Muertos. Los cortadores de señal están funcionando perfecto. Cárcel de máxima seguridad.", dialogue_style))

story.append(Paragraph("(En la oscuridad, un fósforo raspa contra la caja. Una pequeña llama ilumina el rostro cobrizo de ISABEL desde abajo. Con parsimonia, Isabel coloca tres velas anchas sobre la mesa central, derritiendo cera para fijarlas).", stage_dir_style))
story.append(Paragraph("[ILUMINACIÓN]: CÍRCULO ÁMBAR DE VELAS. Los ocho cuerpos se congregan apretados hombro con hombro. Sus sombras se agigantan sobre las paredes negras.", cue_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("(Golpeando la mesa con el nudillo). El generador diésel debería encender en doce segundos.", dialogue_style))

story.append(Paragraph("LUCAS", char_style))
story.append(Paragraph("¿Ya pasaron doce segundos, relojito? ¿O tu cálculo tiene cero coma cinco de margen de error?", dialogue_style))

story.append(Paragraph("ISABEL", char_style))
story.append(Paragraph("No va a prender. El río se llevó el poste de la loma chica. Lo vi en la tarde.", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("(Hiperventilando, acerca su cuaderno a un milímetro de la llama. Dedos temblando). Necesito luz. No veo la línea tres. No veo la maldita línea tres...", dialogue_style))

story.append(Paragraph("CAMILA", char_style))
story.append(Paragraph("Sofi, aleja el papel de la vela. Te vas a quemar.", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("¡No lo veo! ¡Está borroso! ¡Joaquín, prende la laptop, dime que el autoguardado funciona, dímelo!", dialogue_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("Pantalla negra para ahorrar energía. No la voy a prender hasta que vuelva la red. Sería un desperdicio del veintiún por ciento.", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("(El cuaderno roza la vela en un espasmo. Una gota gruesa de cera caliente cae sobre la página abierta). ¡No! ¡No, no, no! ¡La cera! ¡Cayó encima! ¡Me quemó la tabla de variables!", dialogue_style))

story.append(Paragraph("CAMILA", char_style))
story.append(Paragraph("¡Sofi, suelta el cuaderno! ¡No pasa nada, yo te ayudo a rasparlo, vamos!", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("(Raspando el papel con la uña hasta casi sangrar). ¡No sale! ¡Lo arruiné! ¡Lo arruiné todo! ¡Van a leer esto y van a pensar que soy una estúpida! ¡Van a pensar que no sé hacer un informe limpio! ¡Lo raspo y se rompe, Camila, se rompe el papel!", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("(Con desprecio frío, cruzándose de brazos). Es un papel, psicótica. Detente, estás sudando como un cerdo.", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("(Golpe seco en la mesa). ¡Suficiente! Sofía, siéntate y baja la cabeza. Valeria, te callas de una buena vez. Retomaremos el orden. Ahora.", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("(Inclinándose sobre la vela, invadiendo su rostro en el cono de luz). ¿Qué orden vas a retomar en la oscuridad, brigadier? Estás sudando frío tú también. ¿A quién vas a reportar si ni siquiera puedes ver la puerta?", dialogue_style))

story.append(Paragraph("LUCAS", char_style))
story.append(Paragraph("(Sonriendo desde su sombra). Uy. Golpe directo al ego. ¿Te vas a dejar, Mateo? ¿O vas a sacar tu libretita de amonestaciones en braille?", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("Nadie me habla en ese tono. Ustedes dos están al límite del desacato.", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("¿Desacato? ¿Desacato? ¡Eres un alumno, igual que yo! No eres el alcaide, Mateo, ¡eres el perrito faldero que obedece todo para que no lo manden de vuelta a su pueblo!", dialogue_style))

story.append(Paragraph("CAMILA", char_style))
story.append(Paragraph("¡Valeria, por favor! ¡Chicos! ¡Nos estamos ahogando en un vaso de agua!", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("Retrocede, Valeria. Te vas al rincón. Fuera del perímetro de luz. Es una orden.", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("Oblígame.", dialogue_style))

story.append(Paragraph("(MATEO avanza para empujarla. VALERIA no retrocede y le planta el pecho. En el forcejeo físico en el estrecho círculo de luz, ambos trastabillan hacia atrás y embisten con violencia a DANTE, agazapado en el suelo).", stage_dir_style))

story.append(Paragraph("DANTE", char_style))
story.append(Paragraph("(Un grito ahogado). ¡Ah!", dialogue_style))

story.append(Paragraph("(El golpe proyecta a Dante hacia el frente. Sus manos resbalan. La mochila cae de golpe contra las tablas; la costura cede y la cremallera se abre).", stage_dir_style))
story.append(Paragraph("(De su interior, resbala pesadamente sobre el suelo un objeto rígido: un FÓLDER PLÁSTICO DE UN ROJO BRILLANTE Y GRUESO. Se desliza por el piso y se detiene en seco en la punta de los zapatos de ISABEL).", stage_dir_style))
story.append(Paragraph("(Nadie se mueve. Todos reconocen de inmediato ese color y ese membrete oficial).", stage_dir_style))

story.append(Paragraph("JOAQUÍN", char_style))
story.append(Paragraph("(La voz se le quiebra, perdiendo su pulso matemático). Ese... ese es un archivo de Coordinación Psicológica. Los rojos están bajo llave.", dialogue_style))

story.append(Paragraph("DANTE", char_style))
story.append(Paragraph("(En el suelo, encogiéndose en posición fetal, balbuceando hacia las tablas). Se me... se me cayó. Estaba abierto. El cajón estaba abierto.", dialogue_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("(Lívido, petrificado). Robaste un documento confidencial. Eso es expulsión automática.", dialogue_style))

story.append(Paragraph("DANTE", char_style))
story.append(Paragraph("(Murmurando sin alzar la cabeza). Me llamaron. La psicóloga me citó en el recreo. Estaba ahí encima. Solo... solo leí mi nombre en la portada. Vi mi nombre. Y me dio terror. Me lo guardé. No quería. Se me pegó a la mano.", dialogue_style))

story.append(Paragraph("LUCAS", char_style))
story.append(Paragraph("¿Tu nombre?", dialogue_style))

story.append(Paragraph("DANTE", char_style))
story.append(Paragraph("Y los de ustedes.", dialogue_style))

story.append(Paragraph("(El silencio en la sala se vuelve casi irrespirable. Afuera, la lluvia azota los vidrios).", stage_dir_style))

story.append(Paragraph("ISABEL", char_style))
story.append(Paragraph("(Lentamente, sin apresurarse, se agacha. Recoge el fólder rojo con ambas manos. Lo levanta y lo sitúa en el centro exacto de la mesa, bajo la lumbre de las tres velas. Abre la cubierta).", stage_dir_style))

story.append(Paragraph("MATEO", char_style))
story.append(Paragraph("(Con un hilo de voz). Isabel. Ciérralo. Como brigadier exijo que lo cierres.", dialogue_style))

story.append(Paragraph("(Pero Mateo no se mueve ni un centímetro. Sus ojos están clavados en el papel).", stage_dir_style))

story.append(Paragraph("ISABEL", char_style))
story.append(Paragraph("(Voz grave, serena, arrastrando las sílabas. Lee el encabezado oficial). 'Evaluación final de permanencia. Área de Psicología. Confidencial.'", dialogue_style))

story.append(Paragraph("SOFÍA", char_style))
story.append(Paragraph("(Apretándose los nudillos hasta que crujen). No lo leas. Por favor, Isabel, no lo leas.", dialogue_style))

story.append(Paragraph("ISABEL", char_style))
story.append(Paragraph("(La llama parpadea en sus pupilas. Continúa sin inmutarse). 'Resolución treinta y cuatro. Aplicación efectiva: Lunes a primera hora.'", dialogue_style))

story.append(Paragraph("VALERIA", char_style))
story.append(Paragraph("(Completamente tiesa, despojada de su cinismo). ¿Qué dice, Isabel? Ve al grano.", dialogue_style))

story.append(Paragraph("ISABEL", char_style))
story.append(Paragraph("(Alza la mirada despacio, recorriendo uno a uno los rostros del grupo). 'Dos estudiantes del Pabellón B serán separados definitivamente de la institución... por riesgo de colapso psicológico.'", dialogue_style))

story.append(Paragraph("(La respiración colectiva se detiene en seco. Nadie parpadea. Las tres velas tiemblan violentamente).", stage_dir_style))

story.append(Paragraph("CAMILA", char_style))
story.append(Paragraph("(Con la voz destrozada por el pánico, un susurro que hiela la sangre). Somos... el Pabellón B.", dialogue_style))

story.append(Paragraph("(En ese instante: [SONIDO]: [AUDIO 03 - TRUENO_SECO_CERCANO]. Un golpe ensordecedor que sacude las ventanas).", stage_dir_style))
story.append(Paragraph("(Una ráfaga helada de viento entra por la rendija y sopla las tres velas al unísono).", stage_dir_style))
story.append(Paragraph("[ILUMINACIÓN]: APAGÓN SÚBITO. NEGRURA TOTAL.", cue_style))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>TELÓN RÁPIDO / FIN DEL ACTO 1</b>", subtitle_style))

doc.build(story)
print(f"PDF generado exitosamente en: {pdf_path}")
