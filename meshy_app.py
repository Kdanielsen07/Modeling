import streamlit as st
import requests
import io

st.set_page_config(page_title="Meshy 2D to 3D Generator")
st.title("🦊 Meshy 2D → 3D Generator")

# Get API key
api_key = st.text_input("🔑 Enter your Meshy API Key", type="password")

# Drag and drop image
uploaded_file = st.file_uploader("📤 Upload a 2D image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Generate 3D button
if uploaded_file and api_key:
    if st.button("✨ Generate 3D Model"):
        with st.spinner("Sending to Meshy..."):
            try:
                # Fix for file upload
                file_bytes = uploaded_file.read()
                file_tuple = (uploaded_file.name, io.BytesIO(file_bytes), uploaded_file.type)

                response = requests.post(
                    "https://api.meshy.ai/v1/image-to-3d",
                    headers={"Authorization": f"Bearer {api_key}"},
                    files={"image": file_tuple}
                )

                if response.status_code == 200:
                    result = response.json()
                    model_url = result.get("model_url", "")
                    if model_url:
                        st.success("🎉 Model created!")
                        st.markdown(f"[📦 Click here to download your model]({model_url})")
                    else:
                        st.error("Model created but no link found.")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
