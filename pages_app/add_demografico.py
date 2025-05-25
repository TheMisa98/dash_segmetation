import streamlit as st
from data.loader import load_csv
from utils.export import export_results
from utils.plots import (
    plot_countplot, plot_boxplot, plot_heatmap, plot_radar_chart, plot_bar_chart
)


class DemographicEnrichmentPage:
    """Página de enriquecimiento demográfico y visualización."""

    @staticmethod
    def show() -> None:
        st.header("4. Enriquecimiento Demográfico")
        df_demo = load_csv()
        if df_demo is not None and 'models' in st.session_state:
            df = st.session_state['df'][[
                st.session_state['id_col'], 'cluster'] + st.session_state['vars']].copy()
            id_col = st.session_state.get('id_col_demo', None)
            if id_col not in df_demo.columns:
                st.warning(
                    "El identificador no se encontró automáticamente en el dataset demográfico.")
                id_col = st.selectbox(
                    "Selecciona el identificador único para el dataset demográfico",
                    df_demo.columns,
                    index=df_demo.columns.get_loc(
                        st.session_state.get('id_col_demo', df_demo.columns[0]))
                )
                st.session_state['id_col_demo'] = id_col
            else:
                st.session_state['id_col_demo'] = id_col

            df[st.session_state['id_col']
               ] = df[st.session_state['id_col']].astype(str)
            df_demo[st.session_state['id_col_demo']
                    ] = df_demo[st.session_state['id_col_demo']].astype(str)

            st.info(
                "Selecciona las columnas demográficas relevantes para el análisis.")
            demo_vars = st.multiselect(
                "Variables demográficas disponibles",
                [col for col in df_demo.columns if col !=
                    st.session_state['id_col_demo']],
                default=st.session_state.get('demo_vars', [])
            )

            if st.button("Confirmar selección y realizar merge"):
                if not demo_vars:
                    st.warning("Selecciona al menos una variable demográfica.")
                    return

                st.session_state['demo_vars'] = demo_vars
                df_demo_reduced = df_demo[[
                    st.session_state['id_col_demo']] + demo_vars]
                try:
                    merged = df.merge(
                        df_demo_reduced,
                        left_on=st.session_state['id_col'],
                        right_on=st.session_state['id_col_demo'],
                        how='inner'
                    )
                    st.session_state['merged'] = merged
                    st.success("Merge realizado correctamente.")
                except Exception as e:
                    st.error(f"Error al realizar el merge: {e}")
                    return

        if 'merged' in st.session_state:
            st.subheader("Vista previa del merge realizado:")
            st.write(st.session_state['merged'].head())
            export_results(
                st.session_state['merged'], st.session_state['models'])
            st.subheader("Visualizaciones Demográficas")
            st.plotly_chart(plot_countplot(
                st.session_state['merged'], 'cluster'))

            st.subheader("Heatmaps por Variable Demográfica")
            heatmap_cols = st.columns(2)
            for i, var in enumerate(st.session_state['demo_vars']):
                with heatmap_cols[i % 2]:
                    st.plotly_chart(plot_heatmap(
                        st.session_state['merged'], 'cluster', var))
                if i % 2 == 1 and i != len(st.session_state['demo_vars']) - 1:
                    heatmap_cols = st.columns(2)

            st.subheader("Boxplots por Cluster")
            boxplot_cols = st.columns(2)
            for i, var in enumerate(st.session_state['demo_vars']):
                if st.session_state['merged'][var].dtype in ['int64', 'float64']:
                    with boxplot_cols[i % 2]:
                        st.plotly_chart(plot_boxplot(
                            st.session_state['merged'], var, 'cluster'))

            if len(st.session_state['merged']['cluster'].unique()) <= 5:
                st.subheader("Radar Chart")
                st.plotly_chart(plot_radar_chart(
                    st.session_state['merged'], 'cluster', st.session_state['demo_vars']))

            st.subheader("Gráficos de Barras por Categoría")
            barplot_cols = st.columns(2)
            for i, var in enumerate(st.session_state['demo_vars']):
                if st.session_state['merged'][var].dtype == 'object':
                    with barplot_cols[i % 2]:
                        st.plotly_chart(plot_bar_chart(
                            st.session_state['merged'], var, 'cluster'))


# Para compatibilidad
show = DemographicEnrichmentPage.show
