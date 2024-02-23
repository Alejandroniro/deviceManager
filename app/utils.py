import subprocess

def ping_device(ip_address):
    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], capture_output=True, text=True, timeout=10)

        # Contador para contar los intentos
        attempts = 4

        if result.returncode == 0:
            return True, attempts
        else:
            return False, attempts

    except subprocess.TimeoutExpired:
        # Si se agota el tiempo de espera, aún contamos los intentos
        return False, attempts

    except Exception as e:
        print(f"Error al ejecutar ping: {e}")
        return False, attempts
