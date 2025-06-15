import paramiko
import os
import sys
import time

# --- Configuration ---
HOSTS = [
    '10.3.63.201',
    '10.3.63.202',
    # '10.3.63.203',
    # '10.3.63.204',
    '10.3.63.205',
    '10.3.63.206',
    '10.3.63.207',
    '10.3.63.208',
    '10.3.63.209',
    '10.3.63.210',
    '10.3.63.211',
    '10.3.63.212',
    '10.3.63.213',
    '10.3.63.214',
    '10.3.63.215',
    '10.3.63.216',
    '10.3.63.217',
    '10.3.63.218',
    '10.3.63.219',
]  # List of target hosts
USERNAME = 'root'  # SSH username

# --- IMPORTANT: CHOOSE ONE PASSWORD METHOD ---
# 1. Directly in script (NOT RECOMMENDED for production)
PASSWORD = 'root'

# 2. Prompt for password securely (RECOMMENDED for interactive use)
# import getpass
# try:
#     PASSWORD = getpass.getpass(f"Enter password for {USERNAME}: ")
# except Exception as e:
#     print(f"Error getting password: {e}")
#     sys.exit(1)

# 3. Use SSH keys (MOST SECURE and RECOMMENDED)
# private_key_path = os.path.expanduser('~/.ssh/id_rsa') # Path to your private key
# try:
#     # Attempt to load an unencrypted key first, then with a passphrase if needed
#     KEY = paramiko.RSAKey.from_private_key_file(private_key_path)
# except paramiko.ssh_exception.PasswordRequiredException:
#     key_passphrase = getpass.getpass(f"Enter passphrase for {private_key_path}: ")
#     KEY = paramiko.RSAKey.from_private_key_file(private_key_path, password=key_passphrase)
# except Exception as e:
#     print(f"Error loading SSH key: {e}")
#     sys.exit(1)


COMMANDS = [
    # 'rpm -e cohesity-agent',
    # 'rpm -ivh https://artifactory.eng.cohesity.com/artifactory/cohesity-builds-staging/7.2.2_u2/20250611-152419/release_full/internal_only_rpms_package/el-cohesity-agent-7.2.2_u2-1.x86_64.rpm',
    # 'rpm -e cohesity-mongodb-connector',
    # 'rpm -ivh https://artifactory.eng.cohesity.com/artifactory/cohesity-builds-staging/7.2.2_u2/20250611-152419/release_full/internal_only_rpms_package/cohesity-mongodb-connector-7.2.2_u2-1.x86_64.rpm --force'# Add more commands as needed
    'rm -rf /etc/cohesity-agent/server_cert',
    'rm -rf /etc/cohesity-agent/agent.cfg',
    'systemctl restart cohesity-agent',
]

# --- SSH Client Setup ---
ssh_client = paramiko.SSHClient()
# This policy is insecure for production. For production, use AutoAddPolicy
# only after verifying the host key, or use SSHClient().load_system_host_keys().
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto accept host keys


# --- Function to execute commands on a single host ---
def execute_commands_on_host(hostname, username, password, commands, key=None):
    print(f"\n--- Connecting to {hostname} ---")
    try:
        if key:
            ssh_client.connect(hostname=hostname, username=username, pkey=key, timeout=10)
        else:
            ssh_client.connect(hostname=hostname, username=username, password=password, timeout=10)
        print(f"Successfully connected to {hostname}")

        for cmd in commands:
            print(f"\n  Executing command: '{cmd}'")
            stdin, stdout, stderr = ssh_client.exec_command(cmd, timeout=30)  # Add timeout for command execution

            # Read stdout and stderr to prevent hanging due to buffer limits
            stdout_output = stdout.read().decode().strip()
            stderr_output = stderr.read().decode().strip()

            if stdout_output:
                print(f"  --- STDOUT ---\n{stdout_output}")
            if stderr_output:
                print(f"  --- STDERR ---\n{stderr_output}")

            # Check exit status of the command
            exit_status = stdout.channel.recv_exit_status()
            print(f"  Command exited with status: {exit_status}")
            if exit_status != 0:
                print(f"  WARNING: Command '{cmd}' failed on {hostname}")
            time.sleep(0.5)  # Small delay between commands

    except paramiko.AuthenticationException:
        print(f"Authentication failed for {username}@{hostname}. Please check your credentials.")
    except paramiko.SSHException as ssh_err:
        print(f"SSH error connecting to {hostname}: {ssh_err}")
    except paramiko.BadHostKeyException as bhk_err:
        print(f"Bad host key for {hostname}: {bhk_err}. Manual verification needed.")
    except Exception as e:
        print(f"An unexpected error occurred while connecting or executing on {hostname}: {e}")
    finally:
        if ssh_client.get_transport() and ssh_client.get_transport().is_active():
            print(f"Closing connection to {hostname}")
            ssh_client.close()


# --- Main execution ---
if __name__ == "__main__":
    for host in HOSTS:
        # Pass PASSWORD or KEY based on which method you choose above
        execute_commands_on_host(host, USERNAME, PASSWORD,
            COMMANDS)  # For password authentication  # execute_commands_on_host(host, USERNAME, None, COMMANDS, key=KEY) # For key authentication