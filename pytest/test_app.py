from src.quantifier import *
def test_quantifier_to_latex():
    assert quantifier_to_latex("E") == "E"
    assert quantifier_to_latex("A") == "A"
    assert quantifier_to_latex("E8") == r"E^{\infty}"
    assert quantifier_to_latex("A8") == r"A^{\infty}"
