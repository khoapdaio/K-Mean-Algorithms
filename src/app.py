import streamlit as st
from streamlit_option_menu import option_menu

from util.file_util import get_image_html
from view import IntroductionView, ImplementView

view_dict = {
	"Overview": IntroductionView,
	"Implement": ImplementView,
}


def select_view(selected_option):
	return view_dict[selected_option]()


def main():
	st.set_page_config(layout = "wide")
	st.sidebar.markdown("""
		        <h1 style='font-size:35px;text-align:center'>Khoapd</h1>
		    """, unsafe_allow_html = True)

	st.sidebar.markdown(get_image_html("../../data/images/avatar.png",
	                                   60, 'auto', '50%', '12%',
	                                   ), unsafe_allow_html = True)
	st.sidebar.info('❤🌤️Welcome to project🌤️❤️')
	st.sidebar.markdown("---")
	with st.sidebar:
		selected_option = option_menu(
			menu_title = "Main Menu",
			options = ["Overview", "Implement"],
			icons = ["house", "modem"],
			menu_icon = "menu-up"
		)
	selected_view = select_view(selected_option)
	selected_view.display()

	st.sidebar.markdown("---")
	st.sidebar.info("Created and designed by [Pham Dang Khoa](https://github.com/khoapdaio)")


if __name__ == '__main__':
	main()
