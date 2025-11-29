"""测试邮件发送功能"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header

EMAIL_SENDER = "REDACTED_EMAIL"
EMAIL_PASSWORD = "REDACTED_GMAIL_APP_PASSWORD"  # 应用专用密码，去掉空格
EMAIL_RECEIVER = "REDACTED_EMAIL"

def test_email():
    """测试邮件发送"""
    msg = MIMEText("这是一封测试邮件，用于验证邮件配置是否正确。", 'plain', 'utf-8')
    msg['From'] = Header("Research Agent Test", 'utf-8')
    msg['To'] = Header(EMAIL_RECEIVER, 'utf-8')
    msg['Subject'] = Header("测试邮件", 'utf-8')

    try:
        print("正在连接 Gmail SMTP 服务器...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        print("正在登录...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        print("正在发送邮件...")
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！请检查收件箱。")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ 邮件认证失败: {e}")
        print("请检查：")
        print("1. 应用专用密码是否正确（已去掉空格）")
        print("2. 是否已开启两步验证")
        print("3. 是否已生成应用专用密码")
        return False
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    test_email()

