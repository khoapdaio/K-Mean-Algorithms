from util import embed_image, display_file_content
from view.base_view import BaseView
import streamlit as st


class IntroductionView(BaseView):
	def display(self):
		st.title('Introduction')


		file_path = "../../data/images/over_view_k_mean.png"
		embed_image(file_path = file_path, width = 60, height = 'auto')
		st.header("Về thuật toán")
		st.info(display_file_content('../../data/text/overview.txt'))
		col1, col2 = st.columns(2)
		with col1:
			st.subheader("Nguyên lý hoạt động cơ bản")
			st.info(display_file_content('../../data/text/explanation.txt'))

		with col2:
			st.subheader("Bài toán giải quyết")
			st.info(display_file_content('../../data/text/use_case.txt'))



		col3, col4 = st.columns(2)
		with col3:
			st.subheader("Giải thích nguyên lý")
			st.info(display_file_content('../../data/text/work_flow.txt'))

		with col4:
			st.subheader("Flow Work")
			embed_image('../../data/images/work_flow.png', width = 80, height = 'auto')
