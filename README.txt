KProj Python Server version 1.2 Documentation - written by NickLauri (KhoaNguyen).

STRUCTURE:
	/config		: storage configuration files: for aliasing, controling server, identifying type of file.
	/error		: storage default error files: 403, 404, 500, ...
	/info		: storage current server information (not available in this version).
	/libs		: extra functional library for supporting KPS runtime.
	/run		: of course, core scripts of KPS.1.2 .
	/tmp		: storage tmp file (not avalable in this version).
	/www		: aliased-root directory of site (put your project in here).
	/kpserver.py	: KPS launcher.
	/favicon.ico	: Very simple! It's an icon.
	/README.txt	: Simpler than above! Documentation.

WORKING:
	1. init(); 
	2. load_config(); load_mimetype(); load_alias();
	3. starting server -> running:
		3'    if all of work has error: send code 500 and page 500 - Internal Error.
		3.1   process request.
		3.2   check if request has alias?
		3.3   if YES: unalias and goto 3.5
		3.4   if NO and server.access.force_using_root is enable and web.root is not null:
			  mask by web.root and goto 3.5
		3.5   check if request is exist?
		3.6   if YES: check if request if not forbinden?
		3.6.1        if YES: send code 200 and requested page.
		3.6.2        if NO: send code 403 and requested page.
		3.7   if NO: send code 404 and page 404 - Page Not Found.
		
	4. catch exception and shutdown server.