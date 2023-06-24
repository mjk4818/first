import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.title('너한테만 보이는 페이지')

def text_changed():
    print(st.session_state.msg1)
    print(st.session_state.msg2)

expander1 = st.expander("일정")
with expander1:
    selected_date = st.date_input("날짜를 선택하세요", value=None)
    st.write("선택된 날짜:", selected_date)

    input_memo = st.text_area("메모를 입력하세요")

    if st.button("메모 저장"):
        memo_data = pd.read_csv("memo_data.csv") if os.path.isfile("memo_data.csv") else pd.DataFrame({"날짜": [], "메모": []})

        new_memo = pd.DataFrame({"날짜": [selected_date], "메모": [input_memo]})
        memo_data = pd.concat([memo_data, new_memo], ignore_index=True)

        memo_data.to_csv("memo_data.csv", index=False)

        st.write("메모가 저장되었습니다.")

    if os.path.isfile("memo_data.csv"):
        memo_data = pd.read_csv("memo_data.csv")
        st.write("저장된 메모:")
        st.table(memo_data)
    else:
        st.write("저장된 메모가 없습니다.")

    if st.button("메모 삭제"):
        if os.path.isfile("memo_data.csv"):
            memo_data = pd.read_csv("memo_data.csv")
            memo_data = memo_data.drop(memo_data[memo_data["날짜"] == str(selected_date)].index)
            memo_data.to_csv("memo_data.csv", index=False)
            st.write("메모가 삭제되었습니다.")

expander2 = st.expander("체크리스트")
with expander2:
    st.header("체크 리스트")

    checklist_data = pd.read_csv("checklist_data.csv") if os.path.isfile("checklist_data.csv") else pd.DataFrame({"내용": [], "완료": []})

    new_item = st.text_input("체크리스트 항목을 입력하세요")

    if st.button("추가"):
        if new_item:
            new_item_data = pd.DataFrame({"내용": [new_item], "완료": [False]})
            checklist_data = pd.concat([checklist_data, new_item_data], ignore_index=True)
            st.success("체크리스트 항목이 추가되었습니다.")
            st.text("")

    st.header("체크리스트")
    for index, row in checklist_data.iterrows():
        checkbox_label = row["내용"]
        completed = st.checkbox("", value=row["완료"], key=index)
        checklist_data.at[index, "완료"] = completed
        st.markdown(f"- {checkbox_label}")

        if st.button("삭제", key=f"delete_button_{index}"):
            checklist_data = checklist_data.drop(index)
            st.success("체크리스트 항목이 삭제되었습니다.")

    checklist_data.to_csv("checklist_data.csv", index=False)

expander3 = st.expander("그림판")
with expander3:
    st.sidebar.title("그리기 도구")
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data)
    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include=['object']).columns:
            objects[col] = objects[col].astype("str")
        st.dataframe(objects)
