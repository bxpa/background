import io
import re

import streamlit as st
from PIL import Image

# Page config
st.set_page_config(
    page_title="Hex Wallpaper Generator",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Hide streamlit header and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def is_valid_hex(hex_color):
    """Check if the hex color is valid"""
    pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(pattern, hex_color))


def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])
    try:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def generate_wallpaper(hex_color):
    """Generate a solid color wallpaper"""
    if not is_valid_hex(hex_color):
        return None

    rgb_color = hex_to_rgb(hex_color)
    if rgb_color is None:
        return None

    # Phone dimensions (1080x1920 for most modern phones)
    width, height = 1080, 1920

    # Create image with solid color
    image = Image.new("RGB", (width, height), rgb_color)

    return image


# Main app
st.title("Background generator")

# Input field
hex_input = st.text_input(
    "Hex color", placeholder="#3498db", max_chars=7, label_visibility="collapsed"
)

# Auto-add # if missing
if hex_input and not hex_input.startswith("#"):
    hex_input = "#" + hex_input

# Validation and download
if hex_input:
    if is_valid_hex(hex_input):
        # Generate wallpaper
        wallpaper = generate_wallpaper(hex_input)

        if wallpaper:
            # Convert to bytes for download
            img_buffer = io.BytesIO()
            wallpaper.save(img_buffer, format="PNG")
            img_bytes = img_buffer.getvalue()

            # Download button
            filename = f"{hex_input}.png"
            st.download_button(
                label="Download",
                data=img_bytes,
                file_name=filename,
                mime="image/png",
                use_container_width=True,
            )
    else:
        st.error("Please enter a valid hex color (e.g., #000 or #000000)")
else:
    # Show download button (disabled when no input)
    st.download_button(
        label="Download",
        data=b"",
        file_name="wallpaper.png",
        mime="image/png",
        use_container_width=True,
        disabled=True,
    )
