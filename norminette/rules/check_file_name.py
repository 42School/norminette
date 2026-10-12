import os
import re

from norminette.errors import Error, Highlight
from norminette.rules import Rule, Check

allowed = re.compile(r"[a-z0-9_]+")


class CheckFileName(Rule, Check, runs_on_end=True, runs_on_rule=False):
    def run(self, context):
        """
        File and directory names hold lowercases, digits and underscores.
        Directories are read from where the run started, so a file gets the
        same verdict however its path was typed.
        """
        parts = [(context.file.name, context.file.basename)]
        root = context.file.root
        if root is not None:
            folder = os.path.dirname(os.path.abspath(context.file.path))
            relative = os.path.relpath(folder, os.path.abspath(root))
            if not relative.startswith(".."):
                parts += [(part, part) for part in relative.split(os.sep)]
        for part, shown in parts:
            if part in ("", ".", ".."):
                continue
            if allowed.fullmatch(part) is None:
                error = Error.from_name(
                    "FORBIDDEN_CHAR_FILE", highlights=[Highlight(1, 1)]
                )
                error.text = f"'{shown}': {error.text}"
                context.errors.add(error)
                return False, 0
        return False, 0
