# FastAPI Enum-Dict

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/mnvr/fastapi-enum-dict)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

一个强大的FastAPI扩展包，为你的项目自动添加Enum和Dict管理功能。

[English](README_EN.md) | 简体中文

## 🎯 特性

- ✅ **一键安装** - `pip install fastapi-enum-dict`
- ✅ **自动生成** - 自动生成所有必需的API、模型、Schema文件
- ✅ **双重存储** - Enum存储在文件（编译时），Dict存储在数据库（运行时）
- ✅ **完整CRUD** - 提供完整的REST API和CLI命令
- ✅ **遵循约定** - 完全遵循FastAPI项目结构规范
- ✅ **类型安全** - 完整的Pydantic Schema支持

## 🚀 快速开始

### 安装

```bash
pip install fastapi-enum-dict
```

### 初始化到FastAPI项目

```bash
cd your-fastapi-project
enum-dict init
```

这将自动生成：

```
your-fastapi-project/
├── app/
│   ├── api/
│   │   ├── enums.py          # Enum CRUD API
│   │   └── dicts.py          # Dict CRUD API
│   ├── models/
│   │   ├── dict_models.py    # Dict数据库模型
│   │   └── database.py       # 数据库连接
│   ├── schemas/
│   │   └── enum_dict_schemas.py  # Pydantic Schemas
│   ├── core/
│   │   ├── enum_manager.py   # Enum管理器
│   │   ├── dict_manager.py   # Dict管理器
│   │   └── detector.py       # 类型检测器
│   ├── data/
│   │   ├── enums.py          # Enum定义文件
│   │   ├── enum_labels.py    # 标签映射
│   │   └── enum_helper.py    # 辅助函数
│   └── templates/
│       └── ...               # Jinja2模板
├── migrations/
│   └── init_dict_tables.py   # 数据库初始化脚本
└── .enum-dict.yaml           # 配置文件
```

### 集成到main.py

```python
from fastapi import FastAPI
from app.api import enums, dicts

app = FastAPI()

# 注册路由
app.include_router(enums.router, prefix="/api/enums", tags=["Enum管理"])
app.include_router(dicts.router, prefix="/api/dicts", tags=["Dict管理"])
```

### 初始化数据库

```bash
python migrations/init_dict_tables.py
```

### 使用CLI命令

```bash
# 创建Enum（自动检测类型）
enum-dict create 订单状态 待付款 已付款 已发货

# 创建Dict（>10个值自动识别为Dict）
enum-dict create 部门 研发部 测试部 产品部 运维部 设计部

# 列出所有
enum-dict list

# 查看详情
enum-dict show 订单状态

# 更新
enum-dict update 订单状态 add 已完成

# 删除
enum-dict delete 订单状态 --force
```

## 📖 API使用

启动FastAPI后，访问 http://localhost:8000/docs 查看自动生成的API文档。

### Enum API

- `POST /api/enums` - 创建Enum
- `GET /api/enums` - 列出所有Enum
- `GET /api/enums/{name}` - 获取Enum详情
- `PUT /api/enums/{name}` - 更新Enum
- `DELETE /api/enums/{name}` - 删除Enum

### Dict API

- `POST /api/dicts` - 创建Dict
- `GET /api/dicts` - 列出所有Dict
- `GET /api/dicts/{code}` - 获取Dict详情
- `PUT /api/dicts/{code}` - 更新Dict
- `DELETE /api/dicts/{code}` - 删除Dict

## 🔧 配置

编辑 `.enum-dict.yaml` 自定义配置：

```yaml
base_dir: app
database_url: sqlite:///./app.db

enum:
  enums_file: app/data/enums.py
  labels_file: app/data/enum_labels.py
  helper_file: app/data/enum_helper.py

dict:
  types_table: dict_types
  data_table: dict_data
```

## 💡 Enum vs Dict

| 特性 | Enum | Dict |
|------|------|------|
| 存储 | 文件 | 数据库 |
| 值数量 | 少（<10） | 多（>10） |
| 变化频率 | 低（固定） | 高（动态） |
| 访问方式 | import | SQL查询 |
| 版本控制 | Git | 数据库备份 |
| 适用场景 | 性别、状态 | 部门、地区 |

## 📖 文档

- 📘 [安装指南](docs/INSTALL.md)
- 🚀 [快速开始](docs/QUICK_START.md)
- 📋 [快速参考](docs/QUICK_REFERENCE.md)
- 🧪 [测试指南](docs/TESTING_GUIDE.md)
- 💡 [使用示例](examples/)
- 📝 [更新日志](CHANGELOG.md)
- 🤝 [贡献指南](CONTRIBUTING.md)

## 📝 License

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤝 Contributing

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与贡献。
