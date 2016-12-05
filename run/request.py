"""
    KPS:HTTP_Server::request: work with request.
"""

import os, sys;
import time;
from run import config;
from libs.version import KPS

class HTTPRequest:
    def __init__(self, request):
        self.request = request;

    def header(self):
        # if '\n\n' in self.request.strip('\r'):
        #     return self.request.strip('\r').split('\n\n', 1)[0];
        # else:
        #     # all is header.
        #     return self.request;
        return self.request

    def request_line(self):
        return self.request.split('\n', 1)[0].replace('\r', '');

    def method(self):
        return self.request_line().split(' ', 1)[0].upper();

    def request_path(self):
        try:
            rp = self.request_line().split()[1];
            return rp;
        except IndexError, e:
            return "";


    def http_version(self):
        http_string = self.request_line().split()[2];
        return http_string.split('/')[1];

    def keydata(self, key, case_sensitive=False, return_origin_key=False):
        header = self.header().replace('\r', '').replace('\t', '');
        h_key = h_data = "";
        for line in header.split('\n'):
            line.strip();
            while 1:
                if "  " in line:
                    line = line.replace('  ', ' ');
                else:
                    break;
            if not case_sensitive:
                if line.split(':', 1)[0].lower() == key.lower() and len(line.split(':', 1)) == 2:
                    h_key = line.split()[0];
                    h_data = line.split()[1];
                    break;
            else:
                if line.split(':', 1)[0] == key.lower() and len(line.split(':')) == 2:
                    h_key = line.split()[0];
                    h_data = line.split()[1];
                    break;

        if return_origin_key:
            res = [h_key, h_data];
        if h_key == "":
            return "";
        else:
            return h_data;

    def data(self):
        request_method = self.method();
        if request_method == 'POST':
            if '\n\n' in self.request.strip('\r'):
                if len(self.request.split('\n\n', 1)) == 2:
                    return self.request.split('\n\n', 1)[1];
            else:
                return "";
        if request_method == 'GET':
            # GET data is in the middle of requset line.
            if len(self.request_line().split()[1].split('?', 1)) == 2:
                return self.request_line().split()[1].split('?', 1)[1];
            else:
                return "";


class HTTPResponse:
    """
        HTTPResponse: support method to create an packet to HTTP client.
    """
    def __init__(self, file_request="", status_code=200, status_phrase="OK", content_type="", content_length=0, additional_string="", content=""):
        self.status_code = status_code;
        self.status_phrase = status_phrase;
        self.content_type = content_type;
        self.content_length = content_length;
        self.additional_string = additional_string;
        self.file_request = file_request;   # Real file
        self.given_content = content;

    def content(self):
        if os.path.isfile(self.file_request):
            c = open(self.file_request, 'rb').read();
            self.content_length = len(c);
            return c;
        else:
            return "";

    def get_date(self):
        d = ', '.join(time.ctime(time.time()).split(' ', 1));
        d = d.split(' ');
        return ' '.join([d[0], d[1], d[2], d[4], d[3], 'GMT+7'])

    def mimetype(self):
        m = config.mimetype(self.file_request);
        if m:
            self.content_type = "\nContent-Type: " + m;
        return m;

    def header(self):
        self.mimetype();
        if config.http_server("server.header_addition") == "enable" and len(config.http_server("server.header_addition.value")) != 0:
            self.additional_string = config.http_server("server.header_addition.value");
            # print "---------- Added ------------"
        response = "HTTP/1.1 %d %s%s\nServer: KProj Python Server %s\nContent-Length: %d\nDate: %s\nLast-Modified: %s%s\nConnection: close\r\n\r\n" \
            %(self.status_code, self.status_phrase, self.content_type, KPS.version,  self.content_length, self.get_date(), self.get_date(), self.additional_string)
        # response = "HTTP/1.1 %d %s%s\nServer: KProj Python Server %s\nContent-Length: %d\nDate: %s%s\r\n\r\n" \
        #     %(self.status_code, self.status_phrase, self.content_type, KPS.version,  self.content_length, self.get_date(), self.additional_string)
        return response;

    def response(self, blank_content=False):
        if not blank_content:
            # if self.given_content:
            #     content = "HTTP/1.1 200 OK\nServer: KPS %s\nContent-Length: %d\nDate: %s\r\n\r\n %s" \
            #         %(KPS.version, len(self.given_content), self.get_date(), self.given_content);
            content = self.content()
            return ''.join([self.header(), content]);
        else:
            return "HTTP/1.1 200 OK \nServer: KProj Python Server \nContent-Length: 0\nConnection: close\r\n\r\n";
