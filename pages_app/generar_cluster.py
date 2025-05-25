import streamlit as st
from utils.clustering import run_gmm, run_kmeans, compute_aic_bic, compute_silhouette
import plotly.express as px


class ClusteringPage:
    """Página para ejecutar clustering y visualizar métricas."""

    @staticmethod
    def show() -> None:
        st.header("2. Clustering")
        if 'df' not in st.session_state:
            st.warning("Carga primero los datos en la pestaña anterior.")
            return
        df = st.session_state['df'][st.session_state['vars']]

        method = st.selectbox(
            "Selecciona el método de clustering",
            ["GMM", "K-Means"],
            index=[
                "GMM", "K-Means"].index(st.session_state.get('method', "GMM"))
        )

        k_min, k_max = st.slider(
            "Rango de clusters",
            2, 10, (st.session_state.get('k_min', 2),
                    st.session_state.get('k_max', 5))
        )
        st.session_state['k_min'], st.session_state['k_max'] = k_min, k_max

        if st.button("Ejecutar clustering"):
            if method == "GMM":
                models = run_gmm(df, k_min, k_max)
                metrics = compute_aic_bic(models, df)
                st.session_state['metrics'] = metrics
                st.session_state['models'] = models
                st.session_state['method'] = method
            else:
                models = run_kmeans(df, k_min, k_max)
                inertia = [model.inertia_ for model in models.values()]
                st.session_state['inertia'] = inertia
                st.session_state['models'] = models
                st.session_state['method'] = method

            silhouette_scores = compute_silhouette(models, df)
            st.session_state['silhouette_scores'] = silhouette_scores
            available_clusters = list(models.keys())
            st.session_state['optimal_k'] = available_clusters[0]

        if 'models' in st.session_state:
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
                st.session_state['df']['cluster'] = model.predict(df)
                st.session_state['cluster_preview'] = st.session_state['df'][st.session_state['vars'] + [
                    'cluster']].head()
                st.success(f"Clusters asignados automáticamente con {method}.")

        if 'cluster_preview' in st.session_state:
            st.subheader(
                "Vista previa de las variables seleccionadas y el cluster asignado:")
            st.write(st.session_state['cluster_preview'])


# Para compatibilidad
show = ClusteringPage.show
