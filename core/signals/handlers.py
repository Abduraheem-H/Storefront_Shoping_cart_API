from django.conf import settings
from store.signals import order_created
from django.dispatch import receiver


@receiver(order_created)
def handle_order_created(sender, order, **kwargs):
    # Handle the order created signal
    # can be overridden to send confirmation email, update inventory, etc.
    print(
        f"Order created with ID: {order.id} for Customer ID: {order.customer.id}"
    )  # Example action
