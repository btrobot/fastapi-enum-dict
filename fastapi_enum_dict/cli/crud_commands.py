"""
CRUD命令实现
"""
import click
from pathlib import Path
import yaml
import sys


def create_item(name: str, values: list, enum_type: str = None):
    """创建Enum或Dict"""
    click.echo(f"\n[CREATE] 创建: {name}")
    click.echo(f"值: {values}")
    
    # 1. 加载配置
    config = _load_config()
    if not config:
        click.echo("[ERROR] 未找到配置文件 .enum-dict.yaml")
        click.echo("   请先运行: enum-dict init")
        sys.exit(1)
    
    # 2. 添加项目路径到sys.path
    project_root = Path.cwd()
    sys.path.insert(0, str(project_root))
    
    # 3. 动态导入
    base_dir = config['base_dir']
    
    try:
        # 导入检测器
        detector_module = __import__(f'{base_dir}.core.detector', fromlist=['detect_type'])
        detect_type = detector_module.detect_type
        
        # 检测类型
        detected_type = detect_type(name, values, enum_type)
        click.echo(f"类型: {detected_type}\n")
        
        if detected_type == 'enum':
            _create_enum(config, name, values)
        else:
            _create_dict(config, name, values)
            
    except ImportError as e:
        click.echo(f"[ERROR] 导入失败: {e}")
        click.echo(f"   请确保已在 {base_dir}/ 目录中运行 enum-dict init")
        sys.exit(1)
    except Exception as e:
        click.echo(f"[ERROR] 执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _create_enum(config: dict, name: str, values: list):
    """创建Enum（文件操作）"""
    base_dir = config['base_dir']
    
    # 导入EnumManager
    manager_module = __import__(f'{base_dir}.core.enum_manager', fromlist=['EnumManager'])
    EnumManager = manager_module.EnumManager
    
    # 创建管理器
    manager = EnumManager(
        enums_file=config['enum']['enums_file'],
        labels_file=config['enum']['labels_file'],
        helper_file=config['enum']['helper_file'],
        templates_dir=f"{base_dir}/templates"
    )
    
    # 执行创建
    result = manager.create(name, values)
    
    if result.get('success'):
        click.echo(f"[OK] {result.get('message', '创建成功')}")
        click.echo(f"   类名: {result.get('class_name', 'N/A')}")
    else:
        click.echo(f"[ERROR] {result.get('message', '创建失败')}")
        sys.exit(1)


def _create_dict(config: dict, name: str, values: list):
    """创建Dict（数据库操作）"""
    base_dir = config['base_dir']
    
    # 导入DictManager和数据库
    database_module = __import__(f'{base_dir}.models.database', fromlist=['get_db'])
    get_db = database_module.get_db
    
    manager_module = __import__(f'{base_dir}.core.dict_manager', fromlist=['DictManager'])
    DictManager = manager_module.DictManager
    
    # 获取数据库session
    db = next(get_db())
    
    # 创建管理器
    manager = DictManager(db)
    
    # 转换为dict_code
    dict_code = _to_snake_case(name)
    
    # 执行创建
    result = manager.create(
        dict_code=dict_code,
        dict_name=name,
        values=values
    )
    
    if result.get('success'):
        click.echo(f"[OK] {result.get('message', '创建成功')}")
        click.echo(f"   字典编码: {result.get('dict_code', 'N/A')}")
    else:
        click.echo(f"[ERROR] {result.get('message', '创建失败')}")
        sys.exit(1)


def list_all(search: str = None, item_type: str = None):
    """列出所有Enum和Dict"""
    config = _load_config()
    if not config:
        click.echo("[ERROR] 未找到配置文件")
        sys.exit(1)
    
    project_root = Path.cwd()
    sys.path.insert(0, str(project_root))
    base_dir = config['base_dir']
    
    click.echo(f"\n[LIST] 列表")
    if search:
        click.echo(f"搜索: {search}")
    if item_type:
        click.echo(f"类型: {item_type}")
    click.echo()
    
    try:
        # 列出Enums
        if not item_type or item_type == 'enum':
            _list_enums(base_dir, search)
        
        # 列出Dicts
        if not item_type or item_type == 'dict':
            _list_dicts(config, search)
            
    except Exception as e:
        click.echo(f"[ERROR] 列表失败: {e}")
        sys.exit(1)


def _list_enums(base_dir: str, search: str = None):
    """列出Enums"""
    try:
        labels_module = __import__(f'{base_dir}.data.enum_labels', fromlist=['ENUM_METADATA'])
        ENUM_METADATA = labels_module.ENUM_METADATA
        
        click.echo("【Enum】")
        count = 0
        for name, meta in ENUM_METADATA.items():
            if search and search not in name and search not in meta.get('description', ''):
                continue
            
            desc = meta.get('description', '')
            values_count = len(meta.get('values', []))
            click.echo(f"  - {name} - {desc} ({values_count}项)")
            count += 1
        
        if count == 0:
            click.echo("  (无)")
        click.echo()
    except Exception as e:
        click.echo(f"  (未找到Enum: {e})")
        click.echo()


def _list_dicts(config: dict, search: str = None):
    """列出Dicts"""
    try:
        base_dir = config['base_dir']
        database_module = __import__(f'{base_dir}.models.database', fromlist=['get_db'])
        get_db = database_module.get_db
        
        manager_module = __import__(f'{base_dir}.core.dict_manager', fromlist=['DictManager'])
        DictManager = manager_module.DictManager
        
        db = next(get_db())
        manager = DictManager(db)
        
        dicts = manager.list(search=search)
        
        click.echo("【Dict】")
        if dicts:
            for d in dicts:
                click.echo(f"  - {d['dict_code']} - {d['dict_name']} ({d['count']}项)")
        else:
            click.echo("  (无)")
        click.echo()
    except:
        click.echo("  (未找到Dict)")
        click.echo()


def show_item(name: str):
    """显示详情"""
    config = _load_config()
    if not config:
        click.echo("[ERROR] 未找到配置文件")
        sys.exit(1)
    
    project_root = Path.cwd()
    sys.path.insert(0, str(project_root))
    base_dir = config['base_dir']
    
    try:
        # 先尝试Enum
        labels_module = __import__(f'{base_dir}.data.enum_labels', fromlist=['ENUM_LABELS', 'ENUM_METADATA'])
        ENUM_LABELS = labels_module.ENUM_LABELS
        ENUM_METADATA = labels_module.ENUM_METADATA
        
        if name in ENUM_METADATA:
            _show_enum(name, ENUM_LABELS, ENUM_METADATA)
            return
        
        # 再尝试Dict
        dict_code = _to_snake_case(name)
        database_module = __import__(f'{base_dir}.models.database', fromlist=['get_db'])
        manager_module = __import__(f'{base_dir}.core.dict_manager', fromlist=['DictManager'])
        
        db = next(database_module.get_db())
        manager = manager_module.DictManager(db)
        
        result = manager.show(dict_code)
        if result.get('success'):
            _show_dict(result)
            return
        
        click.echo(f"[ERROR] 未找到: {name}")
        sys.exit(1)
        
    except Exception as e:
        click.echo(f"[ERROR] 显示失败: {e}")
        sys.exit(1)


def _show_enum(name: str, labels: dict, metadata: dict):
    """显示Enum详情"""
    meta = metadata[name]
    click.echo(f"\n【Enum】 {name}")
    click.echo(f"描述: {meta.get('description', '')}")
    click.echo(f"类型: {meta.get('type', '')}")
    click.echo(f"数据库类型: {meta.get('db_type', '')}")
    click.echo(f"\n值:")
    
    for v in meta.get('values', []):
        value = v['value']
        label = labels[name].get(value, '')
        click.echo(f"  {v['name']} ({value}) = {label}")
    click.echo()


def _show_dict(result: dict):
    """显示Dict详情"""
    click.echo(f"\n【Dict】 {result['dict_code']}")
    click.echo(f"名称: {result['dict_name']}")
    click.echo(f"描述: {result.get('description', '')}")
    click.echo(f"\n值:")
    
    for v in result.get('values', []):
        click.echo(f"  [{v['id']}] {v['value']} = {v['label']} (排序:{v['sort_order']})")
    click.echo()


def update_item(name: str, operation: str, args: tuple):
    """更新Enum或Dict"""
    click.echo(f"\n[UPDATE] 更新: {name}")
    click.echo(f"操作: {operation}")
    
    config = _load_config()
    if not config:
        click.echo("[ERROR] 未找到配置文件")
        sys.exit(1)
    
    # 解析参数
    kwargs = _parse_update_args(operation, args)
    
    project_root = Path.cwd()
    sys.path.insert(0, str(project_root))
    base_dir = config['base_dir']
    
    try:
        # 检查是Enum还是Dict
        labels_module = __import__(f'{base_dir}.data.enum_labels', fromlist=['ENUM_METADATA'])
        ENUM_METADATA = labels_module.ENUM_METADATA
        
        if name in ENUM_METADATA:
            _update_enum(config, name, operation, kwargs)
        else:
            _update_dict(config, name, operation, kwargs)
            
    except Exception as e:
        click.echo(f"[ERROR] 更新失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _update_enum(config: dict, name: str, operation: str, kwargs: dict):
    """更新Enum"""
    base_dir = config['base_dir']
    manager_module = __import__(f'{base_dir}.core.enum_manager', fromlist=['EnumManager'])
    EnumManager = manager_module.EnumManager
    
    manager = EnumManager(
        enums_file=config['enum']['enums_file'],
        labels_file=config['enum']['labels_file'],
        helper_file=config['enum']['helper_file'],
        templates_dir=f"{base_dir}/templates"
    )
    
    result = manager.update(name, operation, **kwargs)
    
    if result.get('success'):
        click.echo(f"[OK] {result.get('message', '更新成功')}")
    else:
        click.echo(f"[ERROR] {result.get('message', '更新失败')}")
        sys.exit(1)


def _update_dict(config: dict, name: str, operation: str, kwargs: dict):
    """更新Dict"""
    base_dir = config['base_dir']
    dict_code = _to_snake_case(name)
    
    database_module = __import__(f'{base_dir}.models.database', fromlist=['get_db'])
    manager_module = __import__(f'{base_dir}.core.dict_manager', fromlist=['DictManager'])
    
    db = next(database_module.get_db())
    manager = manager_module.DictManager(db)
    
    result = manager.update(dict_code, operation, **kwargs)
    
    if result.get('success'):
        click.echo(f"[OK] {result.get('message', '更新成功')}")
    else:
        click.echo(f"[ERROR] {result.get('message', '更新失败')}")
        sys.exit(1)


def delete_item(name: str, force: bool):
    """删除Enum或Dict"""
    if not force:
        if not click.confirm(f"确认删除 {name}?"):
            click.echo("已取消")
            return
    
    click.echo(f"\n[DELETE]  删除: {name}")
    
    config = _load_config()
    if not config:
        click.echo("[ERROR] 未找到配置文件")
        sys.exit(1)
    
    project_root = Path.cwd()
    sys.path.insert(0, str(project_root))
    base_dir = config['base_dir']
    
    try:
        # 检查类型
        labels_module = __import__(f'{base_dir}.data.enum_labels', fromlist=['ENUM_METADATA'])
        ENUM_METADATA = labels_module.ENUM_METADATA
        
        if name in ENUM_METADATA:
            _delete_enum(config, name)
        else:
            _delete_dict(config, name)
            
    except Exception as e:
        click.echo(f"[ERROR] 删除失败: {e}")
        sys.exit(1)


def _delete_enum(config: dict, name: str):
    """删除Enum"""
    base_dir = config['base_dir']
    manager_module = __import__(f'{base_dir}.core.enum_manager', fromlist=['EnumManager'])
    EnumManager = manager_module.EnumManager
    
    manager = EnumManager(
        enums_file=config['enum']['enums_file'],
        labels_file=config['enum']['labels_file'],
        helper_file=config['enum']['helper_file'],
        templates_dir=f"{base_dir}/templates"
    )
    
    result = manager.delete(name, force=True)
    
    if result.get('success'):
        click.echo(f"[OK] {result.get('message', '删除成功')}")
    else:
        click.echo(f"[ERROR] {result.get('message', '删除失败')}")
        sys.exit(1)


def _delete_dict(config: dict, name: str):
    """删除Dict"""
    base_dir = config['base_dir']
    dict_code = _to_snake_case(name)
    
    database_module = __import__(f'{base_dir}.models.database', fromlist=['get_db'])
    manager_module = __import__(f'{base_dir}.core.dict_manager', fromlist=['DictManager'])
    
    db = next(database_module.get_db())
    manager = manager_module.DictManager(db)
    
    result = manager.delete(dict_code, force=True)
    
    if result.get('success'):
        click.echo(f"[OK] {result.get('message', '删除成功')}")
    else:
        click.echo(f"[ERROR] {result.get('message', '删除失败')}")
        sys.exit(1)


# ==================== 辅助函数 ====================

def _load_config() -> dict:
    """加载配置文件"""
    config_file = Path.cwd() / '.enum-dict.yaml'
    if not config_file.exists():
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _to_snake_case(text: str) -> str:
    """转换为snake_case"""
    import re
    # 简单实现
    text = text.replace(' ', '_')
    text = text.replace('-', '_')
    return text.lower()


def _parse_update_args(operation: str, args: tuple) -> dict:
    """解析update命令参数"""
    kwargs = {}
    
    if operation == 'add':
        # add <label>
        if len(args) >= 1:
            kwargs['label'] = args[0]
    
    elif operation == 'remove':
        # remove <value>
        if len(args) >= 1:
            try:
                kwargs['value'] = int(args[0])
            except:
                kwargs['label'] = args[0]
    
    elif operation == 'rename':
        # rename <old> to <new>
        if len(args) >= 3 and args[1].lower() == 'to':
            kwargs['old_label'] = args[0]
            kwargs['new_label'] = args[2]
    
    return kwargs
