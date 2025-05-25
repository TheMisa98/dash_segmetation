import pandas as pd
import streamlit as st
from io import BytesIO
from pandas import ExcelWriter
from typing import Dict, Any, List


class ExcelExporter:
    """Responsable de exportar resultados de clustering y datos demográficos a Excel."""

    def __init__(self, merged: pd.DataFrame, demo_vars: List[str], id_col: str = None):
        """
        Inicializa el exportador.

        Args:
            merged (pd.DataFrame): DataFrame combinado.
            demo_vars (List[str]): Variables demográficas seleccionadas.
            id_col (str, optional): Columna identificadora. Si no se provee, se busca en session_state.
        """
        self.merged = merged
        self.demo_vars = demo_vars
        self.id_col = id_col or st.session_state.get('id_col', 'ID')

    def validate(self) -> bool:
        """Valida que la columna identificadora exista en el DataFrame."""
        if self.id_col not in self.merged.columns:
            st.error(
                f"El identificador '{self.id_col}' no está presente en los datos combinados.")
            return False
        return True

    def _get_cluster_col(self) -> str:
        """Devuelve el nombre de la columna de cluster/segmento según el método."""
        # Busca la columna de cluster/segmento
        for col in ['cluster', 'Segmento']:
            if col in self.merged.columns:
                return col
        for col in self.merged.columns:
            if 'cluster' in col.lower() or 'segment' in col.lower():
                return col
        raise ValueError("No se encontró columna de cluster/segmento en los datos combinados.")

    def _find_column(self, var: str) -> str:
        """Busca la columna original o con sufijo _x/_y."""
        candidates = [var, f"{var}_x", f"{var}_y"]
        for c in candidates:
            if c in self.merged.columns:
                return c
        return None

    def to_excel_bytes(self) -> bytes:
        """Genera el archivo Excel en memoria."""
        writer = BytesIO()
        cluster_col = self._get_cluster_col()
        with ExcelWriter(writer, engine='xlsxwriter') as ew:
            # Exportar asignaciones
            self.merged[[self.id_col, cluster_col]].to_excel(
                ew, sheet_name='Asignaciones', index=False)
            # Exportar tablas cruzadas para todas las variables seleccionadas
            for var in self.demo_vars:
                col = self._find_column(var)
                if col:
                    crosstab = pd.crosstab(
                        self.merged[col], self.merged[cluster_col])
                    crosstab.to_excel(ew, sheet_name=f'Cross_{var}')
            # Exportar todos los datos del merge
            self.merged.to_excel(ew, sheet_name='Datos Completos', index=False)
        return writer.getvalue()


class DownloadButtonStyler:
    """Responsable de aplicar estilos al botón de descarga."""

    @staticmethod
    def apply():
        st.markdown(
            """
            <style>
            div.stDownloadButton { text-align: right; }
            div.stDownloadButton > button {
                background-color: #116530;
                color: #FAFAFA;
                border: none;
                width: auto;
                padding: 0.6em 1em;
                border-radius: 0.25em;
                font-weight: bold;
            }
            div.stDownloadButton > button:hover {
                background-color: #0f4b3f;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def export_results(merged: pd.DataFrame, models: Dict[int, Any]) -> None:
    """
    Exporta los resultados del clustering y las tablas cruzadas a un archivo Excel descargable.

    Args:
        merged (pd.DataFrame): DataFrame combinado con clusters y datos demográficos.
        models (Dict[int, Any]): Modelos de clustering entrenados.
    """
    demo_vars = st.session_state.get('demo_vars', [])
    exporter = ExcelExporter(merged, demo_vars)
    if not exporter.validate():
        return

    DownloadButtonStyler.apply()
    st.download_button(
        "📥 Descargar Excel",
        data=exporter.to_excel_bytes(),
        file_name="segmentacion.xlsx"
    )
