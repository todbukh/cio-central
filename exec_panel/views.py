from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from django.shortcuts import redirect

@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def executive_redirect(request):
    return redirect("exec_panel:events:events")
