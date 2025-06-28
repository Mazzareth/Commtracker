import os
import hmac
import hashlib
import threading
import logging
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .utils import perform_update

logger = logging.getLogger("updater.webhook")

def _get_webhook_secret():
    return (
        os.environ.get("GITHUB_WEBHOOK_SECRET")
        or getattr(settings, "GITHUB_WEBHOOK_SECRET", None)
    )

def _verify_signature(request):
    secret = _get_webhook_secret()
    if not secret:
        return True  # No secret set, skip verification.
    signature = request.META.get("HTTP_X_HUB_SIGNATURE_256")
    if not signature or not signature.startswith("sha256="):
        logger.warning("Signature missing or invalid format.")
        return False
    mac = hmac.new(secret.encode(), msg=request.body, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    if not hmac.compare_digest(signature, expected):
        logger.warning("GitHub webhook signature mismatch.")
        return False
    return True

@csrf_exempt
def github_webhook(request):
    if not _verify_signature(request):
        return HttpResponseForbidden("Invalid signature")

    event = request.META.get("HTTP_X_GITHUB_EVENT", "")
    if event == "ping":
        return HttpResponse("pong", status=200)
    elif event == "push":
        t = threading.Thread(target=perform_update)
        t.daemon = True
        t.start()
        return HttpResponse("update triggered", status=202)
    else:
        return HttpResponse("ignored", status=200)