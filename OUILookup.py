import subprocess
import sys

#######################################################################################################################################

ips = [] #IP 
MACs = [] #Mac 
Vendor = [] #Vendor

#######################################################################################################################################


# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    # Implementa la lógica para obtener los datos por IP aquí
    Existe = False
    mac = ""
    vendor = ""
    for i in range(len(ips)):
        if ip == ips[i]:
            Existe = True
            mac = MACs[i]
            vendor = Vendor[i]
    
    if Existe:
        print("\nMAC address : ",mac, "\nFabricante  : ",vendor,"\n")
    else:
        print("\nError: ip is outside the host network\n")

    pass



# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    # Implementa la lógica para obtener los datos por MAC aquí
    Existe = False
    vendor = ""
    for i in range(len(MACs)):
        if mac == MACs[i]:
            Existe = True
            vendor = Vendor[i]
    
    if Existe:
        print("\nMAC address : ",mac, "\nFabricante  : ",vendor,"\n")
    else:
        print("\nError: Mac is outside the host network\n")
    pass




# Función para obtener la tabla ARP
def obtener_tabla_arp():

    # Imprime la tabla ARP
    print("\n","{:20}".format("IP"),"{:20}".format("Mac"),"{:20}".format("Vendor") )
    for i in range(len(ips)):
        print("{:20}".format(ips[i]),"{:20}".format(MACs[i]),"{:20}".format(Vendor[i]) )

    print("\n")
    pass

####################################################################################################################

#Funcion para recopilar los datos Iniciales
def Obtener_datos_iniciales():
    result = subprocess.run(["arp","-a"],stdout = subprocess.PIPE)
    salida = str(result.stdout) # obteniendo tabla arp de la salida
    #Filtarndo tabla:

    salida2 = salida.split("    ") 

    #Datos no finalizados
    ip_no_libre = []
    mac_no_libre = []

    for sal in  salida2:
        if (".") in sal: #Filtro IP
            ip_no_libre.append(sal) 
        if ("-") in sal: #Filtro MAC
            mac_no_libre.append(sal)

    if ip_no_libre[0] == mac_no_libre[0]: #limpiando la primera linea obsoleta
        ip_no_libre.remove(ip_no_libre[0])
        mac_no_libre.remove(mac_no_libre[0])

    for ip in ip_no_libre: #Obteniendo IP final
        linea = ip.split(" ")
        ips.append(linea[len(linea)-1])

    for mac in mac_no_libre: #Obteniendo Mac final
        linea = mac.split(" ")
        MACs.append(linea[len(linea)-1])

    for i in range(len(MACs)): #Creando nuevo formato para las Direcciones Fisicas
        mac = MACs[i].replace("-",":")
        MACs[i] = mac
    pass



#funcion para obtener el vendor
def obtener_vendor():
    with open("manuf.txt", "r" , encoding="utf-8") as war:

        for i in range(len(MACs)):
            mac = MACs[i]
            datos = []
            verdad = False
            for linea in war:
                datos = linea.split("\t")
                if datos[0].lower() in mac:
                    verdad = True
                    Vendor.append(datos[1])
            if verdad == False:
                Vendor.append("None")

        war.close()
    pass

###############################################################################################################

def main(argv):
    ip = None
    mac = None
    arp = False
    help = False
    opts = []

    if len(argv) == 0:
         print("Usar: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | [--help] \n --ip : IP del host a consultar. \n --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.  \n --arp:muestra los fabricantes de los host disponibles en la tabla arp. \n --help: muestra este mensaje y termina.")
    else:

        Obtener_datos_iniciales()
        obtener_vendor()

        for i in range(len(argv)):
            m = argv[i] 
            if m[0] == "-" :
                if (i+1 != len(argv)):
                    m2 = argv[i+1]
                    if m2[0] != "-":
                        opts.append([m,m2])
                    else:
                        opts.append([m," "])
                else:
                    opts.append([m," "])
            

    for opt in opts:
        if opt[0] in ("-i", "--ip","-ip","--i"):
            ip = opt[1]
        
        elif opt[0] in ("-m", "--mac","-mac","--m"):
            mac = opt[1]

        elif opt[0] in("-a","--arp","--a","-arp"):
            arp = True 
        
        else:
            help = True


    if ip:
        obtener_datos_por_ip(ip)

    if mac:
        obtener_datos_por_mac(mac)

    if arp:
        obtener_tabla_arp()
    
    if help:
        print("Usar: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | [--help] \n --ip : IP del host a consultar. \n --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.  \n --arp:muestra los fabricantes de los host disponibles en la tabla arp. \n --help: muestra este mensaje y termina.")


##################################################################################################################################################################################################################################################################################################

if __name__ == "__main__":
    main(sys.argv[1:])