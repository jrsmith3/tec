# -*- coding: utf-8 -*-

"""
Some tests for the DimensionlessLangmuirPoissonSoln class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2013 Joshua Ryan Smith"
__license__ = ""

from tec import DimensionlessLangmuirPoissonSoln
import unittest
import numpy as np

class MethodsOutputSanityCheck(unittest.TestCase):
  """
  Tests output in the obvious cases.
  """
  def setUp(self):
    """
    Create dummy object.
    """
    self.dlps = DimensionlessLangmuirPoissonSoln()
    
    

  def test_get_motive_outside_asymptote(self):
    """
    Return value should be NaN.
    """
    self.assertTrue(np.isnan(self.dlps.get_motive(-10)))

  def test_get_motive_lhs_not_nan(self):
    """
    The result for valid input shouldn't be NaN.
    
    This test runs through 10 random values within the allowed range of position on the lhs branch.
    """
    rand_pos = -2.5538 * np.random.random_sample(10)
    for pos in rand_pos:
      self.assertTrue(np.isnan(self.dlps.get_motive(pos)))
  
  def test_get_motive_lhs_positive(self):
    """
    The result for valid input should be positive.
    
    Note: use several random values in the allowed range.
    """
    rand_pos = -2.5538 * np.random.random_sample(10)
    for pos in rand_pos:
      self.assertTrue(self.dlps.get_motive(pos) >= 0)
  
  def test_get_motive_lhs_monotonic_increasing(self):
    """
    The motive should monotonically increase with negative position.
    """
    pass
  
  def test_get_motive_zero_at_origin(self):
    """
    The motive should be zero at the origin.
    """
    pass
  
  def test_get_motive_rhs_positive(self):
    """
    The result for valid input should be positive.
    
    Note: use several random values in the allowed range.
    """
    pass
  
  def test_get_motive_rhs_monotonic_increasing(self):
    """
    The motive should monotonically increase with position.
    """
    pass
  
  
  
  def test_get_position_lhs_negative_input_error(self):
    """
    lhs branch of the get_position method should fail for negative arguments.
    """
    pass
  
  def test_get_position_lhs_zero_at_origin(self):
    """
    The lhs branch should be zero at the origin.
    """
    pass
  
  def test_get_position_lhs_negative(self):
    """
    The position for all values of motive should be negative.
    """
    pass
  
  def test_get_position_lhs_monotonic_decreasing(self):
    """
    The lhs branch position should monotonically decrease with motive.
    """
    pass
  
  def test_get_position_lhs_asymptote(self):
    """
    Beyond a large value of motive, the position should be single-valued.
    """
    pass
  
  def test_get_position_rhs_negative_input_error(self):
    """
    rhs branch of the get_position method should fail for negative arguments.
    """
    pass
  
  def test_get_position_rhs_zero_at_origin(self):
    """
    The rhs branch should be zero at the origin.
    """
    pass
  
  def test_get_position_rhs_positive(self):
    """
    The position for all values of motive should be positive.
    """
    pass
  
  def test_get_position_rhs_monotonic_increasing(self):
    """
    The rhs branch position should monotonically increase with motive.
    """
    pass
  
  
  
  def test_get_position_lhs_round_trip(self):
    """
    Ensure the get_position and get_motive methods are inverses of each other.
    """
    pass
  
  def test_get_motive_lhs_round_trip(self):
    """
    Ensure the get_motive and get_position methods are inverses of each other.
    """
    pass
  
  def test_get_position_rhs_round_trip(self):
    """
    Ensure the get_position and get_motive methods are inverses of each other.
    """
    pass
  
  def test_get_motive_rhs_round_trip(self):
    """
    Ensure the get_motive and get_position methods are inverses of each other.
    """
    pass