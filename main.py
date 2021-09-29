from flask import Flask, render_template, escape, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'frewg t34251twerg6165'
    

@app.route('/')
def home():
    return render_template(escape('index.html'))


@app.route('/<string:url>')
def dynamic(url):
    return render_template(escape(url))


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        email = data["email"].lower()
        subject = data["subject"].lower()
        text = data["text"].lower()
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS contact(email TEXT,subject TEXT,text TEXT)")
        valid = cur.execute(f"SELECT email FROM contact WHERE email like '{email}'")
        valid = valid.fetchone()
        print(valid)
        if valid is None:
            cur.execute("INSERT INTO contact (email,subject,text) VALUES(?,?,?)", (email, subject, text))
            con.commit()
            con.close()
            return render_template("thank_you.html")
        else:
            flash("Request already Sent")
            return render_template("invalid.html")


if __name__ == '__main__':
    app.run(debug=True, port=1000)
