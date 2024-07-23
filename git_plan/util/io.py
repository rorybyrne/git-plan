"""IO Utils."""

import json
from pathlib import Path
from typing import Any


class FlexibleEncoder(json.JSONEncoder):
    """Encode diverse objects for JSON writing."""

    def default(self, o: Any) -> Any:
        if isinstance(o, Path):
            return str(o)
        return super().default(o)
