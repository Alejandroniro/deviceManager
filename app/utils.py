import subprocess

def ping_device(ip_address):
    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            return True
        else:
            return False

    except subprocess.TimeoutExpired:
        return False

    except Exception as e:
        print(f"Error al ejecutar ping: {e}")
        return False
