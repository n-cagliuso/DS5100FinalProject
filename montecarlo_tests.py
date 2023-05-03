import pandas as pd
import unittest
from montecarlo.montecarlo import *

class DieClassTest(unittest.TestCase):
    
    def test_1_change_weight(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        
        self.assertTrue(type(DieClass1.new_weight) == float)
       
    def test_2_roll_die(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        
        expected = 2
        
        self.assertEqual(len(DieClass1.die_roll(Roll_Number)), expected)
        
    def test_3_current_die(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        
        self.assertTrue(type(DieClass1.current_die() == 'pandas.core.frame.DataFrame'))
    
class GameClassTest(unittest.TestCase):
    
    def test_4_play_show(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        GameClass1 = GameClass([DieClass1, DieClass1])
        Play_Number = 50
        GameClass1.play(Play_Number)
        GameClass1.show()
        
        self.assertTrue(type(GameClass1.show()) == pd.core.frame.DataFrame)
            
    def test_5_play_show(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        GameClass1 = GameClass([DieClass1, DieClass1])
        Play_Number = 50
        GameClass1.play(Play_Number)
        GameClass1.show()
        
        expected = 50
        
        self.assertEqual(len(GameClass1.show()), expected)
        
    def test_6_show_narrow(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        GameClass1 = GameClass([DieClass1, DieClass1])
        Play_Number = 50
        GameClass1.play(Play_Number)
        Form = 'narrow'
        GameClass1.show(Form)
        
        expected = 100
        
        self.assertEqual(len(GameClass1.show(Form)), expected)

class AnalyzerClassTest(unittest.TestCase):
    
    def test_7_jackpot(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        GameClass1 = GameClass([DieClass1, DieClass1])
        Play_Number = 50
        GameClass1.play(Play_Number)
        GameClass1.show()
        AnalyzerClass1 = AnalyzerClass(GameClass1)
        AnalyzerClass1.jackpot()

        self.assertTrue(type(AnalyzerClass1.jackpot() == 'numpy.int64'))

    def test_8_combo(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        GameClass1 = GameClass([DieClass1, DieClass1])
        Play_Number = 50
        GameClass1.play(Play_Number)
        GameClass1.show()
        AnalyzerClass1 = AnalyzerClass(GameClass1)
        AnalyzerClass1.jackpot()
        AnalyzerClass1.combo()
        
        expected = 1 
        self.assertEqual(AnalyzerClass1.face_results.shape[1], expected)
        
    def test_9_face_counts(self):
        DieClass1 = DieClass(['A', 'B', 'C'])
        Face = 'B'
        Weight = 5.0
        DieClass1.weight_change(Face, Weight)
        Roll_Number = 2
        DieClass1.die_roll(Roll_Number)
        DieClass1.current_die()
        GameClass1 = GameClass([DieClass1, DieClass1])
        Play_Number = 50
        GameClass1.play(Play_Number)
        GameClass1.show()
        AnalyzerClass1 = AnalyzerClass(GameClass1)
        AnalyzerClass1.jackpot()
        AnalyzerClass1.combo()
        AnalyzerClass1.face_counts_per_roll()
        
        self.assertFalse(len(AnalyzerClass1.face_counts) > 50)
        
if __name__ == '__main__':
    unittest.main(verbosity = 3)