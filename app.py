from flask import Flask, request, render_template
from device_detector import DeviceDetector

app = Flask(__name__)

@app.route('/')
def home():
    # Отримуємо реальний IP користувача
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip:
        # Беремо лише першу IP-адресу зі списку
        user_ip = user_ip.split(',')[0].strip()

    # Аналіз User-Agent за допомогою DeviceDetector
    user_agent_string = request.headers.get('User-Agent', 'Unknown device')
    device = DeviceDetector(user_agent_string).parse()

    # Формуємо інформацію про пристрій
    device_info = {
        "browser": device.client_name() or "Unknown",
        "browser_version": device.client_version() or "Unknown",
        "os": device.os_name() or "Unknown",
        "os_version": device.os_version() or "Unknown",
        "device": device.device_type() or "Unknown",
    }

    # Логування для діагностики
    print(f"User IP: {user_ip}")
    print(f"User-Agent: {user_agent_string}")
    print(f"Parsed Device Info: {device_info}")

    return render_template('index.html', ip=user_ip, user_agent=device_info)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
