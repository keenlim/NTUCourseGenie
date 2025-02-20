# conftest.py
import sys
import os

# Insert the project root into sys.path.
# This assumes that conftest.py is in Course_v2/tests/ or Course_v2/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)