import streamlit as st
from utils.clustering import run_gmm, run_kmeans, compute_aic_bic, compute_silhouette, run_lda_segmentation
import plotly.express as px
import numpy as np


class ClusteringPage:
    """Página para ejecutar clustering y visualizar métricas."""

    @staticmethod
    def show() -> None:
        st.header("2. Clustering")
        if 'df' not in st.session_state:
            st.warning("Carga primero los datos en la pestaña anterior.")
            return
        df = st.session_state['df']
        numeric_vars = st.session_state.get('vars', [])
        cat_vars = st.session_state.get('cat_vars', [])

        method = st.selectbox(
            "Selecciona el método de clustering",
            ["GMM", "K-Means", "LDA"],
            index=["GMM", "K-Means",
                   "LDA"].index(st.session_state.get('method', "GMM"))
        )

        if method == "LDA":
            n_segments = st.slider(
                "Selecciona el número de clusters (LDA)",
                2, 10, st.session_state.get('n_segments', 4)
            )
            st.session_state['n_segments'] = n_segments
        else:
            k_min, k_max = st.slider(
                "Rango de clusters",
                2, 10, (st.session_state.get('k_min', 2),
                        st.session_state.get('k_max', 5))
            )
            st.session_state['k_min'], st.session_state['k_max'] = k_min, k_max

        if st.button("Ejecutar clustering"):
            if method == "GMM":
                models = run_gmm(
                    df[numeric_vars], st.session_state['k_min'], st.session_state['k_max'])
                metrics = compute_aic_bic(models, df[numeric_vars])
                st.session_state['metrics'] = metrics
                st.session_state['models'] = models
                st.session_state['method'] = method
                silhouette_scores = compute_silhouette(
                    models, df[numeric_vars])
                st.session_state['silhouette_scores'] = silhouette_scores
                available_clusters = list(models.keys())
                st.session_state['optimal_k'] = available_clusters[0]
            elif method == "K-Means":
                models = run_kmeans(
                    df[numeric_vars], st.session_state['k_min'], st.session_state['k_max'])
                inertia = [model.inertia_ for model in models.values()]
                st.session_state['inertia'] = inertia
                st.session_state['models'] = models
                st.session_state['method'] = method
                silhouette_scores = compute_silhouette(
                    models, df[numeric_vars])
                st.session_state['silhouette_scores'] = silhouette_scores
                available_clusters = list(models.keys())
                st.session_state['optimal_k'] = available_clusters[0]
            elif method == "LDA":
                if not cat_vars:
                    st.warning(
                        "Selecciona al menos una variable categórica para LDA.")
                    return
                df_out, probas = run_lda_segmentation(
                    df, cat_vars, st.session_state['n_segments'])
                st.session_state['lda_df'] = df_out
                st.session_state['lda_probas'] = probas
                st.session_state['method'] = method
                st.session_state['optimal_k'] = st.session_state['n_segments']

        # Visualización y selección de clusters para GMM/K-Means
        if 'models' in st.session_state and st.session_state.get('method') in ["GMM", "K-Means"]:
            if st.session_state['method'] == "GMM" and 'metrics' in st.session_state:
                st.plotly_chart(
                    px.line(
                        st.session_state['metrics'],
                        x='k',
                        y=['AIC', 'BIC'],
                        title="Gráfica del Codo (AIC/BIC)"
                    ),
                    key="gmm_aic_bic"
                )
            elif st.session_state['method'] == "K-Means" and 'inertia' in st.session_state:
                st.plotly_chart(
                    px.line(
                        x=list(st.session_state['models'].keys()),
                        y=st.session_state['inertia'],
                        title="Elbow Method (Inercia)",
                        labels={'x': 'Número de Clusters', 'y': 'Inercia'}
                    ),
                    key="kmeans_inertia"
                )

            if 'silhouette_scores' in st.session_state:
                st.plotly_chart(
                    px.line(
                        x=list(st.session_state['models'].keys()),
                        y=st.session_state['silhouette_scores'],
                        title="Silhouette Score",
                        labels={'x': 'Número de Clusters',
                                'y': 'Silhouette Score'}
                    ),
                    key="silhouette_score"
                )

            available_clusters = list(st.session_state['models'].keys())
            selected_k = st.selectbox(
                "Selecciona el número de clusters óptimo",
                available_clusters,
                index=available_clusters.index(
                    st.session_state.get('optimal_k', available_clusters[0]))
            )

            if st.button("Confirmar selección de clusters"):
                st.session_state['optimal_k'] = selected_k
                model = st.session_state['models'][st.session_state['optimal_k']]
                # Solo pasar las variables seleccionadas para predecir
                st.session_state['df']['cluster'] = model.predict(
                    df[numeric_vars])
                st.session_state['cluster_preview'] = st.session_state['df'][numeric_vars + [
                    'cluster']].head()
                st.success(f"Clusters asignados automáticamente con {method}.")

        # Visualización y selección para LDA
        if st.session_state.get('method') == "LDA" and 'lda_df' in st.session_state:
            st.success("Segmentación LDA realizada.")
            st.subheader("Asignación de cluster (LDA):")
            # Mostrar solo una tabla con las variables categóricas seleccionadas y el cluster asignado
            cat_vars = st.session_state.get('cat_vars', [])
            cluster_col = 'cluster'
            cols_to_show = cat_vars + [cluster_col]
            st.session_state['df'] = st.session_state['lda_df']
            st.session_state['cluster_preview'] = st.session_state['lda_df'][cols_to_show].head(
            )
            st.write(st.session_state['cluster_preview'])

        if 'cluster_preview' in st.session_state and st.session_state.get('method') != "LDA":
            st.subheader(
                "Vista previa del cluster asignado:")
            st.write(st.session_state['cluster_preview'])


# Para compatibilidad
show = ClusteringPage.show
