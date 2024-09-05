import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import silhouette_score

from model import KMeansModel


class PlotKMeans:

	def plot_animation(self, model: KMeansModel, velocidade):

		# Convert velocity from seconds to miliseconds
		velocidade *= 1000

		# Set default colors

		color_dict = self._get_color_dict()

		# Set Figure Layout

		layout = self._get_layout_fig(velocidade)
		# Set slider for animation
		sliders_dict = self._get_sliders_dict(velocidade)
		# Initialize Frames
		frames = []
		points_init, centroids_init, points, centroids = self._init_scatter(model, color_dict)

		# Add frames in loop
		c = 0
		centroids_updated = model.get_centroids_updated()
		label_updated = model.get_labels_updated()
		for i in range(len(centroids_updated)):

			centroids.update(dict(x = centroids_updated[i][:, 0], y = centroids_updated[i][:, 1]))

			c += 1
			frame1 = go.Frame(data = [
				points,
				centroids
			], name = c)

			frames.append(frame1)
			sliders_dict['steps'].append(self._make_slider_step(c, i + 1))

			colors = pd.Series(label_updated[i]).map(color_dict).values
			points.update(dict(marker = dict(color = colors)))


		# Build figure
		layout['sliders'] = [sliders_dict]
		data = [points_init, centroids_init]

		fig_data = {"data": data, "layout": go.Layout(layout), "frames": frames}
		fig = go.Figure(fig_data)
		return fig

	def _get_color_dict(self):

		tab10_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
		                '#bcbd22',
		                '#17becf']
		color_dict = {i: color for i, color in enumerate(tab10_colors)}
		return color_dict
	def _get_layout_fig(self, velocidade):
		layout = {"showlegend": False, "updatemenus": [
			{
				"buttons": [
					{
						"args": [None, {"frame": {"duration": velocidade, "redraw": False},
						                "fromcurrent": True, "font": {"color": "red"},
						                "transition": {"duration": velocidade, "easing": "quadratic-in-out"}}
						         ],
						"label": "Play",
						"method": "animate"
					},
					{
						"args": [[None], {"frame": {"duration": 0, "redraw": False},
						                  "mode": "immediate",
						                  "transition": {"duration": 0}}],
						"label": "Pause",
						"method": "animate"
					}
				],
				"font": dict(color = "black"),
				"bgcolor": "orange",
				"direction": "left",
				"pad": {"r": 10, "t": 87},
				"showactive": True,
				"type": "buttons",
				"x": 0.1,
				"xanchor": "right",
				"y": 0,
				"yanchor": "top"
			}
		]}
		return layout

	def _get_sliders_dict(self, velocidade):
		return {
			"active": 0,
			"yanchor": "top",
			"xanchor": "left",
			"currentvalue": {
				"font": {"size": 20},
				# "prefix": "Step:",
				"visible": True,
				"xanchor": "right"
			},
			"transition": {"duration": velocidade / 2, "easing": "cubic-in-out"},
			"pad": {"b": 10, "t": 50},
			"len": 0.9,
			"x": 0.1,
			"y": 0,
			"steps": []
		}

	def _init_scatter(self, model, color_dict):
		points_init = go.Scatter(x = model.data[:, 0].tolist(), y = model.data[:, 1].tolist(), mode = "markers",
		                         marker = dict(color = "gray"), name = 'points')
		centroids_init = go.Scatter(x = [], y = [], mode = "markers",
		                            marker = dict(color = list(color_dict.values()), symbol = 'x', size = 30),
		                            name = 'centroids')

		points = go.Scatter(x = model.data[:, 0].tolist(), y = model.data[:, 1].tolist(), mode = "markers",
		                    marker = dict(color = "gray", size = 10, opacity = 0.8), name = 'points')
		centroids = go.Scatter(x = [], y = [], mode = "markers",
		                       marker = dict(color = list(color_dict.values()), symbol = 'x', size = 30),
		                       name = 'centroids')
		return points_init, centroids_init, points, centroids

	def _make_slider_step(self, i, label, value = None, redraw = False, velocidade = 2):
		slider_step = dict(
			args = [
				[i],
				{"frame": {"duration": velocidade / 2, "redraw": redraw},
				 "transition": {"duration": velocidade / 2},
				 "mode": "immediate"}
			],
			label = label,
			value = value if value is not None else label,
			method = "animate"
		)
		return slider_step

	def plot_elbow(self, data, target_k, max_k, mode):

		sse = []
		model = None
		for k in range(1, max_k + 1):

			kmeans_model = KMeansModel(data, k, mode).fit()
			curr_sse = 0

			if k == target_k:
				model = kmeans_model

			for i in range(10):
				centroid = kmeans_model.centroids[kmeans_model.labels[i]]
				curr_sse += sum((data[i] - centroid) ** 2)

			sse.append(curr_sse)

		elbow_fig = go.Figure(
			data = go.Scatter(x = list(range(1, 11)), y = sse),
			layout = dict(
				template = 'seaborn', title = '<b>Elbow method</b>',
				xaxis = dict({'title': 'k'}), yaxis = dict({'title': 'wss'})
			)
		)
		return model, elbow_fig

	def plot_silhouette(self, data, target_k, max_k, mode):

		silhouette_avg = []
		model = None

		for k in range(2, max_k + 1):  # Silhouette score không tính cho k=1

			kmeans_model = KMeansModel(data, k, mode).fit()

			if k == target_k:
				model = kmeans_model

			# Tính silhouette score cho mô hình với k cụm
			score = silhouette_score(data, kmeans_model.labels)
			silhouette_avg.append(score)

		silhouette_fig = go.Figure(
			data = go.Scatter(x = list(range(2, max_k + 1)), y = silhouette_avg),
			layout = dict(
				template = 'seaborn', title = '<b>Silhouette Score</b>',
				xaxis = dict({'title': 'k'}), yaxis = dict({'title': 'Silhouette Score'})
			)
		)

		return model, silhouette_fig
