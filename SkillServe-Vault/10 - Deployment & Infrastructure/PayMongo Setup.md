---
type: deployment
tags: [deployment, payments, paymongo, secrets]
sources: [backend/config/payments.php, backend/app/Modules/Payments, backend/app/Modules/Commissions/Services/CommissionQrPaymentService.php]
---
# PayMongo Setup

> [!info] What PayMongo is for (since 2026-10-11)
> **One thing:** a provider paying their own commission with a dynamic QR Ph code
> ([[ADR-022 Payment QR Codes Without Holding Customer Money]]). Bookings never use PayMongo — the
> customer pays the provider directly ([[ADR-021 Direct Payment with Provider-Remitted Commission]]),
> and `config/payments.php` maps both booking methods to the manual gateway unconditionally.
>
> It is the only way to pay the commission in the app. With no key set, providers are told to contact
> support;
> `php artisan paymongo:status` says "QR Ph payments are off". Section 1 is the rotation runbook
> for an exposed key (`PENDING_FIXES.md` → **C5**, done 2026-09-30).

| Variable | What it is | Where it comes from |
|---|---|---|
| `PAYMONGO_SECRET_KEY` | API credential (`sk_test_…` / `sk_live_…`) | Dashboard → Developers |
| `PAYMONGO_ALLOW_LIVE` | Safety catch: an `sk_live_` key is refused unless this is true | Set by hand; leave `false` |
| `PAYMONGO_WEBHOOK_SECRET` | Webhook signing secret (`whsk_…`) | Returned when the webhook endpoint is created |

`APP_URL` must also be the real backend URL — the customer's return link is built from it.

> [!danger] Never in Vercel
> Vercel runs the admin web, which never talks to PayMongo. A secret in a Vercel `VITE_` variable is
> **bundled into the JavaScript served to every visitor**.

There is no public key: payment intents are created server-side, so the publishable key is never
needed.

## 1. Rotate a compromised key

Anyone holding an `sk_live_` key can charge, refund and create webhooks on the account, so a key
that has been pasted anywhere shared is burned and must be replaced.

Dashboard → **Developers → API Keys**. A *Viewing live data* toggle switches the page between the
test keys (`sk_test_` / `pk_test_`) and the live ones (`sk_live_` / `pk_live_`) — make sure the
right mode is showing before regenerating, because they are separate keys. Regenerate, confirm, then
enter the OTP sent to the registered email or mobile number. The page afterwards shows when the keys
were last regenerated.

> [!warning] Button wording not verified first-hand
> PayMongo retired their "Regenerating API keys" page during a docs restructure (it now 404s), so
> the exact label on the regenerate control could not be confirmed. The location — Developers → API
> Keys — is current. If the control cannot be found there, ask support@paymongo.com; rotation is a
> standard request.

Rotating **invalidates the old key immediately**. That costs nothing here, because nothing uses the
key: both payment methods route to the manual gateway whether or not one is set.

Take the key out of Render **before** regenerating, so no deploy is briefly holding a burned
credential, and confirm with `php artisan paymongo:status`.

### Confirming the old key is dead

```bash
php artisan paymongo:status --probe-key
```

Paste the old key at the prompt — it is not echoed, not logged and not stored. The command asks
PayMongo to read a payment intent that cannot exist: a rejected key answers **401** whatever it is
asked for, and anything else means the key is still accepted and rotation has not taken effect.

### After rotating an exposed live key

Check the account for anything the holder of the old key may have done — in particular, list the
webhooks and delete any endpoint that is not SkillServe's:

```bash
curl https://api.paymongo.com/v1/webhooks -u "sk_NEW_KEY:"
```

A webhook pointed at somebody else's server would leak every payment event.

## 2. Create the webhook and get its secret

**Dashboard:** Developers → Webhooks → *Add endpoint* → enter the URL and events → Save. PayMongo
then displays the endpoint's secret key.

**API:**

```bash
curl -X POST https://api.paymongo.com/v1/webhooks \
  -u "sk_test_YOUR_ROTATED_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"data":{"attributes":{
        "url":"https://YOUR-BACKEND.onrender.com/api/webhooks/paymongo",
        "events":["payment.paid","payment.failed","qrph.expired"]}}}'
```

The response's `data.attributes.secret_key` (`whsk_…`) is `PAYMONGO_WEBHOOK_SECRET`. It is a
different value from the API key, and swapping the two makes every webhook fail verification.

`payment.paid`, `payment.failed` and `qrph.expired` are the events the processor acts on. A
commission is settled only on `payment.paid` whose amount and currency match what was due; a
mismatch is left for a reviewer under Commissions → Provider payments.

Existing webhooks can be listed again later with `GET /v1/webhooks`, which returns `secret_key` as
part of the webhook resource.

## 3. Order of operations

There is a chicken-and-egg: the webhook cannot be registered until the endpoint exists, and the
endpoint refuses everything until it has the secret.

1. **Deploy first** with no PayMongo variables set. Nothing breaks and nothing charges.
2. **Register the webhook** against the deployed URL and keep the `whsk_…` value.
3. **Set the variables in Render** (`sk_test_` first). The provider app then shows *Pay with QR
   code* on the Commission screen. Bookings are unaffected (ADR-021).
4. **Rehearse in test mode:** a provider with an outstanding commission opens *Pay with QR code*;
   pay it with PayMongo's test flow; the webhook confirms it and the block lifts.
5. **Go live deliberately:** swap in `sk_live_` and the live webhook secret, and set
   `PAYMONGO_ALLOW_LIVE=true`. Pay one small real commission end to end before relying on it.

## 4. Test mode first

Use `sk_test_` until a payment has gone through end to end. `sk_live_` charges real cards on a flow
nobody has exercised, so `PayMongoClient` **refuses a live key outright** and logs it as critical
unless `PAYMONGO_ALLOW_LIVE=true` is set as well — one variable should never be all that stands
between a typo and real money. The code derives live/test from the key prefix and verifies the
matching signature segment (`li=` vs `te=`), so switching later needs no code change.

## Troubleshooting

| Symptom | Cause |
|---|---|
| Webhook returns 401 | `PAYMONGO_WEBHOOK_SECRET` missing, or the API key was pasted into it by mistake |
| 401 only in production | Live keys configured but the webhook was created in test mode, so the `li=` segment does not match |
| Commission QR paid but still blocked | The webhook never arrived (check the URL and that the events include `payment.paid`), or PayMongo's amount did not match — see Commissions → Provider payments for the reason |
| App shows no *Pay with QR code* | No usable key: unset, or a live key without `PAYMONGO_ALLOW_LIVE`. `php artisan paymongo:status` says which |
| 502 "We could not create a QR code" | PayMongo refused the request (e.g. QR Ph not enabled on the account); the attempt is closed and can be retried |
| Customer returns but nothing happened | Expected — the return redirect is not trusted; only the webhook records payment |
| 502 on pay | PayMongo refused the request; the response carries their own message |
| 502 "PayMongo is not available." | A live key is configured without `PAYMONGO_ALLOW_LIVE`. The log has a `critical` line; the key is never logged |
| 422 on pay, always | Expected. Both methods route to the manual gateway, so no booking is payable online (ADR-021) |

## Related

[[ADR-022 Payment QR Codes Without Holding Customer Money]] · [[ADR-020 PayMongo Collects Into the Platform Account]] · [[Payments and Refunds]] ·
[[Render Backend Service]] · [[Secrets and Environment]] · [[Go-Live Checklist]]
