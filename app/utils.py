import subprocess

def ping_device(ip_address):
    # Número total de intentos
    total_attempts = 4

    try:
        result = subprocess.run(['ping', '-c', str(total_attempts), ip_address], capture_output=True, text=True, timeout=10)

        # Lista para almacenar el resultado de cada intento
        attempts_result = [{'success': result.returncode == 0} for _ in range(total_attempts)]

        return {
            'success': True,
            'total_attempts': total_attempts,
            'attempts_result': attempts_result,
        }

    except subprocess.TimeoutExpired:
        # Si se agota el tiempo de espera, consideramos todos los intentos como no exitosos
        attempts_result = [{'success': False} for _ in range(total_attempts)]

        return {
            'success': False,
            'total_attempts': total_attempts,
            'attempts_result': attempts_result,
        }

    except Exception as e:
        print(f"Error al ejecutar ping: {e}")
        return {
            'success': False,
            'total_attempts': total_attempts,
            'attempts_result': [{'success': False} for _ in range(total_attempts)],
        }
