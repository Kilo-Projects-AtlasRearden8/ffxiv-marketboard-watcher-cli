"""Allow ``python -m ffxiv_marketboard`` execution."""

import sys

from .cli import main

sys.exit(main())
