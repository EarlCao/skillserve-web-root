---
type: deployment
tags: [deployment, payments, paymongo, secrets]
sources: [backend/config/payments.php, backend/app/Modules/Payments]
---
# PayMongo Setup

How to get GCash working in production. Two values go into Render and nowhere else.

| Variable | What it is | Where it comes from |
|---|---|---|
| `PAYMONGO_SECRET_KEY` | API credential (`sk_test_…` / `sk_live_…`) | Dashboard → Developers |
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

Dashboard → **Developers** → API keys → regenerate. PayMongo confirms, then sends an OTP to the
registered email or mobile number; the dashboard afterwards shows when the keys were last
regenerated.

> [!warning] Not verified first-hand
> PayMongo retired their "Regenerating API keys" documentation page during a docs restructure (it
> now 404s), so the exact button wording may differ from the above. If it cannot be found in the
> Developers section, ask support@paymongo.com — rotation is a standard request.

Rotating **invalidates the old key immediately**. That is free while GCash is still unconfigured,
because nothing is using it yet: with no `PAYMONGO_SECRET_KEY` set, `config/payments.php` routes
GCash to the manual gateway.

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
        "events":["payment.paid","payment.failed"]}}}'
```

The response's `data.attributes.secret_key` (`whsk_…`) is `PAYMONGO_WEBHOOK_SECRET`. It is a
different value from the API key, and swapping the two makes every webhook fail verification.

Only `payment.paid` and `payment.failed` are needed — those are the two the processor acts on.

Existing webhooks can be listed again later with `GET /v1/webhooks`, which returns `secret_key` as
part of the webhook resource.

## 3. Order of operations

There is a chicken-and-egg: the webhook cannot be registered until the endpoint exists, and the
endpoint refuses everything until it has the secret.

1. **Deploy first** with no PayMongo variables set. GCash falls back to manual settlement; nothing
   breaks and nothing charges.
2. **Register the webhook** against the deployed URL and keep the `whsk_…` value.
3. **Set both variables in Render.** Saving restarts the service, and GCash switches on by itself.
4. **Test with a ₱1 booking** — the PayMongo minimum — before trusting it. `payment.paid` should
   arrive within seconds and flip the booking to paid.

## 4. Test mode first

Use `sk_test_` until a booking has been paid end to end. `sk_live_` charges real cards on a flow
nobody has exercised. The code derives live/test from the key prefix and verifies the matching
signature segment (`li=` vs `te=`), so switching later needs no code change — only the variable.

## Troubleshooting

| Symptom | Cause |
|---|---|
| Webhook returns 401 | `PAYMONGO_WEBHOOK_SECRET` missing, or the API key was pasted into it by mistake |
| 401 only in production | Live keys configured but the webhook was created in test mode, so the `li=` segment does not match |
| Booking never becomes paid | The webhook never arrived. Check the endpoint URL and that the events include `payment.paid` |
| Customer returns but nothing happened | Expected — the return redirect is not trusted; only the webhook records payment |
| 502 on pay | PayMongo refused the request; the response carries their own message |

## Related

[[ADR-020 PayMongo Collects Into the Platform Account]] · [[Payments and Refunds]] ·
[[Render Backend Service]] · [[Secrets and Environment]] · [[Go-Live Checklist]]
