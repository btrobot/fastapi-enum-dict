# FastAPI Enum-Dict 增强计划

**日期**: 2026-01-03  
**版本**: v1.1.0  
**目标**: 添加企业级功能（导入导出、批量操作等）

---

## 🎯 需要添加的功能

### 1. 导入导出功能

#### 1.1 导出CSV
```python
@router.get("/{type_code}/export")
def export_dict_data(type_code: str) -> StreamingResponse:
    """导出字典数据为CSV"""
    # 生成CSV文件
    # 返回下载流
```

#### 1.2 导入CSV
```python
@router.post("/{type_code}/import")
async def import_dict_data(type_code: str, file: UploadFile):
    """从CSV导入字典数据"""
    # 解析CSV
    # 批量插入
    # 返回导入结果
```

#### 1.3 导出Excel (可选)
```python
@router.get("/{type_code}/export/excel")
def export_excel(type_code: str) -> StreamingResponse:
    """导出为Excel"""
    # 需要 openpyxl 依赖
```

### 2. 批量操作

#### 2.1 批量删除
```python
@router.delete("/batch")
def batch_delete(ids: List[int]):
    """批量删除字典数据"""
```

#### 2.2 批量启用/禁用
```python
@router.put("/batch/toggle")
def batch_toggle_status(ids: List[int], is_active: bool):
    """批量启用或禁用"""
```

### 3. 模型字段扩展

#### 3.1 DictType增强字段
```python
class DictType:
    # 新增字段
    is_system: bool  # 系统预置（不可删除）
    allow_add: bool  # 允许新增
    allow_delete: bool  # 允许删除
    created_by: int  # 创建人
    updated_by: int  # 更新人
```

#### 3.2 DictData增强字段
```python
class DictData:
    # 新增字段
    parent_code: str  # 父级编码（支持层级）
    css_class: str  # CSS类名
    is_default: bool  # 是否默认值
    remark: str  # 备注
    created_by: int  # 创建人
    updated_by: int  # 更新人
```

### 4. 引用检查

#### 4.1 删除前检查
```python
@router.get("/{type_code}/check-references")
def check_references(type_code: str):
    """检查是否被引用"""
    # 扫描数据库中的引用
    # 返回引用列表
```

### 5. Schema扩展

#### 5.1 ImportResult
```python
class ImportResult(BaseModel):
    total: int  # 总数
    success: int  # 成功
    failed: int  # 失败
    errors: List[str]  # 错误信息
```

#### 5.2 BatchOperationResult
```python
class BatchOperationResult(BaseModel):
    total: int
    success: int
    failed: int
    failed_ids: List[int]
```

---

## 📋 实施步骤

### Phase 1: 模型扩展 (高优先级)
1. [ ] 更新 `models/dict_models.py.j2` 模板
   - 添加 is_system, allow_add, allow_delete 字段
   - 添加 created_by, updated_by 字段
   - 添加 parent_code, css_class, is_default 字段

2. [ ] 更新数据库迁移
   - 创建新的迁移脚本
   - 支持字段升级

### Phase 2: Schema扩展 (高优先级)
1. [ ] 更新 `schemas/enum_dict_schemas.py.j2`
   - 添加 ImportResult
   - 添加 BatchOperationResult
   - 扩展 DictDataCreate/Update

### Phase 3: 导入导出 (中优先级)
1. [ ] 添加导出功能
   - CSV导出
   - 模板文件：`api_dicts.py.j2`
   
2. [ ] 添加导入功能
   - CSV导入
   - 错误处理
   - 验证逻辑

### Phase 4: 批量操作 (中优先级)
1. [ ] 批量删除
2. [ ] 批量启用/禁用
3. [ ] 批量更新

### Phase 5: 引用检查 (低优先级)
1. [ ] 实现引用扫描
2. [ ] 删除保护

---

## 🔧 技术决策

### 依赖项
```toml
[project.dependencies]
click>=8.0.0
jinja2>=3.0.0
pyyaml>=6.0
sqlalchemy>=2.0.0

[project.optional-dependencies]
excel = ["openpyxl>=3.0.0"]  # Excel支持
```

### API路径设计
```
POST   /api/dicts                    # 创建
GET    /api/dicts                    # 列表
GET    /api/dicts/{code}             # 详情
PUT    /api/dicts/{code}             # 更新
DELETE /api/dicts/{code}             # 删除

# 新增
GET    /api/dicts/{code}/export      # 导出CSV
POST   /api/dicts/{code}/import      # 导入CSV
DELETE /api/dicts/batch              # 批量删除
PUT    /api/dicts/batch/toggle       # 批量启用/禁用
GET    /api/dicts/{code}/references  # 引用检查
```

---

## 📝 需要修改的文件

1. **模板文件**
   - `templates/models_dict.py.j2` ✏️
   - `templates/schemas_enum_dict.py.j2` ✏️
   - `templates/api_dicts.py.j2` ✏️
   - `templates/migration_init.py.j2` ✏️

2. **核心文件**
   - `core/dict_manager.py` (可能需要扩展)

3. **文档文件**
   - `README.md`
   - `CHANGELOG.md`
   - `docs/QUICK_START.md`

---

## ⚠️ 向后兼容性

### 数据库迁移
- 新字段设置默认值
- 保持旧字段不变
- 提供升级脚本

### API兼容
- 新端点不影响旧端点
- 保持现有响应格式
- 新字段optional

---

## 🎯 版本规划

### v1.1.0 (当前计划)
- [x] 模型字段扩展
- [x] 导入导出CSV
- [x] 批量操作

### v1.2.0 (未来)
- [ ] Excel支持
- [ ] 引用检查
- [ ] 权限控制集成

---

## 📊 优先级排序

**P0 (必须)**: 
1. 模型字段扩展 - 支持企业级功能
2. CSV导入导出 - 数据迁移必须

**P1 (重要)**:
3. 批量操作 - 提升效率
4. Schema完善 - API响应标准化

**P2 (可选)**:
5. Excel支持 - 用户友好
6. 引用检查 - 数据完整性

---

**计划状态**: 📝 待实施  
**预计时间**: 2-3小时  
**目标版本**: v1.1.0

---

*让fastapi-enum-dict成为企业级的enum/dict管理解决方案！*
