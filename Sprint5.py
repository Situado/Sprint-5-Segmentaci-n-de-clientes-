import json
import sys

class TiposClientes:
    def __init__(self, T_Deb, CA_ARS, C_Corriente, CA_USD, Descubierto, Max_Retiro, T_Cred, Cheq, Comision, Max_Transf):
        self.T_Deb = T_Deb
        self.CA_ARS = CA_ARS
        self.C_Corriente = C_Corriente
        self.CA_USD = CA_USD
        self.Descubierto = Descubierto
        self.Max_Retiro = Max_Retiro
        self.T_Cred = T_Cred
        self.Cheq = Cheq
        self.Comision = Comision
        self.Max_Transf = Max_Transf

class T_Classic(TiposClientes):
    def __init__(self):
        super().__init__(1, True, False, False, 0, 10000, 0, 0, 1.01, 150000)

class T_Gold(TiposClientes):
    def __init__(self):
        super().__init__(1, False, True, True, 10000, 20000, 1, 1, 1.005, 500000)

class T_Black(TiposClientes):
    def __init__(self):
        super().__init__(1, True, True, True, 10000, 100000, 5, 2, 0, float('inf'))

class Cliente:
    def __init__(self, numero, nombre, apellido, DNI, tipo):
        self.numero = numero
        self.nombre = nombre
        self.apellido = apellido
        self.DNI = DNI
        self.tipo = tipo
        self.transacciones = []

    def agregar_transac(self, transac):
        self.transacciones.append(transac)

class Transaccion:
    def __init__(self, estado, tipo, cuentaNumero, cupoDiarioRestante, monto, fecha, numero, saldoEnCuenta, totalTarjetasDeCreditoActualmente, totalChequerasActualmente, Motivo_Rechazo) -> None:
        self.estado = estado
        self.tipo = tipo
        self.cuentaNumero = cuentaNumero
        self.cupoDiarioRestante = cupoDiarioRestante
        self.monto = monto
        self.fecha = fecha
        self.numero = numero
        self.saldoEnCuenta = saldoEnCuenta
        self.totalTarjetasDeCreditoActualmente = totalTarjetasDeCreditoActualmente
        self.totalChequerasActualmente = totalChequerasActualmente
        self.Motivo_Rechazo = Motivo_Rechazo


def Lectura_TPS_json(data, input_json_path):
    
    clientes = []  # Lista de clientes

    for client in data:     # Itera y crea los clientes del JSON  

        tipo = client.get('tipo')
    
        if tipo == 'CLASSIC':
            tipo_cliente = T_Classic()
        elif tipo == 'GOLD':
            tipo_cliente = T_Gold()
        elif tipo == 'BLACK':
            tipo_cliente = T_Black()
        else:
            print(f"Error: Tipo de cliente desconocido {tipo}")
            continue

        cliente_obj = Cliente(client.get('numero'), client.get('nombre'), client.get('apellido'), client.get('DNI'), tipo_cliente)

        transacciones = client.get('transacciones')

        for transac in transacciones:   # Itera y crea las transacciones de cada cliente, y genera el motivo de rechazo

            estado = transac.get('estado')
            tipo = transac.get('tipo')
            cupoDiarioRestante = transac.get('cupoDiarioRestante')
            monto = transac.get('monto')
            saldoEnCuenta = transac.get('saldoEnCuenta')
            totalTarjetasDeCreditoActualmente = transac.get('totalTarjetasDeCreditoActualmente')
            totalChequerasActualmente = transac.get('totalChequerasActualmente')

            if estado == 'RECHAZADA':
                motivo = obtener_motivo_rechazo(tipo_cliente, tipo, cupoDiarioRestante, monto, saldoEnCuenta, totalTarjetasDeCreditoActualmente, totalChequerasActualmente) 
            else:
                motivo = None

            transaccion_obj = Transaccion(
                estado, 
                tipo, 
                transac.get('cuentaNumero'), 
                cupoDiarioRestante, 
                monto, 
                transac.get('fecha'), 
                transac.get('numero'), 
                saldoEnCuenta, 
                totalTarjetasDeCreditoActualmente, 
                totalChequerasActualmente, 
                motivo)

            cliente_obj.agregar_transac(transaccion_obj)

        clientes.append(cliente_obj)  # Añade el cliente a la lista

    return clientes  # Devuelve la lista de clientes

        

def obtener_motivo_rechazo(tipo_cliente, tipo, cupoDiarioRestante, monto, saldoEnCuenta, total_TCredito_Act, total_Cheq_Act):
    
    match tipo:
        case 'RETIRO_EFECTIVO_CAJERO_AUTOMATICO':
            if ( monto > (saldoEnCuenta + tipo_cliente.Descubierto) or ( monto > cupoDiarioRestante) or ( monto > tipo_cliente.Max_Retiro) ):
                return 'El monto supera el máximo permitido'
        
        case 'ALTA_TARJETA_CREDITO':
            if total_TCredito_Act >= tipo_cliente.T_Cred:
                return 'El cliente ya posee el máximo de tarjetas de crédito permitidas'
            
        case 'ALTA_CHEQUERA':
            if total_Cheq_Act >= tipo_cliente.Cheq:
                return 'El cliente ya posee el máximo de chequeras permitidas'
            
        case 'COMPRAR_DOLAR':
            if not tipo_cliente.CA_USD:
                return 'El cliente no posee cuenta en dólares'
            
        case 'TRANSFERENCIA_ENVIADA':
            if ( (monto * tipo_cliente.Comision) > (saldoEnCuenta + tipo_cliente.Descubierto) ) or ((monto * tipo_cliente.Comision) > cupoDiarioRestante):
                return 'El monto supera el máximo permitido, considerando la comisión y el descubierto'
        
        case 'TRANSFERENCIA_RECIBIDA':
            if monto > tipo_cliente.Max_Transf:
                return 'El monto supera el máximo permitido sin autorización'
        
        case _:
            return 'No se reconoce el tipo de operación'



def generar_html(data, output_html_path): 
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
                    <th>Estado</th>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Monto</th>
                    <th>Razón</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for client in data:
        for transaccion in client.transacciones:
            html_content += f"""
            <tr>
            <td>{client.numero}</td>
            <td>{client.nombre}</td>
            <td>{client.apellido}</td>
            <td>{client.DNI}</td>
            <td>Calle {data.index(client) + 1}</td>
            <td>{transaccion.numero}</td>
            <td class="{transaccion.estado.lower()}">{transaccion.estado}</td>
            <td>{transaccion.fecha}</td>
            <td>{transaccion.tipo}</td>
            <td>{transaccion.monto}</td>
            <td>{transaccion.Motivo_Rechazo if transaccion.Motivo_Rechazo else ''}</td>
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



def validar_json(data):
        required_client_fields = {'numero', 'nombre', 'apellido', 'DNI', 'tipo', 'transacciones'}
        required_transac_fields = {'estado', 'tipo', 'cuentaNumero', 'cupoDiarioRestante', 'monto', 'fecha', 'numero', 'saldoEnCuenta', 'totalTarjetasDeCreditoActualmente', 'totalChequerasActualmente'}

        for client in data:

            if not required_client_fields.issubset(client.keys()):
                print(f"Error: Faltan campos de cliente requeridos.")
                return False

            tipo = client.get('tipo')
    
            if tipo == 'CLASSIC':
                tipo_cliente = T_Classic()
            elif tipo == 'GOLD':
                tipo_cliente = T_Gold()
            elif tipo == 'BLACK':
                tipo_cliente = T_Black()
            else:
                print(f"Error: Tipo de cliente desconocido.")
                return False
            
            
            try:
                client_numero = int(client['numero'])
                client_DNI = int(client['DNI'])
            except ValueError:
                print(f"Error: El número de cliente o DNI no son valores enteros.")
                return False

            if client_numero <= 0 or client_DNI <= 0:
                print(f"Error: El número de cliente o DNI no pueden ser menores o iguales a 0.")
                return False
            

            for transac in client.get('transacciones', []):
                if not required_transac_fields.issubset(transac.keys()):
                    print(f"Error: Faltan campos de transaccion requeridos.")
                    return False
                
                if transac['estado'] not in {'ACEPTADA', 'RECHAZADA'}:
                    print(f"Error: Estado de transacción desconocido.")
                    return False
                
                if transac['tipo'] not in {'RETIRO_EFECTIVO_CAJERO_AUTOMATICO', 'ALTA_TARJETA_CREDITO', 'ALTA_CHEQUERA', 'COMPRAR_DOLAR', 'TRANSFERENCIA_ENVIADA', 'TRANSFERENCIA_RECIBIDA'}:
                    print(f"Error: Tipo de transacción desconocido.")
                    return False
                
                if transac['cuentaNumero'] < 0 or transac['cupoDiarioRestante'] < 0 or transac['monto'] < 0 or transac['numero'] < 0 or transac['totalTarjetasDeCreditoActualmente'] < 0 or transac['totalChequerasActualmente'] < 0:
                    print(f"Error: Hay campos de la transaccion que son menores a 0.")
                    return False
                
                if (transac['saldoEnCuenta'] + tipo_cliente.Descubierto) < 0:
                    print(f"Error: El saldo en cuenta más el descubierto no puede ser menor que 0.")
                    return False
                
                if transac['totalTarjetasDeCreditoActualmente'] > tipo_cliente.T_Cred:  
                    print(f"Error: El total de tarjetas de crédito actualmente no puede ser mayor al permitido.")
                    return False
                
                if transac['totalChequerasActualmente'] > tipo_cliente.Cheq:
                    print(f"Error: El total de chequeras actualmente no puede ser mayor al permitido.")
                    return False

        return True



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

    validacion = validar_json(data)
    if not validacion:
        print(f"No se pudo validar el archivo JSON. Cerrando el programa.")
        sys.exit()
    else:
        print(f"Archivo JSON validado correctamente")

    lista_clientes = Lectura_TPS_json(data, input_json_path)
    generar_html(lista_clientes, output_html_path)
    
    print(f"Archivo HTML generado correctamente")