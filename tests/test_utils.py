from src.knockout_competition import get_round_name


def test_final():
    assert get_round_name(1, 2) == "Final"
    assert get_round_name(2, 2) == "Final"
    assert get_round_name(4, 2) == "Final"
    assert get_round_name(6, 2) == "Final"


def test_semifinal():
    assert get_round_name(1, 4) == "Semi-Final"
    assert get_round_name(2, 4) == "Semi-Final"
    assert get_round_name(4, 4) == "Semi-Final"
    assert get_round_name(6, 4) == "Semi-Final"


def test_round_1():
    assert get_round_name(1, 16) == "1st Round"


def test_round_2():
    assert get_round_name(2, 16) == "2nd Round"


def test_round_3():
    assert get_round_name(3, 16) == "3rd Round"
