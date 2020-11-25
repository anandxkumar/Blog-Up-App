from flaskblog import create_app

app = create_app()

if __name__=="__main__": #if code runs from this file
    app.run(host='127.0.0.9',port=4455,debug=True) 
    
    
