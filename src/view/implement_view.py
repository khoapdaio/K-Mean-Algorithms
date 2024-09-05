import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.datasets import make_blobs

from model import PlotKMeans
from view.base_view import BaseView


class ImplementView(BaseView):
	def display(self):
		st.title("K-Means Algorithms")
		plot_kmean = PlotKMeans()
		param_col, _, data_col = st.columns([3, 2, 4])
		with param_col:
			k, std, mode = self._display_param_col()

		data, target = make_blobs(centers = k, cluster_std = std)
		target_df = pd.DataFrame(target, columns = ['target'])
		data_df = pd.DataFrame(data, columns = ['x', 'y'])

		with data_col:
			self._display_data_col(data_df)

		raw_col, animation_col = st.columns([1, 1])
		model, elbow_fig = plot_kmean.plot_elbow(data, k, 10, mode)
		model_silhouette, silhouette_fig = plot_kmean.plot_silhouette(data, k, 10, mode)
		animation_fig = plot_kmean.plot_animation(model, 1)
		with raw_col:
			fig_1 = px.scatter(data_df, x = 'x', y = 'y', title = 'Biểu đồ dữ liệu không label')
			st.plotly_chart(fig_1)

		with animation_col:
			animation_fig = animation_fig.update_layout(autosize = False, height = 560,
			                                            title_text = "<b>Visualizing K-means - animated steps</b>",
			                                            title_font = dict(size = 24))
			st.plotly_chart(animation_fig, use_container_width = True)

		silhouette_col, elbow_col = st.columns([1, 1])

		with silhouette_col:
			st.plotly_chart(silhouette_fig, use_container_width = True)

		with elbow_col:
			st.plotly_chart(elbow_fig, use_container_width = True)

	def _display_param_col(self):
		k = st.select_slider(label = "Số lượng Cluster( nhóm )", options = range(2, 11), value = 2)
		std = st.slider("Độ lệch chuẩn của dữ liệu:", 0.1, 5.0, 1.0, 0.1)
		mode = st.selectbox("Phương pháp khởi tạo Centroids", ['K-Mean++', 'Random'])
		return k, std, mode

	def _display_data_col(self, data_df):
		total_rows = data_df.shape[0]
		total_columns = data_df.shape[1]
		dimension_data = data_df.shape

		col1, col2, col3 = st.columns(3)
		with col1:
			st.info(f"**Total Rows:**\n\n{total_rows} rows")
		with col2:
			st.success(f"**Total Columns:**\n\n{total_columns} columns")
		with col3:
			st.warning(f"**Dimension:**\n\n{dimension_data} ")
		st.dataframe(data_df.head(), width = 13 * 80)
