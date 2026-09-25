# Client Payments

All examples and validation details in this file come from the Laravel backend OpenAPI attributes and request validation.

## `POST /api/client/v1/bookings/{booking}/pay`

Available on the customer's own unpaid booking once it is confirmed, active, completed or disputed, and only when the booking's payment method maps to a gateway that collects money (today: `gcash`, once PayMongo is configured). An `on_hand` booking is refused — it is settled in person.

Returns `redirect_url`; send the customer there. The booking becomes paid when PayMongo calls the webhook, **not** when the customer returns, so poll the booking afterwards rather than assuming success.

Tapping pay again returns the same in-flight payment rather than starting a second one.

**Authentication:** Bearer token

### Parameters

| Name | Location | Required | Type / allowed values |
|---|---|---:|---|
| `booking` | path | yes | integer |
| `Idempotency-Key` | header | no | string |

### Request body and validation

No JSON request body.

### Responses

#### HTTP 200: Payment started

```json
{
    "success": true,
    "message": "Payment started.",
    "data": {
        "redirect_url": "https://secure-authentication.paymongo.com/sources?id=src_...",
        "status": "awaiting_next_action",
        "amount": "200.00",
        "currency": "PHP"
    },
    "errors": null,
    "meta": []
}
```

#### HTTP 401: Unauthenticated

Response schema: `see openapi.json`

#### HTTP 403: Not the customer on this booking, or identity not verified

Response schema: `see openapi.json`

#### HTTP 404: Booking not found

Response schema: `see openapi.json`

#### HTTP 409: Already paid

Response schema: `see openapi.json`

#### HTTP 422: Not payable online, or wrong status

Response schema: `see openapi.json`

#### HTTP 502: The payment provider refused the request

Response schema: `see openapi.json`

