#!/usr/bin/python
# -*- coding: utf-8 -*-

import mole_main as myhttp
import proc_mdplus as mymdplus
import proc_editor as cdata

myapp = myhttp.main()
myeditor = mymdplus.main(myapp)
mydata = cdata.data(myapp)

# 进入循环
myapp.loop(9000);

