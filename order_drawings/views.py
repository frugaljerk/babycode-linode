
from .models import MyBabyDrawings
from .forms import DrawingForm
from game_logs.models import GameDemo, GameCharacter
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# POST REQUEST process order from human code and save to MyBabyDrawing model in order_drawings app.
class OrderDrawingsCreateView(LoginRequiredMixin, CreateView):

    template_name = "order_drawings/order_drawings.html"
    model = MyBabyDrawings
    fields = DrawingForm.fields

    # return to the same path
    def get_success_url(self, **kwargs):
        return self.request.path

    def form_valid(self, form):
        form.instance.game_id = GameDemo.objects.get(pk=self.kwargs["pk"])
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(OrderDrawingsCreateView, self).get_context_data(**kwargs)
        try:
            # Preveiw images
            ctx["mybabydrawings"] = MyBabyDrawings.objects.filter(
                game_id=self.kwargs["pk"], user_id=self.request.user
            ).latest("date_added")

        except:
            # TODO: user has no order. Pass for now
            pass

        ctx["gamedemo"] = GameDemo.objects.get(pk=self.kwargs["pk"])
        ctx["gamecharacter"] = GameCharacter.objects.filter(game=self.kwargs["pk"])

        # Add logics so only required form fields appear as per number of characters in Gamedemo
        for i in range(len(ctx["form"].fields) - ctx["gamedemo"].number_of_characters):
            ctx["form"].fields.popitem()
        # Making the required from fields required = True for validation purpose
        for _ in ctx["form"].fields.values():
            _.required = True
        return ctx
