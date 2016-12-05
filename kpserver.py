"""
    Main KPServer Launcher.
"""
import os, sys, threading;
from libs import kout, version;


welcome = "KProj Python Server version %s - written by NickLauri." %(version.KPS.version)
kout.white(welcome.center(119) + "\n");
kout.info(""); kout.cyan("kps"); kout.out(":");
kout.out(" KPS running on: "); kout.green("Python %s" %version.KPS.python.version)
kout.out(" - OS: "); kout.green("%s %s" %(version.KPS.system.name, version.KPS.system.win_version))
kout.out(" - commandline: "); kout.green("cmd.%s\n" %version.KPS.system.cmd_version);
os.chdir(os.path.split(os.path.abspath(sys.argv[0]))[0]);
kout.info(""); kout.cyan("kps"); kout.out(": current dir:"); kout.green(" %s\n" %os.getcwd());

os.system("title KProj Python Server %s" %version.KPS.version);

try:
    from run import main
    main.current_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    main.init();
    main.start();
except KeyboardInterrupt, e:
    main_thread = threading.current_thread();
    if config.http_server("server.error.beep") == "enable":
        kout.error("\a");
    else:
        kout.error("");
    kout.cyan("kps"); kout.out(": shutting down server: ");
    try:
        for t in threading.enumerate():
            if t != main_thread:
                t.join();
                threading.join(timeout=5);
        kps_server.shutdown(socket.SHUT_WR)
    except RuntimeError:
        kout.red("\tFAILED\n");
        if config.http_server("server.error.beep") == "enable":
            kout.error("\a");
        else:
            kout.error("");
        kout.cyan("kps"); kout.out(": force shutting down server.\n");
        sys.exit(1);
    else:
        kout.cyan("\tOK\n");
        kout.info(""); kout.cyan("kps"); kout.out(": exiting.\n");
        sys.exit(0);
