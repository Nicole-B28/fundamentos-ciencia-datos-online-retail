import pandas as pd
import sqlite3

# ============================================================
# PARTE 2 - EDA
# LECTURA DE DATOS DESDE SQLITE
# ============================================================

# 1. CONECTAR CON LA BASE DE DATOS
conexion = sqlite3.connect("online_retail.db")


# 2. LEER LA TABLA DESDE SQLITE
consulta = """
SELECT *
FROM ventas_limpias
"""

df = pd.read_sql_query(consulta, conexion)


# 3. CERRAR LA CONEXIÓN
conexion.close()


# ============================================================
# 4. MOSTRAR INFORMACIÓN GENERAL
# ============================================================

print("\nDIMENSIONES DEL DATASET:")
print(df.shape)

print("\nPRIMERAS 5 FILAS:")
print(df.head())

print("\nINFORMACIÓN GENERAL:")
df.info()


# ============================================================
# 5. CONVERTIR LA FECHA AL TIPO DATETIME
# ============================================================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])


# ============================================================
# 6. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

print("\nESTADÍSTICAS DESCRIPTIVAS:")
print(
    df[
        [
            "Quantity",
            "UnitPrice",
            "TotalAmount"
        ]
    ].describe()
)


# ============================================================
# 7. NÚMERO DE VALORES ÚNICOS POR COLUMNA
# ============================================================

print("\nVALORES ÚNICOS POR COLUMNA:")
print(df.nunique())


# ============================================================
# 8. PERIODO DE TIEMPO DEL DATASET
# ============================================================

print("\nFECHA INICIAL:")
print(df["InvoiceDate"].min())

print("\nFECHA FINAL:")
print(df["InvoiceDate"].max())


# ============================================================
# 9. NÚMERO DE PAÍSES
# ============================================================

print("\nNÚMERO DE PAÍSES:")
print(df["Country"].nunique())


# ============================================================
# 10. PRINCIPALES PAÍSES POR NÚMERO DE REGISTROS
# ============================================================

print("\nTOP 10 PAÍSES POR NÚMERO DE REGISTROS:")
print(df["Country"].value_counts().head(10))


# ============================================================
# 11. PRODUCTOS MÁS FRECUENTES
# ============================================================

print("\nTOP 10 PRODUCTOS MÁS FRECUENTES:")
print(df["Description"].value_counts().head(10))


# ============================================================
# 12. PRODUCTOS CON MAYOR CANTIDAD VENDIDA
# ============================================================

productos_cantidad = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PRODUCTOS POR CANTIDAD VENDIDA:")
print(productos_cantidad)


# ============================================================
# 13. PAÍSES CON MAYORES VENTAS
# ============================================================

ventas_pais = (
    df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PAÍSES POR VALOR DE VENTAS:")
print(ventas_pais)


# ============================================================
# 14. NÚMERO DE CLIENTES IDENTIFICADOS
# ============================================================

clientes_identificados = df["CustomerID"].notna().sum()

print("\nREGISTROS CON CLIENTE IDENTIFICADO:")
print(clientes_identificados)

print("\nCLIENTES ÚNICOS IDENTIFICADOS:")
print(df["CustomerID"].nunique())


# ============================================================
# 15. VENTAS TOTALES
# ============================================================

print("\nVALOR TOTAL DE LAS VENTAS:")
print(df["TotalAmount"].sum())


# ============================================================
# 16. CREAR VARIABLES TEMPORALES PARA EL ANÁLISIS
# ============================================================

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day
df["Hour"] = df["InvoiceDate"].dt.hour


# ============================================================
# 17. VENTAS POR MES
# ============================================================

ventas_mes = (
    df.groupby(
        [
            df["InvoiceDate"].dt.to_period("M")
        ]
    )["TotalAmount"]
    .sum()
)

print("\nVENTAS POR MES:")
print(ventas_mes)


# ============================================================
# 18. GENERAR ARCHIVO DE TEXTO CON DESCRIPCIÓN DEL DATASET
# ============================================================

with open(
    "descripcion_dataset.txt",
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write(
        "ANÁLISIS EXPLORATORIO - ONLINE RETAIL DATA SET\n\n"
    )

    archivo.write(
        f"Número de registros: {df.shape[0]}\n"
    )

    archivo.write(
        f"Número de columnas: {df.shape[1]}\n"
    )

    archivo.write(
        f"Fecha inicial: {df['InvoiceDate'].min()}\n"
    )

    archivo.write(
        f"Fecha final: {df['InvoiceDate'].max()}\n"
    )

    archivo.write(
        f"Número de países: {df['Country'].nunique()}\n"
    )

    archivo.write(
        f"Número de productos: {df['StockCode'].nunique()}\n"
    )

    archivo.write(
        f"Número de facturas: {df['InvoiceNo'].nunique()}\n"
    )

    archivo.write(
        f"Número de clientes identificados: "
        f"{df['CustomerID'].nunique()}\n"
    )

    archivo.write(
        f"Valor total de ventas: "
        f"{df['TotalAmount'].sum():.2f}\n"
    )

print(
    "\nARCHIVO descripcion_dataset.txt "
    "GENERADO CORRECTAMENTE."
)


# ============================================================
# 19. CREAR ARCHIVO DE METADATOS
# ============================================================

metadatos = pd.DataFrame({
    "Campo": [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
        "TotalAmount"
    ],

    "Descripcion": [
        "Número o código de la factura",
        "Código único del producto",
        "Descripción del producto",
        "Cantidad de unidades compradas",
        "Fecha y hora de la transacción",
        "Precio unitario del producto",
        "Identificador único del cliente",
        "País del cliente",
        "Valor total de la línea de venta"
    ],

    "Tipo_de_dato": [
        "Texto",
        "Texto",
        "Texto",
        "Entero",
        "Fecha y hora",
        "Decimal",
        "Entero / Nulo",
        "Texto",
        "Decimal"
    ]
})

metadatos.to_csv(
    "metadatos.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nARCHIVO metadatos.csv "
    "GENERADO CORRECTAMENTE."
)
