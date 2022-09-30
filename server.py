import time
import flask
import threading 
import requests
import products

list_of_products = products.ListOfProducts(
    products.Product(
        name="Wyze Cam",
        unit_price=34.02,
        quantity=14
    ),
    products.Product(
        name="DJI Drone",
        unit_price=909.00,
        quantity=4
    ),
    products.Product(
        name="Owl 3",
        unit_price=1098.85,
        quantity=3
    )
)

threads_number = 3
extractors_run = False

app = flask.Flask(__name__)

@app.post("/api/")
def handle_post():
    global list_of_products 
    global extractors_run
    response = flask.request.json
    if response.get('status') == 'success':
        print("[INFO] Recieved a package of new Products.")
        if not extractors_run:
            for thread in extractors:
                thread.start()
            extractors_run = True
    else:
        list_of_products.add(response)
    return flask.jsonify({
        "status": "success"
    })

def send_list_of_products():
    global list_of_products
    while len(list_of_products):
        product = list_of_products.pop()
        requests.post(
            "http://localhost:9002/api/return",
            json={
                'name': product.name,
                'price': product.unit_price,
                'quantity': product.quantity
            }
        )
        time.sleep(1)
    else:
        print("ALL PRODUCTS SEND BACK")
        requests.post(
            "http://localhost:9002/api/return",
            json={"status": "success"}
        )
    
if __name__ == '__main__':
    extractors = [threading.Thread(target=send_list_of_products)
                        for _ in range(threads_number)]

    app.run(host='127.0.0.1', port=9003, threaded=True)
