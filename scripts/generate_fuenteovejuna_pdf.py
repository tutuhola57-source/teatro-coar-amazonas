import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

pdf_path = "public/libretos/fuenteovejuna-adaptacion-coar.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=54,
    leftMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

# Custom styles
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
    fontSize=13,
    leading=16,
    alignment=1,
    textColor=colors.HexColor('#d97706')
)

meta_style = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    alignment=1,
    textColor=colors.HexColor('#475569')
)

h1_style = ParagraphStyle(
    'ActHeading',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    spaceBefore=14,
    spaceAfter=8,
    textColor=colors.HexColor('#091224')
)

char_style = ParagraphStyle(
    'CharacterName',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#991b1b'),
    spaceBefore=8,
    spaceAfter=2
)

dialogue_style = ParagraphStyle(
    'Dialogue',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    leftIndent=15,
    spaceAfter=4,
    textColor=colors.HexColor('#1e293b')
)

stage_dir_style = ParagraphStyle(
    'StageDir',
    parent=styles['Italic'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    leading=12,
    leftIndent=15,
    spaceBefore=3,
    spaceAfter=4,
    textColor=colors.HexColor('#64748b')
)

story = []

# Title & Cover Header
story.append(Spacer(1, 20))
story.append(Paragraph("FUENTEOVEJUNA: LA VOZ DE UN PUEBLO", title_style))
story.append(Spacer(1, 6))
story.append(Paragraph("Adaptación Escénica en Tres Actos para el COAR Amazonas", subtitle_style))
story.append(Spacer(1, 8))
story.append(Paragraph("Texto dramático basado en la obra clásica de Félix Lope de Vega • Duración: 45-50 min", meta_style))
story.append(Spacer(1, 15))

# Cast Table
cast_data = [
    [Paragraph("<b>Personaje</b>", meta_style), Paragraph("<b>Perfil Escénico</b>", meta_style)],
    [Paragraph("<b>LAURENCIA</b>", char_style), Paragraph("Joven labradora indómita. Protagonista del levantamiento moral.", dialogue_style)],
    [Paragraph("<b>FRONDOSO</b>", char_style), Paragraph("Labrador valiente enamorado de Laurencia. Desafía al tirano.", dialogue_style)],
    [Paragraph("<b>EL COMENDADOR</b>", char_style), Paragraph("Fernán Gómez. Soberbio déspota feudal y abusador del pueblo.", dialogue_style)],
    [Paragraph("<b>PASCUALA</b>", char_style), Paragraph("Amiga íntima de Laurencia. Astuta, leal y combativa.", dialogue_style)],
    [Paragraph("<b>ESTEBAN</b>", char_style), Paragraph("Padre de Laurencia y Alcalde. Máxima autoridad moral comunal.", dialogue_style)],
    [Paragraph("<b>FLORES / EL JUEZ</b>", char_style), Paragraph("Lugarteniente del tirano (Actos I-II) / Juez Pesquisidor (Acto III).", dialogue_style)],
    [Paragraph("<b>JACINTA</b>", char_style), Paragraph("Joven comunera víctima del Comendador. Despierta el coraje comunal.", dialogue_style)],
    [Paragraph("<b>MENGO / COMUNERO</b>", char_style), Paragraph("Labrador fiel que sufre azotes y resiste el tormento en el juicio.", dialogue_style)],
]
t = Table(cast_data, colWidths=[130, 370])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(Spacer(1, 15))

# ACT I
story.append(Paragraph("ACTO I: EL DESAFÍO EN EL MONTE", h1_style))
story.append(Paragraph("(Iluminación en Ámbar Cálido. Sonido ambiental de campo y arroyo. Laurencia y Pascuala regresan con cestas).", stage_dir_style))
story.append(Paragraph("PASCUALA", char_style))
story.append(Paragraph("¿Y dices que no vas a ceder jamás, Laurencia? ¿Ni aun sabiendo quién es el Comendador?", dialogue_style))
story.append(Paragraph("LAURENCIA", char_style))
story.append(Paragraph("Ni aunque se vista de oro, Pascuala. Que sea dueño de las tierras no lo hace dueño de mi persona. Más vale comer pan seco con honra en una choza que sentarse a la mesa de un señor con la vergüenza en la frente.", dialogue_style))
story.append(Paragraph("(Entra Frondoso con paso apresurado).", stage_dir_style))
story.append(Paragraph("FRONDOSO", char_style))
story.append(Paragraph("¡Laurencia! Ya hablé con tu padre Esteban y me dio su bendición si tú consientes. Quiero desposarte ante el altar, que todo el pueblo sea testigo de que eres mi orgullo.", dialogue_style))
story.append(Paragraph("(Se oyen cascos de caballos. Luces cambian a azul frío. Entra el Comendador con Flores).", stage_dir_style))
story.append(Paragraph("COMENDADOR", char_style))
story.append(Paragraph("¿Dejarte pasar? Un señor feudal no pide permiso para contemplar lo que le pertenece. Tu padre es vasallo mío; tu honra me debe tributo. (Sujeta del brazo a Laurencia).", dialogue_style))
story.append(Paragraph("(Frondoso sale de su escondite y encañona al Comendador con su vara de labranza).", stage_dir_style))
story.append(Paragraph("FRONDOSO", char_style))
story.append(Paragraph("¡Suéltela, Fernán Gómez, o juro por mi sangre que no da un paso más en esta tierra! ¡Laurencia, corre al pueblo!", dialogue_style))
story.append(Spacer(1, 10))

# ACT II
story.append(Paragraph("ACTO II: LA BODA INTERRUMPIDA", h1_style))
story.append(Paragraph("(La plaza en fiesta nupcial. Música alegre de guitarra. Esteban bendice a Laurencia y Frondoso).", stage_dir_style))
story.append(Paragraph("ESTEBAN", char_style))
story.append(Paragraph("¡Por mi hija y por Frondoso! ¡Que haya pan en sus trojes, paz en su choza y justicia en su mesa!", dialogue_style))
story.append(Paragraph("(Irrumpe el Comendador con espadas. Luces en azul gélido y violeta).", stage_dir_style))
story.append(Paragraph("COMENDADOR", char_style))
story.append(Paragraph("¡Apresen a Frondoso y llévenlo a las mazmorras para la horca! ¡Y tú, Laurencia, vendrás a mi palacio ahora mismo!", dialogue_style))
story.append(Paragraph("ESTEBAN", char_style))
story.append(Paragraph("¡Soy el alcalde legítimo de la villa! ¡No puede pisotear la ley!", dialogue_style))
story.append(Paragraph("(El Comendador quiebra la vara de Esteban y se lleva a los novios por la fuerza. Silencio fúnebre).", stage_dir_style))
story.append(Paragraph("(Aparece Laurencia: vestidos desgarrados, marcas en el rostro y fuego en la mirada).", stage_dir_style))
story.append(Paragraph("LAURENCIA", char_style))
story.append(Paragraph("¿Viva? ¡Mírenme! ¿Ven estos golpes? ¿Ven la vergüenza en mi cuerpo? ¡Y ustedes sentados deliberando como ovejas ante el lobo! ¡No son hombres, son liebres cobardes! ¡Si ustedes no pelean, las mujeres de Fuenteovejuna iremos con piedras y con las uñas a derribar las puertas del palacio!", dialogue_style))
story.append(Paragraph("(Campana a rebato y luces rojas. El pueblo entero se alza con hoces y picas).", stage_dir_style))
story.append(Paragraph("ESTEBAN", char_style))
story.append(Paragraph("¡Tiene razón mi hija! ¡Se acabó la paciencia! ¡Esta noche Fuenteovejuna vive libre o muere toda junta! ¡Muera el tirano Fernán Gómez!", dialogue_style))
story.append(Spacer(1, 10))

# ACT III
story.append(Paragraph("ACTO III: EL JUICIO DE LA SANGRE", h1_style))
story.append(Paragraph("(Salón comunal bajo contraluz blanco estricto. Entra el Juez Pesquisidor con pliego real y potro de tortura).", stage_dir_style))
story.append(Paragraph("JUEZ", char_style))
story.append(Paragraph("Vengo en nombre de la Real Corona a esclarecer un crimen de lesa majestad. Anciano Esteban, dime quién mató al Comendador.", dialogue_style))
story.append(Paragraph("ESTEBAN", char_style))
story.append(Paragraph("Fuenteovejuna, señor.", dialogue_style))
story.append(Paragraph("JUEZ", char_style))
story.append(Paragraph("¡Apreten los cordeles en el potro! Tú, Mengo, ¿quién lo mató?", dialogue_style))
story.append(Paragraph("MENGO", char_style))
story.append(Paragraph("¡Fuenteovejuna lo hizo, señor!", dialogue_style))
story.append(Paragraph("JUEZ", char_style))
story.append(Paragraph("(A Laurencia). ¡Dime el nombre de una vez o tu esposo morirá en el patíbulo!", dialogue_style))
story.append(Paragraph("LAURENCIA", char_style))
story.append(Paragraph("La mano que empuñó la justicia fue la de todo un pueblo ofendido. ¡Fuenteovejuna, señor!", dialogue_style))
story.append(Paragraph("(Todo el elenco se une hombro con hombro formando un solo muro humano).", stage_dir_style))
story.append(Paragraph("JUEZ", char_style))
story.append(Paragraph("¿Y quién es Fuenteovejuna?", dialogue_style))
story.append(Paragraph("TODOS (ELENCO COMPLETO)", char_style))
story.append(Paragraph("¡TODO EL PUEBLO A UNA!", dialogue_style))
story.append(Paragraph("(El Juez baja la pluma sobrecogido por la lealtad comunal. Las luces se bañan en dorado teatral triunfal).", stage_dir_style))
story.append(Paragraph("JUEZ", char_style))
story.append(Paragraph("Un pueblo que resiste unido de esta manera no es una banda de facinerosos; es una comunidad que prefiere morir antes que volver a ser esclava. En Fuenteovejuna no hay criminal... el pueblo entero ha respondido por su dignidad.", dialogue_style))
story.append(Paragraph("(Música final campesina. Elenco unido con las manos en alto. Aplausos y oscuro final).", stage_dir_style))

doc.build(story)
print("PDF generado exitosamente en:", pdf_path)
