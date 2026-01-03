# FastAPI Enum-Dict - Quick Start

## 🚀 当前可用功能

### 安装（开发模式）

```bash
cd E:\mnvr\apps\backend\fastapi-enum-dict
pip install -e .
```

### 在FastAPI项目中使用

```bash
# 1. 进入你的FastAPI项目
cd your-fastapi-project

# 2. 运行init命令
enum-dict init

# 3. 按提示集成到main.py
# ... 编辑 app/main.py ...

# 4. 初始化数据库（如果使用Dict功能）
python migrations/init_dict_tables.py
```

---

## 📁 生成的文件结构

```
your-fastapi-project/
├── app/
│   ├── api/
│   │   ├── enums.py          # Enum CRUD API
│   │   ├── dicts.py          # Dict CRUD API
│   │   └── __init__.py
│   ├── models/
│   │   ├── dict_models.py    # DictType/DictData
│   │   ├── database.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── enum_dict_schemas.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── enum_manager.py
│   │   ├── dict_manager.py
│   │   ├── detector.py
│   │   └── __init__.py
│   ├── data/
│   │   ├── enums.py          # Enum定义
│   │   ├── enum_labels.py    # 标签映射
│   │   ├── enum_helper.py
│   │   └── __init__.py
│   └── templates/
│       └── ... (Jinja2模板)
├── migrations/
│   └── init_dict_tables.py
└── .enum-dict.yaml            # 配置文件
```

---

## 🛠️ CLI命令

```bash
# 帮助
enum-dict --help

# 初始化
enum-dict init
enum-dict init --base-dir app --db-url sqlite:///./app.db

# 创建（待模板完成后可用）
enum-dict create OrderStatus Pending Paid Shipped
enum-dict create --type dict Department RD QA OPS

# 列表
enum-dict list
enum-dict list --type enum
enum-dict list --search status

# 显示
enum-dict show OrderStatus

# 更新
enum-dict update OrderStatus add Completed
enum-dict update OrderStatus remove 1
enum-dict update OrderStatus rename Pending to Waiting

# 删除
enum-dict delete OrderStatus
enum-dict delete OrderStatus --force
```

---

## 📝 集成到main.py

```python
# app/main.py
from fastapi import FastAPI
from app.api import enums, dicts

app = FastAPI()

# 注册路由
app.include_router(
    enums.router,
    prefix="/api/enums",
    tags=["Enum"]
)

app.include_router(
    dicts.router,
    prefix="/api/dicts",
    tags=["Dict"]
)
```

---

## 🔍 测试

```bash
# 1. 测试init命令
cd test-fastapi-project
enum-dict init
# 查看生成的文件

# 2. 启动FastAPI
uvicorn app.main:app --reload

# 3. 访问API文档
open http://localhost:8000/docs
```

---

## ⚠️ 当前限制

1. **模板内容**: 大部分模板文件是占位符，需要填充实际内容
2. **CRUD命令**: 框架已完成，但依赖模板内容
3. **Dict功能**: 需要完整的数据库模型模板

---

## 🎯 下一步

填充核心模板文件（预计2小时）:
1. `core_enum_manager.py.j2`
2. `core_dict_manager.py.j2`
3. `models_dict.py.j2`
4. `api_enums.py.j2`
5. `api_dicts.py.j2`

---

## 📞 支持

- GitHub: https://github.com/mnvr/fastapi-enum-dict
- Issues: https://github.com/mnvr/fastapi-enum-dict/issues
- Docs: [README.md](README.md)
