# Initialisation des variables
light_octet_haut = 0
light_octet_bas = 0
light_luminosite = 0
luminosite_strip = 0
niveau_led = 0

VAL_MAX = 100 # Valeur en pleine lumière (à ajuster)
VAL_MIN = 0   # Valeur dans le noir (à ajuster)

# Configuration initiale du capteur de lumière I2C et du ruban LED
pins.i2c_write_number(41, 32771, NumberFormat.UINT16_BE, False)
strip = neopixel.create(DigitalPin.P0, 10, NeoPixelMode.RGB)

# Message d'accueil au démarrage
basic.show_string("HR:")

# Boucle 1 : Gestion de la lecture du capteur et de la luminosité du ruban LED
def gestion_lumiere():
    global light_octet_bas, light_octet_haut, light_luminosite, luminosite_strip
    while True:
        # 1. Lecture du capteur I2C
        pins.i2c_write_number(41, 140, NumberFormat.INT8_LE, True)
        light_octet_bas = pins.i2c_read_number(41, NumberFormat.UINT8_LE, False)
        pins.i2c_write_number(41, 141, NumberFormat.INT8_LE, True)
        light_octet_haut = pins.i2c_read_number(41, NumberFormat.UINT8_LE, False)
        light_luminosite = light_octet_haut * 256 + light_octet_bas
        
        # 2. Calcul et mise à jour du ruban LED (P0)
        luminosite_strip = max(0,
            min(255,
                Math.idiv((VAL_MAX - light_luminosite) * 255, VAL_MAX - VAL_MIN)))
        strip.set_brightness(luminosite_strip)
        strip.show_color(neopixel.colors(NeoPixelColors.WHITE))
        strip.show()
        
        basic.pause(100) # Petite pause pour ne pas surcharger le processeur

# Lancement de la gestion de la lumière en arrière-plan
control.in_background(gestion_lumiere)

# Boucle principale (Forever) : Affichage continu de l'heure (P1 / Écran)
def on_forever():
    # Note : Remplacer par les blocs de votre extension d'écran P1 si nécessaire
    basic.show_string(timeanddate.time(timeanddate.TimeFormat.HMMSSAMPM))
basic.forever(on_forever)