#!/usr/bin/python
# -*- coding: utf-8 -*-

import mole_main as myhttp
import proc_mdplus as mymdplus

myapp = myhttp.main()
myeditor = mymdplus.main(myapp)

# 进入循环
myapp.loop(9000);

