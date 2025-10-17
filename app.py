import os
import streamlit as st
from prediction import predict

st.title("Vehicle Damage Detection")

# Use Streamlit's temp directory (safe in cloud)
UPLOAD_DIR = "/tmp/Uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if uploaded_files:
    for image_file in uploaded_files:
        image_path = os.path.join(UPLOAD_DIR, image_file.name)
        with open(image_path, "wb") as file:
            file.write(image_file.getbuffer())

        with st.container():
            st.image(image_file, use_container_width=True)
            try:
                prediction = predict(image_path)
                st.info(prediction)
                st.write("Model can make mistake!!")
            except Exception as e:
                st.error(f"Prediction error: {e}")





