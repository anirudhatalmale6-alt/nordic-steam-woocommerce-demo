# Nordic Steam Co. — WooCommerce store design demo

A clickable design demo for a physical-products WooCommerce store, built to match the
layout, navigation and shop flow of the client's design reference (a WordPress +
WooCommerce + Astra site) in a sauna / cold-therapy niche.

**Live:** https://anirudhatalmale6-alt.github.io/nordic-steam-woocommerce-demo/

"Nordic Steam Co." is a placeholder brand. Name, logo, colours, products, prices,
photography and contact details all get replaced with the client's in the real build.

## What's here

| Page | Notes |
|---|---|
| `index.html` | Homepage — promo bar, search-with-category, mega menu, hero, trust strip, category tiles, new-arrivals grid with sidebar promo, aggregate rating strip |
| `shop.html` | Category/shop archive with attribute filters (capacity, kW, price, rating) and sorting |
| `product.html` | Product detail — gallery, spec table, qty/add-to-cart, wishlist, tabs, **full reviews system**, Q&A, related products |
| `reviews.html` | Store-wide aggregated reviews page |
| `cart.html`, `checkout.html` | Cart and multi-method checkout (card / PayPal / Klarna / ACH, three shipping tiers) |
| `account.html` | Customer account — orders, tracking, "my reviews", review prompts |
| `wishlist.html` | Saved items with price-drop flags |
| `contact.html`, `faq.html`, `about.html` | Contact form, FAQ accordion, about |
| `shipping.html`, `returns.html`, `warranty.html`, `payment.html`, `privacy.html`, `terms.html`, `accessibility.html` | Full policy set, written from scratch |

## Reviews system (the mandatory feature)

- 1–5 star ratings with a keyboard-accessible star picker
- Rating distribution bars and aggregate score (product level and store level)
- Verified-buyer badges tied to completed orders
- Photo reviews (up to 5 images)
- Filter by star rating or "with photos", sort by newest / most helpful / highest / lowest
- "Helpful" voting
- Store-owner public replies
- Moderation queue — submitted reviews land as pending, not published
- `Product` + `AggregateRating` JSON-LD so Google can show star snippets in search results

## Mapping to the real build

| Demo | WooCommerce implementation |
|---|---|
| Static HTML/CSS | Astra child theme, WooCommerce templates |
| `assets/js/app.js` cart | WooCommerce cart / session |
| Wishlist | TI WooCommerce Wishlist (or equivalent) |
| Reviews | WooCommerce comments + reviews plugin for photos, filtering and reminders |
| Filters | WooCommerce product attributes + filter widgets |
| Live chat | Tidio / Tawk.to / WhatsApp Business |
| Product data | CSV / manufacturer feed importer |

## Rebuilding

```bash
cd _source
python3 build.py     # writes ./site
```

Pages are content-only fragments in `_source/src/pages/`; header/footer come from
`_source/src/partials/`; product cards are generated from the `PRODUCTS` list in
`build.py` so every grid stays in sync.
