import asyncio
import base64
import streamlit as st
import requests
import uuid

from utils import base64_to_image, make_base64


async def request_image(base64_image_data: str):
    req_id = str(uuid.uuid4())
    payload = {"request_id": req_id, "data": base64_image_data}

    response = requests.request(
        method="POST", url="http://127.0.0.1:8000/image_hologram_sign/", json=payload
    )
    response.raise_for_status()
    print(response.headers)
    response_data = response.json()
    if response_data.get("success"):
        data = response_data.get("data")

        if data["hologram data"].get("success"):
            hologram_image_data = data["hologram data"].get("data")
            temp = []
            for image in hologram_image_data.keys():
                base64_data = hologram_image_data[image].get("crop")
                temp.append(base64_to_image(base64_data))
            data["hologram data"]["data"] = temp

        if data["signature data"].get("success"):
            signature_image_data = data["signature data"].get("Signs")
            temp = []
            for image in signature_image_data:
                base64_data = image["base64"]
                temp.append(base64_to_image(base64_data))
            data["signature data"].pop("Signs")
            data["signature data"].update({"data": temp})

    else:
        print(response_data.get("error_message"))
    return response_data["data"]


st.set_page_config(page_title="Image Analyzer Pro", layout="wide")


def main():
    st.title("🔍 Image Analysis Dashboard")
    st.markdown("---")

    # Use columns to separate "Upload/Preview" from "Results"
    col_input, col_results = st.columns([1, 2], gap="large")

    with col_input:
        st.subheader("1. Source Image")
        uploaded_file = st.file_uploader("Drop your file here", type=["jpg", "png"])

        if uploaded_file:
            # Container adds a nice visual border-like spacing
            with st.container():
                st.image(uploaded_file, caption="Preview", use_container_width=True)

                # Logic
                file_bytes = (
                    uploaded_file.getvalue()
                )  # Use getvalue() to avoid read pointer issues
                base64_string = base64.b64encode(file_bytes).decode("utf-8")

                if st.button(
                    "🚀 Run Analysis", use_container_width=True, type="primary"
                ):
                    with st.spinner("Processing image..."):
                        # Simulate/Run API call
                        api_response = asyncio.run(request_image(base64_string))
                        st.session_state["api_res"] = api_response
                        st.success("Analysis Complete!")

    with col_results:
        st.subheader("2. Analysis Results")

        if "api_res" in st.session_state:
            res = st.session_state["api_res"]

            # Use Tabs to keep the UI clean
            tab1, tab2, tab3 = st.tabs(["📊 Metrics", "✍️ Signatures", "💎 Holograms"])

            with tab1:
                st.write("### Image Quality Data")
                st.json(res["image quality data"])

            with tab2:
                st.write("### Detected Signatures")
                sig_data = res["signature data"]["data"]
                if sig_data:
                    for img in sig_data:
                        st.image(img, use_container_width=True)
                else:
                    st.info("No signatures detected.")

            with tab3:
                st.write("### Hologram Verification")
                holo_data = res["hologram data"]["data"]
                if holo_data:
                    for img in holo_data:
                        st.image(
                            img,
                            use_container_width=True,
                        )
                else:
                    st.info("No holograms detected.")
        else:
            # Placeholder when no data is present
            st.info("Upload an image and click 'Run Analysis' to see results.")


if __name__ == "__main__":
    main()
