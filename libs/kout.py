"""
    KPServer::kout.py: Output color for KPServer Console.
"""
import os, sys;
from ctypes import windll
import time;

class color:
	black	= 0
	blue	= 1
	green	= 2
	cyan	= 3
	red		= 4
	pink	= 5
	yellow	= 6
	white	= 7
	gray	= 8
	class light:
		blue	= 9
		green	= 0xA
		cyan	= 0xB
		red		= 0xC
		pink	= 0xD
		yellow	= 0xE
		white	= 0xF

def set_color(color):
	if type(color) != int:
		return False;
	STD_OUTPUT_HANDLE = -11;
	stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE);
	windll.kernel32.SetConsoleTextAttribute(stdout_handle, color);
	return True;

default_color = color.white;
def reset_color():
    return set_color(default_color);

out = lambda msg: sys.stdout.write(msg);
mod_name = "";
mod_name_color = color.light.cyan;

def normal(msg):
    out('[');
    set_color(color.light.green);
    out('+');
    reset_color();
    out('] ');
    if mod_name:
        set_color(mod_name_color);
        out(mod_name); reset_color();
    out(msg);
    return "";

def info(msg):
    out('[');
    set_color(color.light.cyan);
    out('*');
    reset_color();
    out('] ');
    if mod_name:
        set_color(mod_name_color);
        out(mod_name); reset_color();
    out(msg);
    return "";

def warn(msg):
    out('[');
    set_color(color.yellow);
    out('!');
    reset_color();
    out('] ');
    if mod_name:
        set_color(mod_name_color);
        out(mod_name); reset_color();
    out(msg);
    return "";

def error(msg):
    out('[');
    set_color(color.red);
    out('!');
    reset_color();
    out('] ');
    if mod_name:
        set_color(mod_name_color);
        out(mod_name); reset_color();
    out(msg);
    return "";

def critical(msg):
    out('[');
    set_color(color.cyan);
    out(" CRITICAL ");
    reset_color();
    out('] ');
    if mod_name:
        set_color(mod_name_color);
        out(mod_name); reset_color();
    out(msg);
    return "";

def exception(msg):
    if True:
        raise Exception(msg);

def red(msg):
    set_color(color.light.red);
    out(msg);
    reset_color();
    return "";

def blue(msg):
    set_color(color.light.blue);
    out(msg);
    reset_color();
    return "";

def cyan(msg):
    set_color(color.light.cyan);
    out(msg);
    reset_color();
    return " ";

def yellow(msg):
    set_color(color.light.yellow);
    out(msg);
    reset_color();
    return " ";

def green(msg):
    set_color(color.light.green);
    out(msg);
    reset_color();
    return " ";

def white(msg):
    set_color(color.light.white);
    out(msg);
    reset_color();
    return " ";

def time_to_str(sep_day='/', sep_hour=':'):
    return time.strftime("%d %b %y");

def time_to_str_fmt(sep_hour=':'):
    return;
