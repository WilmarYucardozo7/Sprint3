
# -*- coding: utf-8 -*-
import re
import sys

from virtualenv.__main__ import run_with_catch

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run_with_catch())
