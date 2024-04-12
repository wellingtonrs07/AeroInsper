def remove_rows_and_columns_with_zeros(matrix):
    # Encontrar os índices das linhas e colunas que contêm zeros
    zero_rows_indices, zero_cols_indices = np.where(matrix == 0)
    
    # Remover as linhas e colunas com zeros
    matrix_without_zeros = np.delete(matrix, zero_rows_indices, axis=0)
    matrix_without_zeros = np.delete(matrix_without_zeros, zero_cols_indices, axis=1)
    
    return matrix_without_zeros