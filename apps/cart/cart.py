from django.conf import settings
from apps.posts.serializers import PostSerializer
from apps.posts.models import Post

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def __iter__(self):
        post_ids = list(self.cart.keys())
        posts = Post.objects.filter(id__in=post_ids)

        for post in posts:
            post_data = PostSerializer(post).data
            self.cart[str(post.id)]['post_data'] = post_data

        for item in self.cart.values():
            post_data = item['post_data']
            item['total_price'] = float(item['price']) * int(item['quantity'])
            item.update(post_data)
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def add(self, post, quantity=1, update_quantity=False):
        post_id = str(post.id)
        price = post.price

        if post_id not in self.cart:
            self.cart[post_id] ={
                'quantity' : quantity,
                'price': price,
                'slug': post.slug,
                'cover_photo': str(post.cover_photo.url) if post.cover_photo else None
            }
        elif update_quantity:
            self.cart[post_id]['quantity'] = quantity
        else:
            self.cart[post_id]['quantity'] += quantity

        self.session.modified =True

        self.save()

    def has_post(self, post_id):
        return str(post_id) in self.cart
    
    def remove(self, post_id):
        if str(post_id) in self.cart:
            del self.cart[str(post_id)]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_length(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def get_total_cost(self):
        return sum(float(item['price']) * int(item['quantity']) for item in self.cart.values())
        