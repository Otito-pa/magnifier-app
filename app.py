from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'HEAD', 'POST'])
def calculate():
    result = None
    username = None
    error = None  # Initialize error variable
    
    if request.method == 'POST':
        try:
            # Retrieve form data
            username = request.form['username']
            microscope_size = float(request.form['microscope_size'])
            magnification = float(request.form['magnification'])
            
            # Validate magnification
            if magnification == 0:
                error = "Magnification cannot be zero"
            else:
                # Perform the calculation
                result = f"{microscope_size / magnification:.2f}"
                
        except ValueError:
            error = "Please enter valid numbers"
    
    # For 'HEAD' requests, you can just return a minimal response without rendering the template
    if request.method == 'HEAD':
        return '', 200  # Empty response with status code 200
    
    # For 'GET' and 'POST' requests, render the template with results or errors
    return render_template('microscope.html', 
                         result=result, 
                         username=username,
                         error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
