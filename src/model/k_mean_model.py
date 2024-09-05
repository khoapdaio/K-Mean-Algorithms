import numpy as np


class KMeansModel:

	def __init__(self, data, n_clusters = 3, mode = 'K-Mean++', seed = None):
		self.data = data
		self.n_clusters = n_clusters
		self.mode = mode
		self.seed = seed
		self._centroids_updated = []
		self._labels_updated = []

		self.max_iteration = 100
		self.num_individuals, self.num_features = self.data.shape
		self.mode_init_centroids = {
			'K-Mean++': self.initialize_random_centroids,
			'Random': self.initialize_improved_centroids
		}

	def get_centroids_updated(self):
		return self._centroids_updated

	def get_labels_updated(self):
		return self._labels_updated

	def _initialize_centroids(self):
		return self.mode_init_centroids[self.mode]()

	def initialize_random_centroids(self):
		if self.seed is not None:
			rng = np.random.RandomState(self.seed)
			centroids_idx = rng.choice(range(self.num_individuals), size = self.n_clusters, replace = False)
		else:
			centroids_idx = np.random.choice(range(self.num_individuals), size = self.n_clusters, replace = False)
		centroids = self.data[centroids_idx]
		self._centroids_updated = [centroids]
		return centroids

	def initialize_improved_centroids(self):
		dist = [self.data[np.random.randint(0, self.num_individuals)]]
		while len(dist) < self.n_clusters:
			d2 = np.array([min([np.square(np.linalg.norm(i - c, None)) for c in dist]) for i in self.data])
			prob = d2 / d2.sum()
			cum_prob = prob.cumsum()
			r = np.random.random()
			ind = np.where(cum_prob >= r)[0][0]
			dist.append(self.data[ind])
		centroids = np.array(dist)
		self._centroids_updated = [centroids]
		return centroids

	def _create_clusters(self, centroids):

		clusters = [[] for _ in range(self.n_clusters)]

		for point_idx, point in enumerate(self.data):
			closest_centroid = np.argmin(np.sqrt(np.sum((point - centroids) ** 2, axis = 1)))
			clusters[closest_centroid].append(point_idx)

		return clusters

	def _create_new_centroid(self, clusters):
		centroids = np.zeros((self.n_clusters, self.num_features))

		for idx, cluster in enumerate(clusters):
			new_centroid = np.mean(self.data[cluster], axis = 0)
			centroids[idx] = new_centroid

		self._centroids_updated.append(centroids)
		return centroids

	def _predict_cluster(self, clusters):
		y_pred = np.zeros(self.num_individuals, dtype = int)

		for cluster_idx, cluster in enumerate(clusters):
			y_pred[cluster] = cluster_idx

		return y_pred

	def fit(self):
		# khởi tạo random centroids
		centroids = self._initialize_centroids()

		# tạo vòng lặp
		for iteration in range(self.max_iteration):

			# Tạo danh sách cụm dựa trên danh sách centroid
			clusters = self._create_clusters(centroids)

			# Ghi lại lịch sử phân cụm
			self._labels_updated.append(self._predict_cluster(clusters))

			# Lưu lại danh sách centroid cũ
			previous_centroids = centroids

			# tạo danh sách centroid mới  dựa trên danh sách cụm
			centroids = self._create_new_centroid(clusters)

			# Lấy hiệu dựa các điểm centroids
			diff = centroids - previous_centroids

			# Kiểm tra sự khác biệt nếu không thì
			if not diff.any():
				# bỏ danh sách centroid mới nhất
				self._centroids_updated = self._centroids_updated[:-1]
				break

		# lấy danh sách centroids cuối cùng của danh sách cập nhật centroid
		self.centroids = self._centroids_updated[-1]
		# Lấy danh sách nhãn  cuối cùng của danh sách cập nhật nhãn
		self.labels = self._labels_updated[-1]

		return self
