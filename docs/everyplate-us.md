# EveryPlate US

EveryPlate US uses the same integration as HelloFresh. Install **HelloFresh** through HACS,
then add it in **Settings → Devices & services** and select **EveryPlate (US)** in the country
list. Use your EveryPlate credentials, rather than a HelloFresh login. The account is named
**EveryPlate (US)**; it can coexist with a HelloFresh account.

## Supported scope

The contributor confirmed the following against their EveryPlate US account using the original
local changes:

- Sign-in.
- Viewing menus and saving meal choices.
- Delivery details.
- Opening recipes associated with meals.

The standalone **Recipes** section (recipe catalog and cookbook) and **Account → Food preferences**
are unavailable for EveryPlate US. The card hides those controls and its cookbook filter.
Favorite polling is disabled, including favorite lookups when opening a meal's recipe details.
Calling the unsupported integration actions directly returns an explanatory error without sending
an API request. This does not prevent opening recipe details from a menu or delivery.

Other HelloFresh features have not all been verified on EveryPlate. In particular, these changes
are not evidence of working Market purchases, recurring plan changes, or rescheduling. Treat
those as unverified until tested against EveryPlate. Live fleet tracking remains limited to the
existing supported HelloFresh markets.

## Names and appearance

EveryPlate accounts use **EveryPlate** for the device manufacturer, sidebar label, and automatic
card heading. The card uses the Home Assistant theme accent and omits the HelloFresh logo for
EveryPlate. A card's explicitly configured `title` and custom `logo` URL still apply. No
EveryPlate logo asset is bundled.

The integration remains under the `hellofresh` domain, with `hellofresh.*` actions,
`custom:hellofresh-card`, and the existing sidebar URL. Its HACS listing and integration-level
icon remain HelloFresh because this is one integration supporting both brands. Existing account
and entity identifiers are preserved; existing users may rename an older account title manually.
New EveryPlate accounts suggest entity IDs beginning with `everyplate_us_`.

## Regional behavior

The stored setup key is `everyplate_us`, the website is `https://www.everyplate.com`, the API
country/business-unit parameter is `ER`, and the locale is `en-US`. Geographic metadata remains
US and prices fall back to USD only when the response provides no currency. An explicit response
currency takes precedence. `ER` must not be used as an ISO country code or a locale suffix.

## Validation

Automated tests use made-up data and mocked API responses. They cover authentication routing,
recipe details without cookbook requests, currency fallback, setup and account identity,
unsupported actions, Home Assistant loading, and browser behavior. They do not sign in to or
change a real EveryPlate account. A live regression check of these additions remains useful
before release, especially when upgrading from an existing local installation.
