#!/usr/bin/env python3
"""测试定时任务邮件发送功能 - 强制发送一封测试邮件"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from research_agent import send_email, load_env_file, get_eastern_time
from zoneinfo import ZoneInfo
from datetime import datetime

def test_email_sending():
    """测试邮件发送"""
    print("=" * 60)
    print("测试定时任务邮件发送功能")
    print("=" * 60)
    
    # 加载环境变量
    load_env_file()
    
    # 显示当前时间
    eastern_time = get_eastern_time()
    utc_time = datetime.now(ZoneInfo("UTC"))
    
    print(f"\n当前时间（美东）: {eastern_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"当前时间（UTC）: {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("\n" + "=" * 60)
    print("发送测试邮件...")
    print("=" * 60 + "\n")
    
    # 创建测试邮件内容
    test_content = f"""
    <h1>📧 定时任务邮件测试</h1>
    <p>这是一封来自 Research Agent 定时任务的测试邮件。</p>
    
    <h2>⏰ 时间信息</h2>
    <ul>
        <li><b>美东时间:</b> {eastern_time.strftime('%Y-%m-%d %H:%M:%S %Z')}</li>
        <li><b>UTC时间:</b> {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}</li>
    </ul>
    
    <h2>✅ 配置验证</h2>
    <p>定时任务已配置为每天<strong>美东时间 09:00</strong>自动运行。</p>
    
    <p>如果您收到这封邮件，说明：</p>
    <ul>
        <li>✅ Mailgun API 配置正确</li>
        <li>✅ 邮件发送功能正常</li>
        <li>✅ 定时任务可以正常发送邮件</li>
    </ul>
    
    <hr>
    <p><small>此邮件由 Research Agent 自动发送</small></p>
    """
    
    try:
        send_email(test_content, subject="定时任务测试邮件 - Research Agent")
        print("\n" + "=" * 60)
        print("✅ 测试邮件发送成功！")
        print("=" * 60)
        print("\n请检查收件箱（包括垃圾邮件文件夹）确认收到邮件。")
        return True
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ 邮件发送失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_email_sending()
    sys.exit(0 if success else 1)
