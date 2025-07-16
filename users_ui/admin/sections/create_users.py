import streamlit as st


def create_users_ui():
    headercols = st.columns([1,0.1, 0.1], gap="small")
    with headercols[0]:
        st.title("Create Users", anchor=False)
    with headercols[1]:
        on = st.button("Refresh")
        if on:
            st.rerun()
    with headercols[2]:
        logout = st.button("Logout")

    if logout:
        st.session_state.LoggedIn = False
        st.rerun()

    create_users_section()


def create_users_section():
    container=st.container(border=True)
    with container:
        st.subheader("")
        # st.divider()
        create_user_cols=st.columns([0.3,1,0.3],gap="small")
        with create_user_cols[0]:
            pass
        with create_user_cols[1]:
            NODES_NAME=st.session_state.nodesId["identifier"]
            perm_options=[]
            for i in range(1, len(st.session_state.nodesId)):
                perm_options.append(f"{NODES_NAME}-{i}")
            vars_options=[]
            VARIABLES = st.session_state.variables
            for key, variable in VARIABLES.items():
                variable_name = variable.get('name')
                vars_options.append(variable_name)

            with st.form(key="create_user",clear_on_submit=True,border=False):
                name=st.text_input("Name").strip()
                email=st.text_input("Email").strip()
                password=st.text_input("Password",type="password").strip()
                confirm_password=st.text_input("Confirm Password",type="password").strip()
                permissions = st.pills("Permissions", perm_options, selection_mode="multi")
                variables_selected = st.pills("Variables Access", vars_options, selection_mode="multi")
                submit_button = st.form_submit_button(label="Submit")
                if submit_button:
                    if name=="" or email=="" or password=="" or confirm_password=="" or permissions=="":
                        st.error("Please fill all the fields")
                    elif password!=confirm_password:
                        st.error("Passwords do not match")
                    else:
                        create_user(name,email,password,permissions,variables_selected)

def create_user(name,email,password,permissions,variables):
    try:
        response= st.session_state.firestore_client.collection("users").document(email).set({"name":name,"role":"user","email":email,"password":password,"permissions":permissions,"variables_access":variables},merge=True)
        if response is not None:
            st.toast("User created successfully",icon="🎉")
        else:
            st.error("Error in user creation")

    except Exception as e:
        st.error(e)
    

create_users_ui()