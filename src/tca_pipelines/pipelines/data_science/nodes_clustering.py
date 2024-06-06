import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def perform_clustering(preprocessed_data: pd.DataFrame) -> pd.DataFrame:
    df = preprocessed_data.copy()

    date_cols_to_convert = [
        "h_res_fec_ok",
        "h_fec_lld_ok",
        "h_fec_sda_ok",
        "h_fec_reg_ok",
        "h_ult_cam_fec_ok",
    ]

    for col in date_cols_to_convert:
        df[col] = pd.to_datetime(df[col])

    X = df[
        [
            "h_num_per",
            "h_num_adu",
            "h_num_men",
            "h_num_noc",
            "h_tot_hab",
            "h_tfa_total",
            "lead_time",
            "rate_per_night",
            "ID_Agencia",
        ]
    ]

    X = X.dropna()

    num_cols = [
        "h_num_per",
        "h_num_adu",
        "h_num_men",
        "h_num_noc",
        "h_tot_hab",
        "h_tfa_total",
        "lead_time",
        "rate_per_night",
    ]

    cat_cols = [
        "ID_Agencia",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(), cat_cols),
        ]
    )

    X_preprocessed = preprocessor.fit_transform(X)

    optimal_k = 4
    kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42)
    X_clustered_optimal = kmeans_optimal.fit_predict(X_preprocessed)

    X["cluster"] = X_clustered_optimal

    # Analyze clusters
    X_with_label = X.copy()
    X_with_label["cancelled"] = df.dropna()["cancelled"]
    X_with_label["no_show"] = df.dropna()["no_show"]
    X_with_label["ID_canal"] = df.dropna()["ID_canal"]

    return X_with_label
