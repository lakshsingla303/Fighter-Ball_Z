from project import function1
from project import function2
from project import function3


def test_function1():
    assert function1(2) == 2


def test_function2():
    assert function2(3) == 9


def test_function3():
    assert function3(5) == 125
