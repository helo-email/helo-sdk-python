# Templates

Manage templates for sending.

| Method | HTTP request | Description |
| ------ | ------------ | ----------- |
| [**templates.list**](#list) | **GET** /templates |  |
| [**templates.create**](#create) | **POST** /templates |  |
| [**templates.render_draft**](#render_draft) | **POST** /templates/render |  |
| [**templates.retrieve**](#retrieve) | **GET** /templates/{id} |  |
| [**templates.update**](#update) | **PATCH** /templates/{id} |  |
| [**templates.delete**](#delete) | **DELETE** /templates/{id} |  |
| [**templates.render**](#render) | **POST** /templates/{id}/render |  |

## list

`GET /templates`

Fetch a paginated list of templates.

```python Templates_list
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

paginated_response_of_template_summary = client.templates.list(limit=10, offset=10)
```

## create

`POST /templates`

Create a new template.

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

Render ad-hoc template content (Subject/Html/Text) with sample data, without persisting anything.

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

Fetch a single template.

```python Templates_retrieve
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

template = client.templates.retrieve("550e8400-e29b-41d4-a716-446655440000")
```

## update

`PATCH /templates/{id}`

Update an existing template.

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

Delete a template.

```python Templates_delete
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

client.templates.delete("550e8400-e29b-41d4-a716-446655440000")
```

## render

`POST /templates/{id}/render`

Render a saved template with sample data.

```python Templates_render
import sdk_helo_email as helo

client = helo.Helo()  # reads HELO_API_KEY from the environment

render_template = client.templates.render(
    "550e8400-e29b-41d4-a716-446655440000",
    inline_styles=True,
)
```
