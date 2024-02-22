import subprocess

def ping_device(ip_address):
    try:
        # Ejecutar el comando ping y recopilar la salida
        result = subprocess.run(['ping', '-c', '4', ip_address], capture_output=True, text=True, timeout=10)

        # Verificar el código de retorno para determinar si el ping fue exitoso
        if result.returncode == 0:
            return True  # Éxito si el código de retorno es 0
        else:
            return False  # Fallo si el código de retorno no es 0

    except subprocess.TimeoutExpired:
        return False  # Fallo si se excede el tiempo de espera

    except Exception as e:
        return False  # Otra excepción, considerar como fallo
