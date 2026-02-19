import streamlit as st
from utils import generate_script, generate_characters
import base64

st.set_page_config(page_title="Creative Director AI", layout="centered")

# ---------- BACKGROUND UTILITIES ----------
def get_base64_image_url(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    base64_encoded_data = base64.b64encode(bytes_data).decode("utf-8")
    mime_type = uploaded_file.type or "image/png"
    return f"data:{mime_type};base64,{base64_encoded_data}"

def set_cinematic_bg(base64_urls, interval_per_image=6):
    num_images = len(base64_urls)
    if num_images == 0:
        return

    total_duration = num_images * interval_per_image
    overlay = "rgba(0,0,0,0.65)"

    css_keyframes = []
    for i in range(num_images):
        start = (i * 100) / num_images
        hold = start + (100 / num_images)
        css_keyframes.append(f"{start:.2f}% {{ background-image: url('{base64_urls[i]}'); }}")
        css_keyframes.append(f"{hold:.2f}% {{ background-image: url('{base64_urls[i]}'); }}")
    css_keyframes.append(f"100% {{ background-image: url('{base64_urls[0]}'); }}")

    st.markdown(f"""
    <style>
    .stApp {{
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-image: url('{base64_urls[0]}');
        animation: cinematicBg {total_duration}s infinite;
        color:white;
    }}

    @keyframes cinematicBg {{
        {"".join(css_keyframes)}
    }}

    .stApp::before {{
        content:"";
        position:fixed;
        top:0; left:0;
        width:100%; height:100%;
        background:{overlay};
        z-index:0;
    }}

    .result-card {{
        background:#111827;
        padding:20px;
        border-radius:15px;
        border:1px solid #333;
        box-shadow:0px 0px 20px rgba(255,75,75,0.2);
        position:relative;
        z-index:2;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- SIDEBAR BACKGROUND UPLOAD ----------
base64_image_urls = []

with st.sidebar:
    st.header("🎨 Background Images")
    uploaded_files = st.file_uploader(
        "Upload Backgrounds",
        type=["jpg","jpeg","png"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            base64_image_urls.append(get_base64_image_url(file))

set_cinematic_bg(base64_image_urls)

# ---------- TITLE ----------
st.title("🎬 Creative Director AI")

# ---------- IDEA ----------
idea = st.text_input("Enter Movie Idea")

# ---------- DIRECTOR STYLE ----------
director_style = st.selectbox(
    "Director Style",
    ["Normal","Bollywood","Hollywood","Marvel","Horror"]
)

sub_director = None

if director_style == "Bollywood":
    sub_director = st.selectbox(
        "Select Bollywood Director",
        [
            "Karan Johar – Romance / Family Drama",
            "S.S. Rajamouli – Epic Action / Fantasy",
            "Anurag Kashyap – Dark Thriller / Crime",
            "Sanjay Leela Bhansali – Grand Visual Romance",
            "Rohit Shetty – Mass Action / Comedy",
            "Zoya Akhtar – Urban Drama / Coming of Age",
            "Rajkumar Hirani – Emotional Comedy / Social Message",
            "Imtiaz Ali – Deep Romance / Journey Stories",
            "Kabir Khan – War / Patriotism",
            "Ayan Mukerji – Fantasy / Mythology"
        ]
    )

elif director_style == "Hollywood":
    sub_director = st.selectbox(
        "Select Hollywood Director",
        [
            "Christopher Nolan – Mind-Bending Sci-Fi",
            "Steven Spielberg – Adventure / Family Epic",
            "Quentin Tarantino – Stylish Action / Dialogue",
            "James Cameron – Sci-Fi / Visual Spectacle",
            "Martin Scorsese – Crime / Character Drama",
            "Ridley Scott – Historical / Sci-Fi Epic",
            "Peter Jackson – Fantasy / Large Worlds",
            "Denis Villeneuve – Slow-Burn Sci-Fi",
            "David Fincher – Psychological Thriller",
            "Greta Gerwig – Emotional Character Stories"
        ]
    )

# ---------- GENRE ----------
genre = st.selectbox("Genre",[
"Action","Adventure","Comedy","Drama","Fantasy","Horror",
"Romance","Sci-Fi","Thriller","War"
])

# ---------- SCENE MODE ----------
scene_mode = st.radio(
"Scene Mode",
["Full Movie","Opening Scene","Plot Twist","Climax","Ending"]
)

# ---------- CREATIVITY ----------
creativity = st.slider("Creativity",0.5,1.2,0.9,0.1)

# ---------- LENGTH ----------
length_option = st.selectbox("Output Length",["Short","Medium","Long"])

# ---------- GENERATE ----------
if st.button("Generate Script"):
    if idea.strip() != "":
        with st.spinner("🎬 Generating cinematic masterpiece..."):
            result = generate_script(
                idea, genre, creativity, length_option,
                director_style, sub_director, scene_mode
            )

        st.markdown(f"""
        <div class='result-card'>
        <h2>🎬 {genre} Movie</h2>
        <p><b>Director Style:</b> {director_style}</p>
        <p><b>Duration:</b> 2h {len(result)%60}m | Rating: PG-13</p>
        <hr>{result}
        </div>
        """, unsafe_allow_html=True)

        music = "Epic Orchestra" if genre=="Action" else "Emotional Piano"
        st.info(f"🎵 Suggested Music: {music}")

        st.download_button("Download Script", result, "script.txt")

    else:
        st.warning("Enter idea first")
# ---------- CHARACTER GENERATOR ----------
if st.button("🎭 Generate Characters"):
    if idea.strip() != "":
        with st.spinner("Creating cinematic characters..."):
            chars = generate_characters(
                idea, genre, director_style, sub_director
            )

        st.markdown(f"""
        <div class='result-card'>
        <h3>🎭 Movie Characters</h3>
        <hr>{chars}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Enter idea first")

# ---------- FOOTER ----------
st.markdown("<hr><center>Powered by Creative Director AI • Umar Imam</center>",
unsafe_allow_html=True)