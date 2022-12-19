# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


def test_tec_constructor_happy_path(valid_ideal_model):
    with does_not_raise():
        device = tec.TEC(valid_ideal_model)
