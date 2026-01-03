"""
init命令实现 - 初始化Enum-Dict到FastAPI项目
"""
import click
from pathlib import Path
from jinja2 import Environment, PackageLoader
import yaml


def init_project(base_dir: str, db_url: str, force: bool):
    """
    初始化Enum-Dict功能到FastAPI项目
    
    Args:
        base_dir: 基础目录（如 app）
        db_url: 数据库URL
        force: 是否强制覆盖
    """
    click.echo("\n" + "="*60)
    click.echo("[FastAPI Enum-Dict] Initialization")
    click.echo("="*60 + "\n")
    
    # 1. 检测项目根目录
    project_root = Path.cwd()
    click.echo(f"[Project Root] {project_root}")
    
    # 检测是否是FastAPI项目
    if not _is_fastapi_project(project_root):
        click.echo("[WARN]  未检测到FastAPI项目（找不到main.py或requirements.txt中的fastapi）")
        if not click.confirm("   是否继续？", default=True):
            click.echo("\n[ERROR] 已取消\n")
            return
    else:
        click.echo("   [OK] 检测到FastAPI项目")
    
    # 2. 确认基础目录
    base_path = project_root / base_dir
    click.echo(f"\n[DIR] 基础目录: {base_dir}/")
    
    if not base_path.exists():
        click.echo(f"   创建目录: {base_path}")
        base_path.mkdir(parents=True, exist_ok=True)
    else:
        click.echo(f"   [OK] 目录已存在")
    
    # 3. 生成文件
    click.echo("\n正在生成文件...")
    click.echo("-" * 60)
    
    env = Environment(
        loader=PackageLoader('fastapi_enum_dict', 'templates'),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    files_to_create = _get_files_to_create(base_dir)
    created_count = 0
    skipped_count = 0
    
    for display_name, file_path, template_name in files_to_create:
        full_path = project_root / file_path
        
        # 检查文件是否存在
        if full_path.exists() and not force:
            click.echo(f"   [SKIP]  {file_path} (已存在)")
            skipped_count += 1
            continue
        
        # 创建目录
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 渲染模板
        try:
            template = env.get_template(template_name)
            content = template.render(
                base_dir=base_dir,
                db_url=db_url
            )
            
            # 写入文件
            full_path.write_text(content, encoding='utf-8')
            click.echo(f"   [OK] {file_path}")
            created_count += 1
        except Exception as e:
            click.echo(f"   [ERROR] {file_path} - 错误: {e}")
    
    # 4. 创建配置文件
    click.echo()
    config_file = project_root / '.enum-dict.yaml'
    if not config_file.exists() or force:
        config = {
            'base_dir': base_dir,
            'database_url': db_url,
            'enum': {
                'enums_file': f'{base_dir}/data/enums.py',
                'labels_file': f'{base_dir}/data/enum_labels.py',
                'helper_file': f'{base_dir}/data/enum_helper.py',
            },
            'dict': {
                'types_table': 'dict_types',
                'data_table': 'dict_data',
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        click.echo(f"   [OK] .enum-dict.yaml")
        created_count += 1
    else:
        click.echo(f"   [SKIP]  .enum-dict.yaml (已存在)")
        skipped_count += 1
    
    # 5. 显示统计
    click.echo()
    click.echo("-" * 60)
    click.echo(f"[OK] 创建: {created_count} 个文件")
    if skipped_count > 0:
        click.echo(f"[SKIP]  跳过: {skipped_count} 个文件 (已存在)")
    
    # 6. 显示下一步提示
    click.echo("\n" + "="*60)
    click.echo("[INFO] 下一步操作:")
    click.echo("="*60)
    
    click.echo(f"""
Step 1. Register API routes in {base_dir}/main.py:
   
   from {base_dir}.api import enums, dicts
   
   app.include_router(enums.router, prefix="/api/enums", tags=["Enum"])
   app.include_router(dicts.router, prefix="/api/dicts", tags=["Dict"])

Step 2. Initialize database:
   
   python migrations/init_dict_tables.py

Step 3. Start FastAPI:
   
   uvicorn {base_dir}.main:app --reload

Step 4. Use CLI commands:
   
   enum-dict create OrderStatus Pending Paid Shipped
   enum-dict list
   enum-dict show OrderStatus

Step 5. Visit API docs:
   
   http://localhost:8000/docs
""")
    
    click.echo("="*60 + "\n")


def _is_fastapi_project(path: Path) -> bool:
    """检测是否是FastAPI项目"""
    # 检查main.py
    if (path / 'app' / 'main.py').exists():
        return True
    if (path / 'main.py').exists():
        return True
    
    # 检查requirements.txt
    req_file = path / 'requirements.txt'
    if req_file.exists():
        content = req_file.read_text(encoding='utf-8', errors='ignore')
        if 'fastapi' in content.lower():
            return True
    
    # 检查pyproject.toml
    pyproject = path / 'pyproject.toml'
    if pyproject.exists():
        content = pyproject.read_text(encoding='utf-8', errors='ignore')
        if 'fastapi' in content.lower():
            return True
    
    return False


def _get_files_to_create(base_dir: str) -> list:
    """
    获取需要创建的文件列表
    
    Returns:
        List[(display_name, file_path, template_name)]
    """
    return [
        # API路由
        ('API - Enum', f'{base_dir}/api/enums.py', 'api_enums.py.j2'),
        ('API - Dict', f'{base_dir}/api/dicts.py', 'api_dicts.py.j2'),
        ('API - __init__', f'{base_dir}/api/__init__.py', 'api_init.py.j2'),
        
        # 模型
        ('Models - Dict', f'{base_dir}/models/dict_models.py', 'models_dict.py.j2'),
        ('Models - Database', f'{base_dir}/models/database.py', 'models_database.py.j2'),
        ('Models - __init__', f'{base_dir}/models/__init__.py', 'models_init.py.j2'),
        
        # Schemas
        ('Schemas - EnumDict', f'{base_dir}/schemas/enum_dict_schemas.py', 'schemas_enum_dict.py.j2'),
        ('Schemas - __init__', f'{base_dir}/schemas/__init__.py', 'schemas_init.py.j2'),
        
        # 核心功能
        ('Core - EnumManager', f'{base_dir}/core/enum_manager.py', 'core_enum_manager.py.j2'),
        ('Core - DictManager', f'{base_dir}/core/dict_manager.py', 'core_dict_manager.py.j2'),
        ('Core - Detector', f'{base_dir}/core/detector.py', 'core_detector.py.j2'),
        ('Core - __init__', f'{base_dir}/core/__init__.py', 'core_init.py.j2'),
        
        # 数据文件（Enum存储）
        ('Data - Enums', f'{base_dir}/data/enums.py', 'data_enums.py.j2'),
        ('Data - Labels', f'{base_dir}/data/enum_labels.py', 'data_enum_labels.py.j2'),
        ('Data - Helper', f'{base_dir}/data/enum_helper.py', 'data_enum_helper.py.j2'),
        ('Data - __init__', f'{base_dir}/data/__init__.py', 'data_init.py.j2'),
        
        # Jinja2模板（代码生成用）
        ('Templates - EnumClass', f'{base_dir}/templates/enum_class.py.j2', 'jinja2_enum_class.j2'),
        ('Templates - EnumLabels', f'{base_dir}/templates/enum_labels.py.j2', 'jinja2_enum_labels.j2'),
        ('Templates - EnumMetadata', f'{base_dir}/templates/enum_metadata.py.j2', 'jinja2_enum_metadata.j2'),
        ('Templates - Helper', f'{base_dir}/templates/helper_function.py.j2', 'jinja2_helper_function.j2'),
        
        # 迁移脚本
        ('Migration - Init', 'migrations/init_dict_tables.py', 'migration_init.py.j2'),
    ]
