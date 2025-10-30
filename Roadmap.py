import os
import google.generativeai as genai
from dotenv import load_dotenv
import markdown

load_dotenv()

def markdown_to_html(markdown_text):
    html_body = markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Gemini Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #fafafa;
                color: #111;
                max-width: 850px;
                margin: 40px auto;
                padding: 25px;
                border-radius: 10px;
                background-color: #fff;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}
            h1, h2, h3 {{
                color: #2563eb;
                margin-top: 1.5em;
            }}
            strong {{ color: #000; }}
            ul, ol {{ margin-left: 25px; }}
            hr {{ margin: 2em 0; border: none; height: 1px; background: #ddd; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    return html_page

def generate(data):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        f"""{data}""",
        system_instruction=(
            "You are a Leetcode profile analyser who analyses leetcode profiles and helps users get better at DSA for interviews. "
            "You will receive prompt in a json format which will contain the user's leetcode profile data."
        ),
        # You may add generation_config here if you want to set temperature, max_output_tokens, etc.
    )
    markdown_text = response.text
    return markdown_to_html(markdown_text)
