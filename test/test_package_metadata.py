# coding: utf-8
import tec


def test_version_exists():
    assert hasattr(tec, "__version__")
