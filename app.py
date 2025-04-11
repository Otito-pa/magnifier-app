from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate():
    result = None
    username = None
    
    if request.method == 'POST':
        try:
            username = request.form['username']
            microscope_size = float(request.form['microscope_size'])
            magnification = float(request.form['magnification'])
            
            if magnification == 0:
                error = "Magnification cannot be zero"
            else:
                result = f"{microscope_size / magnification:.2f}"
                
        except ValueError:
            error = "Please enter valid numbers"
    
    return render_template('microscope.html', 
                         result=result, 
                         username=username)

if __name__ == '__main__':
    app.run(debug=True, port=5000)