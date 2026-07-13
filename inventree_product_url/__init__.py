from django.http import HttpResponse
from django.urls import path

from plugin import InvenTreePlugin
from plugin.mixins import EventMixin, SettingsMixin, UrlsMixin


class ProductUrlPlugin(EventMixin, SettingsMixin, UrlsMixin, InvenTreePlugin):
    """Auto-populates a Part's external link with a public product URL."""

    NAME = "ProductUrl"
    SLUG = "producturl"
    TITLE = "Product URL Generator"
    DESCRIPTION = "Automatically generates a public product page URL for parts"
    VERSION = "0.2.0"
    AUTHOR = "Fred Corp."

    SETTINGS = {
        "BASE_URL": {
            "name": "Base URL",
            "description": "Base URL prefix for generated product links (include trailing slash)",
            "default": "https://product.fredcorp.cc/",
        },
        "ID_SOURCE": {
            "name": "ID Source",
            "description": "Which part field to use as the identifier",
            "choices": [("pk", "Internal ID (PK)"), ("ipn", "IPN")],
            "default": "pk",
        },
        "ID_PADDING": {
            "name": "ID Zero-Padding",
            "description": "Zero-pad the numeric ID to this many digits (only applies to PK source)",
            "validator": int,
            "default": 8,
        },
        "OVERWRITE_EXISTING": {
            "name": "Overwrite Existing Links",
            "description": "Overwrite the part's link field even if already set",
            "validator": bool,
            "default": False,
        },
        "SALEABLE_ONLY": {
            "name": "Saleable Parts Only",
            "description": "Only generate product URLs for parts marked as saleable",
            "validator": bool,
            "default": False,
        },
    }

    # --- shared helpers ---

    def _should_process(self, part):
        if self.get_setting("SALEABLE_ONLY") and not part.salable:
            return False
        return True

    def _build_link(self, part):
        base_url = self.get_setting("BASE_URL")
        source = self.get_setting("ID_SOURCE")

        if source == "ipn" and part.IPN:
            identifier = part.IPN
        else:
            padding = self.get_setting("ID_PADDING")
            identifier = str(part.pk).zfill(padding)

        return f"{base_url}{identifier}"

    # --- event hook (new parts) ---

    def process_event(self, event, *args, **kwargs):
        if event != "part_part.created":
            return

        from part.models import Part

        part = Part.objects.get(pk=kwargs["id"])

        if not self._should_process(part):
            return

        if part.link and not self.get_setting("OVERWRITE_EXISTING"):
            return

        part.link = self._build_link(part)
        part.save()

    # --- backfill endpoint (existing parts) ---

    def backfill_view(self, request):
        if not request.user.is_staff:
            return HttpResponse("Forbidden - staff access required", status=403)

        from part.models import Part

        overwrite = self.get_setting("OVERWRITE_EXISTING")
        qs = Part.objects.all() if overwrite else Part.objects.filter(link="")

        if self.get_setting("SALEABLE_ONLY"):
            qs = qs.filter(salable=True)

        updated = 0
        for part in qs:
            part.link = self._build_link(part)
            part.save()
            updated += 1

        return HttpResponse(
            f"Backfill complete: updated {updated} part(s). "
            f"<a href='/web/settings/admin/plugin/producturl/'>Back to plugin settings</a>"
        )

    def setup_urls(self):
        return [
            path("backfill/", self.backfill_view, name="backfill"),
        ]