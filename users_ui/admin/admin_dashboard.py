# Show Overview data like total users, total units..
import streamlit as st
import os


def drawAdminDashboard():

    current_dir = os.getcwd()
    NODES_NAME=st.session_state.nodesId["identifier"]
    NUMBER_OF_NODES = len(st.session_state.nodesId)
    
    if ( st.session_state.create_pages == False ):
        st.session_state.create_pages = True
        with open(f"{current_dir}/nodes/node.py", "r") as fr:
            file_content=fr.read()
            if file_content == "":
                st.warning("Node.py file is empty. Please make sure it has the correct content.")
                st.stop()

        for i in range(1, NUMBER_OF_NODES ):
            file_path = f"{current_dir}/nodes/{NODES_NAME}_{i}.py"
            if not os.path.isfile(file_path):
                with open(file_path, "w") as fp:
                    print("Created node file")
                    fp.write(file_content)
            else:
                print("Node file already exists")

    pages = {
        "Admin": [
            st.Page(
                f"{current_dir}/users_ui/admin/sections/admin_dashboard.py",
                title="Admin Dashboard",
            ),
            st.Page(
                f"{current_dir}/users_ui/admin/sections/create_users.py",
                title="Create Users",
                
            ),
            st.Page(
                f"{current_dir}/users_ui/admin/sections/users_managements.py",
                title="Users Managements",
            ),
        ],
        f"{NODES_NAME}s": [
            st.Page(f"{current_dir}/nodes/{NODES_NAME}_1.py", title=f"{NODES_NAME} 1", icon="🛜", default=True) if i == 1 else
            st.Page(f"{current_dir}/nodes/{NODES_NAME}_{i}.py", title=f"{NODES_NAME} {i}", icon="🛜") for i in range(1, NUMBER_OF_NODES)
        ],
    }
    pg = st.navigation(pages)
    # st.logo(f"{current_dir}/images/logo.png", size="large")
    DASHBOARD_NAME=st.secrets["DASHBOARD_NAME"]
    # st.sidebar.subheader(DASHBOARD_NAME)
    ABOUT_DASHBOARD=st.secrets["ABOUT_DASHBOARD"]
    # st.sidebar.markdown(ABOUT_DASHBOARD)
    pg.run()
