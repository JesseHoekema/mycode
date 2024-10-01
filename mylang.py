from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# HTML-sjabloon voor de output
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Output</title>
</head>
<body>
    <div>{{ output|safe }}</div>
</body>
</html>
'''

class CustomLang:
    def __init__(self):
        self.html_output = ""

    def SAY(self, level, text):
        if 1 <= level <= 6:
            self.html_output += f"<h{level}>{text}</h{level}>\n"

    def TYPE(self, placeholder):
        self.html_output += f'<input placeholder="{placeholder}">\n'

    def BUTTON(self, text, link):
        self.html_output += f'<button onclick="window.location.href=\'{link}\'">{text}</button>\n'

    def generate_html(self):
        return self.html_output

def parse_my_code(file_path):
    custom_language = CustomLang()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("SAY"):
                parts = line.split('"')
                level = int(parts[0][4])  # Neem het niveau na 'SAY '
                text = parts[1]
                custom_language.SAY(level, text)
            elif line.startswith("TYPE"):
                parts = line.split('"')
                placeholder = parts[1]
                custom_language.TYPE(placeholder)
            elif line.startswith("BUTTON"):
                parts = line.split('"')
                text = parts[1]
                link = parts[2].split('LINK')[1].strip() if 'LINK' in parts[2] else ''
                custom_language.BUTTON(text, link)
    return custom_language.generate_html()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verkrijg het pad van het bestand van de gebruiker
        file_path = request.form['file_path']
        if os.path.exists(file_path) and file_path.endswith('.mycode'):
            output_html = parse_my_code(file_path)
            return render_template_string(HTML_TEMPLATE, output=output_html)
        else:
            return "Ongeldig bestandspad of bestandstype. Zorg ervoor dat het een .mycode bestand is."
    return '''
    <!doctype html>
    <title>Upload een bestand</title>
    <h1>Voer het pad in naar een .mycode bestand:</h1>
    <form method=post>
      <input type=text name=file_path placeholder="Pad naar je .mycode bestand">
      <input type=submit value=Verzend>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
