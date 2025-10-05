#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import prometheus_client
import os

REQUEST_COUNT = prometheus_client.Counter('http_requests_total', 'Total HTTP Requests')
HOST_TYPE = prometheus_client.Gauge('host_environment_type', 'Host environment type (0=Physical, 1=Virtual, 2=Container)')

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(prometheus_client.generate_latest())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Microservice is running!</h1><a href="/metrics">View Metrics</a>')
        else:
            self.send_response(404)
            self.end_headers()
        REQUEST_COUNT.inc()

def detect_environment():
    """Определяем тип окружения"""
    # Codespaces/GitPod работают в контейнере
    if os.path.exists('/.gitpod') or os.path.exists('/.dockerenv'):
        return 2  # Container
    else:
        # Проверяем другие признаки виртуальной машины
        try:
            import subprocess
            result = subprocess.run(['systemd-detect-virt'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() != 'none':
                return 1  # Virtual Machine
        except:
            pass
        return 0  # Physical Server

def main():
    env_type = detect_environment()
    HOST_TYPE.set(env_type)
    
    env_names = {0: 'Physical Server', 1: 'Virtual Machine', 2: 'Container'}
    print(f"🚀 Starting microservice on port 8080...")
    print(f"📊 Detected environment: {env_names[env_type]}")
    
    # Универсальный способ показать URL
    print(f"🔗 Your microservice is running!")
    print(f"📎 Open the 'Ports' tab in Codespaces to access port 8080")
    
    server = HTTPServer(('0.0.0.0', 8080), MetricsHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
