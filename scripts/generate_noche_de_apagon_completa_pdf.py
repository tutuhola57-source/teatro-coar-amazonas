import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors

pdf_path = "D:/Proyectos/teatro-coar-amazonas/public/libretos/noche-de-apagon-obra-completa.pdf"
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=38,
    leftMargin=38,
    topMargin=32,
    bottomMargin=32
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
    fontSize=11,
    leading=15,
    alignment=1,
    textColor=colors.HexColor('#d97706') # Theater Gold
)

meta_style = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    alignment=1,
    textColor=colors.HexColor('#475569')
)

h1_style = ParagraphStyle(
    'ActHeading',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    spaceBefore=12,
    spaceAfter=5,
    textColor=colors.HexColor('#091224')
)

char_style = ParagraphStyle(
    'CharacterName',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#991b1b'),
    spaceBefore=4,
    spaceAfter=1
)

dialogue_style = ParagraphStyle(
    'Dialogue',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=12,
    leftIndent=12,
    spaceAfter=1.5,
    textColor=colors.HexColor('#1e293b')
)

stage_dir_style = ParagraphStyle(
    'StageDir',
    parent=styles['Italic'],
    fontName='Helvetica-Oblique',
    fontSize=8,
    leading=11,
    leftIndent=12,
    spaceBefore=1.5,
    spaceAfter=1.5,
    textColor=colors.HexColor('#475569')
)

cue_style = ParagraphStyle(
    'TechCue',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10.5,
    leftIndent=12,
    spaceBefore=1.5,
    spaceAfter=1.5,
    textColor=colors.HexColor('#0284c7')
)

story = []

# Title & Cover Header
story.append(Spacer(1, 5))
story.append(Paragraph("NOCHE DE APAGÓN", title_style))
story.append(Spacer(1, 3))
story.append(Paragraph("Obra Teatral Original en Tres Actos — LIBRETO COMPLETO Y DEFINITIVO", subtitle_style))
story.append(Spacer(1, 4))
story.append(Paragraph("Creación Dramatúrgica Original • Elenco de Teatro COAR Amazonas<br/>Duración total: ~48 minutos • 8 Personajes • Escenario único: Sala de Usos Múltiples (SUM), Internado", meta_style))
story.append(Spacer(1, 8))

# Cast & Vocal Score Table
cast_data = [
    [Paragraph("<b>Personaje</b>", meta_style), Paragraph("<b>Rol, Perfil Dramático y Partitura Vocal</b>", meta_style)],
    [Paragraph("<b>MATEO</b>", char_style), Paragraph("<b>El Brigadier:</b> Frases cortas, sintaxis marcial, verbos en imperativo/futuro dictatorial. Tensión maxilar constante. Se aferra al manual para no volver a la precariedad de su pueblo.", dialogue_style)],
    [Paragraph("<b>SOFÍA</b>", char_style), Paragraph("<b>La Excelencia:</b> Respiración clavicular cortada, taquifemia y repeticiones maniáticas. Canaliza el pánico en la obsesión histérica por un error milimétrico.", dialogue_style)],
    [Paragraph("<b>LUCAS</b>", char_style), Paragraph("<b>El Sarcasmo:</b> Arrastra vocales, ritmo sincopado e ironía punzante. Máscara de indiferencia que se quiebra al emerger el abandono filial.", dialogue_style)],
    [Paragraph("<b>VALERIA</b>", char_style), Paragraph("<b>La Fricción:</b> Voz física, cortante, invasiva. Postura corporal de ataque frontal. Corta diálogos ajenos. Desprecia las jerarquías institucionales.", dialogue_style)],
    [Paragraph("<b>DANTE</b>", char_style), Paragraph("<b>El Fantasma:</b> Voz pasiva y murmullos hacia adentro (<i>'se cayó'</i>, <i>'no fui yo'</i>). Habla mirando el piso, consumido por la culpa de ser el delator del internado.", dialogue_style)],
    [Paragraph("<b>ISABEL</b>", char_style), Paragraph("<b>La Raíz:</b> Tempo lentísimo (Largo), graves profundos. Sus pausas pesan más que las palabras. Conectada a la memoria ancestral y al pulso del río con serenidad ética.", dialogue_style)],
    [Paragraph("<b>JOAQUÍN</b>", char_style), Paragraph("<b>El Cálculo:</b> Ametralladora matemática. Porcentajes exactos, estadísticas frías. Cree ciegamente que los números lo protegerán del colapso emocional.", dialogue_style)],
    [Paragraph("<b>CAMILA</b>", char_style), Paragraph("<b>El Pegamento:</b> Tono suplicante y conciliador. Plurales inclusivos (<i>'chicos'</i>, <i>'vamos'</i>). Ansiedad mediadora que busca frenar la desintegración del grupo.", dialogue_style)],
]
t = Table(cast_data, colWidths=[100, 420])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 2),
]))
story.append(t)
story.append(Spacer(1, 8))

# Technical Staging Note
tech_data = [
    [Paragraph("<b>PAUTA TÉCNICA Y UNIVERSO SONORO-VISUAL</b>", meta_style)],
    [Paragraph("<b>Espacio escénico:</b> Sala de estudio (SUM) en el COAR Amazonas (Chachapoyas). Mesas modulares apiñadas al centro. Ventanal oscuro al fondo que recibe el azote del temporal de ceja de selva.<br/>"
               "<b>Evolución lumínica:</b> Blanco clínico fluorescente (Acto I) &rarr; Apagón súbito &rarr; Ring claustrofóbico de tres velas de sebo &rarr; Silencio en tinieblas con haz de linterna exterior (Acto II) &rarr; Vela solitaria confessional &rarr; Fuego purificador &rarr; Regreso enceguecedor de la luz clínica (Acto III).<br/>"
               "<b>Efectos de sonido:</b> [AUDIO 01 - LLUVIA_TORRENCIAL], [AUDIO 02 - TRUENO_SECO_APAGÓN_BRUTAL], [AUDIO 03 - TRUENO_SECO_CERCANO], [AUDIO 04 - LLUVIA_SORDINA_Y_GOTEO_ZINC], [AUDIO 05 - PASOS_BOTAS_PASILLO], [AUDIO 06 - FORCEJEO_CERRADURA_MANIJA], [AUDIO 07 - ZUMBIDO_TRANSFORMADOR_ALTO_VOLTAJE], [AUDIO 08 - CHISPAZO_FLUORESCENTE_PARPADEO].", stage_dir_style)]
]
t_tech = Table(tech_data, colWidths=[520])
t_tech.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fef3c7')),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#d97706')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
]))
story.append(t_tech)
story.append(Spacer(1, 10))

# ==================== ACTO 1 ====================
story.append(Paragraph("ACTO I: LA CUENTA REGRESIVA Y EL ANILLO DE FUEGO", h1_style))
story.append(Paragraph("(El escenario es una caldera a punto de estallar. Los ocho estudiantes están apiñados alrededor de las tres mesas. JOAQUÍN teclea mirando obsesivamente su reloj. SOFÍA tiene los ojos desorbitados pegados a la pantalla, borrando y reescribiendo. LUCAS hace girar un lapicero. VALERIA está despatarrada con zapatillas sobre un diccionario. DANTE, en el suelo, abraza su mochila con nudillos blancos. ISABEL mira fijamente el cristal de la ventana. Suena [AUDIO 01 - LLUVIA_TORRENCIAL] pesada y continua).", stage_dir_style))

dialogues_acto1 = [
    ("JOAQUÍN", "Cero coma cinco de margen de error. Cuarenta y tres minutos para el cierre de la plataforma. Si el servidor no colapsa, enviamos."),
    ("SOFÍA", "(Borrando frenética, voz entrecortada). Cero coma cinco... Cero coma cinco no sirve. No sirve. El manual dice cero coma dos. El manual dice..."),
    ("JOAQUÍN", "El manual es una guía, Sofía. Cincuenta y dos páginas escritas, no las vamos a deshacer por tres décimas. Envío a las once en punto."),
    ("SOFÍA", "No. No, no, no. La línea tres de la página doce. Hay una coma mal puesta. Hay una coma..."),
    ("VALERIA", "(Con la cabeza hacia atrás, bostezando con desdén). Envíalo ya, Joaquín. Me aburro."),
    ("MATEO", "(Voz rígida, militar). Valeria. Bajamos los pies de la mesa. El mobiliario es propiedad del Estado."),
    ("VALERIA", "¿El Estado? Qué tierno. ¿Le vas a mandar una carta al presidente si rayo la fórmica?"),
    ("LUCAS", "(Arrastrando las vocales, sonriendo). ¿A qué presidente? ¿Al que está preso o al que va a entrar?"),
    ("CAMILA", "Chicos, por favor, vamos a concentrarnos, ¿sí? Ya casi terminamos la semana. Un esfuercito más y..."),
    ("ISABEL", "(Sin darse vuelta, voz grave y pausada). El agua está raspando la piedra grande del río."),
    ("JOAQUÍN", "Veintinueve minutos. Sofía, deja de borrar. Vas a malograr el formato."),
    ("SOFÍA", "¡Tengo que leer la línea tres! ¡Si el revisor la lee y no tiene sentido... me van a anular la monografía! Me la anulan y..."),
    ("MATEO", "Cállense. Cállense todos. Hay un protocolo de silencio a partir de las diez y media."),
    ("LUCAS", "¿Y la lluvia leyó tu protocolo, brigadier? Porque suena bastante fuerte allá afuera, ¿no crees?"),
    ("DANTE", "(Desde el rincón, con la voz pegada a las rodillas). Deberíamos irnos a los cuartos. Ya."),
    ("MATEO", "Nadie sale del SUM hasta la ronda del monitor. Esperaremos en nuestros sitios."),
]

for speaker, text in dialogues_acto1:
    story.append(Paragraph(speaker, char_style))
    story.append(Paragraph(text, dialogue_style))

story.append(Paragraph("(Un relámpago violento tiñe la gran ventana de un azul eléctrico cegador).", stage_dir_style))
story.append(Paragraph("[SONIDO]: [AUDIO 02 - TRUENO_SECO_APAGÓN_BRUTAL] — Estruendo sísmico que sacude el piso.", cue_style))
story.append(Paragraph("[ILUMINACIÓN]: APAGÓN TOTAL DE GOLPE. OSCURIDAD ABSOLUTA.", cue_style))
story.append(Paragraph("(En la negrura, la lluvia cobra una presencia colosal. Sonido de sillas arrastradas y respiraciones cortas).", stage_dir_style))

dialogues_acto1_b = [
    ("SOFÍA", "(Un grito ahogado en la oscuridad). La pantalla... Mi pantalla se apagó. ¡Joaquín! ¡La pantalla se apagó!"),
    ("JOAQUÍN", "Sin red. Sin servidor local. Ochenta y dos por ciento de batería, pero sin señal no hay subida. Estamos fuera."),
    ("MATEO", "Nos quedamos quietos. Nadie respira. Nadie camina."),
    ("LUCAS", "¿Cómo hacemos para no respirar, Mateo? Explícanos tu técnica ninja."),
    ("CAMILA", "Chicos, tranquilos, de repente es solo el fusible del piso. ¿Alguien tiene el celular a la mano?"),
    ("VALERIA", "Muertos. Los cortadores de señal están funcionando perfecto. Cárcel de máxima seguridad."),
]

for speaker, text in dialogues_acto1_b:
    story.append(Paragraph(speaker, char_style))
    story.append(Paragraph(text, dialogue_style))

story.append(Paragraph("(En la oscuridad, un fósforo raspa contra la caja. Una pequeña llama ilumina el rostro cobrizo de ISABEL desde abajo. Con parsimonia, Isabel coloca tres velas anchas sobre la mesa central, derritiendo cera para fijarlas).", stage_dir_style))
story.append(Paragraph("[ILUMINACIÓN]: CÍRCULO ÁMBAR DE VELAS. Los ocho cuerpos se congregan apretados hombro con hombro. Sus sombras se agigantan sobre las paredes negras.", cue_style))

dialogues_acto1_c = [
    ("JOAQUÍN", "(Golpeando la mesa con el nudillo). El generador diésel debería encender en doce segundos."),
    ("LUCAS", "¿Ya pasaron doce segundos, relojito? ¿O tu cálculo tiene cero coma cinco de margen de error?"),
    ("ISABEL", "No va a prender. El río se llevó el poste de la loma chica. Lo vi en la tarde."),
    ("SOFÍA", "(Hiperventilando, acerca su cuaderno a un milímetro de la llama. Dedos temblando). Necesito luz. No veo la línea tres. No veo la maldita línea tres..."),
    ("CAMILA", "Sofi, aleja el papel de la vela. Te vas a quemar."),
    ("SOFÍA", "¡No lo veo! ¡Está borroso! ¡Joaquín, prende la laptop, dime que el autoguardado funciona, dímelo!"),
    ("JOAQUÍN", "Pantalla negra para ahorrar energía. No la voy a prender hasta que vuelva la red. Sería un desperdicio del veintiún por ciento."),
    ("SOFÍA", "(El cuaderno roza la vela en un espasmo. Una gota gruesa de cera caliente cae sobre la página abierta). ¡No! ¡No, no, no! ¡La cera! ¡Cayó encima! ¡Me quemó la tabla de variables!"),
    ("CAMILA", "¡Sofi, suelta el cuaderno! ¡No pasa nada, yo te ayudo a rasparlo, vamos!"),
    ("SOFÍA", "(Raspando el papel con la uña hasta casi sangrar). ¡No sale! ¡Lo arruiné! ¡Lo arruiné todo! ¡Van a leer esto y van a pensar que soy una estúpida! ¡Van a pensar que no sé hacer un informe limpio! ¡Lo raspo y se rompe, Camila, se rompe el papel!"),
    ("VALERIA", "(Con desprecio frío, cruzándose de brazos). Es un papel, psicótica. Detente, estás sudando como un cerdo."),
    ("MATEO", "(Golpe seco en la mesa). ¡Suficiente! Sofía, siéntate y baja la cabeza. Valeria, te callas de una buena vez. Retomaremos el orden. Ahora."),
    ("VALERIA", "(Inclinándose sobre la vela, invadiendo su rostro en el cono de luz). ¿Qué orden vas a retomar en la oscuridad, brigadier? Estás sudando frío tú también. ¿A quién vas a reportar si ni siquiera puedes ver la puerta?"),
    ("LUCAS", "(Sonriendo desde su sombra). Uy. Golpe directo al ego. ¿Te vas a dejar, Mateo? ¿O vas a sacar tu libretita de amonestaciones en braille?"),
    ("MATEO", "Nadie me habla en ese tono. Ustedes dos están al límite del desacato."),
    ("VALERIA", "¿Desacato? ¿Desacato? ¡Eres un alumno, igual que yo! No eres el alcaide, Mateo, ¡eres el perrito faldero que obedece todo para que no lo manden de vuelta a su pueblo!"),
    ("CAMILA", "¡Valeria, por favor! ¡Chicos! ¡Nos estamos ahogando en un vaso de agua!"),
    ("MATEO", "Retrocede, Valeria. Te vas al rincón. Fuera del perímetro de luz. Es una orden."),
    ("VALERIA", "Oblígame."),
]

for speaker, text in dialogues_acto1_c:
    story.append(Paragraph(speaker, char_style))
    story.append(Paragraph(text, dialogue_style))

story.append(Paragraph("(MATEO avanza para empujarla. VALERIA no retrocede y le planta el pecho. En el forcejeo físico en el estrecho círculo de luz, ambos trastabillan hacia atrás y embisten con violencia a DANTE, agazapado en el suelo).", stage_dir_style))
story.append(Paragraph("DANTE: (Un grito ahogado). ¡Ah!", dialogue_style))
story.append(Paragraph("(El golpe proyecta a Dante hacia el frente. Sus manos resbalan. La mochila cae de golpe contra las tablas; la costura cede y la cremallera se abre).", stage_dir_style))
story.append(Paragraph("(De su interior, resbala pesadamente sobre el suelo un objeto rígido: un FÓLDER PLÁSTICO DE UN ROJO BRILLANTE Y GRUESO. Se desliza por el piso y se detiene en seco en la punta de los zapatos de ISABEL).", stage_dir_style))
story.append(Paragraph("(Nadie se mueve. Todos reconocen de inmediato ese color y ese membrete oficial).", stage_dir_style))

dialogues_acto1_d = [
    ("JOAQUÍN", "(La voz se le quiebra, perdiendo su pulso matemático). Ese... ese es un archivo de Coordinación Psicológica. Los rojos están bajo llave."),
    ("DANTE", "(En el suelo, encogiéndose en posición fetal, balbuceando hacia las tablas). Se me... se me cayó. Estaba abierto. El cajón estaba abierto."),
    ("MATEO", "(Lívido, petrificado). Robaste un documento confidencial. Eso es expulsión automática."),
    ("DANTE", "(Murmurando sin alzar la cabeza). Me llamaron. La psicóloga me citó en el recreo. Estaba ahí encima. Solo... solo leí mi nombre en la portada. Vi mi nombre. Y me dio terror. Me lo guardé. No quería. Se me pegó a la mano."),
    ("LUCAS", "¿Tu nombre?"),
    ("DANTE", "Y los de ustedes."),
]

for speaker, text in dialogues_acto1_d:
    story.append(Paragraph(speaker, char_style))
    story.append(Paragraph(text, dialogue_style))

story.append(Paragraph("(El silencio en la sala se vuelve casi irrespirable. Afuera, la lluvia azota los vidrios).", stage_dir_style))
story.append(Paragraph("(ISABEL lentamente, sin apresurarse, se agacha. Recoge el fólder rojo con ambas manos. Lo levanta y lo sitúa en el centro exacto de la mesa, bajo la lumbre de las tres velas. Abre la cubierta).", stage_dir_style))

dialogues_acto1_e = [
    ("MATEO", "(Con un hilo de voz). Isabel. Ciérralo. Como brigadier exijo que lo cierres."),
    ("ISABEL", "(Voz grave, serena, arrastrando las sílabas. Lee el encabezado oficial). 'Evaluación final de permanencia. Área de Psicología. Confidencial.'"),
    ("SOFÍA", "(Apretándose los nudillos hasta que crujen). No lo leas. Por favor, Isabel, no lo leas."),
    ("ISABEL", "(La llama parpadea en sus pupilas. Continúa sin inmutarse). 'Resolución treinta y cuatro. Aplicación efectiva: Lunes a primera hora.'"),
    ("VALERIA", "(Completamente tiesa, despojada de su cinismo). ¿Qué dice, Isabel? Ve al grano."),
    ("ISABEL", "(Alza la mirada despacio, recorriendo uno a uno los rostros del grupo). 'Dos estudiantes del Pabellón B serán separados definitivamente de la institución... por riesgo de colapso psicológico.'"),
    ("CAMILA", "(Con la voz destrozada por el pánico, un susurro que hiela la sangre). Somos... el Pabellón B."),
]

for speaker, text in dialogues_acto1_e:
    story.append(Paragraph(speaker, char_style))
    story.append(Paragraph(text, dialogue_style))

story.append(Paragraph("(En ese instante: [SONIDO]: [AUDIO 03 - TRUENO_SECO_CERCANO]. Un golpe ensordecedor que sacude las ventanas).", stage_dir_style))
story.append(Paragraph("(Una ráfaga helada de viento entra por la rendija y sopla las tres velas al unísono).", stage_dir_style))
story.append(Paragraph("[ILUMINACIÓN]: APAGÓN SÚBITO. NEGRURA TOTAL.", cue_style))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>TELÓN RÁPIDO / FIN DEL ACTO I</b>", subtitle_style))
story.append(Spacer(1, 14))

# ==================== ACTO 2 ====================
story.append(PageBreak())
story.append(Paragraph("ACTO II: LA CACERÍA EN LA PENUMBRA", h1_style))
story.append(Paragraph("(Tiempo escénico estimado: 16 a 18 minutos. Oscuridad total tras el trueno. En la negrura absoluta solo se percibe la respiración convulsa y jadeante de SOFÍA, casi un estertor de asfixia. Se escucha el roce nervioso de telas y el raspado de un fósforo sobre la lija. Falla. Un segundo raspado: salta una chispa anaranjada que ilumina fugazmente la cuenca de los ojos de ISABEL. La cerilla prende. Isabel enciende con mano firme la primera vela, luego la segunda, y finalmente la tercera).", stage_dir_style))
story.append(Paragraph("[ILUMINACIÓN]: RETORNO DEL CÍRCULO ÁMBAR DE TRES VELAS. La luz es aún más trémula y opresiva. Los ocho rostros surgen de las sombras como máscaras descompuestas. Sobre el centro de la mesa, el FÓLDER ROJO yace abierto como una incisión quirúrgica. La carátula muestra el sello institucional: 'RESOLUCIÓN 34 - EXPEDIENTE DE SEPARACIÓN INMEDIATA').", cue_style))
story.append(Paragraph("[AUDIO 04 - LLUVIA_SORDINA_Y_GOTEO_ZINC] — El aguacero sobre la calamina se transforma en un rumor constante, un tamborileo sordo e hipnótico.", cue_style))

dialogues_acto2 = [
    ("MATEO", "(Da un paso al frente con el torso erguido por inercia militar, pero las manos le tiemblan ostensiblemente. Apunta con el dedo al fólder). Nadie vuelve a tocar ese documento. Esto califica como infracción de grado tres en el Reglamento de Convivencia: 'Sustracción de material administrativo reservado'. Como brigadier del pabellón asumo la custodia legal del expediente hasta las seis de la mañana."),
    ("VALERIA", "(Avanza de golpe, plantando ambas palmas planas sobre la mesa, inclinándose sobre el fuego; sus ojos brillan con un odio lúcido). Toca esa carpeta, Mateo, y te juro que te parto los dedos contra la fórmica."),
    ("MATEO", "Es procedimiento estándar, Valeria. Si el monitor entra y nos encuentra con esto, no botan a dos: nos expulsan a los ocho por encubrimiento de falta grave. ¡A los ocho!"),
    ("VALERIA", "¡Me importa un carajo tu procedimiento estándar! ¿Te das cuenta de lo que estás diciendo? ¡Tú no quieres guardar la carpeta por el reglamento! ¡Quieres entregársela al director el lunes en bandeja de plata para decirle: 'Aquí tiene, señor Director, yo cumplí con mi deber, consérveme la beca y expulse a los otros dos'!"),
    ("MATEO", "(La mandíbula se le traba en un espasmo). Cuida tus palabras. No tienes derecho a..."),
    ("SOFÍA", "(Sentada de lado, encorvada, meciéndose sobre su propio eje; sus dedos se clavan en sus muslos a través del pantalón escolar). Pabellón B... Pabellón B. No es el pabellón de tercero. No es quinto C. No son los de la costa. Somos nosotros. Esta mesa. Esta maldita mesa."),
    ("LUCAS", "(Apoyado en el marco de la pizarra, soltando una risita seca, quebrada, que resuena hueca en la penumbra). Bienvenidos al matadero, señores de la excelencia. El Estado invierte quince mil soles al año por cada geniecito de provincia... pero si una tuerca se desgasta, no la lubrican. La tiran al tacho y piden otra de repuesto. Control de calidad. ¿O creían que el desayuno gratis era por amor a la patria?"),
    ("CAMILA", "(Con los ojos enrojecidos, interponiéndose entre Mateo y Valeria con las manos temblando en el aire). Chicos, por favor... no nos hablemos así. Debe haber un error. La señora Rivas no haría una lista sin hablar antes con nuestros tutores. Ella... ella nos escucha cuando lloramos..."),
    ("VALERIA", "(Volviéndose hacia Camila con ferocidad). ¡Despierta de una puta vez, Camila! ¡Deja de repartir sonrisas de galletita de avena! ¿No escuchaste lo que leyó Isabel? 'Separados definitivamente este lunes por riesgo de colapso psicológico'. ¡No nos están mandando a descansar a la playa! ¡Nos están botando como a perros rabiosos!"),
    ("JOAQUÍN", "(Ha permanecido inmóvil, pero sus ojos van y vienen de la mesa a las caras de todos con una fijeza obsesiva. De pronto, saca de su bolsillo un bolígrafo de cuatro colores y su libreta de notas cuadriculada). Silencio. Cállense. El pánico es un vector entrópico inútil. Hay que auditar esto con números."),
    ("LUCAS", "Llegó el contador público. Saca tu ábaco, genio, dinos cuánto pesamos en la balanza de carne."),
    ("JOAQUÍN", "(Abre la libreta con un crujido seco. Su voz adopta el ritmo acelerado, monocorde y despiadado de una ametralladora forense). Escuchen. La Dirección de Psicología no opera con intuiciones místicas. Opera bajo la Guía Técnica del Minedu para Colegios de Alto Rendimiento. La matriz de permanencia tiene cuatro parámetros medibles: ausencias injustificadas, caída porcentual de calificaciones, reportes de disciplina y visitas al tópico de enfermería en el último bimestre."),
    ("MATEO", "(Tragando saliva). Eso es confidencial. No puedes saber las visitas al tópico."),
    ("JOAQUÍN", "Yo soy el delegado de salud y convivencia del turno noche. Yo firmo el padrón de botiquín cada viernes para reponer paracetamol. En las últimas ocho semanas el Pabellón B ha registrado exactamente setenta y cuatro visitas a la enfermería."),
    ("CAMILA", "(En un susurro aterrado). ¿Tantas...?"),
    ("JOAQUÍN", "Setenta y cuatro. Pero el ochenta y tres por ciento de esas atenciones... están concentradas en solo tres personas."),
    ("(Un silencio denso y punzante corta la respiración colectiva. Las sombras de los ocho parecen congelarse contra los muros descascarados).", stage_dir_style),
    ("JOAQUÍN", "(Apunta con el extremo metálico del bolígrafo directamente al pecho de SOFÍA). Primera candidata: Sofía Mendoza. Treinta y dos ingresos al tópico entre agosto y octubre. Motivos registrados: 'cefalea tensional invalidante', 'espasmos gastrointestinales', 'taquicardia reactiva en periodos de evaluación'. Caída de rendimiento: de 19.8 a 17.2 en la prueba estandarizada de Química. Y temblor distal en ambas manos desde hace dos meses."),
    ("SOFÍA", "(Se pone de pie de un salto tan violento que su silla cae hacia atrás con un golpe sordo contra el suelo). ¡Cállate! ¡Cállate la boca, Joaquín! ¡No metas mis notas en esto!"),
    ("JOAQUÍN", "Son hechos objetivos, Sofía. Los algoritmos no odian a la gente, solo procesan datos."),
    ("SOFÍA", "(Avanza hacia la mesa con los ojos desorbitados, las venas del cuello infladas; su respiración es un fuelle roto). ¡Mis datos no son un colapso! ¡Esa caída de Química fue porque el profesor Quispe me quitó dos puntos por entregar la prueba tres segundos tarde! ¡Tres segundos! ¡Yo no estoy loca! ¡Tengo diecinueve punto cuatro de promedio acumulado desde tercero! ¡Soy la número uno del cuadro de honor regional!"),
    ("VALERIA", "(Con una crueldad teñida de amargura). Número uno en vomitar bilis en el tacho del segundo piso todos los martes a las seis de la mañana, Sofía. Toda la sección te ha escuchado atragantarte."),
    ("SOFÍA", "(Se tapa los oídos con desesperación infantil). ¡Mentira! ¡Es el desayuno! ¡La avena con soya que nos dan tiene grumos y me cae mal! ¡No estoy enferma!"),
    ("CAMILA", "(Abrazándola por los hombros). Sofi, cálmate, nadie está diciendo que estés enferma..."),
    ("SOFÍA", "(Empuja a Camila con una fuerza descomunal nacida del espanto). ¡Suéltame! ¡No me toquen! ¡Si me botan el lunes mi mamá se muere! ¿Saben cuánto debe al banco? Diez mil soles... Diez mil soles pidió a la cooperativa para comprarme el uniforme de gala, los zapatos de cuero y la laptop para que yo viniera aquí... Toda mi familia le dijo que estaba loca, que una chica de pueblo no aguanta este ritmo... ¡Mi mamá les dijo a todos que yo iba a ser ingeniera en Lima! ¡Si llego a Bagua el martes con la maleta en la mano y el papel de 'colapso psicológico', mi mamá no lo va a resistir! ¡Se muere!"),
    ("(SOFÍA se abalanza ciegamente sobre la mesa para arrebatar el fólder rojo. LUCAS reacciona a tiempo y la sujeta de los antebrazos; ambos forcejean al borde de derribar las velas. La cera líquida salpica los papeles).", stage_dir_style),
    ("LUCAS", "¡Suelta eso, Sofía! ¡Vas a quemar la mesa, carajo!"),
    ("SOFÍA", "(Gritando con un desgarro animal, arañando la manga de Lucas). ¡Déjame ver mi nombre! ¡Tengo que romperlo! ¡Si no está el papel no me pueden sacar! ¡Déjame romperlo!"),
    ("(LUCAS logra sentarla a la fuerza en otra silla. Sofía se derrumba sobre la mesa, enterrando la cara entre los brazos, con sollozos secos, espasmódicos, sin lágrimas ya, puras arcadas de aire).", stage_dir_style),
    ("VALERIA", "(Mirando a Lucas con los ojos entrecerrados, con desdén afilado). Qué eficiente te volviste de repente, payaso. El héroe de la disciplina. ¿Por qué no dejas que Joaquín te lea tus numeritos a ti también?"),
    ("LUCAS", "(Intentando recuperar su mueca burlona, sacudiéndose las solapas). Conmigo no gasten tinta, muchachos. Yo no piso la enfermería porque tengo sistema inmunológico de rata de basural. Soy impermeable a la tragedia."),
    ("JOAQUÍN", "(Sin levantar la vista de su cuaderno, con frialdad implacable). Lucas Paredes. Cero visitas a enfermería, es verdad. Pero cuatro reportes de evasión de clase en el taller de Teoría del Conocimiento. Siete trabajos sin entregar en el programa IB. Y en la ficha de orientación vocacional del lunes pasado... dejaste la casilla de 'Universidad de Destino' en blanco y dibujaste un ahorcado colgando de una rama."),
    ("LUCAS", "(La sonrisa se le congela en una mueca grotesca). Era humor negro, cerebrito. Arte contemporáneo. No tienes sentido de la ironía."),
    ("VALERIA", "(Da dos pasos lentos hacia él, acorralándolo contra el pizarrón; su tono baja a un susurro que corta más que un grito). No era un chiste, Lucas. Diles por qué dejaste la ficha en blanco. Diles por qué nunca sales en las mañanas de domingo cuando bajan los carros de las familias de Chachapoyas y Chiclayo con tapers de comida."),
    ("LUCAS", "(Trata de apartar la mirada). Valeria, cállate. No te metas ahí."),
    ("VALERIA", "Diles por qué en Navidad fuiste el único infeliz que se quedó en el internado comiendo pollo frío con los wachis."),
    ("LUCAS", "(Explota de golpe, la voz se le quiebra en un rugido estridente, despojado de toda máscara cínica). ¡Porque no tengo a dónde mierda ir! ¿Eso querían escuchar todos? ¿Están contentos? ¡Mi papá se largó con otra mujer a Rioja hace dos años y cambió el chip del celular! ¡Mi mamá se fue a Trujillo con su nuevo marido y me dijo bien clarito en la puerta del terminal: 'Aprovecha el internado, Lucas, que allá te dan techo, comida y ropa, porque conmigo ya no hay espacio'! ¡Hicieron fiesta en mi barrio cuando ingresé, pero no de orgullo! ¡Hicieron fiesta porque se libraron de una boca que alimentar!"),
    ("(Los hombros de Lucas caen pesadamente. Se pasa la manga por los ojos en un gesto avergonzado y tosco).", stage_dir_style),
    ("LUCAS", "Si me sacan el lunes de este colegio... no hay bus que me recoja. No hay casa. No hay un carajo. Duermo en la sala de espera del terminal de Chachapoyas hasta que el serenazgo me bote. Así que Joaquín... ponme en tu lista. Saca tu promedio y anótame. Soy el candidato perfecto."),
    ("(Un silencio plúmbeo desciende sobre el cuarto. Isabel no ha pestañeado. Sus manos cobrizas reposan sobre la fórmica como dos raíces centenarias).", stage_dir_style),
    ("ISABEL", "(Voz de pecho, solemne, lentísima). El fólder rojo no estaba en ningún cajón abierto."),
    ("(Todos giran los rostros hacia ella. La luz de las velas tiembla en las miradas).", stage_dir_style),
    ("MATEO", "¿Qué dices, Isabel?"),
    ("ISABEL", "Yo limpié la oficina de Coordinación Psicológica el martes con Camila por la guardia comunitaria. El armario de los expedientes de baja médica es de fierro verde. Tiene cerrojo y candado de combinación de cuatro dígitos. Nadie se encuentra una carpeta confidencial 'tirada por casualidad' en un pasillo."),
    ("(Isabel levanta la vista y clava sus ojos oscuros directamente en DANTE, agazapado contra la pared en el rincón más oscuro del SUM).", stage_dir_style),
    ("ISABEL", "Habla, Dante."),
    ("VALERIA", "(El aire se electrifica. Valeria camina despacio hacia la esquina donde Dante tiembla con la mochila destrozada entre las rodillas). Dante. Mírame a la cara."),
    ("DANTE", "(Con la voz enterrada en el pecho, un gemido inaudible). No me hagan nada... No me miren..."),
    ("MATEO", "(Avanza también, con tono perentorio). Dante, responde. ¿Quién te dio esa carpeta? ¿Por qué estaba en tu mochila?"),
    ("DANTE", "(Empieza a sollozar con espasmos en los hombros, sacudiendo la cabeza en una negativa desesperada). Me dijeron que era la única forma... Me dijeron que era por mi bien..."),
    ("VALERIA", "(Se agacha frente a él, le toma violentamente las manos y lo obliga a levantar el rostro bañado en sudor y lágrimas). ¿Quién te lo dijo, Dante? ¡Habla o te saco las palabras a golpes!"),
    ("DANTE", "(Un alarido contenido que revienta en el cuarto). ¡La señora Rivas! ¡La psicóloga!"),
    ("CAMILA", "(Llevándose las manos a la boca, perdiendo el color). Dios mío..."),
    ("DANTE", "(Las palabras le brotan atropelladas, manchadas de culpa insoportable). En julio... me jalaron en Matemática y en Física Superior. En el COAR no puedes repetir curso. Me tocaba expulsión por rendimiento académico. La señorita Rivas me citó a su consultorio. Cerró la puerta. Me dijo: 'Dante, tú eres un chico invisible, callado, nadie sospecha de ti'. Me entregó una libreta con forro azul. Me dijo que si yo observaba a mis compañeros del pabellón... si yo le anotaba quién se encerraba a llorar después de las diez... quién tenía ataques de pánico antes de los exámenes... quién escondía pastillas en el camarote... ella iba a justificar mis notas en el consejo docente y me iba a proteger."),
    ("MATEO", "(Retrocede un paso, horrorizado, con la boca entreabierta). Fuiste el informante... Eras el topo."),
    ("DANTE", "(Golpeándose las sienes con los puños cerrados). ¡Yo no quería! ¡Tenía miedo! ¡Me daba pánico volver a mi casa como un fracasado! Pero hoy... hoy a las seis de la tarde me llamó para entregarle las notas de la semana. Y vi ese fólder rojo sobre su escritorio con la Resolución 34. Me acerqué mientras ella fue al baño... y leí las hojas del anexo. ¡Eran mis palabras! ¡Las frases exactas que yo le había contado de ustedes estaban redactadas como diagnósticos clínicos! ¡Lo que le conté de las náuseas de Sofía... lo de las burlas de Lucas... lo de las pesadillas de Mateo! ¡Usaron mis notas para justificar la expulsión de dos de nosotros! ¡Yo armé la horca! ¡Yo les puse la soga en el cuello!"),
    ("(La revelación cae como una losa de granito. Sofía alza la cabeza, mirándolo con horror lívido. Camila retrocede hasta chocar contra la biblioteca. Mateo aprieta los puños hasta que los tendones de sus brazos se marcan bajo la camisa blanca).", stage_dir_style),
    ("MATEO", "(Con la voz ahogada en bilis, dando un paso amenazante hacia Dante). ¡Miserable! ¡Nos vendiste por un par de notas aprobatorias! ¡Traidor!"),
    ("(MATEO alza el brazo con el puño cerrado para golpear a Dante. Dante no se cubre, solo cierra los ojos esperando el impacto).", stage_dir_style),
    ("VALERIA", "(Se interpone de un salto feroz, interceptando el brazo de Mateo en el aire con un chasquido seco de muñecas). ¡No lo toques, Mateo!"),
    ("MATEO", "¡Suéltame, Valeria! ¡Este cobarde nos ha destruido a todos!"),
    ("VALERIA", "¡Y tú lo hubieras hecho exactamente igual si te ofrecían conservar tu medalla de brigadier general! ¡No te hagas el santo de altar, que en este internado todos hemos aprendido a pisarle la cabeza al de al lado para que no nos ahoguen!"),
    ("CAMILA", "(Grita con un tono desgarrador que nadie le conocía, quebrando su habitual dulzura en una queja furibunda). ¡Basta! ¡Basta ya! ¿Es que no se dan cuenta de lo que nos han hecho? ¡Nos han convertido en monstruos! ¡Nos encierran aquí, nos dicen que somos la élite de la patria, y nos estamos despedazando vivos a oscuras por un trozo de papel!"),
    ("(Los tres quedan suspendidos en un nudo de respiraciones violentas, a punto de iniciar una gresca física sobre el piso húmedo).", stage_dir_style),
    ("(De pronto: el silencio más atroz corta el aire en seco).", stage_dir_style),
    ("[AUDIO 05 - PASOS_BOTAS_PASILLO] — Pesados, rítmicos, el chirrido inconfundible de suelas de jebe sobre la cera del pasillo exterior. Tienen la cadencia inflexible de la autoridad nocturna.", cue_style),
    ("(Nadie respira. Los ocho cuerpos quedan petrificados en las posturas exactas donde los sorprendió el sonido).", stage_dir_style),
    ("[ILUMINACIÓN]: EL HAZ CEGADOR DE UNA LINTERNA EXTERIOR barre horizontalmente la rendija inferior de la puerta del SUM. La franja de luz blanca corta el suelo de madera, rozando los zapatos de Mateo y Valeria.", cue_style),
    ("(Los pasos se detienen exactamente al otro lado del umbral de madera. Hay un hombre parado a dos metros de ellos, con la linterna apuntando a la cerradura).", stage_dir_style),
    ("MATEO", "(En el susurro más fino y agónico que el oído humano pueda registrar). El monitor..."),
    (Spacer(1, 4), ""),
    ("<b>TELÓN RÁPIDO / FIN DEL ACTO II</b>", subtitle_style),
]

def add_to_story(items):
    for item in items:
        if isinstance(item, tuple):
            val1, val2 = item
            if isinstance(val1, Spacer):
                story.append(val1)
            elif isinstance(val2, ParagraphStyle):
                story.append(Paragraph(val1, val2))
            elif isinstance(val1, str) and isinstance(val2, str):
                story.append(Paragraph(val1, char_style))
                story.append(Paragraph(val2, dialogue_style))
        elif hasattr(item, 'wrap'):
            story.append(item)

add_to_story(dialogues_acto2)

# ==================== ACTO 3 ====================
story.append(PageBreak())
story.append(Paragraph("ACTO III: EL PACTO DE LA NIEBLA", h1_style))
story.append(Paragraph("(Tiempo escénico estimado: 13 a 15 minutos. El escenario está inmovilizado en una tensión claustrofóbica absoluta. Sesenta segundos de silencio escénico riguroso: un asedio invisible donde un solo crujido de madera significa la expulsión inmediata de los ocho por desacato y posesión de material confidencial).", stage_dir_style))
story.append(Paragraph("(ISABEL, con una rapidez fría y sin titubeos, humedece los dedos índice y pulgar con saliva y apaga las tres velas de sebo una por una: chasquido sordo, chisporroteo y penumbra azulada).", stage_dir_style))
story.append(Paragraph("[ILUMINACIÓN]: OSCURIDAD CASI TOTAL. Solo entra por la rendija inferior la franja de luz blanca de la linterna del monitor, y por el ventanal la penumbra grisácea del temporal de niebla amazónica.", cue_style))
story.append(Paragraph("(CAMILA cubre con ambas manos la boca de SOFÍA para silenciar su hiperventilación; Sofía tiembla contra su pecho pero obedece. LUCAS pone una mano firme sobre la nuca de DANTE en el piso, inmovilizándolo como a un animal asustado. MATEO y VALERIA no se mueven ni un milímetro, congelados hombro a hombro frente a la mesa).", stage_dir_style))
story.append(Paragraph("[AUDIO 06 - FORCEJEO_CERRADURA_MANIJA] — El picaporte metálico de la puerta baja lentamente con un crujido agudo. Tiembla contra el seguro interno echado por Mateo. Una fuerza exterior empuja la hoja de madera; el marco cede dos milímetros.", cue_style))
story.append(Paragraph("(Se escucha la respiración cansada del monitor al otro lado de la puerta, un carraspeo tosco y el tintineo de un manojo de llaves pesadas. El haz de luz de la linterna titila por última vez bajo la rendija, gira y se aparta. Los pasos de botas se reanudan, alejándose con lentitud por el pasillo hacia los dormitorios).", stage_dir_style))
story.append(Paragraph("(Pasan diez segundos eternos. El grupo exhala al unísono, como si un solo pulmón gigante volviera a recibir oxígeno).", stage_dir_style))

dialogues_acto3 = [
    ("ISABEL", "(En la negrura, su voz grave resuena con la quietud de una campana sumergida). Ya pasó la loma del pasillo. No va a volver hasta las cuatro."),
    ("(Un fósforo se enciende en las manos de Isabel. Esta vez enciende UNA SOLA VELA, la del centro. Su llama solitaria proyecta sombras íntimas, casi litúrgicas, congregando a los ocho en un círculo mucho más estrecho y vulnerable).", stage_dir_style),
    ("[ILUMINACIÓN]: VELA ÚNICA CENTRAL. Tono ambarino tenue y concentrado. Las facciones duras se suavizan por el agotamiento. Sobre la mesa permanece intacto el FÓLDER ROJO).", cue_style),
    ("VALERIA", "(Exhala un largo hilo de aire, apoyando la frente contra sus palmas; luego levanta los ojos hacia la carpeta). Estuvimos a medio centímetro de la calle. A medio centímetro."),
    ("JOAQUÍN", "(Acomodándose los lentes con dedos rígidos). Si esa manija cedía, la probabilidad de apelación exitosa era de cero coma cero por ciento. Infracción en flagrancia."),
    ("LUCAS", "(Sentado en el piso al lado de Dante, con una sonrisa apagada y humana). Gracias por no hacer tus cálculos en voz alta mientras el hombre probaba la chapa, Joaquín. De verdad te lo agradezco."),
    ("SOFÍA", "(Sentada erguida, secándose las mejillas con las mangas empapadas; su voz ya no tiene el filo de la histeria, solo una desolación transparente). El fólder sigue ahí."),
    ("VALERIA", "(Extiende la mano lentamente sobre la mesa hacia la solapa del documento). Bueno. Ya se terminó la cacería de brujas. Ya sabemos que la lista no fue un milagro divino ni una casualidad: fue un informe redactado con la sangre de todos nosotros. Solo queda un paso. Abramos la última página. Leamos los dos nombres. De una buena vez."),
    ("CAMILA", "¿Para qué, Valeria? ¿Para qué quieres saberlo ahora?"),
    ("VALERIA", "Para saber si tengo que empacar mis cosas a las cinco de la mañana, Camila. Prefiero saber que estoy muerta a esperar que me fusilen en la formación del lunes delante de todo el colegio."),
    ("JOAQUÍN", "Tiene fundamento lógico. Conocer las identidades permite a los dos afectados formular un recurso extraordinario ante el comité de bienestar del Minedu en Lima. El ocultamiento no altera la realidad jurídica del documento."),
    ("(JOAQUÍN extiende la mano para voltear la última página del expediente. Una mano firme se posa sobre la suya y la detiene en seco: es la mano de MATEO).", stage_dir_style),
    ("MATEO", "(Voz serena, sin gritos, pero con una firmeza que no proviene del manual de disciplina, sino de una convicción rota y renacida). No lo abras."),
    ("VALERIA", "¿Ahora vuelves a jugar al brigadier modelo, Mateo? ¿Vas a requisarlo otra vez?"),
    ("MATEO", "(Mira a Valeria a los ojos; por primera vez no hay rigidez militar en su semblante, solo una honda fatiga moral). No soy el brigadier de nadie esta noche, Valeria. Míranos. Míranos bien. Si abrimos esa hoja y leemos los dos nombres... ¿qué va a pasar? Los seis que no estemos en la lista vamos a suspirar de alivio en secreto. Nos vamos a ir a la cama pensando: 'Menos mal no fui yo'. Vamos a mirar a los otros dos con una lástima podrida durante el desayuno del domingo. Y el lunes a las siete de la mañana, cuando el director tome el micrófono en el patio y diga que 'el COAR es solo para los más fuertes, para los que no se quiebran jamás', nos vamos a quedar calladitos en la fila, con el mentón arriba, sintiéndonos superiores. Y ahí sí que seremos unos cobardes. Unos miserables perfectos con diploma de honor."),
    ("ISABEL", "(Sus palabras caen con el peso lento y ancestral de una sentencia de la tierra). En mi pueblo, a orillas del río Santiago, cuando la creciente se lleva la canoa de una familia, no nos reunimos a debatir quién remó más despacio o quién tuvo la culpa por no amarrarla bien. Nos metemos al agua con sogas y sacamos la madera entre todos. Porque si hoy dejamos que el río se trague la barca del vecino diciendo 'él era torpe', mañana la correntada viene por nuestra casa y no queda nadie en la orilla para alcanzarnos una saca."),
    ("CAMILA", "El colegio nos prometió que éramos los mejores del país... los líderes del mañana."),
    ("ISABEL", "Nos prometieron un futuro a cambio de comernos vivos los unos a los otros por dos décimas de promedio. Nos dijeron que ser excelentes era no llorar nunca, no sangrar nunca, no cansarse nunca. Eso no es excelencia, Camila. Eso es una fábrica de piedras."),
    ("LUCAS", "(Pone la mano sobre el hombro de Dante, que sigue encogido en el suelo con la cabeza baja). Dante. Levántate."),
    ("(DANTE alza la mirada despacio, con ojos hinchados y rostro desfigurado por la vergüenza. Con torpeza, se pone de pie y se acerca al borde de la mesa).", stage_dir_style),
    ("DANTE", "(Con la voz quebrada). Si el lunes me expulsan... me lo merezco. Yo escribí las notas. Yo fui el que tuvo miedo."),
    ("SOFÍA", "(Lo mira desde el otro lado de la vela. Una pausa densa, humana). Todos tuvimos miedo, Dante. Yo vomito todas las mañanas porque le tengo terror a mi propia madre. Porque creo que si saco dieciocho ya no valgo nada en este mundo. Tú tuviste miedo a que te botaran... igual que yo. Igual que Lucas. Igual que Mateo."),
    ("JOAQUÍN", "(Mira su libreta de notas, llena de porcentajes y auditorías de tópicos. Lentamente, la cierra). Los datos no registran eso. El protocolo no mide la soledad."),
    ("VALERIA", "¿Y entonces qué hacemos con esta basura de fólder? ¿Se lo dejamos debajo de la puerta a la señora Rivas con una cartita de perdón?"),
    ("LUCAS", "(Una sonrisa luminosa y limpia asoma en sus labios; toma la vela única del centro y la acerca al borde de la mesa). No hay nada que perdonar. Y no hay nada que devolver. Las cosas que no existen no se pueden aplicar el lunes."),
    ("MATEO", "(Mira el fuego de la vela y luego recorre uno a uno los ojos de sus siete compañeros). Si la Resolución 34 no llega al despacho del director... el lunes a primera hora no hay lista que firmar."),
    ("JOAQUÍN", "Van a abrir una investigación general por pérdida de material administrativo. Nos van a interrogar a todos."),
    ("ISABEL", "Que nos interroguen. Pero tendrán que mirarnos a la cara a los ocho juntos. No a dos sombras solas en un cuarto cerrado."),
    ("CAMILA", "(Con determinación serena). A los ocho juntos. En bloque."),
    ("(MATEO toma el FÓLDER ROJO. Con un movimiento deliberado y sin vacilación, desengancha el broche metálico. Extrae el expediente completo: la carátula membretada, el dictamen psicológico y la hoja final con los dos nombres sellados que nadie ha querido leer).", stage_dir_style),
    ("(MATEO extiende el documento hacia DANTE).", stage_dir_style),
    ("MATEO", "Tú lo trajiste hasta aquí para que no lo firmaran, Dante. Tú enciendes el fuego."),
    ("(DANTE mira el papel. Sus manos ya no tiemblan con la cobardía del principio, sino con la reverencia de quien realiza un sacramento. Toma la primera esquina de la hoja de expulsión y la acerca a la llama de la vela de sebo).", stage_dir_style),
    ("[ILUMINACIÓN]: CEREMONIA DE FUEGO. La esquina del papel prende con una llama anaranjada brillante que ilumina los ocho pares de ojos clavados en la combustión. Las sombras se estiran majestuosas sobre las paredes del SUM.", cue_style),
    ("(DANTE sostiene la hoja mientras el fuego devora los sellos oficiales y los párrafos del informe psicológico. Cuando la llama roza sus dedos, suelta la hoja en llamas sobre una bandeja metálica de instrumental que descansa en la mesa central).", stage_dir_style),
    ("(Uno a uno, en un ritual sin discursos ampulosos, los estudiantes toman partes del legajo confidencial y las entregan al fuego):", stage_dir_style),
    ("(SOFÍA arranca las hojas clínicas de seguimiento y las quema, viendo cómo los diagnósticos de colapso se retuercen en ceniza negra).", stage_dir_style),
    ("(LUCAS arroja las hojas de deméritos y amonestaciones con una calma profunda).", stage_dir_style),
    ("(VALERIA pliega la carátula roja plastificada y la sostiene sobre la flama hasta que el plástico se deforma y arde con un zumbido denso).", stage_dir_style),
    ("(JOAQUÍN arranca la hoja cuadriculada de su propia libreta —donde había calculado las probabilidades de descarte de sus compañeros— y la arroja al fuego de la bandeja).", stage_dir_style),
    ("(MATEO se lleva la mano al hombro izquierdo de su camisa blanca. Desprende con un tirón seco el cordón trenzado dorado de brigadier escolar. Lo sostiene un instante en la palma de la mano... y lo deposita suavemente en la mesa, al lado del plato donde las cenizas terminan de humear).", stage_dir_style),
    ("MATEO", "(En un susurro firme). El lunes nos presentamos a las siete. Todos con el uniforme planchado. Todos con la mirada al frente."),
    ("CAMILA", "Y si preguntan por el expediente..."),
    ("ISABEL", "Diremos que la tormenta se llevó muchas cosas este fin de semana. Pero no a nosotros."),
    ("(Las últimas brasas de la bandeja se apagan en un humo fino y azulado que asciende hacia las vigas del techo. Durante unos segundos solo se escucha el susurro de la niebla exterior).", stage_dir_style),
    ("[AUDIO 07 - ZUMBIDO_TRANSFORMADOR_ALTO_VOLTAJE] — A lo lejos, en el patio central, se escucha el chasquido sordo de una subestación eléctrica que reactiva su carga. Un zumbido grave de sesenta hercios empieza a crecer por las canaletas de la pared.", cue_style),
    ("[AUDIO 08 - CHISPAZO_FLUORESCENTE_PARPADEO] — ¡Zas! ¡Zas! Un chisporroteo seco y agudo.", cue_style),
    ("[ILUMINACIÓN]: RETORNO VIOLENTO DE LA ELECTRICIDAD. Los dos tubos fluorescentes del techo parpadean dos veces con una luz violeta pálida y se estabilizan de golpe en una LUZ BLANCA CLÍNICA, CRUDA Y DESPIADADA (6500 Kelvin).", cue_style),
    ("(La vela solitaria queda reducida al instante a un pábilo minúsculo, ahogado por la luminosidad blanca del aula. La atmósfera íntima y confesional de las sombras desaparece de golpe).", stage_dir_style),
    ("(La luz de hospital revela la crudeza del espacio: el aula de paredes descascaradas, las pizarras acrílicas llenas de fórmulas a medio borrar, el suelo salpicado de cera y lluvia, la bandeja metálica con un montoncito de cenizas negras aún humeantes en el centro de la mesa).", stage_dir_style),
    ("(Los ocho estudiantes parpadean encandilados. Sus rostros están deshechos por la noche en vela: ojos enrojecidos, ojeras profundas, camisas desabotonadas, cabellos revueltos por la humedad amazónica. Pero ninguno baja la mirada. Ninguno rehúye el contacto visual).", stage_dir_style),
    ("(Están alineados hombro con hombro alrededor de la mesa. Ya no forman un ring de boxeo ni un tribunal de inquisición: forman un bloque humano indivisible).", stage_dir_style),
    ("[AUDIO 04 - LLUVIA_SORDINA_Y_GOTEO_ZINC] — Afuera, el vendaval ha cesado por completo. Solo queda un goteo suave, rítmico y pacífico sobre las hojas de los árboles de la ceja de selva. Una claridad lechosa empieza a filtrarse débilmente por el ventanal: el amanecer del sábado en Chachapoyas.", cue_style),
    ("MATEO", "(Pasa la vista por cada uno de ellos. No hay orden marcial en su voz, solo una complicidad indestructible). Abran los libros. A las seis tocan diana para el desayuno."),
    ("(Sin decir una sola palabra más, JOAQUÍN se sienta y abre su texto de Cálculo. SOFÍA acomoda su cuaderno sin temblores en las manos. LUCAS levanta la silla caída y se sienta al lado de DANTE, dándole una palmada breve y sólida en la espalda. DANTE toma su lapicero. VALERIA e ISABEL se sientan lado a lado frente a la ventana. CAMILA respira hondo, con una sonrisa serena y descansada).", stage_dir_style),
    ("(A lo lejos, en el campanario del internado, suena el primer tañido limpio de las cinco y media de la mañana).", stage_dir_style),
    ("(Los ocho se inclinan sobre sus mesas bajo la luz blanca, estudiando en un silencio compacto, férreo y fraterno).", stage_dir_style),
    ("[ILUMINACIÓN]: CORTE SECO A OSCURIDAD TOTAL.", cue_style),
    (Spacer(1, 10), ""),
    ("<b>TELÓN FINAL</b>", title_style),
    (Spacer(1, 4), ""),
    ("FIN DE LA OBRA", subtitle_style),
]

add_to_story(dialogues_acto3)

doc.build(story)
print(f"PDF de la obra completa generado exitosamente en: {pdf_path}")
