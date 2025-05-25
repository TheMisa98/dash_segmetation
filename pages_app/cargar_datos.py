import streamlit as st
from data.loader import load_csv
from utils.cleaning import clean_data


class DataSelectionPage:
    """Página de carga y selección de datos."""

    @staticmethod
    def show() -> None:
        st.title("Carga de datos")
        st.header("1. Carga de Datos y Selección")

        if 'preview_cleaned' in st.session_state:
            st.markdown(
                """
                <div style="background-color: rgba(255, 165, 0, 0.2); padding: 10px; border-radius: 5px;">
                    <h4>Datos previamente cargados:</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write(st.session_state['preview_cleaned'])

        df = load_csv()
        if df is not None:
            # Limpiar variables de session_state relacionadas con el dataset anterior
            for key in [
                'id_col', 'vars', 'cat_vars', 'preview_cleaned', 'df', 'models',
                'metrics', 'inertia', 'silhouette_scores', 'optimal_k', 'viz_k_opt',
                'cluster_preview', 'lda_df', 'lda_probas', 'merged', 'id_col_demo',
                'demo_vars'
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.success(
                f"Datos cargados con {df.shape[0]} filas y {df.shape[1]} columnas.")

            id_col = st.selectbox(
                "Selecciona la columna de identificador único",
                df.columns,
                index=0  # Siempre selecciona la primera columna por defecto tras limpiar
            )
            if not df[id_col].is_unique:
                st.error(
                    f"La columna seleccionada '{id_col}' no es única. Por favor, selecciona otra.")
                return
            st.success(f"'{id_col}' es un identificador válido.")
            st.session_state['id_col'] = id_col

            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            cat_cols = df.select_dtypes(include="object").columns.tolist()

            seleccion = st.multiselect(
                "Variables numéricas para segmentar (GMM/K-Means)",
                numeric_cols,
                default=[]
            )
            seleccion_cat = st.multiselect(
                "Variables categóricas para segmentar (LDA)",
                cat_cols,
                default=[]
            )

            if st.button("Confirmar selección de variables"):
                if seleccion:
                    st.write("Variables seleccionadas:", seleccion)
                    df[seleccion] = clean_data(df[seleccion])
                    st.success("Datos limpiados correctamente.")
                st.session_state['df'] = df
                st.session_state['vars'] = seleccion
                st.session_state['cat_vars'] = seleccion_cat
                st.session_state['preview_cleaned'] = df[seleccion].head(
                ) if seleccion else df.head()
                st.subheader(
                    "Vista previa de los datos seleccionados y limpiados:")
                st.write(st.session_state['preview_cleaned'])


# Para compatibilidad
show = DataSelectionPage.show
