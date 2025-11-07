from locust import HttpUser, task, between
from random import randint


class ProductUser(HttpUser):
    wait_time = between(1, 5)

    # @task(2)
    # def list_products(self):
    #     print("Listing products")
    #     collection_id = randint(2, 6)
    #     self.client.get(
    #         f"/store/products/?collection_id={collection_id}", name="/store/products/"
    #     )

    # @task(4)
    # def view_product_details(self):
    #     print("Viewing product details")
    #     product_id = randint(1, 100)
    #     self.client.get(
    #         f"/store/products/{product_id}/", name="/store/products/<product_id>/"
    #     )

    # @task(1)
    # def add_to_cart(self):
    #     print("Adding to cart")
    #     product_id = randint(1, 1000)
    #     payload = {"product_id": product_id, "quantity": 1}
    #     self.client.post(
    #         f"/store/cart/{self.cart_id}/items/",
    #         json=payload,
    #         name="/store/cart/items/",
    #     )

    @task(1)
    def say_hello(self):
        self.client.get("/playground/say-hello/", name="/playground/say-hello/")

    # def on_start(self):
    #     # This method is called when a simulated user starts
    #     response = self.client.post("/store/carts/")
    #     self.cart_id = response.json()["id"]
