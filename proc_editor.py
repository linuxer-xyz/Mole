#!/usr/bin/python
# -*- coding: utf-8 -*-

import demjson
import os

class data:
    def __init__(self, http, dir="./raw"):
        self._http = http
        self._top = dir
        
        # 初始化页面 
        self._page()
        pass
        
    # web请求页面 
    def _page(self):
        self._http.regfun("/editor/file_list", self._file_list);
        self._http.regfun("/editor/file_get", self._file_get);
        self._http.regfun("/editor/file_save", self._file_save);
        self._http.regfun("/auth/login", self._auth_login);
        return
    
    def _user_loginin(self, cgi):
        return cgi['session'].get('username')
        
    def _auth_login(self, cgi):
        a_dict = {'code': -2};
        a_user = {'xyz':'suguineng', 'lijincong':'jc_lee'};
        
        print cgi['username'], cgi['password']
        if a_user.has_key(cgi['username']) and a_user[cgi['username']] == cgi['password']:
        	a_dict['code'] = 0;
    	else:
    		a_dict['code'] = -1;
    		return a_dict;
        
        if cgi['session'].get('username'):
            print("login:" + cgi['session'].get('username')); 
        else:
            cgi['session']['username'] = cgi['username'];
            
        return a_dict
    
    # 获取文件列表
    def _file_list(self, cgi):
        a_dict = {'code':'0', 'data': []}
        
        if not cgi.has_key('param'):
            cgi['param'] = '.*';
        # 打开poen
        a_cmd = os.popen("cd " + self._top +"&& ag -g '" + cgi['param'] + "'");
        a_lists = a_cmd.readlines();
        
        for a_file in a_lists:
            a_item = {};
            a_item['type'] = "file";
            a_item['text'] = a_file.replace("\n","");
            a_dict['data'].append(a_item);
        
        return a_dict
         
    # 获取文件内容
    def _file_get(self, cgi):
        a_dict = {'code':'0','name': 'test.txt',  'last':'2016-05-02 00:00:00',  'data': 'hello!world'}
        a_path = self._top + "/" + cgi['name'];
        
        if not self._user_loginin(cgi):
            a_dict['code'] = -2;
            return a_dict;
        
        a_dict['name'] = cgi['name'];
        
        # 获取文件内容
        if os.path.exists(a_path):
            with open(a_path, 'r') as f:
                a_dict['data'] = f.read(-1)
            a_stat = os.stat(a_path);
            a_dict['last'] = str(a_stat.st_mtime);
            
        else:
            # 默认值
            a_dict['data'] = "# " + a_dict['name'] + " #" + "\n\n"
        
        return a_dict
    
    # 文件保存
    def _file_save(self, cgi):
        a_dict = {'code':'0'};
        a_path = self._top + "/" + cgi['name'];
        a_data = cgi['data']
        
        # 未登录,需要重新登录
        if not self._user_loginin(cgi):
            a_dict['code'] = -2;
            return a_dict;
                    
        # 创建目录
        a_dir = os.path.dirname(a_path)
        if not os.path.exists(a_dir):
            os.makedirs(a_dir);
        
        # 如果路径存在,则判断文件是否已经被修改过
        if os.path.exists(a_path):
            a_stat = os.stat(a_path);
            print("exitsts", a_path, cgi['last'], a_stat.st_mtime);
            if str(a_stat.st_mtime) != cgi['last']:
            	a_dict['code'] = -1	# 返回失败
            	a_dict['last'] = str(a_stat.st_mtime);
            	a_dict['error'] = "file has change"
            	return a_dict
            
        # 保存
        with open(a_path, 'w+b') as f:
            f.write(a_data)
            f.close();
            
        # 获新获取最后一次时间
        if os.path.exists(a_path):
            a_stat = os.stat(a_path);
            a_dict['last'] = str(a_stat.st_mtime);
        
        return a_dict
    
    # 文件删除
    def _file_del(self, cgi):
        pass
    
    # 文件tag
    def _file_tag(self, cgi):
        pass
    
    
    
    
