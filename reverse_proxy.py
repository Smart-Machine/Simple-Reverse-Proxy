import time
import flask 
import threading 
import requests

client_product_list = []
server_product_list = []

threads_number = 3
senders_run = False
recievers_run = False

app = flask.Flask(__name__)

@app.post("/api/update")
def listen_client():
    global client_product_list 
    global senders_run
    response = flask.request.json
    if response.get('status') == 'success': 
        if not senders_run: 
            for thread in senders:
                thread.start()
            senders_run = True 
    else:
        # print(f"recieved {response}")
        client_product_list.append(response)
    return flask.jsonify({
        "status": "success"
    })

@app.post("/api/return")
def listen_server():
    global server_product_list 
    global recievers_run
    response = flask.request.json
    if response.get('status') == 'success':
        if not recievers_run:
            for thread in recievers:
                thread.start()
            recievers_run = True
    else:
        server_product_list.append(response)
    return flask.jsonify({
        "status": "success"
    })

def send_products_sever():
    """
        Sends the products that the user wants to update to the server.
    """
    while len(client_product_list):
        product = client_product_list.pop()
        print(f"SENDING {product} to SERVER")
        requests.post(
            "http://localhost:9003/api/",
            json=product
        )
        time.sleep(1)
    else: 
        requests.post(
            "http://localhost:9003/api/",
            json={"status": "success"}
        )

def send_products_client():
    """
        Sends back to the user the products, which was pushed.
    """
    global server_product_list
    while len(server_product_list):
        product = server_product_list.pop()
        print(f"SENDING {product} to CLIENT")
        requests.post(
            "http://localhost:9001/api/",
            json=product
        )
        time.sleep(1)
    else:
        requests.post(
            "http://localhost:9001/api/",
            json={"status": "success"}
        )


if __name__ == '__main__':
    senders = [threading.Thread(target=send_products_sever) 
                    for _ in range(threads_number)]
    recievers = [threading.Thread(target=send_products_client)
                    for _ in range(threads_number)]


    app.run(host='127.0.0.1', port=9002, threaded=True)