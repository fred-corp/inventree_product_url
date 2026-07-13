# InvenTree Product URL Generator

A quick plugin for InvenTree that automatically generates product URLs for new parts.

This plugin is meant to be used in conjunction with a shortlink service (like [Shlink](https://shlink.io/) or [tinyurl.com](https://tinyurl.com/)) to create short, human-readable product links for your products, that redirect to a longer URL (like a product page on your e-commerce site).

## Usage

Once installed, the plugin automatically generates a product URL for new parts, based on the configured **Base URL** and **ID Source**. The generated URL is stored in the part's `link` field.

### Enabling event integration

This plugin relies on InvenTree's event system to detect newly created parts. After activating the plugin, go to **Settings → Plugin Settings** and make sure **"Enable event integration"** is turned on globally — the plugin won't do anything on part creation until this is enabled. A server restart is recommended after toggling it.

### Rendering the URL as a QR code on labels

The plugin only populates the `link` field — it doesn't touch label templates. To print the generated URL as a scannable QR code, add the following to your part label template:

```html
{% load barcode %}
<img class='qr' src='{% qrcode part.link %}'>
```

Since `link` holds a plain URL rather than InvenTree's internal barcode format, any standard phone camera or QR scanner will resolve it directly — no InvenTree app required on the scanning end.

### Behavior on existing links

By default, the plugin never overwrites a `link` that's already set — whether it was set manually or by a previous run of this plugin. See **Overwrite Existing Links** below to change that.

## Installation

1. In the admin plugin page, click "Install Plugin"
2. Type `inventree-product-url` in the plugin field.
3. Type `git+https://github.com/fred-corp/inventree_product_url.git` in the "Source URL" field.
4. (optional) Type a tag for a specific version in the "Version" field.
5. Check "Confirm plugin installation" and click "Install Plugin".
6. Restart InvenTree.

## Plugin Settings

Configure these from **Admin → Plugins → Product URL Generator** in InvenTree.

| Setting                       | Description                                                                                                                                                                             | Default                     |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| **Base URL**                  | Prefix prepended to the generated identifier to build the full product URL. Include the trailing slash.                                                                                 | `https://your.domain.com/`  |
| **ID Source**                 | Which part field to use as the identifier: `Internal ID (PK)` or `IPN`. If `IPN` is selected but a part has no IPN set, it falls back to the padded PK.                                 | `Internal ID (PK)`          |
| **ID Zero-Padding**           | Number of digits to zero-pad the PK to (only applies when ID Source is `PK`).                                                                                                           | `8`                         |
| **Overwrite Existing Links**  | If enabled, regenerates and overwrites `link` even if a part already has one set — including links set manually. If disabled (default), parts with an existing link are left untouched. | `False`                     |
| **Saleable Parts Only**       | If enabled, only parts marked as **Salable** get a generated link — both for new parts and for the backfill below.                                                                      | `False`                     |

## Backfilling Existing Parts

New parts get their `link` field populated automatically on creation. To apply the same logic retroactively to parts that already existed before this plugin was installed, visit (while logged in as a staff user):

```txt
https://your.inventree.instance/plugin/producturl/backfill/
```

This respects the current **Overwrite Existing Links** and **Saleable Parts Only** settings above. By default it only fills in parts with an empty `link` field, so it's safe to run repeatedly.

## License & Acknowledgements

Made with ❤️, lots of ☕️, and lack of 🛌  
Published under CreativeCommons BY-SA 4.0

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)  
This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
