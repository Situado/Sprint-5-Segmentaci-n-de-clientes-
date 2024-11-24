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


def generar_html(data, output_path):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clientes</title>
    </head>
    <body>
        <h1>Lista de Clientes</h1>
        <table border="1">
            <tr>
                <th>Número</th>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>DNI</th>
                <th>Tipo</th>
                <th>Transacciones</th>
            </tr>
    """
    
    for client in data:
        html_content += f"""
            <tr>
                <td>{client.get('numero')}</td>
                <td>{client.get('nombre')}</td>
                <td>{client.get('apellido')}</td>
                <td>{client.get('DNI')}</td>
                <td>{client.get('tipo')}</td>
                <td>{client.get('transacciones')}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

if __name__ == "__main__":
    file_path = 'SalidaTPS.json'
    Lectura_TPS_json(file_path)
    
    output_html_path = 'clientes.html'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        generar_html(data, output_html_path)
    
    print(f"Archivo HTML generado")