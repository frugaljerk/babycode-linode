from django.shortcuts import reverse
from django.views.generic import ListView, CreateView
from .models import GameDemo, GameCharacter
from order_drawings.models import MyBabyDrawings
from django.contrib.auth.mixins import LoginRequiredMixin
from order_codes.models import MyBabyCodes
from contact.models import Contact
from .forms import OrderForm
from babycode import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from newsletters.models import NewsletterUser
from .forms import SubscriberForm
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from contact.forms import ContactForm
from django.core.mail import send_mail
from users.models import Guest
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser


# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


# Email confirmation
def confirm(request):
    sub = NewsletterUser.objects.get(email=request.GET["email"])
    if sub.conf_num == request.GET["conf_num"]:
        sub.confirmed = True
        sub.save()
        return render(
            request,
            "game_logs/about.html",
            {
                "confirmed": sub.email,
                "action": "confirmed",
                "contact_form": ContactForm(),
            },
        )
    else:
        return render(
            request,
            "game_logs/about.html",
            {"confirmed": sub.email, "action": "denied", "contact_form": ContactForm()},
        )


def validate_email(request):
    email = request.POST.get("email", None)
    if NewsletterUser.objects.filter(email=email).count() > 0:
        res = JsonResponse({"msg": "Sorry, this email has been used."})
    else:
        res = JsonResponse({"msg": ""})
    return res


# Create your views here.
def index(request):
    """The home page for game logs"""
    game_demos = GameDemo.objects.order_by("date_added")
    context = {"game_demos": game_demos}
    return render(request, "game_logs/index.html", context)


def about(request):

    """The about page to explain the site"""

    # Email subscribe POST (for newsletter) and Contact POST (for contact with questions) all pass into this ABOUT page
    if request.method == "POST":
        # try if request.Post['email'] or request.POST['contact_email'] exist then act accordingly
        try:
            sub = NewsletterUser(
                email=request.POST["email"],
                name=request.POST["name"],
                conf_num=random_digits(),
            )
            sub.save()
            # Email confirmtion link to subscriber
            message = Mail(
                from_email=settings.EMAIL_HOST_USER,
                to_emails=sub.email,
                subject="Newsletter Confirmation",
                html_content='Thank you {} for signing up for my BabyCode newsletter! \
                       Please complete the process by \
                       <a href="{}/?email={}&conf_num={}"> clicking here to \
                       confirm your registration</a>.'.format(
                    sub.name,
                    request.build_absolute_uri("/confirm"),
                    sub.email,
                    sub.conf_num,
                ),
            )

            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)


            response = sg.send(message)
            return render(
                request,
                "game_logs/about.html",
                {
                    "email": sub.email,
                    "action": "added",
                    "form": SubscriberForm(),
                    "contact_form": ContactForm(),
                },
            )

        except:
            # email Contact information and messages to Admin Email: frugal_jerk@outlook.com
            contact = Contact(
                contact_email=request.POST["contact_email"],
                contact_subject=request.POST["contact_subject"],
                contact_message=request.POST["contact_message"],
            )
            contact.save()

            email_subject = f"New BabyCode Contact: {request.POST['contact_subject']}. Email: {request.POST['contact_email']}"
            email_message = request.POST["contact_message"]
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                settings.ADMIN_EMAILS,
            )

            return render(
                request,
                "game_logs/about.html/",
                {
                    "contact_subject": contact.contact_subject,
                    "form": SubscriberForm(),
                    "contact_form": ContactForm(),
                },
            )

    else:
        return render(
            request,
            "game_logs/about.html",
            {"form": SubscriberForm(), "contact_form": ContactForm()},
        )

    # return render(request, 'game_logs/about.html')


class GameDemoListView(ListView):
    model = GameDemo
    template_name = "game_logs/index.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "game_demos"
    ordering = ["-date_added"]

#LoginRequiredMixin
# POST REQUEST process order from machine code and save to MyBabyCode model in order_codes app.
class GameDetailCreateView(CreateView):

    template_name = "game_logs/detail.html"
    model = MyBabyCodes
    fields = OrderForm.fields

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("donate:machinecode", kwargs={'pk': pk})


    def form_valid(self, form):
        form.instance.game_id = GameDemo.objects.get(pk=self.kwargs["pk"])

        # use device cookie to create BabyOrders
        device = self.request.COOKIES['device']
        guest, created = Guest.objects.get_or_create(device=device)
        form.instance.user_id = guest

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(GameDetailCreateView, self).get_context_data(**kwargs)
        ctx["gamedemo"] = GameDemo.objects.get(pk=self.kwargs["pk"])
        ctx["gamecharacter"] = GameCharacter.objects.filter(game=self.kwargs["pk"])

        # Add logics so only required form fields appear as per number of characters in Gamedemo
        for i in range(len(ctx["form"].fields) - ctx["gamedemo"].number_of_characters):
            ctx["form"].fields.popitem()
        # Making the required from fields required = True for validation purpose
        for _ in ctx["form"].fields.values():
            _.required = True
        return ctx
