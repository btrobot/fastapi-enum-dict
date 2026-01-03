import pytest
from jinja2 import Environment, PackageLoader


def test_detector_renders():
    """Test detector template renders"""
    env = Environment(loader=PackageLoader('fastapi_enum_dict', 'templates'))
    template = env.get_template('core_detector.py.j2')
    result = template.render(base_dir='app')
    assert 'def detect_type' in result


def test_detect_enum():
    """Test enum detection"""
    env = Environment(loader=PackageLoader('fastapi_enum_dict', 'templates'))
    template = env.get_template('core_detector.py.j2')
    code = template.render(base_dir='app')
    
    namespace = {}
    exec(code, namespace)
    detect_type = namespace['detect_type']
    
    result = detect_type('Status', ['Pending', 'Paid'])
    assert result == 'enum'


def test_detect_dict():
    """Test dict detection"""
    env = Environment(loader=PackageLoader('fastapi_enum_dict', 'templates'))
    template = env.get_template('core_detector.py.j2')
    code = template.render(base_dir='app')
    
    namespace = {}
    exec(code, namespace)
    detect_type = namespace['detect_type']
    
    result = detect_type('Dept', ['RD', 'QA', 'OPS'])
    assert result == 'enum'  # Short English words -> enum
    
    result2 = detect_type('Dept', ['研发部', '测试部'])
    assert result2 == 'dict'  # Chinese -> dict
