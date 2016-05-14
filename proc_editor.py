#!/usr/bin/python
# -*- coding: utf-8 -*-

import demjson

class data:
	def __init__(self, http, dir="./raw"):
		self._http = http
		self._top = dir
		
		# 初始化页面 
		self._page()
		pass
		
	# web请求页面 
	def _page(self):
		self._http.regfun("/editor/file_get", self._file_get);
		self._http.regfun("/editor/file_save", self._file_save);
		self._http.regfun("/auth/login", self._auth_login);
		return
	
	def _auth_login(self, cgi):
	    a_dict = {'code': 0};
	    
	    print cgi['session']
	    if cgi['session'].get('username'):
	        print("login:" + cgi['session'].get('username')); 
	    else:
	        cgi['session']['username'] = cgi['username'];
	        
	    return a_dict
	    
	# 获取文件内容
	def _file_get(self, cgi):
		a_dict = {'name': 'test.txt',  'last':'2016-05-02 00:00:00',  'data': 'hello!world'}
		a_dict['data'] = str(cgi)
		
		print a_dict
		return demjson.encode(a_dict) 
	
	# 文件保存
	def _file_save(self, cgi):
		print cgi;
		return "save"
	
	# 文件删除
	def _file_del(self, cgi):
		pass
	
	# 文件tag
	def _file_tag(self, cgi):
		pass
	
	
	
	
