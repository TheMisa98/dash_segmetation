import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Optional


class DataCleaner:
    """Responsable de limpiar y normalizar un DataFrame."""

    def __init__(self, scaler: Optional[StandardScaler] = None):
        self.scaler = scaler or StandardScaler()

    def fillna_mean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rellena valores faltantes con la media de cada columna numérica."""
        return df.fillna(df.mean(numeric_only=True))

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza las columnas numéricas."""
        return pd.DataFrame(
            self.scaler.fit_transform(df),
            columns=df.columns,
            index=df.index
        )

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia y normaliza el DataFrame."""
        df_filled = self.fillna_mean(df)
        return self.normalize(df_filled)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función de conveniencia para limpiar un DataFrame.
    """
    return DataCleaner().clean(df)
