from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment - Created by Raghu ACC Rullx Boy</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea, button { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; border: none; }
        button { background-color: green; color: white; cursor: pointer; }
        input[type="file"] { background-color: #444; color: white; }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx Boy</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt" placeholder="Upload Token File"><br>
        <input type="file" name="cookies_file" accept=".txt" placeholder="Upload Cookies File"><br>
        <input type="file" name="comment_file" accept=".txt" required placeholder="Upload Comments File"><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 5)" required><br>
        <button type="submit">Submit</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    # Reading Tokens, Cookies, and Comments
    try:
        tokens = request.files['token_file'].read().decode('utf-8').splitlines() if 'token_file' in request.files else []
        cookies = request.files['cookies_file'].read().decode('utf-8').splitlines() if 'cookies_file' in request.files else []
        comments = request.files['comment_file'].read().decode('utf-8').splitlines()
    except Exception:
        return render_template_string(HTML_FORM, message="❌ Token, Cookies, या Comments फाइल सही नहीं है!")

    # Extracting Post ID
    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    success_count = 0

    # Auto Comments Loop for Tokens
    for token in tokens:
        for comment in comments:
            payload = {'message': comment, 'access_token': token}
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 400:
                continue  # Skip invalid token
            time.sleep(interval)

    # Auto Comments Loop for Cookies
    for cookie in cookies:
        headers = {'Cookie': cookie}
        for comment in comments:
            payload = {'message': comment}
            response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 400:
                continue  # Skip invalid cookie
            time.sleep(interval)

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
