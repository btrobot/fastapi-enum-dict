# Contributing to FastAPI Enum-Dict

感谢您考虑为 FastAPI Enum-Dict 做出贡献！

## 🤝 如何贡献

### 报告Bug

如果您发现bug，请创建issue并包含：
- 详细的bug描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（Python版本、OS等）

### 提出新功能

如果您有新功能建议：
- 先创建issue讨论
- 说明功能的用途和价值
- 提供使用示例

### 提交代码

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- 遵循PEP 8
- 添加类型提示
- 编写测试
- 更新文档

### 运行测试

```bash
# 安装测试依赖
pip install -r requirements-test.txt

# 运行测试
pytest tests/ -v

# 生成覆盖率报告
pytest --cov=fastapi_enum_dict --cov-report=html
```

### 提交信息规范

使用清晰的提交信息：
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `test: 添加测试`
- `refactor: 重构代码`

## 📄 许可证

贡献的代码将遵循MIT许可证。
