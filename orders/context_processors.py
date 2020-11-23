from .models import Order


def order_in_profile(request):
    if request.user.is_anonymous:
        return {}
    else:
        orders = Order.objects.filter(user = request.user)
        return {'orders':orders}
