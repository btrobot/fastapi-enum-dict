"""
CLI命令模块
"""
import click
from pathlib import Path


@click.group()
@click.version_option(version="1.0.0", prog_name="enum-dict")
def main():
    """
    FastAPI Enum-Dict 管理工具
    
    快速为FastAPI项目添加Enum和Dict管理功能。
    """
    pass


@main.command()
@click.option('--base-dir', default='app', help='基础目录（默认: app）')
@click.option('--db-url', default='sqlite:///./app.db', help='数据库URL')
@click.option('--force', is_flag=True, help='强制覆盖已存在的文件')
def init(base_dir, db_url, force):
    """初始化Enum-Dict功能到FastAPI项目"""
    from .init_command import init_project
    init_project(base_dir, db_url, force)


@main.command()
@click.argument('name')
@click.argument('values', nargs=-1, required=True)
@click.option('--type', 'enum_type', type=click.Choice(['enum', 'dict']), help='强制类型')
def create(name, values, enum_type):
    """创建Enum或Dict"""
    from .crud_commands import create_item
    create_item(name, list(values), enum_type)


@main.command('list')
@click.option('--search', help='搜索关键词')
@click.option('--type', 'item_type', type=click.Choice(['enum', 'dict']), help='类型过滤')
def list_items(search, item_type):
    """列出所有Enum和Dict"""
    from .crud_commands import list_all
    list_all(search, item_type)


@main.command()
@click.argument('name')
def show(name):
    """显示Enum或Dict详情"""
    from .crud_commands import show_item
    show_item(name)


@main.command()
@click.argument('name')
@click.argument('operation', type=click.Choice(['add', 'remove', 'rename']))
@click.argument('args', nargs=-1)
def update(name, operation, args):
    """更新Enum或Dict"""
    from .crud_commands import update_item
    update_item(name, operation, args)


@main.command()
@click.argument('name')
@click.option('--force', is_flag=True, help='强制删除（跳过确认）')
def delete(name, force):
    """删除Enum或Dict"""
    from .crud_commands import delete_item
    delete_item(name, force)


if __name__ == '__main__':
    main()
