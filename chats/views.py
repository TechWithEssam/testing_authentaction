from django.shortcuts import render, redirect
from .models import Chat, Messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from products.models import Product
from accounts.models import User
# Create your views here.



@login_required
def my_chat_view(request) :
    template_name = "chats/messages.html"
    qs = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by("-timestamp")
    is_empty = True
    if len(qs) > 0 :
        is_empty = False
    context = {
        "qs" : qs,
        "is_empty": is_empty
    }
    return render(request, template_name, context)

@login_required
def prived_message_view(request, slug) : 
    template_name = "chats/chat.html"
    try :
        qs = Chat.objects.get(
            Q(slug=slug) & (Q(sender=request.user) | Q(receiver=request.user))
        )
    except :
        return redirect("products:not_found")
    context = {
        "qs" : qs
    }
    return render(request, template_name, context)

@login_required
def contact_buyer_view(request) :
    if request.method == "GET" :
        product_id = request.GET.get("product_id")
        try :
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist :
            return redirect("products:not_found")
        salesman = product.salesman
        obj, _ = Chat.objects.get_or_create(sender=request.user, receiver = salesman, product=product)
        print(obj.slug)
        return redirect("chats:prived_message", obj.slug)
    return redirect(request.META.get('HTTP_REFERER'))

# @login_required
# def send_message_view(request) :
#     if request.method == "POST" or request.FILES :
#         chat_id = request.POST.get("chat_id")
#         text = request.POST.get("text") or None
#         image = request.FILES.get("image") or None
        
#         chat = Chat.objects.get(pk=chat_id)
#         # print(chat)
#         # if text :
#         #     Messages.objects.create(text=text, user=request.user, chat=chat)
#         # elif image :
#         #     Messages.objects.create(image=image, user=request.user, chat=chat)
#         # if image and text :
#         Messages.objects.create(text=text, image=image, user=request.user, chat=chat)
#     return redirect(request.META.get('HTTP_REFERER'))