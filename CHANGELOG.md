# Changelog

All notable changes to this plugin are documented in this file.

## [0.3.1]

### Fixed

- **Root cause found:** `EventMixin` never worked because InvenTree's `part/events.py` defines no event members for this installed version — no `part.created`-style event is ever fired for Part creation. The plugin now hooks Django's `post_save` signal for the `Part` model directly instead, which is unaffected by this gap and doesn't depend on the "Enable event integration" global setting.

### Changed

- Removed `EventMixin` dependency entirely.
- Note: the Shlink API call (when enabled) now runs synchronously as part of the part-creation request/response cycle, rather than being dispatched to the background worker.

## [0.3.0]

### Added

- Optional Shlink integration: when enabled, automatically creates a matching redirect in a self-hosted [Shlink](https://shlink.io/) instance for every generated product URL, using the same identifier as the custom slug.
- New settings: `SHLINK_ENABLED`, `SHLINK_API_URL`, `SHLINK_API_KEY` (masked), `SHLINK_DEFAULT_LONG_URL`.
- Redirect target selection: if a part already has a manually-set `link` when processed, that link is used as the Shlink redirect destination. Otherwise, `SHLINK_DEFAULT_LONG_URL` is used as a fallback.

### Changed

- **Behavior change:** `OVERWRITE_EXISTING` now only governs whether an *already plugin-generated* link (one starting with `BASE_URL`) gets regenerated. Parts with a manually-set link, or no link at all, are now always processed regardless of this setting — previously, any non-empty `link` field would cause the part to be skipped entirely, silently ignoring manually-entered links at part-creation time.
- Backfill endpoint now targets all parts that don't already carry a plugin-generated link (instead of only parts with a completely empty `link` field), so it also picks up and migrates parts with pre-existing manual links.
- Requests to Shlink are wrapped in error handling; failures are logged as warnings and never block part creation.

### Dependencies

- Added `requests` as a package dependency.

## [0.2.1]

### Fixed

- Fixed the default URL value.

## [0.2.0]

### Added

- `SALEABLE_ONLY` setting to restrict URL generation (and backfill) to parts marked as saleable.
- `/plugin/producturl/backfill/` endpoint (staff-only) to retroactively generate links for existing parts, via `UrlsMixin`.

## [0.1.0]

### Added

- Initial release: `EventMixin`-based auto-generation of a product URL on part creation, stored in the part's `link` field.
- Settings: `BASE_URL`, `ID_SOURCE` (PK or IPN), `ID_PADDING`, `OVERWRITE_EXISTING`.
