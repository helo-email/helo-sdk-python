from __future__ import annotations

from datetime import datetime

from pydantic import Field

from .shared import HeloModel, MailType, WebhookEvent


class WebhookHeader(HeloModel):
    """A custom HTTP header to include in webhook deliveries."""

    name: str
    value: str


class CreateWebhookRequest(HeloModel):
    """Request body for creating a new webhook."""

    url: str
    events: list[WebhookEvent]
    channel_id: str | None = None
    additional_headers: list[WebhookHeader] | None = None
    enabled: bool | None = None


class WebhookLastResponse(HeloModel):
    """The most recent delivery outcome recorded for a webhook."""

    status_code: int | None = None
    error: str | None = None
    at: datetime | None = None


class WebhookResponse(HeloModel):
    """Webhook configuration properties."""

    id: str | None = None
    channel_id: str | None = None
    url: str | None = None
    payload_signing_key: str | None = None
    enabled: bool | None = None
    additional_headers: list[WebhookHeader] | None = None
    events: list[WebhookEvent] | None = None
    last_response: WebhookLastResponse | None = None


class PaginationResultOfWebhookResponse(HeloModel):
    """Paginated list of webhooks."""

    results: list[WebhookResponse]
    total_count: int


class UpdateWebhookRequest(HeloModel):
    """Request body for updating a webhook. Only provided fields are changed."""

    url: str | None = None
    events: list[WebhookEvent] | None = None
    channel_id: str | None = None
    additional_headers: list[WebhookHeader] | None = None
    enabled: bool | None = None


class MessageAcceptedWebhookPayload(HeloModel):
    """Payload delivered for the `message-accepted` event."""

    event_type: WebhookEvent
    recipients: list[str]
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class MessageProcessedWebhookPayload(HeloModel):
    """Payload delivered for the `message-processed` event."""

    event_type: WebhookEvent
    recipients: list[str]
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class DeliveredDetails(HeloModel):
    """Details of an `email-delivered` event."""

    response: str | None = None


class EmailDeliveredWebhookPayload(HeloModel):
    """Payload delivered for the `email-delivered` event."""

    event_type: WebhookEvent
    details: DeliveredDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class BouncedDetails(HeloModel):
    """Details of an `email-bounced` event."""

    type_: str | None = Field(default=None, alias="type")
    sub_type: str | None = None
    code: str | None = None


class EmailBouncedWebhookPayload(HeloModel):
    """Payload delivered for the `email-bounced` event."""

    event_type: WebhookEvent
    details: BouncedDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class ClientDetails(HeloModel):
    """The mail client the recipient engaged with the message from."""

    family: str | None = None
    version: str | None = None


class DeviceDetails(HeloModel):
    """The device the recipient engaged with the message from."""

    brand: str | None = None
    family: str | None = None
    model: str | None = None


class OpenedDetails(HeloModel):
    """Details of an `email-opened` event."""

    ip: str | None = None
    country: str | None = None
    country_code: str | None = None
    client: ClientDetails | None = None
    device: DeviceDetails | None = None


class EmailOpenedWebhookPayload(HeloModel):
    """Payload delivered for the `email-opened` event."""

    event_type: WebhookEvent
    details: OpenedDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class ClickedDetails(HeloModel):
    """Details of a `link-clicked` event."""

    link: str | None = None
    ip: str | None = None
    country: str | None = None
    country_code: str | None = None
    client: ClientDetails | None = None
    device: DeviceDetails | None = None


class LinkClickedWebhookPayload(HeloModel):
    """Payload delivered for the `link-clicked` event."""

    event_type: WebhookEvent
    details: ClickedDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class ComplainedDetails(HeloModel):
    """Details of a `recipient-complained` event."""

    type_: str | None = Field(default=None, alias="type")


class RecipientComplainedWebhookPayload(HeloModel):
    """Payload delivered for the `recipient-complained` event."""

    event_type: WebhookEvent
    details: ComplainedDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class UnsubscribedDetails(HeloModel):
    """Details of a `recipient-unsubscribed` event."""

    ip: str | None = None


class RecipientUnsubscribedWebhookPayload(HeloModel):
    """Payload delivered for the `recipient-unsubscribed` event."""

    event_type: WebhookEvent
    details: UnsubscribedDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class ResubscribedDetails(HeloModel):
    """Details of a `recipient-resubscribed` event."""

    ip: str | None = None


class RecipientResubscribedWebhookPayload(HeloModel):
    """Payload delivered for the `recipient-resubscribed` event."""

    event_type: WebhookEvent
    details: ResubscribedDetails | None = None
    recipient: str
    message_id: str
    channel_id: str
    mail_type: MailType
    subject: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None
    timestamp: datetime


class DomainKeyVerifiedPayload(HeloModel):
    """Payload delivered when a domain key is verified."""

    event_type: WebhookEvent
    domain_id: str
    domain_name: str
    dns_record_host: str
    timestamp: datetime


class DomainKeyVerificationFailedPayload(HeloModel):
    """Payload delivered when a domain key verification fails."""

    event_type: WebhookEvent
    domain_id: str
    domain_name: str
    dns_record_host: str
    timestamp: datetime


class ReturnPathDomainVerifiedPayload(HeloModel):
    """Payload delivered when a return path domain is verified."""

    event_type: WebhookEvent
    domain_id: str
    domain_name: str
    dns_record_host: str
    timestamp: datetime


class ReturnPathDomainVerificationFailedPayload(HeloModel):
    """Payload delivered when a return path domain verification fails."""

    event_type: WebhookEvent
    domain_id: str
    domain_name: str
    dns_record_host: str
    timestamp: datetime
