import pandas as pd


def modify_name(row):
    if row["Agencia_nombre"] == "HOTELES S.A.":
        return f"{row['Agencia_nombre']} {row['Ciudad_Nombre']}"
    return row["Agencia_nombre"].strip()


def distribute_data(
    clustered_data: pd.DataFrame, iar_agencias: pd.DataFrame, iar_canales: pd.DataFrame
) -> dict:
    df = clustered_data.copy()
    ag = iar_agencias.copy()
    ca = iar_canales.copy()

    # Apply the function to the 'Agencia_nombre' column
    ag["Ciudad_Nombre"] = ag["Ciudad_Nombre"].apply(lambda x: x.strip())
    ag["Agencia_nombre"] = ag["Agencia_nombre"].apply(lambda x: x.strip())
    ca["Canal_nombre"] = ca["Canal_nombre"].apply(lambda x: x.strip())
    ag["Agencia_nombre"] = ag.apply(modify_name, axis=1)

    cluster_names = {0: "Lujo", 1: "Escapada", 2: "Familias", 3: "Grupos"}

    df["cluster_name"] = df["cluster"].map(cluster_names)

    # AGENCIA
    grouped = (
        df.groupby(["cluster_name", "ID_Agencia"]).size().reset_index(name="count")
    )
    total_counts = (
        grouped.groupby("cluster_name")["count"].sum().reset_index(name="total_count")
    )
    merged = pd.merge(grouped, total_counts, on="cluster_name")
    merged["percentage"] = (merged["count"] / merged["total_count"]) * 100
    merged = merged.sort_values(by=["cluster_name", "ID_Agencia"])
    merged = merged[["cluster_name", "ID_Agencia", "percentage"]]
    agencia_distribution = pd.merge(merged, ag, on="ID_Agencia")[
        ["cluster_name", "ID_Agencia", "Agencia_nombre", "percentage"]
    ]

    # CANALES
    grouped = df.groupby(["cluster_name", "ID_canal"]).size().reset_index(name="count")
    total_counts = (
        grouped.groupby("cluster_name")["count"].sum().reset_index(name="total_count")
    )
    merged = pd.merge(grouped, total_counts, on="cluster_name")
    merged["percentage"] = (merged["count"] / merged["total_count"]) * 100
    merged = merged.sort_values(by=["cluster_name", "ID_canal"])
    merged = merged[["cluster_name", "ID_canal", "percentage"]]
    canal_distribution = pd.merge(merged, ca, on="ID_canal")[
        ["cluster_name", "ID_canal", "Canal_nombre", "percentage"]
    ]

    return [agencia_distribution, canal_distribution]
