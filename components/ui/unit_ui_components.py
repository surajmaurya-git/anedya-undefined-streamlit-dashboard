import streamlit as st
import streamviz as sv
from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import time
from components.charts import draw_chart
from components.ui.time_range_controller import (
    get_default_time_range,
    auto_update_time_range,
    update_time_range,
    reset_time_range,
    is_within_tolerance,
)

is_options_changed = False


def unit_header(title, des=None, node_client=None, device_status_res=None):
    if title is None:
        st.error("Please provide a valid title.")
    VARIABLES = st.session_state.variables
    headercols = st.columns([1, 0.12, 0.11, 0.11], gap="small")
    with headercols[0]:
        st.title(title, anchor=False)
    with headercols[1]:
        if device_status_res is not None or device_status_res.get("status") is True:
            device_status = None
            if device_status_res.get("device_status"):
                device_status = "Online"
            else:
                device_status = "Offline"
        else:
            device_status = "..."

        with st.container(border=False, height=40):
            if device_status == "Online":
                st.markdown(
                    f"""
                    <div style="
                        margin-top: 0px;
                        height: 38px;
                        margin-right: 0px;
                        padding-top: 0;
                        overflow: hidden;
                        white-space: nowrap;
                        text-overflow: ellipsis;
                        font-size: 16px;
                        line-height: 25px;
                        color: white;
                        font-weight: 600;
                        background-color: green;
                        border-radius: 6px;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        display: flex;
                    ">
                        {device_status}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        margin-top: 0px;
                        height: 38px;
                        margin-right: 0px;
                        padding-top: 0;
                        overflow: hidden;
                        white-space: nowrap;
                        text-overflow: ellipsis;
                        font-size: 16px;
                        line-height: 25px;
                        color: white;
                        font-weight: 600;
                        background-color: red;
                        border-radius: 6px;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        display: flex;
                    ">
                        {device_status}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with headercols[2]:
        on = st.button("Refresh")
        if on:
            st.rerun()
    with headercols[3]:
        logout = st.button("Logout")
        if logout:
            st.session_state.LoggedIn = False
            st.rerun()
    if des is not None:
        st.markdown(des)


def unit_details(data):
    # res=node_client.get_valueStore(key="DEVICEINFO")
    # st.write(res)
    # res_json=json.loads(res)
    # st.write(data)
    st.markdown(f"**Node ID:** {data}")
    # st.markdown(f"**Firmware:**  ")
    # st.text(f"IMEI No.: {data.get('imei_id')}")


def draw_custom_tile(room_name, status):
    if status == "Open":
        st.markdown(
            f"""
            <div style="
                width: 200px;
                height: 105px;
                border: 1px solid #d3d3d3;
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
                background-color: red;
                color: white;
            ">
                <p style="margin: 0px; font-size: 14px; color: white;">{room_name}</p>
                <p style="margin: 4px 0 0 0; padding-top: 10px; padding-left: 90px; font-size: 28px; font-weight: 500;">{status}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                width: 200px;
                height: 105px;
                border: 1px solid #d3d3d3;
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
                background-color: white;
                color: black;
            ">
                <p style="margin: 0px; font-size: 14px; color: black;">{room_name}</p>
                <p style="margin: 4px 0 0 0; padding-top: 10px; padding-left: 90px; font-size: 28px; font-weight: 500;">{status}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def cards_section(node_client=None):
    container = st.container(border=True, height=200)
    with container:
        st.subheader(body="Door Status", anchor=False)
        r1_cols = st.columns([1, 1, 1, 1], gap="small")
        with r1_cols[0]:
            res = node_client.get_valueStore(key="dooropen")
            state = res.get("value")
            if state == 0:
                draw_custom_tile(room_name="Cold Room 1", status="Close")
            else:
                draw_custom_tile(room_name="Cold Room 1", status="Open")
            if st.session_state.doorstate1 != state:
                st.session_state.doorstate1 = state
                if state == 0:
                    st.toast("Cold Room 1 Door Closed", icon="✅")
                else:
                    st.toast("Cold Room 1 Door Opened", icon="⚠️")


def gauge_section(node_client=None):
    container = st.container(border=True, height=330)
    VARIABLES = st.session_state.variables
    with container:

        indian_time_zone = pytz.timezone("Asia/Kolkata")  # set time zone
        r1_guage_cols = st.columns(
            [
                1,
                1,
            ],
            gap="small",
        )
        with r1_guage_cols[0]:
            VARIABLE = VARIABLES["variable_1"]
            data = node_client.get_latestData(VARIABLE["identifier"])
            if data.get("data") != None:
                timestamp = data.get("timestamp")
                hr_timestamp = datetime.fromtimestamp(timestamp, indian_time_zone)
                fm_hr_timestamp = hr_timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
                st.markdown(f"**Last Updated:** {fm_hr_timestamp}")
                value = data.get("data")
                sv.gauge(
                    value,
                    VARIABLE["name"],
                    cWidth=True,
                    gSize="MED",
                    sFix=VARIABLE["unit"],
                    arTop=int(VARIABLE["top_range"]),
                    arBot=int(VARIABLE["bottom_range"]),
                )
            else:
                st.error("No Data Available")
        with r1_guage_cols[1]:
            VARIABLE = VARIABLES["variable_2"]
            data = node_client.get_latestData(VARIABLE["identifier"])
            if data.get("data") != None:
                timestamp = data.get("timestamp")
                hr_timestamp = datetime.fromtimestamp(timestamp, indian_time_zone)
                fm_hr_timestamp = hr_timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
                st.markdown(f"**Last Updated:**  {fm_hr_timestamp}")
                value = data.get("data")
                arTop = int(VARIABLE["top_range"])
                arBot = int(VARIABLE["bottom_range"])
                sv.gauge(
                    value,
                    VARIABLE["name"],
                    cWidth=True,
                    gSize="MED",
                    sFix="V",
                    arTop=arTop,
                    arBot=arBot,
                )
            else:
                st.error("No Data Available")


def sync_controllers_state(node_client=None):

    res = node_client.get_valueStore(key="door")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 0:
            st.session_state.door = "Open Door"
        elif value == 1:
            st.session_state.door = "Close Door"
        else:
            print("Invalid value")

    res = node_client.get_valueStore(key="light")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 0:
            st.session_state.light = "Turn Light On"
        elif value <= 5:
            st.session_state.light = "Turn Light Off"
        else:
            print("Invalid value")

    res = node_client.get_valueStore(key="fan")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 1:
            st.session_state.fan = "Turn Fan Off"
        elif value <= 3:
            st.session_state.fan = "Turn Fan On"

    res = node_client.get_valueStore(key="massage")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 1:
            st.session_state.massage = "Turn Massager Off"
        else:
            st.session_state.massage = "Turn Massager On"


def controllers_section(node_client=None):
    if node_client is None:
        st.stop()
    container = st.container(border=True)
    with container:
        st.subheader(body="Controllers", anchor=False)
        sync_controllers_state(node_client=node_client)
        r1_cols = st.columns([1, 1, 1, 1], gap="small")
        with r1_cols[0]:
            st.subheader("Door")
            state = st.button(st.session_state.door, key="door_key")
            if state:
                if st.session_state.door == "Open Door":
                    st.session_state.door = "Close Door"
                    node_client.set_valueStore(key="door", value=1, type="float")
                else:
                    st.session_state.door = "Open Door"
                    node_client.set_valueStore(key="door", value=0, type="float")
                st.rerun()
        with r1_cols[1]:
            st.subheader("Light")
            state = st.button(st.session_state.light, key="light_toggle")
            if state:
                if st.session_state.light == "Turn Light On":
                    st.session_state.light = "Turn Light Off"
                    node_client.set_valueStore(key="light", value=1, type="float")
                else:
                    st.session_state.light = "Turn Light On"
                    node_client.set_valueStore(key="light", value=0, type="float")
                st.rerun()
        with r1_cols[2]:
            st.subheader("Fan")
            state = st.button(st.session_state.fan, key="fan_toggle")
            if state:
                if st.session_state.fan == "Turn Fan On":
                    st.session_state.fan = "Turn Fan Off"
                    node_client.set_valueStore(key="fan", value=1, type="float")
                else:
                    st.session_state.fan = "Turn Fan On"
                    node_client.set_valueStore(key="fan", value=0, type="float")
                st.rerun()
        with r1_cols[3]:
            st.subheader("Massager")
            state = st.button(st.session_state.massage, key="massage_toggle")
            if state:
                if st.session_state.massage == "Turn Massager On":
                    st.session_state.massage = "Turn Massager Off"
                    node_client.set_valueStore(key="massage", value=1, type="float")
                else:
                    st.session_state.massage = "Turn Massager On"
                    node_client.set_valueStore(key="massage", value=0, type="float")
                st.rerun()


def handle_change(*args, **kwargs):
    st.write("Selection changed!")
    st.write("Args:", args)
    st.write("Kwargs:", kwargs)


def graph_section(node_client=None):
    global is_options_changed
    if node_client is None:
        st.error("Invalid Node Client")
        st.stop()
    container = st.container(border=True)
    with container:
        st.subheader(body="Visualizations", anchor=False)
        currentTime = int(time.time())  # to means recent time
        pastHour_Time = int(currentTime - 86400)

        # -----------------------------------------Time range filter-----------------------------------------
        datetime_cols = st.columns(
            [1, 1, 0.2], gap="small", vertical_alignment="bottom"
        )

        with datetime_cols[0]:
            from_cols = st.columns(2, gap="small")
            with from_cols[0]:
                # st.text("From:")
                from_start_datetime = st.date_input(
                    "From", key="from:date", value=st.session_state.from_date
                )
            with from_cols[1]:
                from_time_input = st.time_input(
                    "time",
                    key="from:time",
                    value=st.session_state.from_time,
                    label_visibility="hidden",
                )

            if from_start_datetime and from_time_input:
                st.session_state.from_time = from_time_input
                st.session_state.from_date = from_start_datetime

                combined_datetime = pd.to_datetime(
                    f"{from_start_datetime} {from_time_input}"
                )
                # st.write("Combined datetime:", combined_datetime)
                # Define the India time zone
                india_tz = pytz.timezone("Asia/Kolkata")

                # Localize the combined datetime to the India time zone
                localized_datetime = india_tz.localize(combined_datetime)

                # Convert the localized datetime to epoch time
                from_time = int(localized_datetime.timestamp())
                if from_time != st.session_state.from_input_time:
                    st.session_state.from_input_time = from_time
                    st.rerun()

        with datetime_cols[1]:
            to_cols = st.columns(2)
            with to_cols[0]:
                # st.text("To:")
                to_start_datetime = st.date_input(
                    "To", key="to:date", value=st.session_state.to_date
                )
            with to_cols[1]:
                to_time_input = st.time_input(
                    "time",
                    key="to:time",
                    value=st.session_state.to_time,
                    label_visibility="hidden",
                )
            if to_start_datetime and to_time_input:
                st.session_state.to_time = to_time_input
                st.session_state.to_date = to_start_datetime
                combined_datetime = pd.to_datetime(
                    f"{to_start_datetime} {to_time_input}"
                )
                # st.write("Combined datetime:", combined_datetime)

                # Define the India time zone
                india_tz = pytz.timezone("Asia/Kolkata")

                # Localize the combined datetime to the India time zone
                localized_datetime = india_tz.localize(combined_datetime)

                # Convert the localized datetime to epoch time
                to_time = int(localized_datetime.timestamp())
                if to_time != st.session_state.to_input_time:
                    st.session_state.to_input_time = to_time
                    st.rerun()
        default_time_range = get_default_time_range()
        # Check if the dates and times are within the tolerance range
        if (
            from_start_datetime == default_time_range[2]
            and is_within_tolerance(from_time_input, default_time_range[3])
        ) and (
            to_start_datetime == default_time_range[0]
            and is_within_tolerance(to_time_input, default_time_range[1])
        ):
            auto_update_time_range(True)
        else:
            auto_update_time_range(False)

        with datetime_cols[2]:
            reset_btn = st.button(
                label="Default", on_click=reset_time_range, use_container_width=True
            )
            if reset_btn:
                auto_update_time_range(True)
                # st.rerun()

        if st.session_state.var_auto_update_time_range:
            update_time_range()

        # ==================== Charts ======================
        interval = st.session_state.to_input_time - st.session_state.from_input_time
        agg_interval = 0
        if interval > 2592000:
            agg_interval = 60
        elif interval > 864000:
            agg_interval = 30
        elif interval > 100080:
            agg_interval = 10
        elif interval <= 100080:
            agg_interval = 0

        VARIABLES = st.session_state.variables
        options: list = []
        user_variables_access = st.session_state.user_variables_access
        if st.session_state.view_role == "user":
            for key, variable in VARIABLES.items():
                variable_name = variable.get("name")
                if variable_name in user_variables_access:
                    options.append(variable_name)
        else:
            for key, variable in VARIABLES.items():
                variable_name = variable.get("name")
                options.append(variable_name)

        # st.write(VARIABLES)
        if not options:
            st.error("No variables available")
            st.stop()
        multislect_cols = st.columns(
            [3.5, 1, 0.5], gap="medium", vertical_alignment="bottom"
        )
        with multislect_cols[0]:
            print(st.session_state.show_charts)
            show_charts = st.multiselect(
                "Show Charts",
                placeholder="Show Charts",
                options=options,
                default=st.session_state.show_charts,
                label_visibility="hidden",
                on_change=change_callback,
            )
            # if  is_options_changed:
            #     if show_charts != st.session_state.show_charts:
            #         st.session_state.show_charts = show_charts
            #     is_options_changed = False
            if st.session_state.show_charts != show_charts:
                st.session_state.show_charts = show_charts
                st.rerun()

        with multislect_cols[1]:
            pass
        with multislect_cols[2]:
            submit = st.button(label="Submit", use_container_width=True)
            if submit:
                st.rerun()

        number_of_graphs_per_row = [1]
        for i in range(
            0, len(st.session_state.show_charts), len(number_of_graphs_per_row)
        ):
            graph_cols = st.columns(number_of_graphs_per_row, gap="small")
            for j, chart in enumerate(
                st.session_state.show_charts[i : i + len(number_of_graphs_per_row)]
            ):
                with graph_cols[j]:
                    VARIABLE_KEY = get_variable_key_by_name(VARIABLES, chart)
                    if VARIABLE_KEY is not None:
                        VARIABLE = VARIABLES.get(VARIABLE_KEY)
                        # data=pd.DataFrame()
                        aggregate_or_value = "value"
                        if interval <= 100080:
                            data = node_client.get_data(
                                variable_identifier=VARIABLE.get("identifier"),
                                from_time=st.session_state.from_input_time,
                                to_time=st.session_state.to_input_time,
                            )
                            aggregate_or_value = "value"
                        else:
                            data = node_client.get_aggData(
                                variable_identifier=VARIABLE.get("identifier"),
                                from_time=st.session_state.from_input_time,
                                to_time=st.session_state.to_input_time,
                                agg_interval_mins=agg_interval,
                            )
                            aggregate_or_value = "aggregate"
                        minData = 0
                        maxData = 0
                        if not data.empty:
                            minData = data[aggregate_or_value].min()
                            maxData = data[aggregate_or_value].max()

                        sub_graph_sec = st.columns([1, 1], gap="small")
                        with sub_graph_sec[0]:
                            draw_chart(
                                chart_title=chart,
                                chart_data=data,
                                y_axis_title=VARIABLE.get("unit"),
                                bottomRange=(minData - (minData * 0.2)),
                                topRange=(maxData + (maxData * 0.2)),
                                agg=agg_interval,
                                aggregate_or_value=aggregate_or_value,
                            )
                        with sub_graph_sec[1]:

                            st.dataframe(data, use_container_width=True)
                    else:
                        st.subheader(chart)
                        st.error("Variable not found")


def change_callback():
    global is_options_changed
    is_options_changed = True


def map_section(node_client=None):
    container = st.container(border=True)
    currentTime = int(time.time())  # to means recent time
    pastHour_Time = int(currentTime - 86400)
    with container:
        st.subheader(body="Device Location", anchor=False)
        res = node_client.get_map_data("location", pastHour_Time, currentTime)
        if not res.empty:
            # st.write(res)
            last_updated_time = res.iloc[0]["Datetime"]
            st.markdown(f"**Last Updated:**  {last_updated_time}")
            st.map(
                res,
                zoom=13,
                # latitude="lat",
                # longitude="long",
                color="#0044ff",
                size=50,
                use_container_width=True,
            )
        else:
            res = node_client.get_latestData("Location")
            if res.get("data") is not None:
                location = res.get("data")
                last_updated = res.get("timestamp")
                indian_time_zone = pytz.timezone("Asia/Kolkata")  # set time zone
                hr_timestamp = datetime.fromtimestamp(last_updated, indian_time_zone)
                fm_hr_timestamp = hr_timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
                st.markdown(f"**Last Updated:**  {fm_hr_timestamp}")

                latitude = location.get("lat")
                longitude = location.get("long")
                locationData = pd.DataFrame(
                    {"latitude": [latitude], "longitude": [longitude]}
                )
                st.map(
                    locationData,
                    zoom=13,
                    color="#0044ff",
                    size=50,
                    use_container_width=True,
                )
            else:
                st.error("No Data Available")


def get_variable_key_by_name(data, search_name):
    for key, variable in data.items():
        if variable["name"] == search_name:
            return key
    return None
