import win32print

# Récupérer la liste des imprimantes disponibles
printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

# Afficher le nom et le modèle de chaque imprimante
for printer in printers:
    print(f"Nom: {printer[2]}, Modèle: {printer[1]}")
