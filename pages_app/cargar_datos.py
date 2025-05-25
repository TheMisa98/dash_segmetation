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
            st.success(
                f"Datos cargados con {df.shape[0]} filas y {df.shape[1]} columnas.")

            id_col = st.selectbox(
                "Selecciona la columna de identificador único",
                df.columns,
                index=df.columns.get_loc(
                    st.session_state.get('id_col', df.columns[0]))
            )
            if not df[id_col].is_unique:
                st.error(
                    f"La columna seleccionada '{id_col}' no es única. Por favor, selecciona otra.")
                return
            st.success(f"'{id_col}' es un identificador válido.")
            st.session_state['id_col'] = id_col

            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            seleccion = st.multiselect(
                "Variables para segmentar",
                numeric_cols,
                default=st.session_state.get('vars', [])
            )

            if st.button("Confirmar selección de variables"):
                if seleccion:
                    st.write("Variables seleccionadas:", seleccion)
                    df[seleccion] = clean_data(df[seleccion])
                    st.success("Datos limpiados correctamente.")
                    st.session_state['df'] = df
                    st.session_state['vars'] = seleccion
                    st.session_state['preview_cleaned'] = df[seleccion].head()
                    st.subheader(
                        "Vista previa de los datos seleccionados y limpiados:")
                    st.write(st.session_state['preview_cleaned'])


# Para compatibilidad
show = DataSelectionPage.show
