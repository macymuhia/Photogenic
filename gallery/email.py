# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import request


def send_welcome_email(name, receiver):
    # Creating message subject and sender
    subject = "Activate Your Photopedia Account"
    current_site = Site.objects.get_current()
    print(current_site.domain)
    # current_site = get_current_site(request)
    sender = "atst.acc19@gmail.com"

    # passing in the context vairables
    text_content = render_to_string(
        "account_activation_email.txt",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    html_content = render_to_string(
        "account_activation_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
