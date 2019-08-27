from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/secondpage')
def secondpage():
	return render_template('secondpage.html')

if __name__ == '__main__':
	app.run(debug=True)