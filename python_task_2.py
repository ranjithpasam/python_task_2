
    import pandas as pd
    import networkx as nx

    def calculate_distance_matrix(dataset_path):

        df = pd.read_csv(dataset_path)

        G = nx.from_pandas_edgelist(df, 'source', 'target', ['distance'], create_using=nx.DiGraph())

        all_pairs_shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G, weight='distance'))

        nodes = sorted(G.nodes)
        distance_matrix = pd.DataFrame(index=nodes, columns=nodes)

        for i in nodes:
            for j in nodes:
                if i == j:
                    distance_matrix.loc[i, j] = 0
                elif j in all_pairs_shortest_paths[i]:
                    distance_matrix.loc[i, j] = all_pairs_shortest_paths[i][j]
                else:
                    distance_matrix.loc[i, j] = float('inf')

        return distance_matrix

    dataset_path = 'C:\Users\user\Downloads\MapUp-Data-Assessment-F-main\MapUp-Data-Assessment-F-main\2-1'
    result_distance_matrix = calculate_distance_matrix(dataset_path)
    print(result_distance_matrix)


    def unroll_distance_matrix(distance_matrix):

        distance_matrix_reset = distance_matrix.reset_index()
        columns_list = distance_matrix_reset.columns.to_list()

        unrolled_distances = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

        for i in range(len(distance_matrix_reset)):
            id_start = distance_matrix_reset.iloc[i]['index']

            for j in range(len(columns_list)):
                if columns_list[j] != 'index':
                    id_end = columns_list[j]
                    distance = distance_matrix_reset.iloc[i][id_end]

                    if id_start != id_end:
                        unrolled_distances = unrolled_distances.append(
                            {'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)

        return unrolled_distances

    result_unrolled_distances = unroll_distance_matrix(result_distance_matrix)
    print(result_unrolled_distances)

    def find_ids_within_ten_percentage_threshold(distance_matrix, reference_value):
        reference_rows = distance_matrix[distance_matrix['id_start'] == reference_value]

        reference_avg_distance = reference_rows['distance'].mean()

        lower_bound = reference_avg_distance - (0.1 * reference_avg_distance)
        upper_bound = reference_avg_distance + (0.1 * reference_avg_distance)

        result_ids = \
        distance_matrix[(distance_matrix['distance'] >= lower_bound) & (distance_matrix['distance'] <= upper_bound)][
            'id_start'].unique()

        result_ids.sort()

        return result_ids

    reference_value = 42
    result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_distances, reference_value)
    print(result_within_threshold


    def calculate_toll_rate(distance_matrix):
        toll_rate_df = distance_matrix.copy(deep=True)
        toll_rate_df['moto'] = distance_matrix['distance'] * 0.8
        toll_rate_df['car'] = distance_matrix['distance'] * 1.2
        toll_rate_df['rv'] = distance_matrix['distance'] * 1.5
        toll_rate_df['bus'] = distance_matrix['distance'] * 2.2
        toll_rate_df['truck'] = distance_matrix['distance'] * 3.6

        return toll_rate_df

    result_with_toll_rates = calculate_toll_rate(result_unrolled_distances)
    print(result_with_toll_rates)


    from datetime import time

    def calculate_time_based_toll_rates(input_df):

        time_based_toll_df = input_df.copy(deep=True)

        weekday_time_ranges = [
            (time(0, 0, 0), time(10, 0, 0)),
            (time(10, 0, 0), time(18, 0, 0)),
            (time(18, 0, 0), time(23, 59, 59))
        ]

        weekend_time_ranges = [
            (time(0, 0, 0), time(23, 59, 59))
        ]

        weekday_discount_factors = [0.8, 1.2, 0.8]
        weekend_discount_factor = 0.7

        for start_time, end_time in weekday_time_ranges:
            mask = (time_based_toll_df['start_time'] >= start_time) & (time_based_toll_df['end_time'] <= end_time)
            time_based_toll_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekday_discount_factors[
                weekday_time_ranges.index((start_time, end_time))]

        for start_time, end_time in weekend_time_ranges:
            mask = (time_based_toll_df['start_time'] >= start_time) & (time_based_toll_df['end_time'] <= end_time)
            time_based_toll_df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factor

        return time_based_toll_df

    result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_unrolled_distances)
    print(result_with_time_based_toll_rates)
