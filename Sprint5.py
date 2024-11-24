import json
import sys

class TiposCuentas:
    def __init__(self, T_Deb, TipoCaja, Max_Retiro, T_Cred, Cheq, Comision, Max_Transf):
        self.T_Deb = T_Deb
        self.TipoCaja = TipoCaja
        self.Max_Retiro = Max_Retiro
        self.T_Cred = T_Cred
        self.Cheq = Cheq
        self.Comision = Comision
        self.Max_Transf = Max_Transf

def Lectura_TPS_json(data, input_json_path):
    
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


def generar_html(data, output_html_path): #INCOMPLETO
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de transacción</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f4f4f4;
            }
            .aceptada {
                background-color: #006341;
                color: chiwte;
            }
            .rechazada{
                background-color: #c8102e;
                color:white;
            }
        </style> 
    </head>
    <body>
        <h1>Registro de Clientes</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Cliente</th>
                    <th>Nombre</th>
                    <th>Apellido</th>
                    <th>DNI</th>
                    <th>Dirección</th>
                    <th>Transacción</th>
                    <th>Monto</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                    <th>Razón</th>
                    <th>Tipo</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for client in data:
        html_content += f"""
            <tr>
                <td>{client.get('numero')}</td>
                <td>{client.get('nombre')}</td>
                <td>{client.get('apellido')}</td>
                <td>{client.get('DNI')}</td>
                <td>Ingresar direccion</td>
                <td>{client.get('tipo')}</td>
                <td>{client.get('transacciones')}</td>
            </tr>
        """
    
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    with open(output_html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


if __name__ == "__main__":

    input_json_path = 'SalidaTPS.json'
    output_html_path = 'clientes.html'

    try:
        with open(input_json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: El archivo {input_json_path} no se encontró.")
        sys.exit()
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el archivo JSON.")
        sys.exit()

    Lectura_TPS_json(data, input_json_path)
    generar_html(data, output_html_path)
    
    print(f"Archivo HTML generado")