# FastAPI Enum-Dict - 快速参考

**一页纸速查手册**

---

## 🚀 安装

```bash
cd E:\mnvr\apps\backend\fastapi-enum-dict
pip install -e .
```

---

## 📝 命令速查

### 初始化
```bash
python -m fastapi_enum_dict.cli init [--base-dir app] [--db-url sqlite:///./app.db]
```

### 创建Enum
```bash
python -m fastapi_enum_dict.cli create <name> <value1> <value2> ...

# 示例
python -m fastapi_enum_dict.cli create OrderStatus Pending Paid Shipped
python -m fastapi_enum_dict.cli create Gender Male Female Other
```

### 创建Dict
```bash
python -m fastapi_enum_dict.cli create <name> --type dict <value1> <value2> ...

# 示例  
python -m fastapi_enum_dict.cli create Department --type dict RD QA OPS
python -m fastapi_enum_dict.cli create Team --type dict TeamA TeamB
```

### 列表
```bash
python -m fastapi_enum_dict.cli list [--search <keyword>] [--type enum|dict]

# 示例
python -m fastapi_enum_dict.cli list                    # 所有
python -m fastapi_enum_dict.cli list --search Status   # 搜索
python -m fastapi_enum_dict.cli list --type dict       # 只显示Dict
```

### 显示详情
```bash
python -m fastapi_enum_dict.cli show <name>

# 示例
python -m fastapi_enum_dict.cli show OrderStatus
python -m fastapi_enum_dict.cli show department
```

### 更新（Dict）
```bash
python -m fastapi_enum_dict.cli update <name> add <value>

# 示例
python -m fastapi_enum_dict.cli update department add HR
```

### 删除
```bash
echo y | python -m fastapi_enum_dict.cli delete <name>

# 示例
echo y | python -m fastapi_enum_dict.cli delete team
```

---

## 💻 Python使用

### 导入Enum
```python
from app.data.enums import Orderstatus
from app.data.enum_labels import get_enum_label, ENUM_METADATA

# 使用
status = Orderstatus.PAID
print(status.value)  # 1
print(status.name)   # PAID

# 获取标签
label = get_enum_label("Orderstatus", status.value)
print(label)  # Paid

# 元数据
meta = ENUM_METADATA["Orderstatus"]
print(meta["description"])  # OrderStatus
```

### 使用Dict
```python
from app.core.dict_manager import DictManager
from app.models.database import get_db

db = next(get_db())
manager = DictManager(db)

# 列表
dicts = manager.list()

# 详情
dept = manager.show("department")
print(dept["values"])  # [{id, label, value, ...}, ...]
```

---

## 📁 生成的文件

```
app/
├── api/
│   ├── enums.py      # Enum API路由
│   └── dicts.py      # Dict API路由
├── core/
│   ├── enum_manager.py   # Enum管理器
│   ├── dict_manager.py   # Dict管理器
│   └── detector.py       # 类型检测
├── data/
│   ├── enums.py          # ← Enum类定义
│   ├── enum_labels.py    # ← 标签和元数据
│   └── enum_helper.py    # 辅助函数
├── models/
│   ├── dict_models.py    # DictType/DictData
│   └── database.py       # 数据库连接
└── schemas/
    └── enum_dict_schemas.py  # Pydantic

migrations/
└── init_dict_tables.py   # 数据库初始化

.enum-dict.yaml   # 配置文件
```

---

## 🔧 常见操作

### 初始化数据库（Dict功能）
```bash
python migrations/init_dict_tables.py
```

### 集成到FastAPI
```python
# app/main.py
from fastapi import FastAPI
from app.api import enums, dicts

app = FastAPI()

app.include_router(enums.router, prefix="/api/enums", tags=["Enum"])
app.include_router(dicts.router, prefix="/api/dicts", tags=["Dict"])
```

### 在SQLAlchemy模型中使用
```python
from app.data.enums import Orderstatus

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    status = Column(Integer)  # 存储为整数
    
# 使用
order = Order(status=Orderstatus.PENDING)
```

---

## 🎯 测试命令

```bash
# 完整测试流程
cd test-project
mkdir app && echo "from fastapi import FastAPI; app = FastAPI()" > app/main.py
python -m fastapi_enum_dict.cli init --base-dir app
python -m fastapi_enum_dict.cli create OrderStatus Pending Paid
python -m fastapi_enum_dict.cli list
python -m fastapi_enum_dict.cli show Orderstatus

# 验证导入
python -c "import sys; sys.path.insert(0, '.'); from app.data.enums import Orderstatus; print('OK')"
```

---

## 📚 文档链接

- **安装**: `INSTALL.md`
- **完整文档**: `README.md`
- **测试指南**: `TESTING_GUIDE.md`
- **快速测试**: `如何测试.md`
- **Enum测试**: `TEST_RESULTS.md`
- **Dict测试**: `DICT_TEST_RESULTS.md`
- **综合总结**: `COMPLETE_TEST_SUMMARY.md`

---

## ❓ 常见问题

**Q: 找不到enum-dict命令？**  
A: 使用 `python -m fastapi_enum_dict.cli` 代替

**Q: 如何选择Enum还是Dict？**  
A: 编译时确定→Enum，运行时动态→Dict

**Q: 中文显示乱码？**  
A: PowerShell编码问题，不影响功能

**Q: 数据库文件在哪？**  
A: 项目根目录 `app.db`（SQLite）

---

## 🎓 最佳实践

1. **命名规范**: 使用PascalCase或英文单词
2. **值的选择**: 简洁明了的英文
3. **Enum vs Dict**: 
   - 订单状态、角色 → Enum
   - 部门、地区 → Dict
4. **版本控制**: Enum代码提交Git，Dict数据备份
5. **测试**: 每次修改后运行 `list` 验证

---

## ⚡ 快捷键（推荐）

在PowerShell中设置别名（可选）:
```powershell
Set-Alias ed "python -m fastapi_enum_dict.cli"

# 使用
ed init
ed create OrderStatus Pending Paid
ed list
ed show OrderStatus
```

---

**快速参考卡 v1.0.0**  
**更多信息**: 查看完整文档

**状态**: ✅ PRODUCTION READY
