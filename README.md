# Network-Services-Administration
Example of detection:

# Administración de Servicios en Red - ASR
Este repositorio contiene prácticas, ejercicios y proyecto final de la materia de ***Administración de Servicios en Red*** dada en la ***Escuela Superior de Cómputo*** del ***Instituto Politécnico Nacional.***

Hasta el momento, este repositorio contiene 1 práctica.
## PRÁCTICA 01: Implementación de un Sistema de Administración de Red usando *SNMP*.
### Objetivo: Implementar la arquitectura básica del protocolo SNMP
- Implementar la comunicación (intercambio de mensajes) entre el agente y el gestor usando
SNMP.
- Implementar la persistencia de información de una manera eficiente.
- Generar reportes para controlar y vigilar los agentes.
- Implementar un modelo de administración de red.

#### Arquitectura SNMP
![snmp](https://user-images.githubusercontent.com/22998708/53384543-e0940d00-3940-11e9-832a-7fc16d052b61.PNG)

### Configuración de la Arquitectura SNMP en la práctica 01.
- **Manager = Observium (using virual machine)**

- **Manager instructions:**
    - Install Observium in a virtual manager
    - Configure /etc/hosts (This file is only to add agents)
	
- **Windows Agent:**
  - Install SNMP service
  - Configure SNMP service, using a community 

- **Linux Agent:**
  - Install package: snmp, snmpd
  - Configure snmpd.conf using snmpconfig

- **Instalation of Obervium stepts:**
  - In VB you have to choose Linux and Debian64 bits
	- Create a virtual disk 
	- Use VDI
	- Dimanic allocated 
	- Choose 4 gb
	- In storage put IDE Primary master
	- In network you have to change NAT to Bridged adapter (Wi-fi) but if you wanna use eth cable select eth0 and you have to enable in advanced mode the Promiscous mode (Allow all).
  - Install hd 
  - Select Second option in partition (use entire disk)
	- And you have to put yes (GRUB)
	- After the instalation you have to put your credentials:
  - LaQueQuieres (password for all the users)

	- Were not using API so click skip
  - After that login into the url direction and the user is admin and Pepechido2 (http://10.100.64.162/)
  - And quit the console
  - When youre only in terminal mode put: root and enter key

- **Windows Agent:**
  - In vb you have to put the same as Observium in Network mode (check Linux network configuration)
	- Go to panelcontrol/Programs/Turn on off features/ and turn on SNMP and second option 
	- After that you have to search "local services" 
	- You have to start SNMP trap manually always 
	- You have to edit SNMP Service, (right clic and properties) 
     - Clic on traps, put a community name (its like an authentication level) (grupo4cm3)
	- In security option clic add, READ/WRITE and in a community name put grupo4cm2
	- And put SNMP packet from any hosts 
	- And after that, you have yo restart the service
	- Disable the firewall (both options)
	- Check your ip with ipconfig (ipconfig) Remember you have to always be in the same network 
	- If you wanna retrieve information you have to install NET-SNMP:
      - snmpget -v2c -c grupo4cm3 10.100... 1.3.6.1.2.1.1.1.0
      - snmpset -v2c -c grupo4cm3 10.100... 1.3.6.1.2.1.1.6.0 s "Merica"

- **Observium**
  - In nano /etc/hosts/ put the ip of windows and the name you wanna use ping nameofthe device
  - Now in the panel put skip ICMP, v2c, UDP, and community you have to put the same name in windows grupo4cm3 and remember the hostname is the name that is on the nano file

- **Linux**
  - sudo apt update
  - sudo apt-get install snmp snmpd(listen the port with a demon) 
  - sudo gedit /etc/snmp/snmpd.conf
  - snmpconf -r none -g basic_setup
  - y
  - location of the system: "lab. escom. ipn. "
  - sys contact: buscadordebugs
  - n
  - Dou you want to configure the agents acces control: y
  - Dou you want to allow SNMPv3: n
  - Dou you ...: n
  - Dou you want to allow SNMPv1 ... read-write: y
  - Comunity_name: gr_4cm3
  - Put RETURN for all (Enter)
  - OID: RETURN for all (Enter)
  - And finally write no (and so on ...) 
  - move the /usr/share/snmp 
  - sudo mv snmpd.conf /etc/snmp/snmpd.conf
  - sudo service snmpd restart
	_Remember to add the new machine on observium (to see the ip on linux is "ip addr show")
	_If youre on linux you could use "sudo tcpdump -i any -nn port snmp"

### Interfaz principal - Práctica 01
![interfaz principal](https://user-images.githubusercontent.com/22998708/53431587-198bba80-39f1-11e9-99b6-d3f4fe84d366.png)

### Interfaz principal - Práctica 02
Inline-style: 
![alt text](https://github.com/JesusDiaz08/Network-Services-Administration/blob/master/02_Practice_matplot/equipo_06.PNG "Threshold at 90% of CPU Load")


## Implementación de una DNS en *Ubuntu 18.04.1*
- **Domain**: asrDNS.local
- **Primary Name Server**: (It is the master server, and all DNS records are created here.)
- **Server Name**: ns1.asrDNS.local
- **IP Address**: User's IP. example: 192.168.1.10
- **Secondary Name Server**:  (It is a slave server, gets DNS records from the Master server. You can have multiple slave DNS server in your environment. Slave server acts as a backup DNS server and serves clients DNS requests if the primary server goes down.)
- **Server Name**: ns2.asrDNS.local
- **IP Address**: 192.168.1.20

### Pre-requisitos.
- Nos cambiamos a super administrador (**root user**):
  ```bash
    > sudo su -
  ```
- Actualizamos los repositorios.
  ```bash
    > apt update
  ```
- Nos aseguramos que **primary and secondary DNS servers** tienen una IP estática.

### Instalación servidor DNS sobre Ubuntu 18.04
- **Instalamos bind9**: Este paquete nos permite configurar una DNS en Ubuntu.
  ```bash
    > apt install -y bind9 bind9utils bind9-doc dnsutils
  ```
- **Configuramos el servidor DNS**
  - El directorio de configuración principal de bind9 es **/etc/bind/**. Éste contiene **los archivos de configuración** y **archivos de búsqueda de zona**(zone lookup files).

- **Creamos la 'Zona'**: Se hará la creación de la zona de avance para nuestro dominio.
  ```bash
    > nano /etc/bind/named.conf.local
  ```
- **Forward Zone**: La siguiente es la **entrada de la zona de reenvío** para el dominio **asrDNS.local** en el archivo **named.conf.local.**
  ```bash
    > zone "asrDNS.local" IN { // Nombre del dominio
           type master; //Primary DNS
           file "/etc/bind/fwd.asrDNS.local.db"; //Forward lookup file
           allow-update { none; }; // Since this is the primary DNS, it should be none.
      };
  ```
- **Reverse Zone**: Las siguientes entradas son para la **zona inversa/zona de retroceso** en el **archivo named.conf.local**.
  ```bash
    > zone "1.168.192.in-addr.arpa" IN { //Reverse lookup name, should match your network in reverse order
           type master; // Primary DNS
           file "/etc/bind/rev.asrDNS.local.db"; //Reverse lookup file
           allow-update { none; }; //Since this is the primary DNS, it should be none.
      };
  ```
  Una vez creadas las zonas, se puede empezar a **crear los archivos de datos de zona** los cuales **contienen registros DNS** para *la zona de avance* y la *zona de retroceso*.
 - **Forward Zone lookup file:** Es el archivo de búsqueda de **zona de entrada/zona de reenvío**. **Copie las entradas** de muestra al archivo de zona denominado **fwd.asrDNS.local.db** para la zona de reenvío en el directorio **/etc/bind**.
   - Tipos de registro en el archivo de zona:
      - SOA - Inicio de la Autoridad
      - NS - Servidor de nombres
      - A - Un disco
      - MX - Mail for Exchange
      - CN - Nombre canónico
     
   - **Los nombres de dominio deben terminar con un punto (.)**.
  ```bash
     > cp /etc/bind/db.local /etc/bind/fwd.asrDNS.local.db
   ```
   - **Editamos la zona**:
   ```bash
     > nano /etc/bind/fwd.asrDNS.local.db
   ```
   - **Actualiza el contenido**: Cuando cambie cualquier registro en el archivo de búsqueda(**lookup file**), **asegúrese de actualizar el número de serie a un número aleatorio**, más alto que el actual.
   ```assembly
      ;
      ; BIND data file for local loopback interface
      ;
      $TTL    604800
      @       IN      SOA     ns1.asrDNS.local. root.asrDNS.local. (
                                   20         ; Serial
                               604800         ; Refresh
                                86400         ; Retry
                              2419200         ; Expire
                               604800 )       ; Negative Cache TTL
      ;
      ;@      IN      NS      localhost.
      ;@      IN      A       127.0.0.1
      ;@      IN      AAAA    ::1

      ;Name Server Information
             IN      NS      ns1.asrDNS.local.
             IN      NS      ns2.asrDNS.local.
      ;IP address of Name Server
      ns1     IN      A       192.168.1.10
      ns2     IN      A       192.168.1.20

      ;Mail Exchanger
      asrDNS.local.   IN     MX   10   mail.asrDNS.local.

      ;A - Record HostName To Ip Address
      www     IN       A      192.168.1.100
      mail    IN       A      192.168.1.150
      @       IN       A      192.168.1.200
      ;CNAME record
      ftp     IN      CNAME   www.asrDNS.local.
   ```
 - **Reverse Zone lookup file**: Copie las entradas de muestra en el **archivo de zona** llamado **rev.asrDNS.local.db** para **la zona inversa** en el directorio **/etc/bind** y **cree punteros inversos para los registros de la zona anterior**.
    - PTR – Pointer
    - SOA – Start of Authority 
 
    ```bash
       > cp /etc/bind/db.127 /etc/bind/rev.asrDNS.local.db
    ```
    
    - Editamos el **archivo de zona inversa**.
    ```bash
       > nano /etc/bind/rev.asrDNS.local.db
    ```
    - **Actualizar contenido**: Siempre que cambie cualquier registro DNS en el archivo de búsqueda(**lookup file**), **asegúrese de actualizar el número de serie a un número aleatorio**, más alto que el actual.
    ```assembly
       ;
       ; BIND reverse data file for local loopback interface
       ;
       $TTL    604800
       @       IN      SOA     asrDNS.local. root.asrDNS.local. (
                                    20         ; Serial
                                604800         ; Refresh
                                 86400         ; Retry
                               2419200         ; Expire
                                604800 )       ; Negative Cache TTL
       ;
       ;@      IN      NS      localhost.
       ;1.0.0  IN      PTR     localhost.

       ;Name Server Information
              IN      NS     ns1.asrDNS.local.
              IN      NS     ns2.asrDNS.local.
       ;Reverse lookup for Name Server
       10      IN      PTR    ns1.asrDNS.local.
       20      IN      PTR    ns2.asrDNS.local.
       ;PTR Record IP address to HostName
       100     IN      PTR    www.asrDNS.local.
       150     IN      PTR    mail.asrDNS.local.
       200     IN      PTR    asrDNS.local.
    ```
- Checar **sintaxis de configuración de BIND**: Utilizando el comando **named-checkconf** para verificar la sintaxis y los archivos named.conf * en busca de errores.
  ```bash
       > named-checkconf
  ```
  El comando volverá al shell **si no hay errores**. Además, puede usar la zona de comprobación con nombre (**named-checkzone**) para verificar los errores de sintaxis en los archivos de zona.
- **Para la 'Forward Zone'**:
  ```bash
       > named-checkzone itzgeek.local /etc/bind/fwd.itzgeek.local.db
       output:
              zone asrDNS.local/IN: loaded serial 20
              OK
  ```
- **Para la 'Reverse Zone'**:
  ```bash
       > named-checkzone 1.168.192.in-addr.arpa /etc/bind/rev.asrDNS.local.db
       output:
              zone 1.168.192.in-addr.arpa/IN: loaded serial 20
              OK
  ```
- **Restarurar el servicio bind**:
  ```bash
       >  systemctl restart bind9
  ```
- **Habilitamos el servicio bind en el inicio del sistema**:
  ```bash
       >  systemctl enable bind9
  ```
- **Verificamos el estado del servicio bind9**:
  ```bash
       >  systemctl status bind9
  ```
  output:
  ```assembly
    bind9.service - BIND Domain Name Server
    Loaded: loaded (/lib/systemd/system/bind9.service; enabled; vendor preset: enabled)
    Active: active (running) since Sun 2018-06-17 13:33:05 UTC; 21s ago
     Docs: man:named(8)
    Main PID: 2683 (named)
    Tasks: 4 (limit: 2323)
    CGroup: /system.slice/bind9.service
           └─2683 /usr/sbin/named -f -u bind

    Jun 17 13:33:05 server named[2683]: network unreachable resolving './NS/IN': 2001:500:3::42#53
    Jun 17 13:33:05 server named[2683]: managed-keys-zone: Key 19036 for zone . acceptance timer complete: key now tr
    Jun 17 13:33:05 server named[2683]: managed-keys-zone: Key 20326 for zone . acceptance timer complete: key now tr
    Jun 17 13:33:05 server named[2683]: resolver priming query complete
    Jun 17 13:33:06 server named[2683]: checkhints: b.root-servers.net/A (199.9.14.201) missing from hints
    Jun 17 13:33:06 server named[2683]: checkhints: b.root-servers.net/A (192.228.79.201) extra record in hints
    Jun 17 13:33:06 server named[2683]: checkhints: b.root-servers.net/AAAA (2001:500:200::b) missing from hints
    Jun 17 13:33:06 server named[2683]: checkhints: b.root-servers.net/AAAA (2001:500:84::b) extra record in hints
    Jun 17 13:33:06 server named[2683]: checkhints: l.root-servers.net/AAAA (2001:500:9f::42) missing from hints
    Jun 17 13:33:06 server named[2683]: checkhints: l.root-servers.net/AAAA (2001:500:3::42) extra record in hints
  ```
- **Verificamos la DNS**: Vaya a **cualquier máquina cliente** y **agregamos nuestra nueva dirección IP del servidor DNS** en el archivo **/etc/resolv.conf**.
  ```bash
       >  nano /etc/resolv.conf
  ```
- **Realizando una entrada**:
  ```bash
       >  nameserver 192.168.1.10
  ```
- **Checamos la 'Forward Zone'**: Utilice el comando **dig** para comprobar la zona de avance.
  ```bash
       >  dig www.asrDNS.local
  ```
  Si el comando no es encontrado, instale el paquete **bind-utils**.
  ```assembly
      ; <<>> DiG 9.11.3-1ubuntu1.1-Ubuntu <<>> www.asrDNS.local
      ;; global options: +cmd
      ;; Got answer:
      ;; WARNING: .local is reserved for Multicast DNS
      ;; You are currently testing what happens when an mDNS query is leaked to DNS
      ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60898
      ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

      ;; OPT PSEUDOSECTION:
      ; EDNS: version: 0, flags:; udp: 65494
      ;; QUESTION SECTION:
      ;www.asrDNS.local.             IN      A

      ;; ANSWER SECTION:
      www.asrDNS.local.      604800  IN      A       192.168.1.100

      ;; Query time: 0 msec
      ;; SERVER: 127.0.0.53#53(127.0.0.53)
      ;; WHEN: Sun Jun 17 13:44:57 UTC 2018
      ;; MSG SIZE  rcvd: 62
  ```
**La respuesta del servidor DNS para la búsqueda directa: 192.168.1.100 como dirección IP para www.asrDNS.local**
- **Confirmar** la búsqueda inversa(Reverse lookup) con el **comando dig**.
  ```bash
       >  dig -x 192.168.1.100
  ```
  output:
  ```assembly
    ; <<>> DiG 9.11.3-1ubuntu1.1-Ubuntu <<>> -x 192.168.1.100
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25695
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 65494
    ;; QUESTION SECTION:
    ;100.1.168.192.in-addr.arpa.    IN      PTR

    ;; ANSWER SECTION:
    100.1.168.192.in-addr.arpa. 604800 IN   PTR     www.asrDNS.local.

    ;; Query time: 0 msec
    ;; SERVER: 127.0.0.53#53(127.0.0.53)
    ;; WHEN: Sun Jun 17 13:45:50 UTC 2018
    ;; MSG SIZE  rcvd: 86
  ```
**La respuesta del servidor DNS para la búsqueda inversa: www.asrDNS.local como nombre para 192.168.1.100.**
Este resultado **confirma que ambas búsquedas de zona funcionan bien.** 

Ahora ha configurado correctamente el servidor DNS en Ubuntu 18.04 como el servidor maestro.
