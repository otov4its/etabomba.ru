# coding=utf8
# Initial settings for scripts

import sys
import os

dn = os.path.dirname
  
prj_root = dn(dn(dn(os.path.abspath(__file__))))

sys.path.append(prj_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'etabomba.settings'