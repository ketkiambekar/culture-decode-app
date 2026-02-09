from flask import Flask, render_template, request
from dotenv import load_dotenv
import vibescanner as vs
import os

app = Flask(__name__)
#app.config["DEBUG"]=True

print(os.getcwd())


@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@app.route('/result', methods=['POST'])
def analyze():
    try:
        load_dotenv()
        scanner = vs.VibeScanner(api_key=os.getenv("API_KEY"))
        jd_text =  (request.form.get("jd_text"))
        response = scanner.analyze_jd(jd_text=jd_text)        
        
        if response is None:
            raise Exception("Something went wrong. Please try again.")        
        
        
        return  render_template('/index.html',message=response)
    except Exception as e:
        return render_template('/index.html', message="Please check your inputs: "+str(e) )
 
if __name__ == '__main__':
   app.run()