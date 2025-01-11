"""
This file is an api interface for sefgh engine.
For ui kindly use ui.py, this file shall run independetly from ui.py and will call the sefgh-engine (acts as middle-ware)
No need to run engine.py seperatly
"""
import json
from flask import Flask, request, Response
import Engine as engine

app = Flask(__name__)

@app.route('/engine',methods=['POST'])
def calling_engine():
    searchDescription = request.data.decode('utf-8') #gives raw data entered by user
    print("raw-data: \n",searchDescription)

    def generate_sse():
        # Send the initial "wait process started!" message
        yield "data: wait process started!\n\n"

        # Process the data using the engine
        output = engine.run(searchDescription)
        print(output)

        # Send the final output as the SSE message
        yield f"data: {json.dumps(output)}\n\n"

    # Return the response as an SSE stream
    return Response(generate_sse(), content_type='text/event-stream')

@app.route('/engineInfo',methods=['GET'])
def engineInfo():
    return str(engine.Info())

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,use_reloader=False)