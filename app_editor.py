#!/usr/bin/python
# -*- coding: utf-8 -*-

import mole_main as myhttp
import proc_mdplus as mymdplus
import proc_editor as cdata
from optparse import OptionParser

# 解析参数
a_parser = OptionParser(usage="usage: python %prog [options] filename");
a_parser.add_option("-p", "--port",
              action="store",
              type="int",
              dest="port",
              default=8002,
              help="Listen Port. default=8002")
(a_opt, a_args) = a_parser.parse_args()
              
                      
myapp = myhttp.main()
myeditor = mymdplus.main(myapp)
mydata = cdata.data(myapp)

# 进入循环
myapp.loop(a_opt.port);

