def test_one_plus_one():
    assert 1 + 1 == 2

def test_string_equals():
    assert "hello" == "hello"

def test_import_jinja2():
    from jinja2 import Environment
    assert Environment is not None
