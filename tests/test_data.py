import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("data_analysis",ROOT/"examples/data/analyze.py")
analysis=importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


class DataTests(unittest.TestCase):
    def test_weighted_rates_and_distinct_change_units(self):
        result=analysis.analyze(ROOT/"examples/data/input/cohorts.csv")
        self.assertAlmostEqual(result["totals"]["A"]["rate_pct"],1.9)
        self.assertAlmostEqual(result["totals"]["B"]["rate_pct"],7.2)
        self.assertAlmostEqual(result["change_pp"],5.3)
        self.assertAlmostEqual(result["relative_change_pct"],278.94736842105266)
        self.assertLess(result["cohorts"]["heavy"]["B"]["rate_pct"],result["cohorts"]["heavy"]["A"]["rate_pct"])

    def test_zero_baseline_and_invalid_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"data.csv"
            path.write_text("variant,cohort,requests,errors\nA,x,10,0\nB,x,10,1\n")
            self.assertIsNone(analysis.analyze(path)["relative_change_pct"])
            for rows in ["A,x,0,0\nB,x,10,1\n","A,x,10,11\nB,x,10,1\n","A,x,10,0\nA,x,10,0\nB,x,10,1\n","A,x,10,0\nB,y,10,1\n"]:
                path.write_text("variant,cohort,requests,errors\n"+rows)
                with self.assertRaises(ValueError):
                    analysis.analyze(path)


if __name__=="__main__":
    unittest.main()
