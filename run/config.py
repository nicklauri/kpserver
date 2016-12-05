
import os, sys;
from libs import kout;

###     Load config/mimetypes
if not os.path.isfile('config/mimetypes'):
    kout.error(""); kout.cyan("config"); kout.out(": can't load mimetypes.\n");
try:
    _mimetypes = open("config/mimetypes").readlines();
except IOError, e:
    kout.error(""); kout.cyan("config"); kout.out(": can't load mimetypes.\n");
def mimetype(filename):
    global _mimetypes
    try:
        if filename.startswith('.'):
            ext = filename;
        else:
            ext = os.path.splitext(filename)[1]     # Return tuple ('file_path', '.extension')
    except IndexError:
        return "";
    for line in _mimetypes:
        try:
            if line.split()[0] == ext:  # See usage in config/mimetypes
                return line.split()[1];
        except IndexError:
            pass
    return "";
    # if not os.path.isfile("config/abs_load_data"):
    #     try:
    #         _mimetypes = open("config/mimetypes").readlines();
    #     except IOError, e:
    #         kout.error(""); kout.cyan("config"); kout.out(": can't load mimetypes.\n");
    #         return "";
    #     try:
    #         if filename.startswith('.'):
    #             ext = filename;
    #         else:
    #             ext = os.path.splitext(filename)[1]     # Return tuple ('file_path', '.extension')
    #     except IndexError:
    #         return "";
    #     for line in _mimetypes:
    #         try:
    #             if line.split()[0] == ext:  # See usage in config/mimetypes
    #                 return line.split()[1];
    #         except IndexError:
    #             pass
    #     return "";
    # else:
    #     try:
    #         if filename.startswith('.'):
    #             ext = filename;
    #         else:
    #             ext = os.path.splitext(filename)[1]     # Return tuple ('file_path', '.extension')
    #     except IndexError:
    #         return "";
    #     for line in _mimetypes:
    #         try:
    #             if line.split()[0] == ext:  # See usage in config/mimetypes
    #                 return line.split()[1];
    #         except IndexError:
    #             pass
    #     return "";

###     Load config/http_server
if not os.path.isfile('config/http_server'):
    kout.error(""); kout.cyan("config"); kout.out(": can't load http server configuration.\n");
try:
    _http_server = open("config/http_server").readlines();
except IOError, e:
    pass
def http_server(key):
    global _http_server;
    if not os.path.isfile("config/abs_load_data"):
        try:
            _http_server = open("config/http_server").readlines();
        except IOError, e:
            return "";
        for line in _http_server:
            try:
                if line.split(' ', 1)[0] == key:
                    return line.split(' ', 1)[1].strip();
            except IndexError:
                pass
        return "";
    else:
        for line in _http_server:
            try:
                if line.split(' ', 1)[0] == key:
                    return line.split(' ', 1)[1].strip();
            except IndexError:
                pass
        return "";

###     Load config/alias
if not os.path.isfile('config/alias'):
    kout.error(""); kout.cyan("config"); kout.out(": can't load alias request path.\n");
def alias(request_path=''):
    if http_server("web.alias") == "disable":
        return request_path;
    try:
        _alias = open('config/alias').readlines();
    except IOError:
        return "";
    count_line = 0;
    for line in _alias:
        count_line += 1;
        try:
            if not line.strip().startswith('#') or len(line.strip()):
                # Check if it is a comment, because a comment is not an alias.
                # It makes fatal error.
                try:
                    if line.strip().split(':', 1)[0] == request_path and request_path != '':
                        return line.strip().split(':', 1)[1];
                except IndexError:
                    kout.warn(""); kout.cyan("config"); kout.out(": alias doesn't has data on line %d.\n" %count_line);
        except Exception, e:
            kout.error(e + '\n')
    return request_path;    # Return original path if not alias of it.
