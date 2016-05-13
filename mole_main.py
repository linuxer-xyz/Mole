# -*- coding: utf-8 -*-
from mole import route, run, static_file, error,get, post, put, delete, Mole
from mole.template import template
from mole import request
from mole import response

# 用于判断文件是否慧
from os import path
import thread

g_web_dict = {}
g_web_proc = g_web_dict
    

@route(':url#.*#', method="ANY")
def _web_router(url):
    a_dict = {}
    a_key = {}
    a_sess = {}    # session变量 
    a_hdr = {}    # 头信息
    a_data = ""    # 数据
    
    # 构建请求参数
    a_dict['SCRIPT_NAME'] = url;
    for a_key in request.GET.keys():
        a_dict[a_key] = request.GET.get(a_key)

    for a_key in request.POST.keys():
        a_dict[a_key] = request.POST.get(a_key)
    

    if g_web_proc.has_key('proc'):
        a_data = g_web_proc['proc'](a_dict)
    else:
        a_data = "hello!" + url
        
    return a_data

def _web_run(port = 8000):
    run(host='localhost', port = port, reloader = True);
    
# 主程序
class main:
    def __init__(self, dir="./"):
        g_web_proc = self._handler
        self._func = {}
        self._handle = {}
        self._top = dir
        self.type = "http"
        
        # 注册测试页面
        self.regfun("/hello", self._test_page)
        return

    def register(self, key, val):
        self._handle[key] = val
        
    def regfun(self, key, val):
        self._func[key] = val      
    
    def _test_page(self, cgi):
        return "test Page" + cgi["SCRIPT_NAME"]
    
    # 处理器
    def _handler(self, cgi):
        a_name = cgi["SCRIPT_NAME"]
        
        print a_name
        if self._func.has_key(a_name):
            a_func = self._func[a_name]
            a_out = a_func(cgi)
        #elif path.isfile(a_name):
        #    a_out = static_file(a_name, ".")
        #    pass
        else:
            a_out = static_file(a_name, self._top)
            
        return a_out
        
    def loop(self, port = 8000):
        g_web_dict['proc'] = self._handler
        print g_web_proc
        _web_run(port)
    
    def _task(self, port):
        print "task", port
        _web_run(port)
        print "end"
        
    def thread(self, port = 9000):
        thread.start_new_thread(self._task, (port, ))

