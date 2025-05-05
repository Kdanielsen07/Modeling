import streamlit as st
import requests

st.set_page_config(page_title="Meshy 2D to 3D Generator")
st.title("🦊 Meshy 2D → 3D Generator")

# Step 1: User input
api_key = st.text_input("🔑 Enter your Meshy API Key", type="password")
uploaded_file = st.file_uploader("📤 Upload a 2D image (JPG or PNG)", type=["jpg", "jpeg", "png"])

# Step 2: Process when both fields are filled
if uploaded_file and api_key:
    if st.button("✨ Generate 3D Model"):
        with st.spinner("Sending your image to Meshy..."):
            try:
                # Clean, stripped-down file payload
                files = {
                    "image": (uploaded_file.name, uploaded_file, "application/octet-stream")
                }

                headers = {
                    "Authorization": f"Bearer {api_key}"
                }

                response = requests.post(
                    "https://api.meshy.ai/v1/image-to-3d",
                    headers=headers,
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()
                    model_url = result.get("model_url", "")
                    if model_url:
                        st.success("🎉 Model created successfully!")
                        st.markdown(f"[📦 Click here to download your model]({model_url})")
                    else:
                        st.error("Model created, but no download link was returned.")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
