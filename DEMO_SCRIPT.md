# SkillServe — Defense Demo Script

A rehearsed, end-to-end walkthrough on the **deployed** system: two phones and the admin web,
about 20 minutes. Every step says who acts, where, and what the audience should see. Button and
page names are the real ones in the app and admin web.

> Rehearse it at least once on the deployed stack before the defense, and record each step's result
> in the Result column of `TEST_PLAN.md` (admin) and the Flutter repo's `TEST_PLAN.md` (mobile).
> Never run `scripts/fresh-demo.sh` against production — it wipes the database.

## Cast

| Role | Device | Account |
|---|---|---|
| **Admin** | Laptop, admin web | The super-admin from `ADMIN_EMAIL` / `ADMIN_PASSWORD` on Render |
| **Customer** | Phone A, SkillServe app | Registered during preparation (a real inbox — the OTP is emailed) |
| **Provider** | Phone B, SkillServe app | Registered during preparation (a second real inbox) |

Production has no demo accounts (`SEED_MODE=admin-only` creates only the super-admin), so the
categories are created in the admin web and the customer and provider are created through the app,
which also demonstrates registration.

---

## Part 0 — Preparation (the day before, ~20 min)

Do these once; they are not part of the live demo unless you want to show registration.

| # | Who | Where | Do | Expect |
|---|---|---|---|---|
| 0.0 | Admin | Admin web → **Service Categories** | Create **Appliance Repair** (and any others you want to show) | Enabled categories appear in the app's Explore |
| 0.1 | Admin | Admin web → **System Settings** → Policies | Fill in Terms of Service, Privacy Policy, Community Guidelines. Save. | Saved; the app's policy screens show the text |
| 0.2 | Admin | **Dashboard** → Commission card → **Standard** → **Apply rates** | Apply the Standard preset | Rates read ₱0–199.99 5% · ₱200–499.99 10% · ₱500–999.99 15% · ₱1,000+ 20% |
| 0.3 | Provider | Phone B → Register (role **Provider**) → email OTP | Create the provider account | Lands on provider onboarding |
| 0.4 | Provider | **Provider onboarding** / **Verification status** | Upload the verification documents and submit | Status *pending* |
| 0.5 | Admin | **Provider Management** → the provider → approve verification | Approve | Provider gets a notification; status *verified* |
| 0.6 | Provider | Profile → **GCash details** | Save a GCash number and account name | Saved |
| 0.7 | Provider | Services → **Availability** | Publish hours covering the demo time (e.g. Mon–Sun 08:00–18:00) | Saved |
| 0.8 | Provider | Services → **Add Service** | "Aircon Cleaning" in **Appliance Repair**, fixed price **₱500**, 2 hours | Status pending approval. At the Standard rates SkillServe's share is 15% (₱75) and the provider keeps ₱425 |
| 0.9 | Admin | **Services** → the service → Approve | Approve | Provider notified; the service appears in the app's catalog |
| 0.10 | Customer | Phone A → Register (role **Customer**) → email OTP | Create the customer account | Lands on the customer home |

**Check before the demo:** Customer can find "Aircon Cleaning" under Explore; Provider's Home shows
no outstanding commission; both phones have notifications allowed.

---

## Part 1 — A GCash job from booking to settled commission (~10 min)

| # | Who | Where | Do | Expect |
|---|---|---|---|---|
| 1.1 | Customer | Explore → Aircon Cleaning → Book | Tomorrow 10:00, payment **GCash**, address and contact | Booking created, status **pending**; Phone B gets a new-booking notification |
| 1.2 | Customer | Bookings → the booking → **Reschedule** | Move it to 14:00 | Still **pending** (a confirmed booking also returns to pending); Phone B notified of the new time |
| 1.3 | Provider | Bookings → the request → **Accept request** | Accept | **confirmed**; Phone A notified |
| 1.4 | Provider | Same booking → **Start job**, then **Mark as completed** | Do the job | **active**, then **completed**; Phone A notified each time |
| 1.5 | Customer | Booking details | Show the payment card | Provider's **GCash number, account name, amount ₱500 and the booking number as reference**, with **Copy GCash number**. SkillServe never holds the money (ADR-021) |
| 1.6 | Provider | Booking details → **Payment received** | Record that the customer paid | Payment **paid**; the ₱75 commission becomes **outstanding** |
| 1.7 | Provider | Profile → **Commissions** | Show the debt | ₱75 owed on one booking; account blocked from new work |
| 1.8 | Customer, then Provider | Book the service again; Provider taps **Accept request** | Try to take new work | Refused: *"Settle your outstanding commission before taking on new work."* Finishing agreed jobs is never blocked |
| 1.9 | Admin | **Commissions** → Commissions & Payments → the booking → **Settle** | Method GCash, a reference | Commission **settled**; Phone B gets *Commission payment recorded … You have no outstanding commission.* and 1.8's booking can now be accepted |
| 1.10 | Admin | **Dashboard** → Commission card | Show it | **Collected ₱75 · 15% of ₱500** in settled bookings; the active rates listed |

> Optional (M8): in **System Settings** → Marketplace, set *Block providers once unpaid commission
> reaches* to ₱200 and show that a ₱75 debt no longer blocks. Set it back to 0 afterwards.

---

## Part 2 — Review, report and moderation (~4 min)

| # | Who | Where | Do | Expect |
|---|---|---|---|---|
| 2.1 | Customer | The completed booking → **Leave a review** | 5 stars and a comment | Review appears on the provider's profile; the service rating reads 5.0, and the provider rating is the average of its service ratings |
| 2.2 | Customer | Booking details → **Report an issue** | Report the provider, with a reason | *Report submitted*, with a reference number |
| 2.3 | Admin | **Reports and Moderation** → the report | Investigate, then take an action (e.g. a **warning**) and resolve | Status moves pending → investigating → resolved; the provider is notified of the warning |
| 2.4 | Admin | **Reviews and Ratings** → the review → Hide, then Restore | Moderate the review | Hidden from the app, then back; the rating recalculates each time; the reviewer is notified |

---

## Part 3 — A dispute (~3 min)

Uses the booking from step 1.8 (accepted after 1.9).

| # | Who | Where | Do | Expect |
|---|---|---|---|---|
| 3.1 | Provider | That booking → **Start job** | Start it | **active** |
| 3.2 | Customer | Booking details → **Raise a dispute** | A reason, and a photo as evidence | Booking **disputed**, dispute **pending**; Phone B notified |
| 3.3 | Admin | **Dispute Management** → the booking | **Investigate**, add a note, view the evidence photo, then **Resolve** with a resolution | Dispute **resolved**, booking **completed**; both phones notified |

---

## Part 4 — Admin wrap-up (~3 min)

| # | Who | Where | Do | Expect |
|---|---|---|---|---|
| 4.1 | Admin | **Dashboard** | Walk through the summary cards, the charts and the commission card | Counts include the demo's users, bookings and reports |
| 4.2 | Admin | **Reports** → **General report (Excel)** | Download it | One workbook: Summary sheet, then Users, Providers, Services, Bookings, Reviews, System Activity and Commissions |
| 4.3 | Admin | **Security & Audit** | Filter to today | Every admin action from the demo — approvals, settlement, moderation, dispute — with who did it and when |
| 4.4 | Both phones | Notifications | Open the list | Every step above left a notification; tapping one deep-links to the booking |

---

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Booking refused with 422 about hours | Time outside the provider's published hours | Pick a time inside them (0.7) |
| Booking refused with 409 | Overlaps another booking of the provider | Pick another slot |
| "Accept request" refused at 1.3 | An earlier rehearsal left a commission outstanding | Settle it in **Commissions** first |
| Provider cannot add a service | Not yet verified, or a commission is outstanding | Do 0.5, or settle |
| No payment card at 1.5 | No GCash number saved, or the booking is not GCash | Do 0.6; book with GCash |
| Notifications late on a phone | Closed-app notifications are polled (WorkManager) | Keep the app open during the demo |
| First request very slow | Render instance waking up | Open the admin web and the app 5 minutes before starting |

For a second rehearsal, register fresh customer and provider accounts, or delete the old ones and
purge them in **Data Management**; do not wipe the production database.

## Talking points (D3)

Monolith (Laravel API + React admin web) with a separate Flutter client · Sanctum tokens with
rotating mobile refresh tokens · Spatie roles and permissions, enforced by the API · realtime via
Laravel Reverb instead of Firebase · closed-app notifications via WorkManager polling with a
read-only token · uploads on a Render persistent disk · every admin action audit-logged · SkillServe
never holds customer money: the provider is paid directly and remits the commission (ADR-021).
