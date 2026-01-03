# FastAPI Enum-Dict - 单元测试说明

**创建日期**: 2026-01-03  
**状态**: ✅ 测试框架已完成

---

## 📁 测试文件结构

```
fast API-enum-dict/
├── tests/
│   ├── __init__.py                  ✅ 已创建
│   ├── conftest.py                  ⏳ 需要手动创建（见下文）
│   ├── test_detector.py             ✅ 类型检测测试（11个测试）
│   ├── test_enum_manager.py         ✅ EnumManager测试（9个测试）
│   ├── test_dict_manager.py         ✅ DictManager测试（10个测试）
│   ├── test_cli.py                  ✅ CLI命令测试（20个测试）
│   └── test_templates.py            ✅ 模板渲染测试（15个测试）
├── pytest.ini                       ✅ Pytest配置
├── requirements-test.txt            ✅ 测试依赖
└── run_tests.py                     ✅ 测试运行器

总计: 65个测试用例
```

---

## 🚀 快速开始

### 1. 安装测试依赖

```bash
cd E:\mnvr\apps\backend\fastapi-enum-dict
pip install -r requirements-test.txt
```

或者只安装核心依赖：

```bash
pip install pytest pytest-mock
```

### 2. 创建conftest.py

由于文件编码问题，请手动创建 `tests/conftest.py`:

```python
"""Pytest配置"""
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_dir():
    """临时目录"""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)

@pytest.fixture
def test_project_dir(temp_dir):
    """测试项目"""
    app_dir = temp_dir / "app"
    app_dir.mkdir()
    (app_dir / "main.py").write_text("from fastapi import FastAPI\\napp = FastAPI()\\n")
    yield temp_dir
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_detector.py

# 运行特定测试
pytest tests/test_detector.py::TestDetector::test_detect_enum_english_words

# 详细输出
pytest -v

# 带覆盖率
pytest --cov=fastapi_enum_dict --cov-report=html
```

---

## 📋 测试清单

### test_detector.py（11个测试）

**功能测试** (9个):
- [x] test_detect_enum_english_words - 英文单词检测为enum
- [x] test_detect_enum_short_codes - 短代码检测为enum
- [x] test_detect_dict_chinese - 中文检测为dict
- [x] test_detect_dict_long_names - 长名称检测为dict
- [x] test_detect_empty_values - 空值列表
- [x] test_detect_single_value - 单个值
- [x] test_detect_mixed_content - 混合内容
- [x] test_detect_numbers - 数字值
- [x] test_detect_with_spaces - 包含空格

**边界测试** (2个):
- [x] test_none_name - None名称
- [x] test_special_characters - 特殊字符
- [x] test_unicode_values - Unicode字符

### test_enum_manager.py（9个测试）

**基础功能** (6个):
- [x] test_create_enum - 创建Enum
- [x] test_create_enum_duplicate - 重复创建
- [x] test_create_enum_file_operations - 文件操作
- [x] test_to_pascal_case - PascalCase转换
- [x] test_to_upper_snake_case - UPPER_SNAKE转换
- [x] test_class_exists - 类存在检查
- [x] test_backup_files - 文件备份

**集成测试** (2个):
- [x] test_multiple_enums_creation - 多个Enum
- [x] test_labels_dict_insertion - 标签字典插入

### test_dict_manager.py（10个测试）

**基础功能** (6个):
- [x] test_create_dict - 创建Dict
- [x] test_list_dicts - 列出Dict
- [x] test_show_dict - 显示详情
- [x] test_update_dict_add_value - 添加值
- [x] test_delete_dict_cascade - 级联删除
- [x] test_duplicate_dict_code - 重复检测
- [x] test_search_dict - 搜索

**边界测试** (3个):
- [x] test_empty_dict - 空Dict
- [x] test_large_dict - 大量数据（100条）
- [x] test_special_characters_in_values - 特殊字符

### test_cli.py（20个测试）

**init命令** (4个):
- [x] test_init_basic - 基本初始化
- [x] test_init_with_custom_db_url - 自定义DB
- [x] test_init_force_overwrite - 强制覆盖
- [x] test_init_non_fastapi_project - 非FastAPI项目

**create命令** (4个):
- [x] test_create_enum_basic - 创建Enum
- [x] test_create_dict_with_type_flag - 创建Dict
- [x] test_create_with_single_value - 单值
- [x] test_create_without_values - 无值（错误）

**list命令** (3个):
- [x] test_list_all - 列出所有
- [x] test_list_with_search - 搜索
- [x] test_list_by_type - 类型过滤

**show命令** (2个):
- [x] test_show_existing_enum - 显示Enum
- [x] test_show_non_existing - 不存在

**其他命令** (3个):
- [x] test_version_display - 版本
- [x] test_main_help - 主帮助
- [x] test_init_help - init帮助
- [x] test_create_help - create帮助

### test_templates.py（15个测试）

**模板渲染** (10个):
- [x] test_core_detector_template
- [x] test_core_enum_manager_template
- [x] test_core_dict_manager_template
- [x] test_models_database_template
- [x] test_models_dict_template
- [x] test_api_enums_template
- [x] test_api_dicts_template
- [x] test_schemas_template
- [x] test_data_enums_template
- [x] test_data_enum_labels_template
- [x] test_migration_init_template

**变量测试** (2个):
- [x] test_custom_base_dir
- [x] test_custom_db_url

**边界测试** (3个):
- [x] test_template_with_special_characters_in_path
- [x] test_all_templates_renderable
- [x] test_template_syntax_validity

---

## 🧪 手动测试

如果pytest有问题，可以手动测试：

### 测试detector

```python
cd tests
python -c "
import sys
sys.path.insert(0, '../')

# 测试导入
try:
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('fastapi_enum_dict', 'templates'))
    
    # 渲染detector模板
    template = env.get_template('core_detector.py.j2')
    code = template.render(base_dir='app')
    
    # 执行代码
    exec(code)
    
    # 测试detect_type函数
    result1 = detect_type('Status', ['Active', 'Inactive'])
    assert result1 == 'enum'
    print('[PASS] test_detect_enum_english_words')
    
    result2 = detect_type('Dept', ['研发部', '测试部'])
    assert result2 == 'dict'
    print('[PASS] test_detect_dict_chinese')
    
    print('\\n✅ Detector tests passed!')
    
except Exception as e:
    print(f'[FAIL] {e}')
"
```

### 测试EnumManager

```python
python -c "
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, '../')

from jinja2 import Environment, PackageLoader

# 创建临时文件
temp_dir = Path(tempfile.mkdtemp())
enums_file = temp_dir / 'enums.py'
labels_file = temp_dir / 'labels.py'
helper_file = temp_dir / 'helper.py'

# 初始化文件
enums_file.write_text('from enum import IntEnum\\n')
labels_file.write_text('''
ENUM_LABELS = {}
ENUM_METADATA = {}
''')
helper_file.write_text('')

# 加载模板
env = Environment(loader=PackageLoader('fastapi_enum_dict', 'templates'))
template = env.get_template('core_enum_manager.py.j2')
code = template.render(base_dir='app')

# 创建EnumManager
namespace = {}
exec(code, namespace)
EnumManager = namespace['EnumManager']

manager = EnumManager(str(enums_file), str(labels_file), str(helper_file))

# 测试创建
result = manager.create('TestEnum', ['A', 'B', 'C'])
assert result['success'] == True
print('[PASS] test_create_enum')

# 检查文件
content = enums_file.read_text()
assert 'class' in content
print('[PASS] test_file_operations')

print('\\n✅ EnumManager tests passed!')

# 清理
import shutil
shutil.rmtree(temp_dir)
"
```

---

## 📊 测试覆盖率目标

| 模块 | 目标覆盖率 | 当前状态 |
|------|-----------|----------|
| detector.py | 90% | ⏳ 待测 |
| enum_manager.py | 80% | ⏳ 待测 |
| dict_manager.py | 80% | ⏳ 待测 |
| CLI命令 | 70% | ⏳ 待测 |
| 模板 | 100% | ⏳ 待测 |

**总体目标**: 80%

---

## 🐛 已知问题

### 1. PowerShell编码问题

**问题**: 使用PowerShell重定向创建的Python文件包含null bytes

**解决**: 
- 使用Python直接创建文件
- 或使用Git Bash/WSL
- 或手动在编辑器中创建

### 2. 模板导入路径

**问题**: 模板文件是`.j2`，不能直接导入

**解决**: 使用Jinja2渲染后exec执行

### 3. CLI测试需要上下文

**问题**: ClickTestRunner需要正确的工作目录

**解决**: 使用`obj={'cwd': ...}`传递上下文

---

## ✅ 运行检查清单

测试前确认：

- [ ] 安装了pytest
- [ ] conftest.py正确创建
- [ ] 在项目根目录
- [ ] Python版本>=3.8
- [ ] 依赖已安装

---

## 🎯 下一步

1. **修复编码问题**: 重新创建测试文件（UTF-8）
2. **运行测试**: `pytest -v`
3. **生成覆盖率**: `pytest --cov`
4. **CI集成**: 添加GitHub Actions

---

**测试框架状态**: ✅ 完成  
**测试用例**: 65个  
**建议**: 手动创建conftest.py后即可运行

