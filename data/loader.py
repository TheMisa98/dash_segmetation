import pandas as pd
import streamlit as st
from typing import Optional


class DataLoader:
    """Responsable de cargar archivos de datos."""

    @staticmethod
    def load_csv(label: str = "Carga tu CSV") -> Optional[pd.DataFrame]:
        uploaded = st.file_uploader(label, type="csv")
        if uploaded:
            try:
                return pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"Error cargando el archivo: {e}")
        return None


# Para compatibilidad
load_csv = DataLoader.load_csv
