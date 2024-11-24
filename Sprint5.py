import json

def Lectura_TPS_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encontró.")
        return
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el archivo JSON.")
        return
    
    for client in data:
        numero = client.get('numero')
        nombre = client.get('nombre')
        apellido = client.get('apellido')
        dni = client.get('DNI')
        tipo = client.get('tipo')
        transacciones = client.get('transacciones')
        
        print(f"Cliente {numero}: {nombre} {apellido}")
        print(f"DNI: {dni}")
        print(f"Tipo: {tipo}")
        print(f"Transacciones: {transacciones}")
        print("-" * 40)

if __name__ == "__main__":
    file_path = 'SalidaTPS.json'
    Lectura_TPS_json(file_path)