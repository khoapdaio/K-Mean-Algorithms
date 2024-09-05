import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.datasets import make_blobs

from model import PlotKMeans, KMeansModel
from util import display_file_content
from view.base_view import BaseView


class ImplementView(BaseView):
	def display(self):
		st.title("K-Means Algorithms")

		plot_kmean = PlotKMeans()
		param_col, _, data_col = st.columns([3, 2, 4])
		with param_col:
			k, std, mode = self._display_param_col()
			button = st.button("Khởi tạo dữ liệu và model")

		if 'load_state_1' not in st.session_state:
			st.session_state.load_state_1 = True
			self.set_data_state(k, mode, plot_kmean, std)

		if button or st.session_state.load_state_1:

			if button and st.session_state.param_state:
				self.set_data_state(k, mode, plot_kmean, std)

			data, target = st.session_state["make_blobs"]
			data_df = pd.DataFrame(data, columns = ['x', 'y'])

			with data_col:
				self._display_data_col(data_df)

			raw_col, animation_col = st.columns([1, 1])

			animation_fig = st.session_state["animation_fig"]

			with raw_col:
				fig_1 = px.scatter(data_df, x = 'x', y = 'y', title = 'Biểu đồ dữ liệu không label')
				st.plotly_chart(fig_1)

			with animation_col:
				animation_fig = animation_fig.update_layout(autosize = False, height = 560,
				                                            title_text = "<b>Visualizing K-means - animated steps</b>",
				                                            title_font = dict(size = 24))
				st.plotly_chart(animation_fig, use_container_width = True)

			elbow_fig = st.session_state["elbow_fig"]
			model_silhouette, silhouette_fig = st.session_state["plot_silhouette"]

			st.subheader("Sử dụng phương pháp Average Silhouette Method trong K-Mean")
			st.info(display_file_content('../../data/text/silhouette_method.txt'))
			silhouette_col, silhouette_animation_col = st.columns([1, 1])

			st.subheader("Sử dụng phương pháp khuỷu tay trong K-Mean")
			st.info(display_file_content('../../data/text/elbow_chart.txt'))
			elbow_col, elbow_animation_col = st.columns([1, 1])

			with silhouette_col:

				if 'state_change_k' not in st.session_state:
					st.session_state['K_value_silhouette'] = model_silhouette.n_clusters
					st.session_state.state_chane_k = True

				if st.session_state.state_chane_k:

					k_silhouette = st.slider('K-silhouette', value = st.session_state['K_value_silhouette'],
					                         min_value = 1,
					                         max_value = 10)
					change_k_btn = st.button("Thay đổi K")

					if change_k_btn:
						st.session_state['K_value_silhouette'] = k_silhouette
						model_silhouette.n_clusters = k_silhouette
						model_silhouette.fit()

					animation_silhouette_fig = plot_kmean.plot_animation(model_silhouette, 1)
					st.plotly_chart(silhouette_fig, use_container_width = True)

			with silhouette_animation_col:
				animation_silhouette_fig = animation_silhouette_fig.update_layout(autosize = False, height = 560,
				                                                                  title_text = "<b>Visualizing K-means - animated steps after use Silhouette Score</b>",
				                                                                  title_font = dict(size = 24))
				st.plotly_chart(animation_silhouette_fig, use_container_width = True)

			with elbow_col:
				st.plotly_chart(elbow_fig, use_container_width = True)

			with elbow_animation_col:
				pass

	def set_data_state(self, k, mode, plot_kmean, std):
		st.session_state["k"] = k
		st.session_state["std"] = std
		st.session_state["mode"] = mode
		st.session_state["make_blobs"] = make_blobs(centers = st.session_state["k"],
		                                            cluster_std = st.session_state["std"])
		st.session_state["animation_fig"] = plot_kmean.plot_animation(
			KMeansModel(st.session_state["make_blobs"][0], st.session_state["k"],
			            st.session_state["mode"]).fit(), 1)
		st.session_state["elbow_fig"] = plot_kmean.plot_elbow(st.session_state["make_blobs"][0], 10,
		                                                      st.session_state["mode"])
		st.session_state["plot_silhouette"] = plot_kmean.plot_silhouette(st.session_state["make_blobs"][0], 10,
		                                                                 st.session_state["mode"])

	def _display_param_col(self):
		k = st.select_slider(label = "Số lượng Cluster( nhóm )", options = range(2, 11), value = 2)
		std = st.slider("Độ lệch chuẩn của dữ liệu:", 0.1, 5.0, 1.0, 0.1)
		mode = st.selectbox("Phương pháp khởi tạo Centroids", ['K-Mean++', 'Random'])

		if k or std or mode:
			st.session_state['param_state'] = True

		return k, std, mode

	def _display_data_col(self, data_df):
		total_rows = data_df.shape[0]
		total_columns = data_df.shape[1]
		dimension_data = data_df.shape
		st.subheader("Tổng quan dữ liệu")
		col1, col2, col3 = st.columns(3)
		with col1:
			st.info(f"**Total Rows:**\n\n{total_rows} rows")
		with col2:
			st.success(f"**Total Columns:**\n\n{total_columns} columns")
		with col3:
			st.warning(f"**Dimension:**\n\n{dimension_data} ")
		st.dataframe(data_df, width = 13 * 80, height = 240)
