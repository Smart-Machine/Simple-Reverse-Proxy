import time 
import flask 
import threading 
import requests
import products

list_of_products = [
    products.Product(
        name="Iphone",
        unit_price=1000.00,
        quantity=312
    ),
    products.Product(
        name="Samsung",
        unit_price=432.00,
        quantity=432
    )
]
list_of_recieved_products = []
threads_number = 3

app = flask.Flask(__name__)

@app.get("/")
def display():
    global list_of_products
    global list_of_recieved_products
    return flask.render_template(
        "client.html",
        list_of_products=str(list_of_products),
        list_of_recieved_products=str(list_of_recieved_products)
    )

@app.get("/show/")
def show():
    return flask.redirect(flask.url_for("display"))

@app.get("/start/")
def start():
    for thread in senders:
        thread.start()
    print("The process started")
    return flask.redirect(flask.url_for("display"))

@app.post("/api/")
def handle_received_data():
    global list_of_recieved_products
    response = flask.request.json
    if response.get('status') == 'success':
        print("[INFO] Server got new Products.")
    else:
        product = products.Product(
            name=response.get('name'),
            unit_price=response.get('price'),
            quantity=response.get('quantity')
        )
        list_of_recieved_products.append(product)
    return flask.jsonify({
        "status": "success"
    })

def update_list_of_products():
    global list_of_products
    while len(list_of_products):
        product = list_of_products.pop()
        print(product)
        requests.post(
            "http://localhost:9002/api/update",
            json={
                'name': product.name,
                'price': product.unit_price,
                'quantity': product.quantity
            }
        )
        time.sleep(1)
    else:
        requests.post(
            "http://localhost:9002/api/update",
            json={"status": "success"}
        )

if __name__ == '__main__':
    senders = [threading.Thread(target=update_list_of_products)
                    for _ in range(threads_number)]

    app.run(host='127.0.0.1', port=9001, threaded=True)