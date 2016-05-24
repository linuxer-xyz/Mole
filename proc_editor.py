#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import datetime
import base64

class data:
    def __init__(self, http, dir="./raw", auth="{'admin':'admin'}"):
        self._http = http
        self._top = dir
        self._skipdir = "upload";
        self._upload = dir + "/upload"
        self._user = eval(auth);
        
        # 初始化页面 
        self._page()
        pass
        
    # web请求页面 
    def _page(self):
        self._http.regfun("/editor/flist_oper", self._flist_oper);
        self._http.regfun("/editor/file_list", self._file_list);
        self._http.regfun("/editor/file_get", self._file_get);
        self._http.regfun("/editor/file_save", self._file_save);
        self._http.regfun("/editor/img_save", self._img_save);
        self._http.regfun("/auth/login", self._auth_login);
        return
    
    def _user_loginin(self, cgi):
        return cgi['session'].get('username')
        
    def _auth_login(self, cgi):
        a_dict = {'code': -2};
        a_user = self._user;
        
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
    
    # 转化成树形的
    def _file_tolvl(self, a_out, a_path, a_isdir): 
        a_dir = os.path.dirname(a_path)
        a_base = os.path.basename(a_path)
        return
        

    def _flist_dir(self, dtop, dpath):
        a_dlist = dpath.split("/");
        if not dtop.has_key('children'):
            dtop['children'] = []
            
        if dpath == "":
            return dtop;
                      
        a_cur = dtop
        a_path = ""
        for a_dir in a_dlist:
            a_ctop = None
            a_path = a_path + "/" + a_dir
            if not a_cur.has_key('children'):
                a_cur['children'] = []
            
            # 判断是否存在 
            for a_cnode in a_cur['children']:
                if a_cnode['text'] == a_dir:
                    a_ctop = a_cnode;
                    break;
            
            if not a_ctop:
                a_dict = {}
                a_dict['id'] = ''
                a_dict['dir'] = a_path;
                a_dict['text'] = a_dir
                a_dict['children'] = []
                a_ctop = a_dict;
                a_cur['children'].append(a_ctop)
            a_cur = a_ctop
        
        return a_cur
        
    # 获取文件列表
    def _file_list(self, cgi):
        a_dict = {'code':'0', 'data': []}
        a_json = "";
        
        if not cgi.has_key('param'):
            cgi['param'] = '.*';
        # 打开poen
        a_cmd = os.popen("mkdir -p " + self._top + "&& cd " + self._top +"&& ag -g '" + cgi['param'] + "' --ignore '" +  self._skipdir + "'");
        a_lists = a_cmd.readlines();
        a_dict_top = {}
        a_out_dict = {}
        a_dict_cur = []
        a_list_top = {'children':[], 'text':'/', 'id':'', 'dir':"/"}
        for a_file in a_lists:
            a_item = {};
            a_name = a_file.replace("\n","")
            a_item['id'] = a_name;
            a_item['type'] = "file";
            a_item['text'] = a_file.replace("\n","");
            a_dict['data'].append(a_item);
            
            # 形成文件层次
            a_path = a_name;
            a_dir = os.path.dirname(a_path)
            a_base = os.path.basename(a_path)
            a_item['id'] = a_name;
            a_item['text'] = a_base;
            if a_dir != "":
                # alloc路径
                a_cdir = self._flist_dir(a_list_top, a_dir);
            else:
                a_cdir = a_list_top
            a_cdir['children'].append(a_item)
        
        if cgi.has_key('dataonly'):
            a_json = json.dumps([a_list_top], ensure_ascii=False);
            return a_json;
        a_cmd.close();
        return a_dict
        
    def _flist_oper(self, cgi):
        a_dict = {'code':'0'}
        a_cmd = ""
        
        a_ret = "";
        if not self._user_loginin(cgi):
            a_dict['code'] = -2;
            return a_dict;
        
        # 判断参数合法性
        if not cgi.has_key('oper'):
            a_dict['code'] = -1;
            return a_dict;
        
        if not cgi.has_key('curdir'):
            a_dict['code'] = -1;
            return a_dict;
        
        a_path = self._top + cgi['curdir']
        if not os.path.exists(a_path):
            a_dict['code'] = -1;
            return;
        
        if (not cgi.has_key('name')) or (cgi['name'] == ""):
            a_dict['code'] = -1;
            return;
        
        # 添加文件
        if cgi['oper'] == 'addfile':
            a_path = self._top + "/" + cgi['curdir'] + "/" + cgi['name'];
            a_cmd = "touch " + a_path
        
        if cgi['oper'] == 'adddir':
            a_path= self._top + "/" + cgi['curdir'] + "/" + cgi['name'];
            a_cmd = "mkdir -p " + a_path + "; touch " + a_path + "/index"
        
        a_dict['info'] = os.popen(a_cmd).readlines()
        print a_cmd
        return a_dict;
    
    def _img_save(self, cgi):
        a_dict = {'success':'0', 'message':"上传失败", 'url':''};
        
        print cgi
        if cgi.has_key('paste'):
            a_array =  cgi['editormd-image-file'].split("base64,");
            if len(a_array) < 2:
            	return a_dict
            a_bindata = a_array[1];
            a_bindata = base64.decodestring(a_bindata)
            a_name = "paste";
        else :
            uploadfile = cgi['editormd-image-file'];
            a_bindata = uploadfile.file.read()
            a_name = uploadfile.filename

        tnow = datetime.datetime.now()
        parent_path = os.path.join(self._upload, tnow.strftime('%Y%m'))
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        
        m_f = ("000"+str(tnow.microsecond/1000))[-3:]
        filename = tnow.strftime("%d%H%M%S")+m_f+"_" + a_name;
        upload_path = os.path.join(parent_path, filename)
        with open(upload_path, 'w+t') as f:
            f.write(a_bindata)
            f.close();
        url = '%s/%s/%s'%(self._upload, tnow.strftime('%Y%m'), filename)
        return {'success': 1, 'message': '上传成功', 'url': url}
    
        return a_dict;
        
           
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
                a_dict['code'] = -1    # 返回失败
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
    
    
    
    
