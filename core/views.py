from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Membership


# Create your views here.
# @login_required(login_url="/login/")
def home(request):
    membership = Membership.objects.filter(user=request.user).first()

    if membership.status == Membership.status.PENDING:
        return render(request, 'core/pending.html')
    if membership.status == Membership.status.REJECTED:
        return render(request, "core/rejected.html", )
    if membership.status == Membership.status.BANNED:
        return render(request, "core/banned.html")

    is_exec = membership.role in [Membership.Role.OWNER, Membership.Role.ADMIN]

    return render(request, 'core/home.html', {'is_exec': is_exec})

# @login_required(login_url="/login/")
def executive_page(request):
    pass