import pytest
global a
a = 1

@pytest.mark.run(order=(1))
def test_one():
    global a
    assert a == 1

@pytest.mark.run(order=(2))
def test_two():
    global a
    a = 2
    assert a == 2
