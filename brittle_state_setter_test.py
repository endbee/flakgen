import pytest

class test_class():
    member_a = 'failure_state'

    def set_member_a(self, value):
        self.member_a = value

    def get_member_a(self):
        return self.member_a

    def some_function(self):
        return 3.1415

global instance
instance = test_class()

def test_state_setter():
    global instance
    instance.set_member_a('success_state')
    assert (instance.some_function() == 3.1415)

def test_brittle():
    global instance
    actual = instance.get_member_a()
    expected = 'success_state'
    assert actual == expected