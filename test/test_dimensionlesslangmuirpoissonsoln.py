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
    Beyond asymptote return value should be NaN.
    """
    self.assertTrue(np.isnan(self.dlps.get_motive(-10)))

  def test_get_motive_lhs_not_nan(self):
    """
    The result for valid input shouldn't be NaN.
    
    This test runs through 10 random values within the allowed range of position on the lhs branch.
    """
    rand_pos = -2.5538 * np.random.random_sample(10)
    for pos in rand_pos:
      self.assertFalse(np.isnan(self.dlps.get_motive(pos)))
  
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
    
    # Monotonically decreasing array of legal lhs position values.
    rand_pos = -2.5538 * np.sort(np.random.random_sample(10))
    rand_mot = []
    for pos in rand_pos:
      rand_mot.append(self.dlps.get_motive(pos))
    self.assertTrue( all(x<y for x, y in zip(rand_mot, rand_mot[1:])))
    
  def test_get_motive_zero_at_origin(self):
    """
    The motive should be zero at the origin.
    """
    self.assertEqual(self.dlps.get_motive(0), 0)
  
  def test_get_motive_rhs_positive(self):
    """
    The result for valid input should be positive.
    
    Note: use several random values in the allowed range.
    """
    rand_pos = 100. * np.random.random_sample(10)
    for pos in rand_pos:
      self.assertTrue(self.dlps.get_motive(pos) >= 0)
  
  def test_get_motive_rhs_monotonic_increasing(self):
    """
    The motive should monotonically increase with position.
    """

    # Monotonically increasing array of legal rhs position values.
    rand_pos = 100. * np.sort(np.random.random_sample(10))
    rand_mot = []
    for pos in rand_pos:
      rand_mot.append(self.dlps.get_motive(pos))
    self.assertTrue(all(x<y for x, y in zip(rand_mot, rand_mot[1:])))
  
  
  def test_get_position_lhs_default(self):
    """
    Or whatever the default should be.
    """
    pass
    
    
  def test_get_position_lhs_negative_input_error(self):
    """
    get_position method should be NaN for negative motive and lhs branch.
    """
    self.assertTrue(np.isnan(self.dlps.get_position(-10,"lhs")))

  def test_get_position_lhs_zero_at_origin(self):
    """
    The position should be zero at the origin on the lhs branch.
    """
    self.assertEqual(self.dlps.get_position(0, "lhs"), 0)

  def test_get_position_lhs_negative(self):
    """
    The position for all values of defined motive should be negative.
    """
    rand_mot = 100. * np.random.random_sample(10)
    self.assertTrue(all(self.dlps.get_position(mot,"lhs") < 0 for mot in rand_mot))
  
  def test_get_position_lhs_monotonic_decreasing(self):
    """
    position should monotonically decrease to equilibration with motive on lhs branch.
    """
    rand_mot = 20. * np.sort(np.random.random_sample(10))
    rand_pos = []
    for mot in rand_mot:
      rand_pos.append(self.dlps.get_position(mot,"lhs"))
    self.assertTrue(all(x>=y for x, y in zip(rand_pos, rand_pos[1:])))
  
  def test_get_position_lhs_asymptote(self):
    """
    Beyond a large value of motive, the position should be single-valued.
    """
    self.assertEqual(self.dlps.get_position(100,"lhs"), self.dlps.get_position(200,"lhs"))
  
  def test_get_position_rhs_negative_input_error(self):
    """
    get_position method should be NaN for negative motive and rhs branch.
    """
    self.assertTrue(np.isnan(self.dlps.get_position(-10,"rhs")))
  
  def test_get_position_rhs_zero_at_origin(self):
    """
    The position should be zero at the origin on the rhs branch.
    """
    self.assertEqual(self.dlps.get_position(0,"rhs"), 0)
  
  def test_get_position_rhs_positive(self):
    """
    The position for all values of motive should be positive.
    """
    rand_mot = 100. * np.random.random_sample(10)
    self.assertTrue(all(self.dlps.get_position(mot,"rhs") > 0 for mot in rand_mot))

  def test_get_position_rhs_monotonic_increasing(self):
    """
    position should monotonically increase with motive on rhs branch.
    """
    # Monotonically increasing array of motive values
    rand_mot = 100. * np.sort(np.random.random_sample(10))
    rand_pos = []
    for mot in rand_mot:
      rand_pos.append(self.dlps.get_position(mot,"rhs"))
    self.assertTrue(all(x<y for x, y in zip(rand_mot, rand_mot[1:])))



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