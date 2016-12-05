"""
    KPServer::jobs: schedule jobs.
"""

import os, sys, time, threading;
from libs import kout, version;
from run import config;

stop = False;
def run(warm_up=True):
    if warm_up:
        kout.info(""); kout.cyan("jobs"); kout.out(": jobs is running.\n")
    if stop:
        kout.info(""); kout.cyan("jobs"); kout.out(": jobs is stopping.\n");
    try:
        make_list();

    except Exception, e:
        kout.info(""); kout.cyan("jobs"); kout.out(": jobs is stopped causing error(s).\n");
        kout.info(""); kout.cyan("jobs"); kout.out(": EXCEPTION: %s.\n" %(str(e)));
    time.sleep(2);
    if stop:
        kout.info(""); kout.cyan("jobs"); kout.out(": jobs is stopping.\n");
    return;

all_item = [];
def make_list():
    global all_item;
    if config.http_server("server.access.force_using_root") == "enable" and os.path.isdir('.' + config.http_server("web.root")):
        where= '.' + config.http_server("web.root");
    else:
        if not os.path.isdir('.' + config.http_server("web.root")):
            kout.warn(""); kout.cyan("jobs"); kout.out(": parameter in config for web.root is invalid `%s`\n" %where);
        where = '.';
    current_dir = os.getcwd();
    try:
        os.chdir(where);
    except IOError, e:
        kout.warn(""); kout.cyan("jobs"); kout.out(": can't move to dir:'%s'\n" %where);
        return;
    all_item = list_all_files();
    if config.http_server("jobs.make_list.verbose") == "enable":
        kout.info(""); kout.cyan("jobs"); kout.out(": current_dir: %s\n" %(os.getcwd()));
    f = open("list.html", "w");
    os.chdir(current_dir);
    f.write("<html>\n<head>\n");
    f.write("<title> KProj Python Server %s </title>\n" %version.KPS.version);
    f.write("<link rel='icon' href='/favicon.ico'/>\n")
    f.write('<link rel="stylesheet" type="text/css" href="/css/list.css">');
    f.write("</head>\n<body>\n");
    f.write("<div class='h3'> List files from KPServer %s </div>\n" %version.KPS.version);
    f.write("<img src='/img/line.png'></img></br></br>\n");

    item_counting = 0;


    try:
        max_col = int(config.http_server("jobs.make_list.max_col"));
    except ValueError, e:
        max_col = 20;
    if len(all_item) > max_col:
        table_tr_td1 = "<td style='vertical-align: top;' > ";
        table_tr_td2 = "<td style='vertical-align: top' class='td2'> ";
        f.write(" <table>\n  <tr>\n");
        for item in all_item:
            if not item:
                continue;
            hidden = False;
            if config.http_server("jobs.make_list.hidden"):
                for _item in config.http_server("jobs.make_list.hidden").strip(';').split(";"):
                    if ''.join([where.replace('.', '', 1), item.replace('.', '', 1)]).startswith(_item):
                        hidden = True;
                        item_counting -= 1;
                        # print '------', ''.join([where.replace('.', '', 1), item.replace('.', '', 1)])
            if not hidden:
                item_counting += 1;
                item = item.replace(where, '/', 1).replace('.', '', 1);
                if len(all_item)/2 < item_counting:
                    table_tr_td2 += "<a href='%s'> %s </a></br>\n" %(item, item[1:]);
                else:
                    table_tr_td1 += "<a href='%s'> %s </a></br>\n" %(item, item[1:]);
        table_tr_td1 += "</td>";
        table_tr_td2 += "</td>";
        f.write("%s\n%s\n" %(table_tr_td1, table_tr_td2));
        f.write("</tr> </table>\n");
    else:
        for item in all_item:
            if not item:
                continue;
            hidden = False;
            if config.http_server("jobs.make_list.hidden"):
                for _item in config.http_server("jobs.make_list.hidden").strip(';').split(";"):
                    if ''.join([where.replace('.', '', 1), item.replace('.', '', 1)]).startswith(_item):
                        hidden = True;
                        # print '------', ''.join([where.replace('.', '', 1), item.replace('.', '', 1)])
            if not hidden:
                item_counting += 1;
                item = item.replace(where, '/', 1).replace('.', '', 1);
                f.write("<a href='%s'> %s </a></br>" %(item, item[1:]));

    f.write("<img src='/img/line.png'></img></br><br>\n");
    # f.write("<div class='get-back-index'> Go back to Index page </div>")
    f.write("<div class='h5'> KProj Python Server %s on %s %s, Python %s - written by NickLaurie ipman.ak@gmail.com </div>" \
        %(version.KPS.version, version.KPS.system.name, version.KPS.system.win_version, version.KPS.python.version));
    f.write("</body></html>");
    # f.write("<h3 style")
    # print all_item;


### Only perform is function when in current directory
def list_all_files(dir='.', perform='.'):
    """
    list_all_files() -> list_all_files_and_folders
        Only working with current directory.
    """
    _all = os.listdir('.');
    res = [];
    perform += '/'; # ignore dot when it in root dir.
    for i in _all:
        if os.path.isfile(i):
            res.append(perform + i)
    for i in _all:
        if os.path.isdir(i):
            os.chdir(i);
            res += list_all_files(i, perform + i);
            os.chdir('..')
    return res;


# List all site folders valid in /www
def list_site_map():
    pas
