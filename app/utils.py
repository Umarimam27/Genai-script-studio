from transformers import pipeline

print("Loading AI model... please wait ⏳")

generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

def generate_script(prompt, genre, creativity, length_option,
                    director_style=None, sub_director=None, scene_mode=None):

    # ---------- LENGTH LOGIC ----------
    if length_option == "Short":
        max_tokens = 350
        min_tokens = 120
    elif length_option == "Medium":
        max_tokens = 600
        min_tokens = 250
    else:
        max_tokens = 900
        min_tokens = 400

    # ---------- STYLE INJECTION ----------
    style_line = ""

    if director_style and director_style != "Normal":
        style_line += f"Write in {director_style} cinematic style. "

    if sub_director:
        style_line += f"Follow storytelling of {sub_director}. "

    if scene_mode and scene_mode != "Full Movie":
        style_line += f"Generate only the {scene_mode}. "

    # ---------- PROMPT ----------
    style_prompt = style_line + f"""
Create a detailed {genre} movie screenplay with characters,
acts, dialogues and emotional storytelling.

Write AT LEAST 8 paragraphs.
Each paragraph must have 4–5 sentences.
Do not end early.

Movie Idea: {prompt}
"""

    # ---------- GENERATION ----------
    result = generator(
        style_prompt,
        max_length=max_tokens,
        min_length=min_tokens,
        temperature=creativity,
        repetition_penalty=1.4,
        do_sample=True
    )

    return result[0]["generated_text"]
def generate_characters(prompt, genre, director_style=None, sub_director=None):

    style_line = ""

    if director_style and director_style != "Normal":
        style_line += f"Write in {director_style} cinematic style. "

    if sub_director:
        style_line += f"Follow storytelling style of {sub_director}. "

    char_prompt = style_line + f"""
Create compelling characters for a {genre} movie.

Movie Idea: {prompt}

Generate:
- Hero (Name + Personality)
- Villain (Name + Motivation)
- Supporting Character 1
- Supporting Character 2
- Mentor or Twist Character

Keep each description 2–3 lines.
Be cinematic and creative.
"""

    result = generator(
        char_prompt,
        max_length=350,
        temperature=0.9,
        repetition_penalty=1.3,
        do_sample=True
    )

    return result[0]["generated_text"]
