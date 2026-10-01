"""Compatibility entrypoint for deployments configured to run Untitled.py."""

import runpy
from pathlib import Path


runpy.run_path(str(Path(__file__).with_name("app.py")))




