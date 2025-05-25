import streamlit as st
from utils.plots import (
    plot_membership_heatmap,
    plot_dimensionality_reduction,
    plot_dimensionality_reduction_3d,
    plot_bar_chart
)
import numpy as np
import plotly.express as px


class VisualizationPage:
    """Página de visualización de pertenencias y reducción de dimensionalidad."""

    @staticmethod
    def show() -> None:
        st.header("3. Visualización de Pertenencias")
        if st.session_state.get('method') == "LDA" and 'lda_probas' in st.session_state:
            df = st.session_state['df']
            cat_vars = st.session_state.get('cat_vars', [])
            st.subheader(
                "Distribución de variables categóricas por cluster (LDA)")
            if cat_vars:
                bar_cols = st.columns(2)
                for i, var in enumerate(cat_vars):
                    with bar_cols[i % 2]:
                        st.plotly_chart(
                            plot_bar_chart(df, var, "cluster"),
                            use_container_width=True
                        )
                    if i % 2 == 1 and i != len(cat_vars) - 1:
                        bar_cols = st.columns(2)
            else:
                st.info("No hay variables categóricas seleccionadas para mostrar.")
            return

        if 'models' not in st.session_state:
            st.warning("Ejecuta primero el clustering.")
            return

        k_opt = st.selectbox(
            "Número de clusters óptimo",
            list(st.session_state['models'].keys()),
            index=list(st.session_state['models'].keys()).index(
                st.session_state.get('viz_k_opt', list(
                    st.session_state['models'].keys())[0])
            )
        )

        if st.button("Confirmar selección de clusters"):
            st.session_state['viz_k_opt'] = k_opt
            model = st.session_state['models'][k_opt]
            st.session_state['heatmap'] = plot_membership_heatmap(
                model, st.session_state['vars'], width=1000, height=800)
            selected_df = st.session_state['df'][st.session_state['vars']]
            st.session_state['scatter_plot'] = plot_dimensionality_reduction(
                selected_df, model, method="PCA"
            )
            st.session_state['scatter_plot_3d'] = plot_dimensionality_reduction_3d(
                selected_df, model, method="PCA"
            )

        if 'heatmap' in st.session_state:
            st.markdown(
                """
                <style>
                .centered-plotly {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown('<div class="centered-plotly">',
                        unsafe_allow_html=True)
            st.subheader("Probabilidades de Pertenencia a Clusters")
            st.plotly_chart(
                st.session_state['heatmap'],
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        if 'scatter_plot' in st.session_state:
            st.subheader(
                "Scatter Plot con Reducción de Dimensionalidad (PCA - 2D)")
            st.plotly_chart(
                st.session_state['scatter_plot'],
                use_container_width=True
            )

        if 'scatter_plot_3d' in st.session_state:
            st.subheader(
                "Scatter Plot con Reducción de Dimensionalidad (PCA - 3D)")
            st.plotly_chart(
                st.session_state['scatter_plot_3d'],
                use_container_width=True
            )


# Para compatibilidad
show = VisualizationPage.show
