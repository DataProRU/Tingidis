import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("Python Path:", sys.path)
print("Current Working Directory:", os.getcwd())

from main import app


def test_example():
    assert app is not None
