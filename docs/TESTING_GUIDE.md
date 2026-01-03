# FastAPI Enum-Dict - 测试指南

完整的测试流程，确保所有功能正常工作。

---

## 🚀 快速测试（5分钟）

### 1. 安装包

```bash
cd E:\mnvr\apps\backend\fastapi-enum-dict
pip install -e .
```

**预期结果**:
```
Successfully installed fastapi-enum-dict
```

### 2. 验证安装

```bash
enum-dict --help
```

**预期结果**:
```
Usage: enum-dict [OPTIONS] COMMAND [ARGS]...

Commands:
  init    初始化Enum-Dict功能到FastAPI项目
  create  创建新的Enum或Dict
  list    列出所有Enum和Dict
  show    显示Enum或Dict的详细信息
  update  更新Enum或Dict
  delete  删除Enum或Dict
```

---

## 📋 完整功能测试

### 测试环境准备

```bash
# 创建测试项目
cd E:\mnvr\apps\backend
mkdir test-enum-dict-demo
cd test-enum-dict-demo

# 创建基本结构
mkdir app
echo "from fastapi import FastAPI; app = FastAPI()" > app/main.py
echo "fastapi" > requirements.txt
```

### 测试1: init命令

```bash
enum-dict init --base-dir app
```

**预期结果**:
```
============================================================
[FastAPI Enum-Dict] Initialization
============================================================

[Project Root] E:\mnvr\apps\backend\test-enum-dict-demo
   [OK] 检测到FastAPI项目

[DIR] 创建目录: app/
   [OK] 目录已创建

正在生成文件...
------------------------------------------------------------
   [OK] app/api/enums.py
   [OK] app/api/dicts.py
   [OK] app/api/__init__.py
   [OK] app/models/dict_models.py
   [OK] app/models/database.py
   [OK] app/models/__init__.py
   [OK] app/schemas/enum_dict_schemas.py
   [OK] app/schemas/__init__.py
   [OK] app/core/enum_manager.py
   [OK] app/core/dict_manager.py
   [OK] app/core/detector.py
   [OK] app/core/__init__.py
   [OK] app/data/enums.py
   [OK] app/data/enum_labels.py
   [OK] app/data/enum_helper.py
   [OK] app/data/__init__.py
   [OK] app/templates/enum_class.py.j2
   [OK] app/templates/enum_labels.py.j2
   [OK] app/templates/enum_metadata.py.j2
   [OK] app/templates/helper_function.py.j2
   [OK] migrations/init_dict_tables.py
   [OK] .enum-dict.yaml

------------------------------------------------------------
[OK] 生成: 21 个文件
```

**验证文件**:
```bash
ls app/
# 应该看到: api, core, data, models, schemas, templates

ls migrations/
# 应该看到: init_dict_tables.py

cat .enum-dict.yaml
# 应该看到配置内容
```

### 测试2: create命令（第一个Enum）

```bash
enum-dict create OrderStatus Pending Paid Shipped Completed Cancelled
```

**预期结果**:
```
[CREATE] 名称: OrderStatus
值: ['Pending', 'Paid', 'Shipped', 'Completed', 'Cancelled']
类型: enum

[OK] Successfully created Orderstatus
   类名: Orderstatus
```

**验证生成的代码**:
```bash
# 查看Enum类
cat app/data/enums.py
```

**应该看到**:
```python
class Orderstatus(IntEnum):
    """Pending等（整数编码）"""
    PENDING = 0  # Pending
    PAID = 1  # Paid
    SHIPPED = 2  # Shipped
    COMPLETED = 3  # Completed
    CANCELLED = 4  # Cancelled
```

**查看标签映射**:
```bash
cat app/data/enum_labels.py
```

**应该看到**:
```python
ENUM_LABELS: Dict[str, Dict[int, str]] = {
    "Orderstatus": {
        0: "Pending",
        1: "Paid",
        2: "Shipped",
        3: "Completed",
        4: "Cancelled",
    }
}

ENUM_METADATA: Dict[str, Dict[str, Any]] = {
    "Orderstatus": {
        "description": "OrderStatus",
        "type": "enum",
        "db_type": "tinyint",
        "values": [
            {"name": "PENDING", "value": 0, "label": "Pending"},
            ...
        ]
    }
}
```

### 测试3: create命令（第二个Enum）

```bash
enum-dict create UserStatus Active Inactive Suspended
```

**预期结果**:
```
[CREATE] 名称: UserStatus
值: ['Active', 'Inactive', 'Suspended']
类型: enum

[OK] Successfully created Userstatus
   类名: Userstatus
```

**验证追加逻辑**:
```bash
cat app/data/enums.py
```

**应该看到两个类**:
```python
class Orderstatus(IntEnum):
    ...

class Userstatus(IntEnum):
    """Active等（整数编码）"""
    ACTIVE = 0  # Active
    INACTIVE = 1  # Inactive
    SUSPENDED = 2  # Suspended
```

**验证标签文件**:
```bash
cat app/data/enum_labels.py | grep -A 5 "Userstatus"
```

**应该看到正确的逗号分隔**:
```python
ENUM_LABELS = {
    "Orderstatus": {...},  # 第一个有逗号
    "Userstatus": {...}    # 最后一个没有逗号
}
```

### 测试4: list命令

```bash
enum-dict list
```

**预期结果**:
```
[LIST] 列表

【Enum】
  - Orderstatus - OrderStatus (5项)
  - Userstatus - UserStatus (3项)

【Dict】
  (未找到Dict)
```

**带搜索测试**:
```bash
enum-dict list --search Status
```

**应该同时显示两个Enum**

```bash
enum-dict list --search Order
```

**应该只显示OrderStatus**

### 测试5: show命令

```bash
enum-dict show Orderstatus
```

**预期结果**:
```
【Enum】 Orderstatus
描述: OrderStatus
类型: enum
数据库类型: tinyint

值:
  PENDING (0) = Pending
  PAID (1) = Paid
  SHIPPED (2) = Shipped
  COMPLETED (3) = Completed
  CANCELLED (4) = Cancelled
```

```bash
enum-dict show Userstatus
```

**应该显示UserStatus的详细信息**

### 测试6: Python导入测试

创建测试脚本:
```bash
cat > test_imports.py << 'EOF'
import sys
sys.path.insert(0, '.')

# 测试1: 导入Enum类
from app.data.enums import Orderstatus, Userstatus
print("[OK] 导入Enum类成功")

# 测试2: 使用Enum
status = Orderstatus.PENDING
print(f"[OK] Enum值: {status} = {status.value}")

# 测试3: 导入标签函数
from app.data.enum_labels import get_enum_label, ENUM_METADATA
label = get_enum_label("Orderstatus", status.value)
print(f"[OK] 标签: {label}")

# 测试4: 导入管理器
from app.core.enum_manager import EnumManager
from app.core.dict_manager import DictManager
from app.core.detector import detect_type
print("[OK] 导入管理器成功")

# 测试5: 类型检测
result = detect_type("TestEnum", ["A", "B", "C"])
print(f"[OK] 类型检测: {result}")

# 测试6: 元数据
meta = ENUM_METADATA.get("Orderstatus")
print(f"[OK] 元数据: {meta['description']}, {len(meta['values'])}个值")

print("\n✅ 所有导入测试通过！")
EOF

python test_imports.py
```

**预期输出**:
```
[OK] 导入Enum类成功
[OK] Enum值: Orderstatus.PENDING = 0
[OK] 标签: Pending
[OK] 导入管理器成功
[OK] 类型检测: enum
[OK] 元数据: OrderStatus, 5个值

✅ 所有导入测试通过！
```

### 测试7: FastAPI集成测试

**更新main.py**:
```python
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from app.api import enums, dicts

app = FastAPI(title="Enum-Dict Test")

# 注册路由
app.include_router(enums.router, prefix="/api/enums", tags=["Enum"])
app.include_router(dicts.router, prefix="/api/dicts", tags=["Dict"])

@app.get("/")
def root():
    return {"message": "Enum-Dict Test API"}

@app.get("/test-enum")
def test_enum():
    from app.data.enums import Orderstatus
    from app.data.enum_labels import get_enum_label
    
    status = Orderstatus.PAID
    return {
        "value": status.value,
        "name": status.name,
        "label": get_enum_label("Orderstatus", status.value)
    }
EOF
```

**启动服务**:
```bash
pip install uvicorn
uvicorn app.main:app --reload
```

**测试API** (在新终端):
```bash
# 测试根路径
curl http://localhost:8000/
# {"message":"Enum-Dict Test API"}

# 测试Enum使用
curl http://localhost:8000/test-enum
# {"value":1,"name":"PAID","label":"Paid"}

# 测试Enum列表API
curl http://localhost:8000/api/enums/
# [...Enum列表...]

# 测试Enum详情API
curl http://localhost:8000/api/enums/Orderstatus
# {...详细信息...}

# 查看OpenAPI文档
# 浏览器打开: http://localhost:8000/docs
```

**预期**: 所有API返回正确的JSON数据

---

## 🧪 高级测试

### 测试8: 多次create测试

```bash
enum-dict create Gender Male Female Other
enum-dict create Priority Low Medium High Urgent
enum-dict create Color Red Green Blue Yellow

enum-dict list
```

**预期**: 应该看到5个Enum，所有都正确生成

### 测试9: 错误处理测试

```bash
# 测试重复创建
enum-dict create OrderStatus Test
# 应该报错：已存在

# 测试不存在的Enum
enum-dict show NonExistent
# 应该报错：未找到
```

### 测试10: 配置文件测试

```bash
cat .enum-dict.yaml
```

**应该看到**:
```yaml
base_dir: app
db_url: sqlite:///./app.db
```

**修改配置**:
```bash
# 修改db_url
echo "base_dir: app" > .enum-dict.yaml
echo "db_url: postgresql://localhost/testdb" >> .enum-dict.yaml

# 验证命令仍然工作
enum-dict list
```

---

## 🔍 代码质量测试

### 测试11: Python语法检查

```bash
# 检查生成的文件是否有语法错误
python -m py_compile app/data/enums.py
python -m py_compile app/data/enum_labels.py
python -m py_compile app/core/enum_manager.py
python -m py_compile app/core/dict_manager.py
python -m py_compile app/api/enums.py
python -m py_compile app/api/dicts.py

echo "✅ 语法检查通过"
```

### 测试12: 导入循环检查

```bash
python -c "import app.api.enums; print('[OK] api.enums')"
python -c "import app.models.dict_models; print('[OK] models')"
python -c "import app.schemas.enum_dict_schemas; print('[OK] schemas')"
```

**预期**: 无ImportError

---

## 📊 性能测试

### 测试13: 批量创建

```bash
# 创建多个Enum测试性能
time enum-dict create Test1 A B C
time enum-dict create Test2 A B C D E
time enum-dict create Test3 A B C D E F G H I J

# 列表性能
time enum-dict list
```

**预期**: 每个操作 < 1秒

---

## ✅ 测试检查清单

完成所有测试后，检查：

- [ ] 安装成功
- [ ] `enum-dict --help` 显示帮助
- [ ] `init` 命令生成21个文件
- [ ] 第一次 `create` 成功
- [ ] 第二次 `create` 成功（测试追加）
- [ ] `list` 显示所有Enum
- [ ] `show` 显示详细信息
- [ ] Python可以导入所有模块
- [ ] Enum类可以正常使用
- [ ] 标签函数返回正确结果
- [ ] FastAPI服务启动成功
- [ ] API端点返回正确数据
- [ ] OpenAPI文档可访问
- [ ] 无Python语法错误
- [ ] 无导入循环错误

---

## 🐛 常见问题排查

### 问题1: ModuleNotFoundError

```bash
# 错误: No module named 'app'
# 原因: 不在项目根目录
# 解决: 
cd test-enum-dict-demo  # 确保在项目根目录
python test_imports.py
```

### 问题2: Jinja2错误

```bash
# 错误: TemplateSyntaxError
# 原因: 模板文件问题
# 解决: 重新安装
cd E:\mnvr\apps\backend\fastapi-enum-dict
pip install -e . --force-reinstall
```

### 问题3: 编码错误

```bash
# 错误: UnicodeEncodeError
# 原因: PowerShell编码
# 解决: 已修复，不应该再出现
# 如果仍有问题，使用 Git Bash 或 WSL
```

### 问题4: 数据库初始化失败

```bash
# 如果使用Dict功能，需要先初始化数据库
cd test-enum-dict-demo
python migrations/init_dict_tables.py
```

---

## 📝 自动化测试脚本

创建完整的测试脚本:

```bash
cat > run_all_tests.sh << 'EOF'
#!/bin/bash
set -e

echo "=========================================="
echo "FastAPI Enum-Dict 完整测试"
echo "=========================================="

# 清理
echo "[1/10] 清理旧环境..."
cd E:\mnvr\apps\backend
rm -rf test-enum-dict-demo
mkdir test-enum-dict-demo
cd test-enum-dict-demo

# 创建项目
echo "[2/10] 创建测试项目..."
mkdir app
echo "from fastapi import FastAPI; app = FastAPI()" > app/main.py

# 初始化
echo "[3/10] 测试 init 命令..."
enum-dict init --base-dir app > /dev/null
echo "✅ Init成功"

# 创建第一个Enum
echo "[4/10] 测试 create 命令（第一次）..."
enum-dict create OrderStatus Pending Paid Shipped > /dev/null
echo "✅ Create #1成功"

# 创建第二个Enum
echo "[5/10] 测试 create 命令（第二次）..."
enum-dict create UserStatus Active Inactive > /dev/null
echo "✅ Create #2成功"

# 列表
echo "[6/10] 测试 list 命令..."
enum-dict list > /dev/null
echo "✅ List成功"

# 显示
echo "[7/10] 测试 show 命令..."
enum-dict show Orderstatus > /dev/null
echo "✅ Show成功"

# Python导入
echo "[8/10] 测试 Python 导入..."
python -c "from app.data.enums import Orderstatus; from app.data.enum_labels import get_enum_label"
echo "✅ Import成功"

# 语法检查
echo "[9/10] 测试语法..."
python -m py_compile app/data/enums.py
python -m py_compile app/data/enum_labels.py
echo "✅ 语法检查成功"

# 完成
echo "[10/10] 清理..."
cd ..
# rm -rf test-enum-dict-demo

echo ""
echo "=========================================="
echo "✅ 所有测试通过！"
echo "=========================================="
EOF

chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

## 🎯 快速验证命令

只想快速验证是否工作：

```bash
# 一键测试（在fastapi-enum-dict目录）
cd E:\mnvr\apps\backend\test-fastapi-project
enum-dict list
enum-dict show Orderstatus
```

如果能看到输出，说明一切正常！✅

---

## 📞 获取帮助

如果测试失败：

1. 检查是否在正确的目录
2. 检查Python版本（需要3.8+）
3. 重新安装包：`pip install -e . --force-reinstall`
4. 查看错误日志
5. 参考文档：`README.md`, `INSTALL.md`

**祝测试顺利！** 🚀
