from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Membership


# Create your views here.
@login_required(login_url="/login/")
def home(request):
    membership = Membership.objects.filter(user=request.user).first()

    if membership.status == Membership.status.PENDING:
        return render(request, 'core/pending-approval.html')
    if membership.status == Membership.status.REJECTED:
        return render(request, "core/rejected.html", )
    if membership.status == Membership.status.BANNED:
        return render(request, "core/banned.html")
    return render(request, 'core/org-page.html')
