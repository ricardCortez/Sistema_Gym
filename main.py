from conexionDB import conectar

def main():
    # Llama a la función conectar para obtener la conexión
    conexion = conectar()

    if conexion:
        print("Se estableció la conexión correctamente.")
        # Aquí puedes realizar operaciones con la conexión, como ejecutar consultas SQL
    else:
        print("No se pudo establecer la conexión.")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

