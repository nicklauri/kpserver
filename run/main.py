"""
    KPServer:main - Main executed file.
"""

import os, sys, time, socket, threading, urllib;
from run import config, request, jobs;
from libs import kout, version;
from imp import reload;

current_dir = ""

def get_wanip():
    global kps_wanip;
    try:
        kps_wanip =  urllib.urlopen('http://icanhazip.com/').read().strip('\n');
    except Exception:
        return False;
    return True;


def init():
    global kps_port, kps_ip;
    global kps_server;
    os.chdir(current_dir)
    kps_ip = config.http_server("server.init.ip");
    if not kps_ip:
        kout.warn(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": can't get ip from config/http_server.\n");
        kps_ip = socket.gethostbyname(socket.gethostname());
    try:
        kps_port = int(config.http_server("server.init.port"));
    except ValueError:
        kps_port = 0;
        if not kps_port:
            kout.warn(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": can't get port from config/http_server.\n");
            kps_port = 8080;
        elif kps_port < 0 or kps_port > 65535:
            kout.error(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": port value(%d) must be between 0 and 6555.\n" %kps_port);
            kps_port = 8080;
    ###     Create new server socket.
    kps_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP);
    try:
        kps_server.bind((kps_ip, kps_port));
    except Exception, e:
        kout.error(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": bind error with IP: %s - port: %d.\n" %(kps_ip, kps_port));
        kout.normal(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": using default information.\n");
        try:
            kps_ip = socket.gethostbyname(socket.gethostname());
            if not kps_port:
                kps_port = 8080;
            kps_server.bind((kps_ip, kps_port));
        except Exception, e:
            kout.error(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": fatal: can't init server.\n");
            kout.normal("exit now.\n");
            sys.exit(1);

    try:
        listen = int(config.http_server("server.init.listen"));
    except ValueError:
        listen = 10;
    if not listen:
        listen = 10;
    kps_server.listen(listen);
    del listen;
    ###     Verbose information:
    kout.normal(""); kout.cyan("kps"); kout.out(": "); kout.yellow("init"); kout.out(": init done.\n");
    kout.info(""); kout.cyan("kps"); kout.out(": server information: \n");
    if get_wanip():
        kout.out("\tWAN IP:"); kout.yellow(" %s\n" %kps_wanip);
    kout.out("\tLAN IP:"); kout.yellow(" %s\n" %kps_ip);
    kout.out("\tPort  :"); kout.yellow(" %d\n" %kps_port);

    #### Start server:
    start();
    return None;

# Define chedule jobs:
def chedule_jobs():
    jobs.run(warm_up=True);
    try:
        while 1:
            time.sleep(1);
            reload(jobs);
            jobs.run(warm_up=False);
    except Exception:
        jobs.stop = True;
        jobs.run();

# Handle request:
def handle_request(client, address, id):
    if config.http_server('server.socket_timeout') not in ("", "disable"):
        try:
            client.settimeout(int(config.http_server("server.socket_timeout.value")));
        except ValueError, e:
            client.settimeout(10);
    client_request = request.HTTPRequest(client.recv(1000));
    # if client_request.method() not in ("GET", "POST"):
    #     client.close();
    kout.out(" " * 119 + "\r");
    try:
        if len(client_request.header()) > 0:
            request_path = client_request.request_path();
            if request_path != config.alias(request_path):
                request_path = config.alias(request_path);
            elif config.http_server("server.access.force_using_root") == "enable" and config.http_server("web.root") != "" :
                request_path = request_path.replace("/", config.http_server("web.root") + '/', 1);
            forbinden = False;
            for item in config.http_server("server.access.deny").strip(';').split(';'):
                if request_path.startswith(item) and config.http_server("server.access.deny_status") == "enable":
                    forbinden = True;
            if not request_path:
                request_path = config.http_server("web.error.404");
                status_code = 404;
                status_phrase = "not found";
            elif forbinden:
                request_path = config.http_server("web.error.403");
                status_code = 403;
                status_phrase = "forbinden";
            elif not os.path.isfile('.' + str(request_path)):
                if os.path.isdir('.' + str(request_path)):
                    if not request_path.endswith('/'):
                        request_path = ''.join([request_path, '/']);
                    for item_list in config.http_server("jobs.show_site.file_name").strip(';').split(';'):
                        if os.path.isfile(''.join(['.' + str(request_path), item_list ])):
                            request_path = ''.join([str(request_path), item_list ]) ;
                            status_code = 200;
                            status_phrase = "OK";
                            break;
                    else:
                        request_path = config.http_server("web.error.404");
                        status_code = 404;
                        status_phrase = "not found";
                else:
                    request_path = config.http_server("web.error.404");
                    status_code = 404;
                    status_phrase = "not found";
            else:
                status_code = 200;
                status_phrase = "OK";
            # Real path process:
            real_path = ''.join(['.', request_path]);
            client.send(request.HTTPResponse(real_path, status_code, status_phrase).response());
            blank_content = False;
        else:
            client.send(request.HTTPResponse().response(blank_content=True));
            blank_content = True;
    except IndexError, e:
        if config.http_server("server.error.beep") == "enable":
            kout.error("\a");
        else:
            kout.error("");
        kout.cyan("kps"); kout.out(": runtime error: %s" %str(e));
        request_path = config.http_server("web.error.500");
        status_code = 500;
        real_path = '.' + request_path;
        client.send(request.HTTPResponse('.' + request_path, 500, "intenal error").response());
    except socket.error, e:
        if config.http_server("server.error.beep") == "enable":
            kout.error("\a");
        else:
            kout.error("");
        kout.cyan("kps"); kout.out(": runtime error: %s\n" %str(e));
        kout.info(""); kout.cyan("kps"); kout.out(": restarting server.\n");
        threading.Thread(target=init).run()
    except TypeError, e:
        if config.http_server("server.error.beep") == "enable":
            kout.error("\a");
        else:
            kout.error("");
        kout.cyan("kps"); kout.out(": runtime warning: %s.\n" %str(e));
        request_path = config.http_server("web.error.404");
        status_code = 404;
        real_path = '.' + request_path;
        client.send(request.HTTPResponse('.' + request_path, 404, "invalid request").response());
    except socket.timeout, e:
        if config.http_server("server.error.beep") == "enable":
            kout.error("\a");
        else:
            kout.error("");
        kout.cyan("kps"); kout.out(": request timeout: `%s`.\n" %str(client_request.request_path()));
        print "           --- Header:\n", client_request.header();
        kout.info(""); kout.cyan("kps"); kout.out(": restarting server.\n");
        kps_server.shutdown(socket.SHUT_RDWR);
        threading.Thread(target=init).run()
        # request_path = config.http_server("web.error.408");
        # status_code = 408;
        # real_path = '.' + request_path;
        # client.send(request.HTTPResponse('.' + request_path, 408, "request timeout").response());
    if client:
        if not blank_content:
            if not config.http_server("server.show.verbose") == "disable":
                kout.out('-'); kout.red("%3d" %id); kout.out(" - ")
                kout.cyan("from"); kout.out(": "); kout.white("%15s" %address[0]); kout.out(" - ");
                kout.cyan("req"); kout.out(": "); kout.yellow("%-32s" %client_request.request_path()); kout.out(" - ");
                kout.cyan("res"); kout.out(": "); kout.yellow("%-38s" %real_path); kout.out("\n")
                if config.http_server("server.show.request_info") == "enable":
                    if len(str(client_request.header())) != 0:
                        kout.out("\t| req-content: "); kout.cyan('\"%s\"\n' %(str(client_request.request_path())));
                    kout.out("\t| req-len: "); kout.cyan('%4d' %len(str(client_request.header()))); kout.out(" - ")
                    kout.out("req-path-len: "); kout.blue('%3d\n\n' %len(str(client_request.request_path())));
                if config.http_server("server.show.http_header") == "enable":
                    print client_request.header().strip("\r").strip("\n\n");
            client.close();
        else:
            if not config.http_server("server.show.verbose") == "disable":
                kout.out('-'); kout.red("%3d" %id); kout.out(" - ")
                kout.cyan("from"); kout.out(": "); kout.white("%15s" %address[0]); kout.out(" - ");
                kout.cyan("req"); kout.out(": "); kout.out("%-32s" %("NULL")); kout.out(" - ");
                kout.cyan("res"); kout.out(": "); kout.out("%-38s" %("200 OK")); kout.out("\n")
                if config.http_server("server.show.request_info") == "enable":
                    if len(str(client_request.header())) != 0:
                        kout.out("\t| req-content: "); kout.cyan('\"\"\n' );
                    kout.out("\t| req-len: "); kout.cyan('   0'); kout.out(" - ")
                    kout.out("req-path-len: "); kout.blue('  0\n\n');
            # client.close();


# Start server:
def start(arg=""):
    kout.info(""); kout.cyan("kps"); kout.out(": server is running.\n");
    # Starting chedule jobs:
    time.sleep(0.05);
    threading.Thread(target=chedule_jobs).start();
    time.sleep(0.05);

    # Start server:
    request_id = 0;
    while 1:
        kout.info(""); kout.cyan("kps"); kout.out(": server is waiting for client:\t");
        client, address = kps_server.accept();
        kout.cyan("OK\r");
        request_id += 1;
        # handle_request(client, address, request_id);
        threading.Thread(target=handle_request, args=(client, address, request_id)).run();
