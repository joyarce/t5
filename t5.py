import imaplib,configparser,re,datetime

cuenta = "xxxxxxxxxx@gmail.com"
contrasena = "xxxxxxxxxxxxxxxxxxx"
imap_h = "imap.gmail.com"

datos = []
with open("input.txt") as fname:
    lineas = fname.readlines()
    for linea in lineas:
        datos.append(linea.strip('\n'))

print("Correo Objetivo:",datos[0])
print("Fecha último correo patrón:",datos[1])
print("Regex:",datos[2])


#### Parametros ####
objetivo = datos[0]
ddmmyyyy = datos[1]
fecha = datetime.datetime.strptime(ddmmyyyy, "%d/%m/%Y").strftime("%d-%b-%Y") 
pattern = re.compile(datos[2])
####################

imap = imaplib.IMAP4_SSL(imap_h)
imap.login(cuenta,contrasena)
imap.select('INBOX')
typ,data = imap.search(None,'(FROM "%s" SINCE "%s")'% (objetivo,fecha),)

for num in data[0].split():
    typ, data1 = imap.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    for response_part in data1:
        if isinstance(response_part, tuple):
            aux = (response_part[1].decode("utf-8").split())[1]
            aux1 = aux[1:(len(aux)-1)]
            result = bool(re.match(pattern, aux1))
            if result == False:
                print('Correo falso tiene MESSAGE-ID:',aux1)
            else: 
                print("MESSAGE-ID: %s = %s"%(aux1,result))