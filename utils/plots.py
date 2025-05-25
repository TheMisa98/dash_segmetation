import plotly.express as px
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from typing import Any, List


class ClusterPlotter:
    """Responsable de generar visualizaciones para clustering."""

    @staticmethod
    def membership_heatmap(model: Any, variables: List[str], width: int = 800, height: int = 800):
        if hasattr(model, "means_"):
            centroids = model.means_
        elif hasattr(model, "cluster_centers_"):
            centroids = model.cluster_centers_
        else:
            raise ValueError("Modelo no compatible.")

        df = pd.DataFrame(centroids, columns=variables, index=[
            f"Cluster {i}" for i in range(centroids.shape[0])])
        scaler = MinMaxScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(
            df.T).T, columns=variables, index=df.index)
        fig = px.imshow(
            df_scaled,
            labels=dict(x="Variables", y="Clusters",
                        color="Valor normalizado"),
            x=variables,
            y=df_scaled.index,
            aspect="auto",
            title="Perfil normalizado de clusters por variable",
            template="plotly_white",
            color_continuous_scale="Viridis",
            width=width,
            height=height
        )
        return fig

    @staticmethod
    def dimensionality_reduction(df: pd.DataFrame, model: Any, method: str = "PCA", width: int = 800, height: int = 800):
        labels = model.predict(df) if hasattr(
            model, "predict") else model.labels_
        if method == "PCA":
            reducer = PCA(n_components=2, random_state=0)
        else:
            raise ValueError(
                "Método de reducción de dimensionalidad no soportado.")
        reduced_data = reducer.fit_transform(df)
        reduced_df = pd.DataFrame(reduced_data, columns=["Dim 1", "Dim 2"])
        reduced_df["Cluster"] = labels
        fig = px.scatter(
            reduced_df,
            x="Dim 1",
            y="Dim 2",
            color="Cluster",
            title=f"Scatter Plot con {method}",
            color_continuous_scale="Viridis",
            labels={"Cluster": "Cluster"},
            template="plotly_white",
            width=width,
            height=height
        )
        return fig

    @staticmethod
    def dimensionality_reduction_3d(df: pd.DataFrame, model: Any, method: str = "PCA", width: int = 800, height: int = 800):
        labels = model.predict(df) if hasattr(
            model, "predict") else model.labels_
        if method == "PCA":
            reducer = PCA(n_components=3, random_state=0)
        else:
            raise ValueError(
                "Método de reducción de dimensionalidad no soportado.")
        reduced_data = reducer.fit_transform(df)
        reduced_df = pd.DataFrame(reduced_data, columns=[
                                  "Dim 1", "Dim 2", "Dim 3"])
        reduced_df["Cluster"] = labels
        fig = px.scatter_3d(
            reduced_df,
            x="Dim 1",
            y="Dim 2",
            z="Dim 3",
            color="Cluster",
            title=f"Scatter Plot con {method} (3D)",
            color_continuous_scale="Viridis",
            labels={"Cluster": "Cluster"},
            template="plotly_white",
            width=width,
            height=height
        )
        return fig

    @staticmethod
    def countplot(df: pd.DataFrame, cluster_col: str):
        return px.pie(
            df,
            names=cluster_col,
            title="Distribución de Clusters",
            hole=0.3
        )

    @staticmethod
    def boxplot(df: pd.DataFrame, var: str, cluster_col: str):
        return px.box(
            df,
            x=cluster_col,
            y=var,
            title=f"Boxplot de {var} por Cluster",
            color=cluster_col,
            template="plotly_white"
        )

    @staticmethod
    def heatmap(df: pd.DataFrame, cluster_col: str, var: str):
        crosstab = pd.crosstab(
            df[cluster_col], df[var], normalize='index') * 100
        return px.imshow(
            crosstab,
            labels=dict(x=var, y="Cluster", color="Proporción (%)"),
            title=f"Mapa de Calor: Cluster vs {var}",
            color_continuous_scale="Viridis"
        )

    @staticmethod
    def radar_chart(df: pd.DataFrame, cluster_col: str, vars: List[str]):
        df_encoded = pd.get_dummies(df[vars], drop_first=True)
        df_encoded[cluster_col] = df[cluster_col]
        proportions = df_encoded.groupby(cluster_col).sum()
        proportions = proportions.div(
            proportions.sum(axis=1), axis=0).reset_index()
        fig = px.line_polar(
            proportions.melt(id_vars=cluster_col,
                             var_name="Variable", value_name="Proporción"),
            r="Proporción",
            theta="Variable",
            color=cluster_col,
            line_close=True,
            title="Radar Chart con Proporciones Normalizadas por Cluster",
            template="plotly_dark"
        )
        return fig

    @staticmethod
    def bar_chart(df: pd.DataFrame, var: str, cluster_col: str):
        return px.bar(
            df.groupby([cluster_col, var]).size().reset_index(name="count"),
            x=var,
            y="count",
            color=cluster_col,
            title=f"Gráfico de Barras de {var} por Cluster",
            barmode="group",
            template="plotly_white"
        )


# Funciones de conveniencia para mantener compatibilidad
plot_membership_heatmap = ClusterPlotter.membership_heatmap
plot_dimensionality_reduction = ClusterPlotter.dimensionality_reduction
plot_dimensionality_reduction_3d = ClusterPlotter.dimensionality_reduction_3d
plot_countplot = ClusterPlotter.countplot
plot_boxplot = ClusterPlotter.boxplot
plot_heatmap = ClusterPlotter.heatmap
plot_radar_chart = ClusterPlotter.radar_chart
plot_bar_chart = ClusterPlotter.bar_chart
