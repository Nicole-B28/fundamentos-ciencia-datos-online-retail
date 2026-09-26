import pandas as pd

# ============================================================
# 1. CARGAR EL ARCHIVO EXCEL
# ============================================================

archivo = "Online Retail.xlsx"

df = pd.read_excel(archivo)


# ============================================================
# 2. MOSTRAR LAS PRIMERAS FILAS
# ============================================================

print("\nPRIMERAS 5 FILAS DEL DATASET:")
print(df.head())


# ============================================================
# 3. REVISAR LAS DIMENSIONES DEL DATASET
# ============================================================

print("\nDIMENSIONES DEL DATASET:")
print(df.shape)


# ============================================================
# 4. MOSTRAR LOS NOMBRES DE LAS COLUMNAS
# ============================================================

print("\nNOMBRES DE LAS COLUMNAS:")
print(df.columns)


# ============================================================
# 5. INFORMACIÓN GENERAL DEL DATASET
# ============================================================

print("\nINFORMACIÓN GENERAL:")
df.info()


# ============================================================
# 6. REVISAR VALORES NULOS
# ============================================================

print("\nVALORES NULOS POR COLUMNA:")
print(df.isnull().sum())


# ============================================================
# 7. REVISAR REGISTROS DUPLICADOS
# ============================================================

print("\nREGISTROS DUPLICADOS:")
print(df.duplicated().sum())


# ============================================================
# 8. REVISAR CANTIDADES NEGATIVAS O CERO
# ============================================================

print("\nCANTIDADES NEGATIVAS O CERO:")
print((df["Quantity"] <= 0).sum())


# ============================================================
# 9. REVISAR PRECIOS NEGATIVOS O CERO
# ============================================================

print("\nPRECIOS NEGATIVOS O CERO:")
print((df["UnitPrice"] <= 0).sum())


# ============================================================
# 10. IDENTIFICAR FACTURAS CANCELADAS
# ============================================================

print("\nFACTURAS CANCELADAS:")
print(df["InvoiceNo"].astype(str).str.startswith("C").sum())


# ============================================================
# 11. MOSTRAR EJEMPLOS DE CANTIDADES NEGATIVAS
# ============================================================

print("\nEJEMPLOS DE CANTIDADES NEGATIVAS:")
print(df[df["Quantity"] < 0].head())


# ============================================================
# 12. MOSTRAR EJEMPLOS DE PRECIOS CERO O NEGATIVOS
# ============================================================

print("\nEJEMPLOS DE PRECIOS CERO O NEGATIVOS:")
print(df[df["UnitPrice"] <= 0].head())


# ============================================================
# 13. MOSTRAR EJEMPLOS DE FACTURAS CANCELADAS
# ============================================================

print("\nEJEMPLOS DE FACTURAS CANCELADAS:")
print(
    df[
        df["InvoiceNo"]
        .astype(str)
        .str.startswith("C")
    ].head()
)

# ============================================================
# 14. CREAR UNA COPIA PARA REALIZAR LA LIMPIEZA
# ============================================================

df_limpio = df.copy()

print("\nREGISTROS ANTES DE LA LIMPIEZA:")
print(len(df_limpio))


# ============================================================
# 15. ELIMINAR REGISTROS DUPLICADOS
# ============================================================

df_limpio = df_limpio.drop_duplicates()

print("\nREGISTROS DESPUÉS DE ELIMINAR DUPLICADOS:")
print(len(df_limpio))


# ============================================================
# 16. ELIMINAR FACTURAS CANCELADAS
# Las facturas que empiezan con C corresponden a cancelaciones.
# ============================================================

df_limpio = df_limpio[
    ~df_limpio["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
]

print("\nREGISTROS DESPUÉS DE ELIMINAR FACTURAS CANCELADAS:")
print(len(df_limpio))


# ============================================================
# 17. CONSERVAR SOLO CANTIDADES POSITIVAS
# ============================================================

df_limpio = df_limpio[df_limpio["Quantity"] > 0]

print("\nREGISTROS DESPUÉS DE FILTRAR CANTIDADES POSITIVAS:")
print(len(df_limpio))


# ============================================================
# 18. CONSERVAR SOLO PRECIOS POSITIVOS
# ============================================================

df_limpio = df_limpio[df_limpio["UnitPrice"] > 0]

print("\nREGISTROS DESPUÉS DE FILTRAR PRECIOS POSITIVOS:")
print(len(df_limpio))


# ============================================================
# 19. ELIMINAR REGISTROS SIN DESCRIPCIÓN DEL PRODUCTO
# ============================================================

df_limpio = df_limpio.dropna(subset=["Description"])

print("\nREGISTROS DESPUÉS DE ELIMINAR DESCRIPCIONES NULAS:")
print(len(df_limpio))


# ============================================================
# 20. LIMPIAR ESPACIOS EN LA DESCRIPCIÓN Y EL PAÍS
# ============================================================

df_limpio["Description"] = df_limpio["Description"].str.strip()
df_limpio["Country"] = df_limpio["Country"].str.strip()


# ============================================================
# 21. CONVERTIR CUSTOMERID A ENTERO PERMITIENDO NULOS
# ============================================================

df_limpio["CustomerID"] = df_limpio["CustomerID"].astype("Int64")


# ============================================================
# 22. CREAR VARIABLE DE VALOR TOTAL DE LA VENTA
# ============================================================

df_limpio["TotalAmount"] = (
    df_limpio["Quantity"] * df_limpio["UnitPrice"]
)


# ============================================================
# 23. REVISAR EL RESULTADO FINAL DE LA LIMPIEZA
# ============================================================

print("\nDIMENSIONES DEL DATASET LIMPIO:")
print(df_limpio.shape)

print("\nVALORES NULOS DEL DATASET LIMPIO:")
print(df_limpio.isnull().sum())

print("\nPRIMERAS 5 FILAS DEL DATASET LIMPIO:")
print(df_limpio.head())

print("\nINFORMACIÓN DEL DATASET LIMPIO:")
df_limpio.info()

# ============================================================
# 24. GUARDAR LOS DATOS LIMPIOS EN UNA BASE DE DATOS SQLITE
# ============================================================

import sqlite3

# Nombre de la base de datos
nombre_bd = "online_retail.db"

# Crear conexión con SQLite
conexion = sqlite3.connect(nombre_bd)

# Guardar el DataFrame limpio en una tabla llamada ventas_limpias
df_limpio.to_sql(
    "ventas_limpias",
    conexion,
    if_exists="replace",
    index=False
)

print("\nDATOS GUARDADOS CORRECTAMENTE EN SQLITE.")


# ============================================================
# 25. COMPROBAR QUE LOS DATOS SE GUARDARON
# ============================================================

consulta = """
SELECT COUNT(*) AS total_registros
FROM ventas_limpias
"""

resultado = pd.read_sql_query(consulta, conexion)

print("\nREGISTROS GUARDADOS EN SQLITE:")
print(resultado)


# ============================================================
# 26. LEER ALGUNOS REGISTROS DESDE SQLITE PARA VERIFICAR
# ============================================================

consulta_ejemplo = """
SELECT *
FROM ventas_limpias
LIMIT 5
"""

verificacion = pd.read_sql_query(
    consulta_ejemplo,
    conexion
)

print("\nPRIMEROS 5 REGISTROS LEÍDOS DESDE SQLITE:")
print(verificacion)


# ============================================================
# 27. CERRAR LA CONEXIÓN
# ============================================================

conexion.close()

print("\nCONEXIÓN CON SQLITE CERRADA CORRECTAMENTE.")
