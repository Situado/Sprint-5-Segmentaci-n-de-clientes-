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

        # PRINTS QUE FUNCIONAN, SON PARA CONTROLAR QUE SE HAYA LEIDO BIEN EL JSON
          
        # print(f"Cliente {cliente_obj.numero}: {cliente_obj.nombre} {cliente_obj.apellido}")
        # print(f"DNI: {cliente_obj.DNI}")
        # print(f"Tipo: {cliente_obj.tipo.__class__.__name__}")
        # for transaccion in cliente_obj.transacciones:
        #     print(f"Transacción {transaccion.numero}:")
        #     print(f"  Estado: {transaccion.estado}")
        #     print(f"  Tipo: {transaccion.tipo}")
        #     print(f"  Cuenta Número: {transaccion.cuentaNumero}")
        #     print(f"  Cupo Diario Restante: {transaccion.cupoDiarioRestante}")
        #     print(f"  Monto: {transaccion.monto}")
        #     print(f"  Fecha: {transaccion.fecha}")
        #     print(f"  Saldo en Cuenta: {transaccion.saldoEnCuenta}")
        #     print(f"  Total Tarjetas de Crédito Actualmente: {transaccion.totalTarjetasDeCreditoActualmente}")
        #     print(f"  Total Chequeras Actualmente: {transaccion.totalChequerasActualmente}")
        # print("-" * 40)

# GENERACIÓN DE HTML INCOMPLETA, FALTA ACOMODAR EL FORMATO DE LAS COLUMNAS

# def generar_html(data, output_html_path): 
#     html_content = """
#     <!DOCTYPE html>
#     <html lang="es">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Reporte de transacción</title>
#         <style>
#             table {
#                 width: 100%;
#                 border-collapse: collapse;
#             }
#             th, td {
#                 border: 1px solid #ddd;
#                 padding: 8px;
#                 text-align: left;
#             }
#             th {
#                 background-color: #f4f4f4;
#             }
#             .aceptada {
#                 background-color: #006341;
#                 color: chiwte;
#             }
#             .rechazada{
#                 background-color: #c8102e;
#                 color:white;
#             }
#         </style> 
#     </head>
#     <body>
#         <h1>Registro de Clientes</h1>
#         <table border="1">
#             <thead>
#                 <tr>
#                     <th>Cliente</th>
#                     <th>Nombre</th>
#                     <th>Apellido</th>
#                     <th>DNI</th>
#                     <th>Dirección</th>
#                     <th>Transacción</th>
#                     <th>Monto</th>
#                     <th>Estado</th>
#                     <th>Fecha</th>
#                     <th>Razón</th>
#                     <th>Tipo</th>
#                 </tr>
#             </thead>
#             <tbody>
#     """
    
#     for client in data:
#         html_content += f"""
#             <tr>
#                 <td>{client.get('numero')}</td>
#                 <td>{client.get('nombre')}</td>
#                 <td>{client.get('apellido')}</td>
#                 <td>{client.get('DNI')}</td>
#                 <td>Ingresar direccion</td>
#                 <td>{client.get('tipo')}</td>
#                 <td>{client.get('transacciones')}</td>
#             </tr>
#         """
    
#     html_content += """
#             </tbody>
#         </table>
#     </body>
#     </html>
#     """
    
#     with open(output_html_path, 'w', encoding='utf-8') as file:
#         file.write(html_content)


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
    # generar_html(data, output_html_path)
    
    print(f"Archivo HTML generado")