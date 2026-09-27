"""Catálogo de estilos de interiorismo.

Cada estilo reúne lo que un interiorista decidiría antes de dibujar nada:
paleta con reparto de uso, materiales, principios de distribución,
mobiliario y decoración por estancia, e iluminación. Lo usa el motor local
(sin IA) y también se le pasa a Claude como guía de estilo.

Los colores de `render` pintan la ilustración del salón en la ficha.
"""

ESTILOS = {
    "moderno_elegante": {
        "nombre": "Moderno elegante",
        "lema": "Blanco, negro y espacios abiertos de lujo",
        "palabras": ["elegante", "moderna", "moderno", "lujo", "lujosa", "sofisticada", "blanco y negro"],
        "coste_m2": (900, 1500),
        "concepto": (
            "Una casa de líneas puras y planta abierta donde el blanco envuelve y el negro "
            "dibuja: carpinterías, perfiles y piezas clave en negro mate sobre paredes y "
            "suelos claros. El lujo no viene de acumular, sino de la escala, la continuidad "
            "de materiales y una luz indirecta muy cuidada que hace que todo se sienta cálido."
        ),
        "principios": [
            "Planta abierta salón–comedor–cocina sin tabiques, zonificada con alfombras, luz y cambios de techo.",
            "Regla 70/20/10: 70 % blanco roto, 20 % negro mate, 10 % madera cálida y latón cepillado.",
            "Mismo pavimento continuo en toda la planta para ampliar visualmente el espacio.",
            "Almacenaje integrado y sin tiradores: la vista queda limpia y ordenada.",
            "Pocas piezas, pero grandes y de calidad: un sofá de escala generosa, una mesa escultórica.",
        ],
        "paleta": [
            ("Blanco roto", "#F4F2EE", "Paredes y techos (70 %)"),
            ("Negro mate", "#1C1C1E", "Carpinterías, perfiles, grifería, isla (20 %)"),
            ("Gris piedra", "#B9B5AE", "Textiles, microcemento, sombras"),
            ("Roble natural", "#B8895A", "Tarima, mesa de comedor, calidez"),
            ("Latón cepillado", "#B59A5B", "Detalles puntuales en luminarias y tiradores (acento)"),
        ],
        "materiales": [
            ("Porcelánico gran formato efecto mármol blanco (120×260)", "Suelo continuo de salón, cocina y baños"),
            ("Lacado negro mate antihuellas", "Frentes de cocina y armarios empotrados"),
            ("Roble natural aceitado", "Mesa de comedor, estanterías y cabeceros"),
            ("Mármol Nero Marquina", "Encimera o frente de isla, lavabos"),
            ("Vidrio y perfilería negra fina", "Puertas correderas, mamparas y separadores"),
        ],
        "render": {
            "pared": "#F4F2EE", "suelo": "#E4DED5", "techo": "#FAF9F7", "viga": "#1C1C1E",
            "sofa": "#D9D4CC", "madera": "#B8895A", "acento": "#1C1C1E", "metal": "#B59A5B",
            "textil": "#8E8A84", "led": "#FFD9A0",
        },
        "viga": "viga de madera lacada en negro mate (o falsa viga de pladur negra) con perfil LED empotrado en su cara inferior y superior",
        "estancias": {
            "salon": {
                "distribucion": "Gran espacio diáfano con el sofá flotando de espaldas al comedor y mirando al ventanal; la viga del techo marca el eje entre zona de estar y comedor.",
                "mobiliario": ["Sofá modular en L de 3,40 m tapizado en bouclé blanco roto", "Mesa de centro de mármol negro con base escultórica", "Dos butacas de piel negra con estructura metálica", "Mueble TV suspendido lacado negro de 3 m"],
                "decoracion": ["Alfombra de lana gris piedra de 3×4 m que ancla la zona de estar", "Cortinas de lino blanco de suelo a techo en riel oculto", "Un único cuadro abstracto de gran formato en blanco y negro", "Cojines en bouclé, lino y terciopelo negro para dar textura sin romper la paleta"],
                "toque": "Deja 90 cm de paso libre alrededor del sofá: el lujo es poder moverse sin esquivar muebles.",
            },
            "cocina": {
                "distribucion": "Cocina abierta al salón con isla central de 2,80 m que funciona como barra y zona de preparación; columnas de electrodomésticos integradas en el fondo.",
                "mobiliario": ["Isla con encimera de mármol Nero Marquina y taburetes altos de piel negra", "Frentes lacados negros sin tiradores (gola)", "Columna de horno y frigorífico integrados", "Campana integrada en encimera o en techo para no romper la vista"],
                "decoracion": ["Tres lámparas colgantes de latón sobre la isla", "Un bol de cerámica blanca y una tabla de roble como únicos objetos a la vista"],
                "toque": "Tira LED bajo el vuelo de la isla: por la noche parece flotar.",
            },
            "dormitorio": {
                "distribucion": "Cama centrada frente a la ventana o de lado a ella, con cabecero de pared completa y vestidor a continuación.",
                "mobiliario": ["Cabecero tapizado en gris piedra que ocupa todo el ancho de la pared", "Mesillas suspendidas de roble", "Banco a pie de cama tapizado en bouclé", "Armario empotrado de suelo a techo lacado blanco"],
                "decoracion": ["Ropa de cama en lino blanco y manta negra", "Apliques de lectura articulados negro mate", "Cortinas opacas + visillo de lino"],
                "toque": "Retroiluminación LED cálida tras el cabecero, regulable, en lugar de lámpara de techo.",
            },
            "bano": {
                "distribucion": "Ducha de obra a ras de suelo con mampara fija de vidrio y perfil negro; lavabo suspendido.",
                "mobiliario": ["Mueble de lavabo suspendido en roble con encimera de mármol", "Grifería negro mate empotrada", "Espejo retroiluminado sin marco"],
                "decoracion": ["Toallas blancas de rizo grueso", "Una planta de sombra (pothos o sansevieria)"],
                "toque": "Hornacina en la ducha con LED lineal: sustituye estantes y queda de hotel.",
            },
            "exterior": {
                "distribucion": "Terraza como prolongación del salón, con el mismo suelo en versión antideslizante.",
                "mobiliario": ["Sofá exterior de aluminio negro con cojines blancos", "Mesa de comedor de teca para 6"],
                "decoracion": ["Macetas grandes de fibra negra con olivos o gramíneas", "Farolillos LED de latón"],
                "toque": "Bañador de luz rasante en el muro para dar profundidad de noche.",
            },
        },
    },
    "minimalista": {
        "nombre": "Minimalista",
        "lema": "Menos es más: calma, luz y orden",
        "palabras": ["minimalista", "minimal", "simple", "limpia", "sencilla", "pocos muebles"],
        "coste_m2": (700, 1200),
        "concepto": (
            "Espacios silenciosos donde cada objeto tiene un motivo. Paredes blancas, suelos "
            "continuos, almacenaje oculto y una luz indirecta que baña superficies en lugar de "
            "iluminar puntos. El resultado es una casa que respira y descansa la vista."
        ),
        "principios": [
            "Almacenaje oculto en todas las estancias: nada a la vista que no se haya elegido.",
            "Máximo tres colores y dos materiales dominantes por estancia.",
            "Luz indirecta (foseados y rodapiés LED) por encima de las lámparas decorativas.",
            "Muebles bajos y ligeros que despejan el campo visual.",
            "Superficies continuas: microcemento o tarima sin cambios de nivel ni rodapiés marcados.",
        ],
        "paleta": [
            ("Blanco puro", "#FFFFFF", "Paredes, techos y frentes"),
            ("Negro carbón", "#222222", "Perfiles, grifería y una pieza protagonista"),
            ("Gris perla", "#D6D6D3", "Microcemento, textiles"),
            ("Arena", "#E5DCCB", "Textiles y alfombras"),
            ("Fresno claro", "#D2B48C", "Madera única en mesas y estantes"),
        ],
        "materiales": [
            ("Microcemento gris perla", "Suelo continuo y paredes de baño"),
            ("Lacado blanco mate", "Armarios empotrados y cocina"),
            ("Fresno claro", "Mesa de comedor y estante flotante"),
            ("Corian o compacto blanco", "Encimeras y lavabos integrados"),
            ("Lino y algodón natural", "Textiles"),
        ],
        "render": {
            "pared": "#FFFFFF", "suelo": "#D6D6D3", "techo": "#FFFFFF", "viga": "#EDEDEA",
            "sofa": "#E5DCCB", "madera": "#D2B48C", "acento": "#222222", "metal": "#222222",
            "textil": "#C9C2B4", "led": "#FFE4B8",
        },
        "viga": "falsa viga de pladur blanca con foseado LED perimetral, que proyecta la luz hacia el techo sin ver la fuente",
        "estancias": {
            "salon": {
                "distribucion": "Salón despejado con un sofá bajo, una mesa de centro y nada más en el suelo; la TV integrada en un paño de armario con puertas.",
                "mobiliario": ["Sofá bajo de líneas rectas en lino arena", "Mesa de centro baja de fresno", "Un banco-estante suspendido corrido bajo la ventana"],
                "decoracion": ["Alfombra lisa de lana arena", "Un jarrón grande de cerámica negra con una rama", "Cortinas blancas translúcidas"],
                "toque": "Si un objeto no aporta función o belleza, fuera: deja al menos una pared completamente vacía.",
            },
            "cocina": {
                "distribucion": "Cocina lineal en paño completo con isla simple o península; electrodomésticos 100 % integrados.",
                "mobiliario": ["Frentes blancos sin tiradores de suelo a techo", "Isla con encimera compacta blanca", "Taburetes de fresno sin respaldo"],
                "decoracion": ["Encimera vacía salvo una tabla de cortar"],
                "toque": "Enchufes escamoteables en la encimera para no romper el frontal.",
            },
            "dormitorio": {
                "distribucion": "Cama baja tipo tatami o plataforma, armario empotrado en toda una pared y ninguna cómoda.",
                "mobiliario": ["Cama plataforma de fresno", "Mesillas integradas en el propio cabecero", "Armario empotrado blanco con puertas enrasadas"],
                "decoracion": ["Ropa de cama blanca y manta arena", "Una sola lámina enmarcada"],
                "toque": "Línea de luz LED bajo la cama como luz nocturna.",
            },
            "bano": {
                "distribucion": "Baño en microcemento continuo, plato de ducha enrasado y lavabo integrado.",
                "mobiliario": ["Lavabo integrado en encimera blanca", "Espejo-armario enrasado", "Grifería negra empotrada"],
                "decoracion": ["Toallas blancas", "Jabonera de piedra"],
                "toque": "Foseado LED sobre el espejo en lugar de apliques.",
            },
            "exterior": {
                "distribucion": "Terraza despejada con un único conjunto de estar.",
                "mobiliario": ["Tumbonas blancas de líneas rectas", "Mesa baja de hormigón"],
                "decoracion": ["Grava blanca y una sola especie vegetal repetida"],
                "toque": "Balizas empotradas en el suelo, nada colgado.",
            },
        },
    },
    "nordico": {
        "nombre": "Nórdico",
        "lema": "Luz natural, madera clara y hygge",
        "palabras": ["nordico", "nórdico", "escandinavo", "hygge", "acogedor", "acogedora", "calido", "cálido"],
        "coste_m2": (600, 1000),
        "concepto": (
            "Una casa luminosa y amable, pensada para vivirse: maderas claras, blancos cálidos, "
            "lana y lino, y rincones con luz tenue que invitan a quedarse. Funcional sin ser fría."
        ),
        "principios": [
            "Maximizar la luz natural: cortinas ligeras, paredes claras, espejos frente a ventanas.",
            "Madera clara (roble, abedul, pino) en suelos y muebles para aportar calidez.",
            "Textiles en capas: mantas, cojines, alfombras de lana.",
            "Muebles de formas redondeadas y patas finas.",
            "Plantas verdes en todas las estancias.",
        ],
        "paleta": [
            ("Blanco cálido", "#F7F4EF", "Paredes"),
            ("Gris niebla", "#C8C8C4", "Sofá y textiles"),
            ("Roble claro", "#D8B98C", "Suelos y muebles"),
            ("Verde salvia", "#9CAF88", "Acento en textiles y plantas"),
            ("Negro suave", "#2E2E2E", "Lámparas y detalles"),
        ],
        "materiales": [
            ("Tarima de roble claro", "Suelo de toda la vivienda"),
            ("Lana y lino", "Textiles, mantas y alfombras"),
            ("Abedul contrachapado", "Estanterías y frentes"),
            ("Azulejo blanco artesanal", "Frente de cocina y baño"),
            ("Cerámica mate", "Accesorios y vajilla vista"),
        ],
        "render": {
            "pared": "#F7F4EF", "suelo": "#D8B98C", "techo": "#FBFAF7", "viga": "#C9A77A",
            "sofa": "#C8C8C4", "madera": "#D8B98C", "acento": "#9CAF88", "metal": "#2E2E2E",
            "textil": "#9CAF88", "led": "#FFD49A",
        },
        "viga": "viga vista de madera de roble claro con tira LED cálida (2700 K) oculta en un canal en su cara superior, creando luz rebotada en el techo",
        "estancias": {
            "salon": {
                "distribucion": "Zona de estar orientada a la ventana con un rincón de lectura junto a ella.",
                "mobiliario": ["Sofá de tres plazas gris niebla con patas de madera", "Butaca de lectura con otomana", "Mesa de centro redonda de roble", "Estantería abierta de abedul"],
                "decoracion": ["Alfombra de lana tejida", "Mantas de punto grueso", "Plantas: monstera y ficus lyrata", "Velas y láminas botánicas"],
                "toque": "Una lámpara de pie junto a la butaca: el rincón de lectura es el corazón hygge de la casa.",
            },
            "cocina": {
                "distribucion": "Cocina abierta con península y mesa de comedor de madera cerca de la ventana.",
                "mobiliario": ["Frentes blancos con tiradores de cuero", "Encimera de madera maciza", "Mesa de comedor de roble con sillas de varillas"],
                "decoracion": ["Estante abierto con vajilla de cerámica", "Hierbas aromáticas en maceta"],
                "toque": "Colgantes de fibra natural sobre la mesa del comedor.",
            },
            "dormitorio": {
                "distribucion": "Cama con cabecero de madera, textiles en capas y banco a los pies.",
                "mobiliario": ["Cama de roble claro", "Mesillas redondas", "Armario con frentes de abedul"],
                "decoracion": ["Ropa de cama de lino lavado", "Alfombra de piel sintética junto a la cama"],
                "toque": "Lámparas de mesilla de cerámica con pantalla de lino: luz cálida y baja.",
            },
            "bano": {
                "distribucion": "Baño luminoso con azulejo blanco y madera.",
                "mobiliario": ["Mueble de lavabo de roble", "Espejo redondo", "Ducha con mampara"],
                "decoracion": ["Toallas de algodón gris", "Planta de helecho"],
                "toque": "Escalera toallero de madera.",
            },
            "exterior": {
                "distribucion": "Porche o terraza con mobiliario de madera y mantas.",
                "mobiliario": ["Banco de madera con cojines", "Mesa plegable de teca"],
                "decoracion": ["Guirnalda de luces cálidas", "Lavanda y gramíneas"],
                "toque": "Mantas en un cesto para las noches frescas.",
            },
        },
    },
    "japandi": {
        "nombre": "Japandi",
        "lema": "Serenidad japonesa y calidez nórdica",
        "palabras": ["japandi", "japones", "japonés", "zen", "wabi", "sereno", "serena", "relajante"],
        "coste_m2": (800, 1300),
        "concepto": (
            "La fusión de la austeridad japonesa con la calidez escandinava: muebles bajos, "
            "maderas de tonos medios, tonos tierra y artesanía imperfecta. Un hogar sereno, "
            "honesto con los materiales y muy acogedor."
        ),
        "principios": [
            "Muebles bajos y a ras de suelo para crear horizontalidad y calma.",
            "Contraste entre madera clara y detalles en madera oscura o negro.",
            "Artesanía y materiales naturales con imperfecciones (wabi-sabi).",
            "Separaciones con celosías de listones en lugar de tabiques.",
            "Espacios vacíos intencionales (ma).",
        ],
        "paleta": [
            ("Arroz", "#EFE9DF", "Paredes"),
            ("Arcilla", "#C4A484", "Textiles y cerámica"),
            ("Nogal", "#6B4E37", "Muebles y celosías"),
            ("Carbón", "#2B2B2B", "Detalles"),
            ("Musgo", "#7D8465", "Plantas y acentos"),
        ],
        "materiales": [
            ("Roble y nogal", "Muebles y celosías de listones"),
            ("Papel washi", "Lámparas y paneles"),
            ("Enlucido de cal", "Paredes con textura"),
            ("Piedra natural", "Baño y encimeras"),
            ("Ratán y yute", "Alfombras y cestos"),
        ],
        "render": {
            "pared": "#EFE9DF", "suelo": "#C9AE8C", "techo": "#F4EFE7", "viga": "#6B4E37",
            "sofa": "#D8CBB8", "madera": "#6B4E37", "acento": "#2B2B2B", "metal": "#2B2B2B",
            "textil": "#C4A484", "led": "#FFD49A",
        },
        "viga": "viga de nogal con listones y tira LED cálida (2700 K) oculta entre ellos, difundida como a través de papel washi",
        "estancias": {
            "salon": {
                "distribucion": "Salón con sofá bajo y celosía de listones de madera que separa del comedor sin cerrar.",
                "mobiliario": ["Sofá bajo de lino arcilla", "Mesa de centro baja de nogal", "Celosía de listones de roble del suelo al techo"],
                "decoracion": ["Alfombra de yute", "Lámpara de papel washi", "Bonsái o rama de cerezo en jarrón de cerámica artesana"],
                "toque": "Menos objetos, más vacío: un solo objeto protagonista por superficie.",
            },
            "cocina": {
                "distribucion": "Cocina con frentes de madera y encimera de piedra; comedor con mesa baja-media.",
                "mobiliario": ["Frentes de roble con veta vertical", "Encimera de piedra mate", "Mesa de nogal y bancos"],
                "decoracion": ["Vajilla de cerámica gres", "Tetera de hierro"],
                "toque": "Estante abierto único para la cerámica artesana.",
            },
            "dormitorio": {
                "distribucion": "Cama tipo plataforma baja, casi a ras de suelo.",
                "mobiliario": ["Cama plataforma de roble", "Mesillas de nogal", "Armario con puertas de listones"],
                "decoracion": ["Lino arcilla y blanco", "Lámpara de papel en el suelo"],
                "toque": "Tatami o alfombra de fibra natural alrededor de la cama.",
            },
            "bano": {
                "distribucion": "Baño tipo onsen con piedra, madera y ducha abierta.",
                "mobiliario": ["Lavabo de piedra sobre encimera de madera", "Taburete de madera en la ducha"],
                "decoracion": ["Toallas de lino", "Planta de bambú"],
                "toque": "Tarima de iroko en la ducha.",
            },
            "exterior": {
                "distribucion": "Jardín seco o terraza con grava, piedra y un árbol.",
                "mobiliario": ["Banco de madera bajo", "Cojines de suelo"],
                "decoracion": ["Grava rastrillada", "Arce japonés en maceta"],
                "toque": "Farol de piedra con LED.",
            },
        },
    },
    "industrial": {
        "nombre": "Industrial",
        "lema": "Loft urbano: hierro, ladrillo y hormigón",
        "palabras": ["industrial", "loft", "urbano", "ladrillo", "hierro", "hormigon", "hormigón"],
        "coste_m2": (650, 1100),
        "concepto": (
            "Un loft con alma de fábrica rehabilitada: techos altos, estructura vista, ladrillo, "
            "hormigón y hierro, suavizados con cuero envejecido, madera recuperada y luz cálida."
        ),
        "principios": [
            "Dejar a la vista estructura e instalaciones como parte del diseño.",
            "Contrastar materiales duros con textiles cálidos (cuero, lana).",
            "Carpintería metálica negra con vidrio para separar sin cerrar.",
            "Iluminación con carriles, bombillas de filamento y focos orientables.",
            "Espacios amplios y abiertos, pocas puertas.",
        ],
        "paleta": [
            ("Gris hormigón", "#9A9A96", "Suelos y paredes"),
            ("Ladrillo", "#9C4F36", "Pared protagonista"),
            ("Negro hierro", "#232323", "Carpinterías y estructura"),
            ("Cuero coñac", "#8B5A2B", "Sofá y butacas"),
            ("Madera recuperada", "#7A5C3E", "Mesas y estantes"),
        ],
        "materiales": [
            ("Hormigón pulido", "Suelo"),
            ("Ladrillo visto", "Pared principal del salón"),
            ("Acero negro", "Carpinterías, estanterías, escalera"),
            ("Madera recuperada", "Mesa y estantes"),
            ("Cuero envejecido", "Sofá y butacas"),
        ],
        "render": {
            "pared": "#B8B4AE", "suelo": "#9A9A96", "techo": "#8E8C88", "viga": "#232323",
            "sofa": "#8B5A2B", "madera": "#7A5C3E", "acento": "#9C4F36", "metal": "#232323",
            "textil": "#5E5A55", "led": "#FFC477",
        },
        "viga": "viga de acero en I pintada en negro con tira LED cálida (2400–2700 K) dentro del alma de la viga, iluminando hacia abajo y hacia el techo",
        "estancias": {
            "salon": {
                "distribucion": "Loft abierto con pared de ladrillo como fondo del salón.",
                "mobiliario": ["Sofá Chester de cuero coñac", "Mesa de centro de madera recuperada y hierro", "Estantería de acero y madera"],
                "decoracion": ["Alfombra kilim desgastada", "Bombillas de filamento vistas", "Láminas de planos y fotografía urbana"],
                "toque": "Una planta grande (strelitzia) suaviza tanto material duro.",
            },
            "cocina": {
                "distribucion": "Cocina abierta con isla de acero y madera.",
                "mobiliario": ["Isla con encimera de hormigón", "Taburetes metálicos tipo Tolix", "Estantes abiertos de hierro"],
                "decoracion": ["Colgantes metálicos esmaltados", "Pizarra en la pared"],
                "toque": "Campana de acero inoxidable vista como pieza protagonista.",
            },
            "dormitorio": {
                "distribucion": "Dormitorio separado por cerramiento de vidrio con perfil negro.",
                "mobiliario": ["Cama de hierro", "Mesillas de madera recuperada", "Burro de ropa de acero"],
                "decoracion": ["Lino gris carbón", "Manta de lana"],
                "toque": "Apliques de brazo articulado estilo taller.",
            },
            "bano": {
                "distribucion": "Baño con hormigón y azulejo metro.",
                "mobiliario": ["Lavabo sobre encimera de madera y patas de hierro", "Espejo con marco metálico"],
                "decoracion": ["Toallas gris antracita"],
                "toque": "Grifería vista de latón envejecido o negra.",
            },
            "exterior": {
                "distribucion": "Azotea o terraza con suelo de madera y jardineras de acero corten.",
                "mobiliario": ["Mesa de palets tratados", "Sillones de metal"],
                "decoracion": ["Guirnaldas de bombillas", "Jardineras de corten"],
                "toque": "Estufa exterior de acero para alargar las noches.",
            },
        },
    },
    "mediterraneo": {
        "nombre": "Mediterráneo",
        "lema": "Luz, cal, fibras naturales y azul",
        "palabras": ["mediterraneo", "mediterráneo", "playa", "costa", "ibicenco", "rustico", "rústico", "campo"],
        "coste_m2": (650, 1100),
        "concepto": (
            "Una casa fresca y luminosa inspirada en la costa: paredes encaladas, formas curvas, "
            "fibras naturales, terracota y toques de azul. Espacios que se abren al exterior."
        ),
        "principios": [
            "Paredes blancas encaladas y formas curvas (arcos, hornacinas, bancos de obra).",
            "Fibras naturales: ratán, yute, esparto, lino.",
            "Conexión interior–exterior con grandes aberturas.",
            "Terracota y barro en suelos y cerámica.",
            "Acentos en azul añil y verde oliva.",
        ],
        "paleta": [
            ("Cal blanca", "#FAF7F0", "Paredes"),
            ("Terracota", "#C8704B", "Suelos y cerámica"),
            ("Arena", "#E3D3B5", "Textiles"),
            ("Azul añil", "#2F5D8C", "Acentos"),
            ("Verde oliva", "#7C8B4F", "Plantas y textiles"),
        ],
        "materiales": [
            ("Barro cocido o terracota", "Suelos"),
            ("Enlucido de cal", "Paredes y bancos de obra"),
            ("Ratán y esparto", "Lámparas y sillas"),
            ("Madera de pino envejecida", "Vigas y puertas"),
            ("Azulejo artesano", "Cocina y baño"),
        ],
        "render": {
            "pared": "#FAF7F0", "suelo": "#C8704B", "techo": "#FFFFFF", "viga": "#A7825C",
            "sofa": "#E3D3B5", "madera": "#A7825C", "acento": "#2F5D8C", "metal": "#7C8B4F",
            "textil": "#2F5D8C", "led": "#FFD08A",
        },
        "viga": "viga de madera envejecida con tira LED cálida (2700 K) oculta en su parte superior, que baña el techo encalado",
        "estancias": {
            "salon": {
                "distribucion": "Salón con banco de obra curvo con cojines y apertura al exterior.",
                "mobiliario": ["Sofá de lino arena", "Banco de obra con cojines", "Mesa de centro de madera rústica"],
                "decoracion": ["Lámpara de ratán", "Cojines azul añil", "Cerámica y cestos de esparto", "Olivo en maceta"],
                "toque": "Hornacinas en la pared con LED para cerámica.",
            },
            "cocina": {
                "distribucion": "Cocina de obra con encimera de piedra y azulejo artesano.",
                "mobiliario": ["Cocina de obra encalada", "Mesa de comedor de madera maciza", "Sillas de enea"],
                "decoracion": ["Azulejo artesano azul", "Cestos y ristras"],
                "toque": "Cortinas de lino en lugar de puertas bajo encimera.",
            },
            "dormitorio": {
                "distribucion": "Dormitorio fresco con cabecero de obra o de fibras.",
                "mobiliario": ["Cabecero de ratán", "Mesillas de madera", "Baúl a pie de cama"],
                "decoracion": ["Mosquitera de lino", "Ropa de cama blanca"],
                "toque": "Ventilador de techo de madera y ratán.",
            },
            "bano": {
                "distribucion": "Baño con microcemento blanco y formas curvas.",
                "mobiliario": ["Lavabo de piedra", "Espejo de ratán", "Ducha con arco"],
                "decoracion": ["Toallas de rayas", "Jarrones de barro"],
                "toque": "Banco de obra en la ducha.",
            },
            "exterior": {
                "distribucion": "Porche con pérgola de cañizo y comedor exterior.",
                "mobiliario": ["Mesa larga de madera", "Sillas de enea", "Tumbonas de lino"],
                "decoracion": ["Buganvilla", "Farolillos de hierro"],
                "toque": "Pérgola con tiras LED cálidas entre el cañizo.",
            },
        },
    },
    "clasico_lujo": {
        "nombre": "Clásico de lujo",
        "lema": "Molduras, mármol y terciopelo",
        "palabras": ["clasico", "clásico", "señorial", "palacio", "molduras", "barroco", "art deco", "hotel"],
        "coste_m2": (1300, 2500),
        "concepto": (
            "Elegancia atemporal con aire de hotel boutique: molduras, suelos de espiga, mármoles "
            "veteados, terciopelos y latón, reinterpretados con una distribución contemporánea."
        ),
        "principios": [
            "Molduras y boiseries en paredes y techos como base arquitectónica.",
            "Simetría en la distribución del mobiliario.",
            "Materiales nobles: mármol, latón, terciopelo, maderas oscuras.",
            "Iluminación en capas con lámpara de araña o colgante escultórica.",
            "Paleta profunda equilibrada con neutros cálidos.",
        ],
        "paleta": [
            ("Marfil", "#F3EDE2", "Paredes y molduras"),
            ("Verde esmeralda", "#1F4D3F", "Terciopelos y acentos"),
            ("Mármol Calacatta", "#E8E4DC", "Suelos y encimeras"),
            ("Latón", "#C2A15A", "Metales"),
            ("Nogal oscuro", "#4A3222", "Suelos y muebles"),
        ],
        "materiales": [
            ("Parqué de roble en espiga", "Salón y dormitorios"),
            ("Mármol Calacatta", "Baños, encimeras y chimenea"),
            ("Terciopelo", "Sofás y butacas"),
            ("Latón pulido", "Luminarias y grifería"),
            ("Molduras de escayola", "Paredes y techos"),
        ],
        "render": {
            "pared": "#F3EDE2", "suelo": "#8A6446", "techo": "#FAF6EE", "viga": "#E9E1D2",
            "sofa": "#1F4D3F", "madera": "#4A3222", "acento": "#1F4D3F", "metal": "#C2A15A",
            "textil": "#C2A15A", "led": "#FFD9A0",
        },
        "viga": "viga-moldura de escayola con cornisa y foseado LED cálido en su interior, integrada con las molduras del techo",
        "estancias": {
            "salon": {
                "distribucion": "Salón simétrico con dos sofás enfrentados y chimenea de mármol como eje.",
                "mobiliario": ["Dos sofás de terciopelo esmeralda", "Mesa de centro de mármol y latón", "Par de butacas bergère"],
                "decoracion": ["Lámpara de araña contemporánea de latón", "Espejo dorado sobre la chimenea", "Alfombra persa en tonos suaves"],
                "toque": "Pinta las molduras del mismo color que la pared para una elegancia más actual.",
            },
            "cocina": {
                "distribucion": "Cocina con frentes con moldura y gran isla de mármol.",
                "mobiliario": ["Frentes con moldura lacados", "Isla de Calacatta", "Taburetes tapizados"],
                "decoracion": ["Grifería de latón", "Colgantes de vidrio y latón"],
                "toque": "Campana revestida como una chimenea clásica.",
            },
            "dormitorio": {
                "distribucion": "Dormitorio con cabecero capitoné y zona de estar.",
                "mobiliario": ["Cabecero capitoné de terciopelo", "Mesillas de nogal", "Chaise longue"],
                "decoracion": ["Cortinas de terciopelo con visillo", "Apliques de latón"],
                "toque": "Boiserie tras el cabecero con LED oculto en la moldura.",
            },
            "bano": {
                "distribucion": "Baño de mármol con bañera exenta.",
                "mobiliario": ["Bañera exenta", "Doble lavabo sobre mueble de nogal", "Espejos con marco de latón"],
                "decoracion": ["Toallas blancas bordadas", "Flores frescas"],
                "toque": "Suelo de mármol en espiga.",
            },
            "exterior": {
                "distribucion": "Terraza con balaustrada y comedor exterior.",
                "mobiliario": ["Mesa de hierro forjado", "Sillones tapizados"],
                "decoracion": ["Topiarios de boj en maceteros de piedra"],
                "toque": "Farolas clásicas con LED cálido.",
            },
        },
    },
    "boho": {
        "nombre": "Boho chic",
        "lema": "Libre, cálido y lleno de texturas",
        "palabras": ["boho", "bohemio", "bohemia", "hippie", "etnico", "étnico", "colorido", "plantas"],
        "coste_m2": (500, 900),
        "concepto": (
            "Una casa cálida y personal: fibras naturales, tonos tierra, estampados, muchas "
            "plantas y piezas con historia, con un orden relajado que se siente vivido."
        ),
        "principios": [
            "Mezclar texturas: macramé, ratán, lino, lana, cuero.",
            "Paleta tierra (terracota, mostaza, ocre) sobre base blanca.",
            "Muchas plantas a distintas alturas.",
            "Asientos bajos, pufs y cojines de suelo.",
            "Piezas vintage y artesanía.",
        ],
        "paleta": [
            ("Blanco hueso", "#F5EFE6", "Paredes"),
            ("Terracota", "#C06C4B", "Textiles"),
            ("Mostaza", "#D4A24C", "Acentos"),
            ("Ratán", "#C49A6C", "Muebles"),
            ("Verde selva", "#4F6B45", "Plantas"),
        ],
        "materiales": [
            ("Ratán y mimbre", "Sillas, lámparas y cabecero"),
            ("Macramé", "Tapices"),
            ("Barro y cerámica", "Macetas"),
            ("Madera de mango", "Mesas"),
            ("Kilims y alfombras bereberes", "Suelos"),
        ],
        "render": {
            "pared": "#F5EFE6", "suelo": "#B78A5E", "techo": "#FAF6EF", "viga": "#8C6A48",
            "sofa": "#C06C4B", "madera": "#C49A6C", "acento": "#D4A24C", "metal": "#4F6B45",
            "textil": "#D4A24C", "led": "#FFC98A",
        },
        "viga": "viga de madera natural con tira LED cálida y guirnalda de luz entrelazada",
        "estancias": {
            "salon": {
                "distribucion": "Salón informal con sofá bajo, pufs y rincón de plantas.",
                "mobiliario": ["Sofá bajo terracota", "Butaca de ratán tipo pavo real", "Pufs de cuero"],
                "decoracion": ["Alfombra bereber", "Tapiz de macramé", "Plantas colgantes"],
                "toque": "Agrupa plantas en número impar y a distintas alturas.",
            },
            "cocina": {
                "distribucion": "Cocina abierta con estantes a la vista.",
                "mobiliario": ["Mesa de madera de mango", "Sillas desparejadas"],
                "decoracion": ["Cestos colgados", "Cerámica artesanal"],
                "toque": "Azulejo hidráulico en el frente.",
            },
            "dormitorio": {
                "distribucion": "Cama baja con dosel de lino y muchos cojines.",
                "mobiliario": ["Cabecero de ratán", "Mesillas de mimbre"],
                "decoracion": ["Colcha de estampado étnico", "Guirnalda de luz"],
                "toque": "Dosel ligero de lino blanco.",
            },
            "bano": {
                "distribucion": "Baño con plantas y fibras.",
                "mobiliario": ["Mueble de teca", "Espejo de ratán"],
                "decoracion": ["Helechos colgantes", "Toallas de algodón turco"],
                "toque": "Suelo de baldosa hidráulica.",
            },
            "exterior": {
                "distribucion": "Terraza chill-out con cojines y alfombras exteriores.",
                "mobiliario": ["Sofá de palets con colchones", "Hamaca"],
                "decoracion": ["Farolillos marroquíes", "Plantas en barro"],
                "toque": "Guirnaldas de luz cálida en la pérgola.",
            },
        },
    },
}

ESTILO_POR_DEFECTO = "moderno_elegante"


def detectar_estilo(texto):
    """Devuelve la clave del estilo cuyas palabras aparecen más en el texto."""
    t = (texto or "").lower()
    mejor, puntos_max = None, 0
    for clave, e in ESTILOS.items():
        puntos = sum(1 for p in e["palabras"] if p in t)
        if puntos > puntos_max:
            mejor, puntos_max = clave, puntos
    return mejor or ESTILO_POR_DEFECTO
