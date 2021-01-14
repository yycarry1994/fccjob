#!C:\Users\86181\Desktop\myword\ÄûÃÊ°à¿Î³Ì\fccDjangoAdmin\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyDocX==0.9.10','console_scripts','pydocx'
__requires__ = 'PyDocX==0.9.10'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('PyDocX==0.9.10', 'console_scripts', 'pydocx')()
    )
