"""测试邮件发送功能"""
import os
import sys

# 本地/测试运行默认使用开发数据库，避免污染生产数据
os.environ.setdefault("APP_ENV", "development")

# 添加项目路径以导入配置加载函数
sys.path.insert(0, os.path.dirname(__file__))
from research_agent import (
    load_env_file, send_email,
    EMAIL_SENDER, EMAIL_RECEIVER,
    USE_MAILGUN_API, MAILGUN_API_KEY, MAILGUN_DOMAIN,
    SMTP_SERVER, SMTP_PORT
)

# 加载环境变量
load_env_file()

def test_email():
    """测试邮件发送"""
    print("=" * 60)
    print("邮件发送测试")
    print("=" * 60)
    
    if USE_MAILGUN_API:
        print(f"使用 Mailgun API")
        print(f"  - Domain: {MAILGUN_DOMAIN}")
        print(f"  - API Key: {'已设置' if MAILGUN_API_KEY else '未设置'}")
    else:
        print(f"使用 SMTP")
        print(f"  - 服务器: {SMTP_SERVER}:{SMTP_PORT}")
    
    print(f"  - 发件人: {EMAIL_SENDER}")
    print(f"  - 收件人: {EMAIL_RECEIVER}")
    print("=" * 60)
    
    try:
        # 使用统一的send_email函数
        test_content = """
        <h1>测试邮件</h1>
        <p>这是一封测试邮件，用于验证邮件配置是否正确。</p>
        <p>如果您收到这封邮件，说明配置成功！</p>
        """
        
        print("\n正在发送测试邮件...")
        send_email(test_content)
        print("\n✅ 邮件发送成功！请检查收件箱（包括垃圾邮件文件夹）。")
        return True
    except Exception as e:
        print(f"\n❌ 邮件发送失败: {e}")
        print("\n请检查配置：")
        if USE_MAILGUN_API:
            print("  - MAILGUN_API_KEY 是否正确")
            print("  - MAILGUN_DOMAIN 是否正确")
        else:
            print("  - SMTP服务器地址和端口")
            print("  - SMTP用户名和密码")
        return False

if __name__ == "__main__":
    test_email()
