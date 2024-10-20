import serial
import time

# Fonction pour réinitialiser le port série
def reset_serial(ser):
    ser.close()  # Fermer le port série
    time.sleep(1)  # Attendre 1 seconde
    ser.open()  # Réouvrir le port série
    print("Port série réinitialisé.")

# Initialisation du port série
ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=1200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=1
)

# Fonction pour lire un groupe d'information
def read_group():
    group_data = b''
    
    # Lire jusqu'à trouver le caractère de début (x0A)
    while True:
        byte = ser.read(1)
        if byte == b'\x0A':  # x0A (nouvelle ligne) indique le début d'un groupe
            break

    # Lire jusqu'à trouver le caractère de fin (x0D)
    while True:
        byte = ser.read(1)
        if byte == b'\x0D':  # x0D (retour chariot) indique la fin du groupe
            break
        group_data += byte
    
    return group_data

# Boucle principale pour lire et afficher les groupes d'information
try:
    print("Lecture des groupes d'information à 1200 bauds sur /dev/ttyUSB2...")
    while True:
        try:
            group = read_group()  # Lire un groupe d'information
            if group:  # Si un groupe a été lu
                print(f"Groupe lu : {group.decode('ascii')}")  # Affichage du groupe
        except serial.SerialException as e:
            print(f"Erreur série : {e}")
            reset_serial(ser)  # Réinitialiser le port série en cas d'erreur
except KeyboardInterrupt:
    print("Arrêt de la lecture série.")
finally:
    ser.close()  # Fermer le port série lorsque terminé
