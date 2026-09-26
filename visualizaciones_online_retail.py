import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# ============================================================
# 1. LEER LOS DATOS DESDE SQLITE
# ============================================================

conexion = sqlite3.connect("online_retail.db")

df = pd.read_sql_query(
    "SELECT * FROM ventas_limpias",
    conexion
)

conexion.close()


# ============================================================
# 2. CONVERTIR LA FECHA
# ============================================================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])


# ============================================================
# GRÁFICO 1
# VENTAS TOTALES POR MES
# ============================================================

ventas_mes = (
    df.groupby(
        df["InvoiceDate"].dt.to_period("M")
    )["TotalAmount"]
    .sum()
)

ventas_mes.index = ventas_mes.index.astype(str)

plt.figure(figsize=(12, 6))

plt.plot(
    ventas_mes.index,
    ventas_mes.values,
    marker="o"
)

plt.title("Evolución mensual de las ventas")
plt.xlabel("Mes")
plt.ylabel("Ventas totales")

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "grafico_1_ventas_mensuales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# GRÁFICO 2
# TOP 10 PAÍSES POR VALOR DE VENTAS
# ============================================================

ventas_pais = (
    df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    ventas_pais.index,
    ventas_pais.values
)

plt.title("Top 10 países por valor de ventas")
plt.xlabel("Ventas totales")
plt.ylabel("País")

plt.tight_layout()

plt.savefig(
    "grafico_2_ventas_por_pais.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# GRÁFICO 3
# TOP 10 PRODUCTOS POR CANTIDAD VENDIDA
# ============================================================

productos = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(11, 7))

plt.barh(
    productos.index,
    productos.values
)

plt.title("Top 10 productos por cantidad vendida")
plt.xlabel("Cantidad total vendida")
plt.ylabel("Producto")

plt.tight_layout()

plt.savefig(
    "grafico_3_productos_mas_vendidos.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nGRÁFICOS GENERADOS Y GUARDADOS CORRECTAMENTE.")
