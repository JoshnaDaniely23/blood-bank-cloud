from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

home_page = '''
<!DOCTYPE html>
<html>
<head>
<title>Blood Bank Cloud</title>
<style>
body { font-family: Arial; text-align: center; background: #e6f2ff; }
.box { margin-top: 100px; }
a { padding: 12px 25px; background: #007BFF; color: white; text-decoration: none; margin: 10px; display: inline-block; border-radius: 5px;}
</style>
</head>
<body>
<div class="box">
<h1>🩸 Cloud Blood Bank System</h1>
<a href="/register">Register Donor</a>
<a href="/search">Search Blood</a>
</div>
</body>
</html>
'''

register_page = '''
<!DOCTYPE html>
<html>
<head>
<title>Register</title>
</head>
<body>
<h2>Register Donor</h2>
<form method="post" action="/submit">
<input type="text" name="name" placeholder="Name" required><br><br>
<input type="text" name="blood" placeholder="Blood Group" required><br><br>
<input type="text" name="location" placeholder="Location" required><br><br>
<input type="text" name="phone" placeholder="Phone" required><br><br>
<button type="submit">Register</button>
</form>
</body>
</html>
'''

search_page = '''
<!DOCTYPE html>
<html>
<head>
<title>Search</title>
</head>
<body>
<h2>Search Blood</h2>
<form method="post">
<input type="text" name="blood" placeholder="Enter Blood Group">
<button type="submit">Search</button>
</form>

{% if data %}
<h3>Results:</h3>
<ul>
{% for row in data %}
<li>{{ row['name'] }} - {{ row['blood'] }} - {{ row['location'] }} - {{ row['phone'] }}</li>
{% endfor %}
</ul>
{% endif %}

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/register')
def register():
    return render_template_string(register_page)

@app.route('/submit', methods=['POST'])
def submit():
    donor = {
        "name": request.form['name'],
        "blood": request.form['blood'].upper(),
        "location": request.form['location'],
        "phone": request.form['phone']
    }
    data = load_data()
    data.append(donor)
    save_data(data)
    return "✅ Registered Successfully"

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        blood = request.form['blood'].upper()
        all_data = load_data()
        data = [d for d in all_data if d['blood'] == blood]
    return render_template_string(search_page, data=data)

if __name__ == '__main__':
    app.run(debug=True)