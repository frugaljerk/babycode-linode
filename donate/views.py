
from users.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from game_logs.models import GameDemo
from order_drawings.models import MyBabyDrawings
from order_codes.models import MyBabyCodes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.fields.files import ImageField
from .forms import ConfirmForm
from django.views.generic.edit import FormMixin
import datetime
import pytz
from users.forms import UserUpdateForm, ProfileUpdateForm
from babycode import settings
import stripe
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def index(request):
    # generic donate page at homepage navbar
    return render(request, "donate/index.html")


def charge(request):
    # charge set out by stripe API

    if request.method == "POST":
        print("Data:", request.POST)

        amount = int(request.POST["amount"])

        customer = stripe.Customer.create(
            email=request.POST["email"],
            name=request.POST["nickname"],
            source=request.POST["stripeToken"],
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency="cad",
            description="Donation",
        )

    return redirect(reverse("donate:success", args=[amount]))


def successMsg(request, args):
    # donated amount
    amount = args
    # set timezone for datetime.min
    utc = pytz.UTC
    # logics for successpage to take user back to previous/latest order: machine or human
    try:
        draw_order = MyBabyDrawings.objects.filter(user_id=request.user.id).latest(
            "date_added"
        )
        draw_order_time = draw_order.date_added
    except MyBabyDrawings.DoesNotExist:
        draw_order = None
        draw_order_time = utc.localize(datetime.datetime.min)
    try:
        machine_order = MyBabyCodes.objects.filter(user_id=request.user.id).latest(
            "date_added"
        )
        machine_order_time = machine_order.date_added
    except MyBabyCodes.DoesNotExist:
        machine_order = None
        machine_order_time = utc.localize(datetime.datetime.min)

    # logics for successpage to take user back to previous/latest order: machine or human
    if machine_order == None and draw_order == None:
        context = {
            "amount": amount
        }
    elif draw_order_time > machine_order_time:
        context = {
            "amount": amount,
            "draw_game_id": draw_order.game_id.id,
        }
    else:
        context = {
            "amount": amount,
            "machine_game_id": machine_order.game_id.id,
        }

    return render(request, "donate/success.html", context)


# Donate page wher user can download their game zipfile.
class MachineCodeDonateView(LoginRequiredMixin, DetailView):
    model = GameDemo
    template_name = "donate/machinecode.html"

    def get_context_data(self, **kwargs):
        ctx = super(MachineCodeDonateView, self).get_context_data(**kwargs)
        try:

            # Preveiw images
            order = MyBabyCodes.objects.filter(
                game_id=self.kwargs["pk"], user_id=self.request.user
            ).latest("date_added")
            imgList = [
                x
                for x in order._meta.fields
                if type(x) == ImageField and getattr(order, x.name)
            ]
            ctx["mybabycodes"] = [getattr(order, x.name) for x in imgList]
            ctx["gamefile"] = getattr(order, "gamefile")
            ctx["game_id"] = getattr(order, "game_id")

        except:
            # TODO: user has no order. Pass for now
            pass

        return ctx


# Get confirmation of drawing ordr and terms of service at HumanCode donate page.
class HumanCodeDonateView(LoginRequiredMixin, FormMixin, DetailView):
    model = GameDemo
    template_name = "donate/humancode.html"
    form_class = ConfirmForm

    def get_success_url(self):
        return reverse("profile")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConfirmForm(request.POST)

        if form.is_valid():
            # check how many pending orders(confirmed by user, but status not ready).And set a max of three pending orders for now.
            # order not saved confirmed if exceeded three and return to profile page with error message
            pending_order_count = MyBabyDrawings.objects.filter(
                user_id=self.request.user, status=False, confirm_status=True
            ).count()
            if pending_order_count >= 2:
                user_orders = MyBabyDrawings.objects.filter(
                    user_id=request.user.id, confirm_status=True
                ).order_by("-date_added")
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                context = {
                    "error": "Sorry. You have exceeded maximum Drawing Orders of Two.",
                    "user_orders": user_orders,
                    "u_form": u_form,
                    "p_form": p_form,
                }
                return render(request, "users/profile.html", context)

            order = MyBabyDrawings.objects.filter(
                game_id=self.kwargs["pk"], user_id=self.request.user
            ).latest("date_added")

            order.confirm_status = True
            order.save()

            # Send a confirmation email to user

            email_subject = f"New BabyCode Order: #{order.order_id}"
            user = User.objects.get(pk = request.user.id)
            email_user = [user.email]
            email_message = f"""
            Dear {request.user},
            
            Thank you for ordering BabyCode Draw. Estimated completion time is 2 weeks. 
            You will be notified via Email once your order is ready.
            If you have any questions, feel free to contact us with your order id {order.order_id}.
            Thank you,
            babycodes.canada@gmail.com
            (604)760-6289
            The BabyCode Team.
    
            """
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                email_user,
            )





            return redirect("profile")
        else:

            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super(HumanCodeDonateView, self).get_context_data(**kwargs)
        try:
            # Preveiw images

            order = MyBabyDrawings.objects.filter(
                game_id=self.kwargs["pk"], user_id=self.request.user
            ).latest("date_added")
            imgList = [
                x
                for x in order._meta.fields
                if type(x) == ImageField and getattr(order, x.name)
            ]
            ctx["mybabydrawings"] = [getattr(order, x.name) for x in imgList]

        except:
            # TODO: user has no order. Pass for now
            pass

        return ctx
