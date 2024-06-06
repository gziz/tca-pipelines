import numpy as np
import pandas as pd


def preprocess_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    df = raw_data.copy()

    # Remover valores con fecha placeholder
    df = df[df["h_fec_sda_ok"] != "2000-01-01 "]
    df = df[df["h_fec_lld_ok"] != "2000-01-01 "]

    # Remover valores de "aa"
    df = df[df["h_num_per"] != 0]

    # Feature engineering
    df["rate_per_night"] = df["h_tfa_total"] / df["h_num_noc"]
    df["rate_per_night"] = df["rate_per_night"].replace([np.inf, -np.inf], np.nan)

    date_cols_to_convert = [
        "h_res_fec_ok",
        "h_fec_lld_ok",
        "h_fec_sda_ok",
        "h_fec_reg_ok",
        "h_ult_cam_fec_ok",
    ]

    for col in date_cols_to_convert:
        df[col] = pd.to_datetime(df[col])

    # ultimo cambio - fecha de llegada
    df["cam_diff_lld"] = (df["h_ult_cam_fec_ok"] - df["h_fec_lld_ok"]).dt.days
    # fecha de llegada - fecha de reserva
    df["lead_time"] = (df["h_fec_lld_ok"] - df["h_res_fec_ok"]).dt.days
    # ultimo cambio - fecha de salida
    df["cam_diff_sda"] = (df["h_ult_cam_fec_ok"] - df["h_fec_sda_ok"]).dt.days
    # ultimo cambio - fecha de registro
    df["cam_diff_reg"] = (df["h_ult_cam_fec_ok"] - df["h_fec_sda_ok"]).dt.days

    # Fecha de Reserva
    df["h_fec_reg_day"] = df["h_fec_reg_ok"].dt.day
    df["h_fec_reg_month"] = df["h_fec_reg_ok"].dt.month

    # Fecha de Llegada
    df["h_fec_lld_day"] = df["h_fec_lld_ok"].dt.day
    df["h_fec_lld_month"] = df["h_fec_lld_ok"].dt.month

    df["cancelled"] = df["ID_estatus_reservaciones"].isin([2]).astype(int).values
    df["no_show"] = df["ID_estatus_reservaciones"].isin([3]).astype(int).values

    df = df[
        [
            "h_num_per",
            "h_num_adu",
            "h_num_men",
            "h_num_noc",
            "h_tot_hab",
            "h_tfa_total",
            "lead_time",
            "ID_canal",
            "ID_Agencia",
            "rate_per_night",
            "cam_diff_lld",
            "cam_diff_sda",
            "cam_diff_reg",
            "h_fec_reg_day",
            "h_fec_reg_month",
            "h_fec_lld_day",
            "h_fec_lld_month",
            "cancelled",
            "no_show",
            # date columns
            "h_res_fec_ok",
            "h_fec_lld_ok",
            "h_fec_sda_ok",
            "h_fec_reg_ok",
            "h_ult_cam_fec_ok",
            "ID_canal",
        ]
    ]
    return df
