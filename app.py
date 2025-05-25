import streamlit as st
from pages_app import add_demografico, cargar_datos, generar_cluster, vizualizacion
import config


def set_custom_styles() -> None:
    """Aplica estilos personalizados a los botones de la app."""
    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            min-height: 2.5em;
        }
        div.stButton {
            margin-bottom: 0.5em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def main() -> None:
    """Función principal de la aplicación."""
    st.set_page_config(**config.PAGE_CONFIG)
    set_custom_styles()
    st.title(config.TITLE)

    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Carga de datos"

    PAGES = {
        "Carga de datos": cargar_datos,
        "Clustering": generar_cluster,
        "Visualización": vizualizacion,
        "Demográficos": add_demografico,
    }

    st.sidebar.title("Navegación")
    for page_name in PAGES:
        if st.sidebar.button(page_name):
            st.session_state.selected_page = page_name

    PAGES[st.session_state.selected_page].show()


if __name__ == "__main__":
    main()
