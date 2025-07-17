import streamlit as st
from components.ui.unit_ui_components import unit_header
from components.ui.unit_ui_components import unit_details
from components.ui.unit_ui_components import cards_section
from components.ui.unit_ui_components import gauge_section
from components.ui.unit_ui_components import controllers_section
from components.ui.unit_ui_components import graph_section
from components.ui.unit_ui_components import map_section
from components.ui.unit_ui_components import alerts_section
from cloud.anedya_cloud import Anedya

import os


def draw_unit_1_dashboard():

    file_name = os.path.basename(__file__).split(".")[0]
    pre_name = file_name.split("_")[0].capitalize()
    NODE_NUMBER = int(file_name.split("_")[1])
    
    NUMBER_OF_NODES = len(st.session_state.nodesId)
    if NUMBER_OF_NODES < NODE_NUMBER:
        st.error("Node ID not found")
        st.stop()

    anedya = Anedya()
    NODE_ID = st.session_state.nodesId[f"node_{NODE_NUMBER}"]
    node = anedya.new_node(st.session_state.anedya_client, nodeId=NODE_ID)
    device_status_res = node.get_deviceStatus()
    unit_header(
        f"{pre_name} {NODE_NUMBER}",
        node_client=node,
        device_status_res=device_status_res,
    )
    unit_details(NODE_ID)
    gauge_section(node)
    cards_section(node)
    # controllers_section(node)
    alerts_section(node)
    graph_section(node)
    # map_section(node)


draw_unit_1_dashboard()
