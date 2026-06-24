//  Initialisation des variables
let light_octet_haut = 0
let light_octet_bas = 0
let light_luminosite = 0
let luminosite_strip = 0
let niveau_led = 0
let VAL_MAX = 100
//  Valeur en pleine lumière (à ajuster)
let VAL_MIN = 0
//  Valeur dans le noir (à ajuster)
//  Configuration initiale du capteur de lumière I2C et du ruban LED
pins.i2cWriteNumber(41, 32771, NumberFormat.UInt16BE, false)
let strip = neopixel.create(DigitalPin.P0, 10, NeoPixelMode.RGB)
//  Message d'accueil au démarrage
basic.showString("HR:")
//  Boucle 1 : Gestion de la lecture du capteur et de la luminosité du ruban LED
//  Petite pause pour ne pas surcharger le processeur
//  Lancement de la gestion de la lumière en arrière-plan
control.inBackground(function gestion_lumiere() {
    
    while (true) {
        //  1. Lecture du capteur I2C
        pins.i2cWriteNumber(41, 140, NumberFormat.Int8LE, true)
        light_octet_bas = pins.i2cReadNumber(41, NumberFormat.UInt8LE, false)
        pins.i2cWriteNumber(41, 141, NumberFormat.Int8LE, true)
        light_octet_haut = pins.i2cReadNumber(41, NumberFormat.UInt8LE, false)
        light_luminosite = light_octet_haut * 256 + light_octet_bas
        //  2. Calcul et mise à jour du ruban LED (P0)
        luminosite_strip = Math.max(0, Math.min(255, Math.idiv((VAL_MAX - light_luminosite) * 255, VAL_MAX - VAL_MIN)))
        strip.setBrightness(luminosite_strip)
        strip.showColor(neopixel.colors(NeoPixelColors.White))
        strip.show()
        basic.pause(100)
    }
})
//  Boucle principale (Forever) : Affichage continu de l'heure (P1 / Écran)
basic.forever(function on_forever() {
    //  Note : Remplacer par les blocs de votre extension d'écran P1 si nécessaire
    basic.showString(timeanddate.time(timeanddate.TimeFormat.HMMSSAMPM))
})
