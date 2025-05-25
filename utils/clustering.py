"""Funciones para clustering y métricas."""

import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from typing import Dict, Any, List


class ClusteringStrategy:
    """Interfaz para estrategias de clustering."""

    def fit(self, df: pd.DataFrame, k: int) -> Any:
        raise NotImplementedError

    def fit_range(self, df: pd.DataFrame, k_min: int, k_max: int) -> Dict[int, Any]:
        return {k: self.fit(df, k) for k in range(k_min, k_max + 1)}


class GMMClustering(ClusteringStrategy):
    """Estrategia de clustering usando Gaussian Mixture Models."""

    def fit(self, df: pd.DataFrame, k: int) -> GaussianMixture:
        gm = GaussianMixture(n_components=k, random_state=0)
        gm.fit(df)
        return gm


class KMeansClustering(ClusteringStrategy):
    """Estrategia de clustering usando KMeans."""

    def fit(self, df: pd.DataFrame, k: int) -> KMeans:
        km = KMeans(n_clusters=k, random_state=0)
        km.fit(df)
        return km


class ClusteringMetrics:
    """Responsable de calcular métricas de clustering."""

    @staticmethod
    def compute_aic_bic(models: Dict[int, GaussianMixture], df: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for k, model in models.items():
            rows.append({
                'k': k,
                'AIC': model.aic(df),
                'BIC': model.bic(df)
            })
        return pd.DataFrame(rows)

    @staticmethod
    def compute_inertia(models: Dict[int, KMeans]) -> List[float]:
        return [model.inertia_ for model in models.values()]

    @staticmethod
    def compute_silhouette(models: Dict[int, Any], df: pd.DataFrame) -> List[float]:
        scores = []
        for k, model in models.items():
            labels = model.predict(df)
            if len(set(labels)) > 1:
                score = silhouette_score(df, labels)
            else:
                score = float('nan')
            scores.append(score)
        return scores


def run_gmm(df: pd.DataFrame, k_min: int, k_max: int) -> Dict[int, GaussianMixture]:
    return GMMClustering().fit_range(df, k_min, k_max)


def run_kmeans(df: pd.DataFrame, k_min: int, k_max: int) -> Dict[int, KMeans]:
    return KMeansClustering().fit_range(df, k_min, k_max)


def compute_aic_bic(models: Dict[int, GaussianMixture], df: pd.DataFrame) -> pd.DataFrame:
    return ClusteringMetrics.compute_aic_bic(models, df)


def compute_silhouette(models: Dict[int, Any], df: pd.DataFrame) -> List[float]:
    return ClusteringMetrics.compute_silhouette(models, df)
