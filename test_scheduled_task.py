#!/usr/bin/env python3
"""测试定时任务功能 - 立即运行一次并发送邮件"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from research_agent import main, load_env_file, get_eastern_time
from zoneinfo import ZoneInfo
from datetime import datetime

def test_scheduled_task():
    """测试定时任务"""
    print("=" * 60)
    print("测试定时任务 - 立即运行一次")
    print("=" * 60)
    
    # 加载环境变量
    load_env_file()
    
    # 显示当前时间
    eastern_time = get_eastern_time()
    utc_time = datetime.now(ZoneInfo("UTC"))
    
    print(f"\n当前时间（美东）: {eastern_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"当前时间（UTC）: {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("\n" + "=" * 60)
    print("开始执行任务...")
    print("=" * 60 + "\n")
    
    # 运行主任务
    try:
        main()
        print("\n" + "=" * 60)
        print("✅ 任务执行完成！")
        print("=" * 60)
        return True
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ 任务执行失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scheduled_task()
    sys.exit(0 if success else 1)
