"""
Deploy Wizards of X to VM.
"""

import os
import paramiko
import time

# VM connection details
HOST = "35.236.42.175"
USERNAME = "alexandrelermen"
PORT = 22

def run_ssh_command(ssh, command, sudo=False):
    """Run command over SSH"""
    if sudo:
        command = f"sudo {command}"
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def deploy():
    """Deploy to VM"""
    try:
        # Connect to VM
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, port=PORT, username=USERNAME)
        
        print("Connected to VM...")
        
        # Create directories
        print("Creating directories...")
        commands = [
            "sudo mkdir -p /opt/wizards-of-x /var/log/wizards-of-x /var/backups/wizards-of-x /etc/wizards-of-x",
            "sudo chown -R $USER:$USER /opt/wizards-of-x",
            "cd /opt/wizards-of-x && python3.8 -m venv venv",
            "source /opt/wizards-of-x/venv/bin/activate && pip install mysql-connector-python"
        ]
        
        for cmd in commands:
            print(f"Running: {cmd}")
            out, err = run_ssh_command(ssh, cmd)
            if err:
                print(f"Error: {err}")
            else:
                print(f"Output: {out}")
            time.sleep(1)
        
        # Set up environment variables
        print("Setting up environment...")
        env_vars = {
            'MYSQL_ROOT_PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD', 'changeme'),
            'DISCORD_ERROR_WEBHOOK': os.environ.get('DISCORD_ERROR_WEBHOOK', 'https://discord.com/api/webhooks/error'),
            'DISCORD_INFO_WEBHOOK': os.environ.get('DISCORD_INFO_WEBHOOK', 'https://discord.com/api/webhooks/info'),
            'DISCORD_ALERT_WEBHOOK': os.environ.get('DISCORD_ALERT_WEBHOOK', 'https://discord.com/api/webhooks/alert')
        }
        
        env_file = "\\n".join([f"export {k}='{v}'" for k, v in env_vars.items()])
        cmd = f"echo -e '{env_file}' | sudo tee /etc/wizards-of-x/environment"
        out, err = run_ssh_command(ssh, cmd)
        
        # Set up service
        print("Setting up systemd service...")
        service_content = """[Unit]
Description=Wizards of X Game Service
After=network.target mysql.service

[Service]
Type=simple
User=wizardsofx
Group=wizardsofx
WorkingDirectory=/opt/wizards-of-x
ExecStart=/opt/wizards-of-x/venv/bin/python main.py
Restart=always
Environment=PYTHONPATH=/opt/wizards-of-x
Environment=PRODUCTION=true
EnvironmentFile=/etc/wizards-of-x/environment

[Install]
WantedBy=multi-user.target"""
        
        cmd = f"echo '{service_content}' | sudo tee /etc/systemd/system/wizards-of-x.service"
        out, err = run_ssh_command(ssh, cmd)
        
        # Deploy code
        print("Deploying code...")
        commands = [
            "cd /opt/wizards-of-x && git clone https://github.com/scarfacexxx/wz.git .",
            "cd /opt/wizards-of-x && source venv/bin/activate && pip install -e .",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable wizards-of-x",
            "sudo systemctl start wizards-of-x"
        ]
        
        for cmd in commands:
            print(f"Running: {cmd}")
            out, err = run_ssh_command(ssh, cmd)
            if err:
                print(f"Error: {err}")
            else:
                print(f"Output: {out}")
            time.sleep(1)
        
        print("Deployment completed!")
        
    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return False
    finally:
        ssh.close()
    
    return True

if __name__ == '__main__':
    deploy() 