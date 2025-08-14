from flask import Flask, request, render_template_string
import os
from git import Repo

app = Flask(__name__)

# Folder to store cloned repos
CLONE_DIR = "cloned_repos"
os.makedirs(CLONE_DIR, exist_ok=True)

# HTML Template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Git Repo Manager</title>
</head>
<body>
    <h2>Clone a Git Repository</h2>
    <form method="POST" action="/clone">
        <input type="text" name="repo_url" placeholder="Enter Git Repo URL" size="50" required>
        <button type="submit">Clone</button>
    </form>

    {% if files %}
        <h3>Repository Files:</h3>
        <ul>
        {% for file in files %}
            <li>{{ file }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/clone", methods=["POST"])
def clone_repo():
    repo_url = request.form["repo_url"]
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(CLONE_DIR, repo_name)

    # Clone if not already cloned
    if not os.path.exists(repo_path):
        Repo.clone_from(repo_url, repo_path)

    # Get file list
    files = []
    for root, _, filenames in os.walk(repo_path):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), repo_path))

    return render_template_string(HTML_PAGE, files=files)

if __name__ == "__main__":
    app.run(debug=True)
