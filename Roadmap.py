import os
import google.generativeai as genai
from google.generativeai import types
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
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""{data}""",
        config=types.GenerateContentConfig(
            system_instruction="you are a Leetcode profile Analyser who analysis leetcode profiles and help user get better at dsa for interviews. You will receive prompt in a json format while will contain a user's leetcode profile data like[No of ques solved , contest history ,no of ques topic wise]etc. you have to analyse that data and give response which tells. Things that user am doing wrong or mistakes user am making how can user improve on that what are some good things about user profile etc then you have to give a 6 weeks roadmap which tells week wise what to do which question or topics to solve how to solve some good resources to look up eg, Neetcode 150 , striver etc. and last also tell the expected outcomes of that 6 weeks roadmap. You have to be very raw and honest",
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    markdown_text = response.text
    return markdown_to_html(markdown_text)





