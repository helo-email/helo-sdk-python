# Templates

Manage templates for sending.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**templates.list**](#list) | **GET** /templates | List all templates |
| [**templates.create**](#create) | **POST** /templates | Create a template |
| [**templates.render_draft**](#render_draft) | **POST** /templates/render | Render template content |
| [**templates.retrieve**](#retrieve) | **GET** /templates/{id} | Retrieve a template |
| [**templates.update**](#update) | **PATCH** /templates/{id} | Update a template |
| [**templates.delete**](#delete) | **DELETE** /templates/{id} | Delete a template |
| [**templates.render**](#render) | **POST** /templates/{id}/render | Render a template |

## list

`GET /templates`

Retrieves a paginated list of templates, optionally filtered by name or channel.

```python Templates_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_template_summary = client.templates.list(limit=10, offset=10)
```

## create

`POST /templates`

Creates a new template from HTML, MJML, or plain-text content. MJML is compiled to HTML when the template is saved.

```python Templates_create
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

template = client.templates.create(
    name="test-name",
    subject="test-subject",
    html="test-html",
    mjml="test-mjml",
    text="test-text",
    channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
)
```

## render_draft

`POST /templates/render`

Renders unsaved template content (subject, HTML or MJML, and text) with sample data, without persisting anything.

```python Templates_renderDraft
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

render_template = client.templates.render_draft(
    subject="test-subject",
    html="test-html",
    mjml="test-mjml",
    text="test-text",
    inline_styles=True,
)
```

## retrieve

`GET /templates/{id}`

Fetches the details and content of a specific template.

```python Templates_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

template = client.templates.retrieve("550e8400-e29b-41d4-a716-446655440000")
```

## update

`PATCH /templates/{id}`

Modifies an existing template. Only the provided fields are changed.

```python Templates_update
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

template = client.templates.update(
    "550e8400-e29b-41d4-a716-446655440000",
    name="test-name",
    subject="test-subject",
    html="test-html",
    mjml="test-mjml",
    text="test-text",
    channel_ids=["550e8400-e29b-41d4-a716-446655440000"],
    version=10,
)
```

## delete

`DELETE /templates/{id}`

Permanently removes a template. This action cannot be undone.

```python Templates_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.templates.delete("550e8400-e29b-41d4-a716-446655440000")
```

## render

`POST /templates/{id}/render`

Renders a saved template with sample data, to preview the output before sending.

```python Templates_render
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

render_template = client.templates.render(
    "550e8400-e29b-41d4-a716-446655440000",
    inline_styles=True,
)
```
