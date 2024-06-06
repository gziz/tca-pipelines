import pandas as pd

def generate_statistics(clustered_data: pd.DataFrame) -> dict:
    df = clustered_data.copy()

    variable_labels = {
        'h_num_per': 'Número de personas',
        'h_num_adu': 'Número de adultos',
        'h_num_men': 'Número de menores',
        'h_num_noc': 'Número de noches',
        'h_tot_hab': 'Total de habitaciones',
        'h_tfa_total': 'Tarifa total',
        'lead_time': 'Tiempo de anticipación (en días)',
        'rate_per_night': 'Tarifa por noche'
    }

    cluster_names = {
        0: 'Lujo',
        1: 'Escapada',
        2: 'Familias',
        3: 'Grupos'
    }

    # Map the cluster numbers to names
    df['cluster_name'] = df['cluster'].map(cluster_names)

    ### 1. Preprocess for percentage of cancellations ###
    cancellation_counts = df[df['cancelled'] == 1].groupby('cluster_name')['cancelled'].count()
    total_counts = df.groupby('cluster_name')['cancelled'].count()
    cancellation_percentages_df = (cancellation_counts / total_counts * 100).reset_index(name='percentage')

    ### 3-4. Preprocess for median and mean values ###
    median_values = df.groupby('cluster_name').median().reset_index()
    mean_values = df.groupby('cluster_name').mean().reset_index()

    return [cancellation_percentages_df, median_values, mean_values]
