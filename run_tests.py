"""
测试运行脚本

方便运行各种测试配置
"""
import subprocess
import sys


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("运行所有测试...")
    print("=" * 60)
    
    result = subprocess.run([
        "pytest",
        "-v",
        "--tb=short"
    ])
    
    return result.returncode


def run_unit_tests():
    """只运行单元测试"""
    print("=" * 60)
    print("运行单元测试...")
    print("=" * 60)
    
    result = subprocess.run([
        "pytest",
        "-v",
        "-m", "unit",
        "--tb=short"
    ])
    
    return result.returncode


def run_with_coverage():
    """运行测试并生成覆盖率报告"""
    print("=" * 60)
    print("运行测试（带覆盖率）...")
    print("=" * 60)
    
    result = subprocess.run([
        "pytest",
        "-v",
        "--cov=fastapi_enum_dict",
        "--cov-report=term-missing",
        "--cov-report=html"
    ])
    
    print("\n覆盖率报告已生成到 htmlcov/ 目录")
    return result.returncode


def run_specific_test(test_file):
    """运行特定测试文件"""
    print("=" * 60)
    print(f"运行测试: {test_file}")
    print("=" * 60)
    
    result = subprocess.run([
        "pytest",
        "-v",
        test_file,
        "--tb=short"
    ])
    
    return result.returncode


def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "all":
            return run_all_tests()
        elif command == "unit":
            return run_unit_tests()
        elif command == "coverage":
            return run_with_coverage()
        elif command.startswith("test_"):
            return run_specific_test(f"tests/{command}.py")
        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  all       - 运行所有测试")
            print("  unit      - 只运行单元测试")
            print("  coverage  - 运行测试并生成覆盖率")
            print("  test_*    - 运行特定测试文件")
            return 1
    else:
        print("测试运行器")
        print("\n用法:")
        print("  python run_tests.py all          # 运行所有测试")
        print("  python run_tests.py unit         # 运行单元测试")
        print("  python run_tests.py coverage     # 生成覆盖率")
        print("  python run_tests.py test_cli     # 运行CLI测试")
        
        return run_all_tests()


if __name__ == '__main__':
    sys.exit(main())
