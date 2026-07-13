from plugin import InvenTreePlugin
from plugin.mixins import EventMixin, SettingsMixin


class ProductUrlPlugin(EventMixin, SettingsMixin, InvenTreePlugin):
    """Auto-populates a Part's external link with a public product URL on creation."""

    NAME = "ProductUrl"
    SLUG = "producturl"
    TITLE = "Product URL Generator"
    DESCRIPTION = "Automatically generates a public product page URL for new parts"
    VERSION = "0.1.0"
    AUTHOR = "Fred Corp."

    SETTINGS = {
        "BASE_URL": {
            "name": "Base URL",
            "description": "Base URL prefix for generated product links (include trailing slash)",
            "default": "https://your.domain.com/",
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
    }

    def process_event(self, event, *args, **kwargs):
        if event != "part_part.created":
            return

        from part.models import Part

        part = Part.objects.get(pk=kwargs["id"])

        if part.link and not self.get_setting("OVERWRITE_EXISTING"):
            return

        base_url = self.get_setting("BASE_URL")
        source = self.get_setting("ID_SOURCE")

        if source == "ipn" and part.IPN:
            identifier = part.IPN
        else:
            padding = self.get_setting("ID_PADDING")
            identifier = str(part.pk).zfill(padding)

        part.link = f"{base_url}{identifier}"
        part.save()
