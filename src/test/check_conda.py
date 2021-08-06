"""Test requires externally produced file"""
import json
import sys

if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, 'r') as f:
        data = json.load(f)
        assert data == {
            "PTable": "BSD",
            "click": "BSD",
            "configparser": "MIT",
            "liccheck": "Apache Software",
            "loguru": "MIT",
            "pip-licenses": "MIT",
            "pydantic": "MIT",
            "semantic-version": "BSD",
            "toml": "MIT",
            "typing-extensions": "Python Software Foundation",
            "pyyaml": "MIT",
            "libgcc-ng": "GPL-3.0-only WITH GCC-exception-3.1",
            "yaml": "MIT"
        }, "Failed"
