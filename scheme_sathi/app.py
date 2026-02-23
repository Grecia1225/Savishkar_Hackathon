from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'POST':
        user = {
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'income': float(request.form['income']),
            'state': request.form['state'],
            'category': request.form['category'],
            'occupation': request.form['occupation']
        }

        # Connect to database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM schemes")
        all_schemes = c.fetchall()
        conn.close()

        eligible = []
        for s in all_schemes:
            _, name, min_age, max_income, gender_req, category_req, occupation_req, benefit, link = s

            # Check age
            if user['age'] < min_age:
                continue
            # Check income
            if user['income'] > max_income:
                continue
            # Check gender
            if gender_req != 'Any' and gender_req != user['gender']:
                continue
            # Check occupation
            if occupation_req != 'Any' and occupation_req != user['occupation']:
                continue
            # Check category (handle multiple categories separated by comma)
            allowed_categories = [c.strip() for c in category_req.split(',')]
            if 'Any' not in allowed_categories and user['category'] not in allowed_categories:
                continue

            # If all checks passed, add to eligible list
            eligible.append({'name': name, 'benefit': benefit, 'link': link})

        return render_template('results.html', schemes=eligible)

    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)