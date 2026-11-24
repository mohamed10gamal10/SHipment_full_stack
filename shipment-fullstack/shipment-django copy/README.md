# Shipment Management API — Django REST Framework

Converted from the supplied Java + Spring Boot project to Python + Django REST Framework.

## Stack
- Python / Django
- Django REST Framework
- Simple JWT authentication
- Django ORM
- MySQL (optional) or SQLite for local development
- Django local-memory cache

## Architecture mapping

| Spring Boot | Django |
|---|---|
| `@Entity` | Django `models.Model` |
| Spring Data `Repository` | Django ORM QuerySets / Managers |
| `@RestController` | DRF API Views |
| DTO | DRF Serializer |
| Service / ServiceImpl | `services.py` |
| Spring Security | DRF permissions + JWT |
| JJWT | Simple JWT |
| `@Cacheable` | Django cache framework |
| Pageable | DRF PageNumberPagination |

## Setup

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS

python manage.py makemigrations accounts customers shipments
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

By default the project uses SQLite so it runs immediately. To use MySQL, edit `.env` and set `DB_ENGINE=mysql`, then provide `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`. Install the MySQL client dependency for your platform.

## Authentication

### Register
`POST /auth/registeruser`

```json
{
  "username": "gamal",
  "email": "gamal@example.com",
  "password": "StrongPass123"
}
```

Public registration always assigns the `customer` role. A client cannot register itself as admin or delivery.

### Login
`POST /auth/loginuser`

```json
{
  "email": "gamal@example.com",
  "password": "StrongPass123"
}
```

Response includes `access`, `refresh`, and user details. Send the access token on protected requests:

`Authorization: Bearer <access-token>`

### Current user
`GET /auth/me`

## Main endpoints

| Method | Endpoint | Access |
|---|---|---|
| POST | `/auth/registeruser` | Public |
| POST | `/auth/loginuser` | Public |
| POST | `/auth/token/refresh` | Public |
| GET | `/auth/me` | Authenticated |
| POST | `/Customer/ADD` | Customer |
| GET | `/Customer/me` | Authenticated (own profile, 404 if not created yet) |
| GET | `/Customer/get` | Admin |
| GET | `/Customer/getuser/{customer_id}` | Own profile or Admin |
| POST | `/Shipment/add` | Authenticated customer with profile |
| GET | `/Shipment/Get` | Own shipments; Admin sees all |
| GET | `/Shipment/{shipment_id}` | Owner or Admin |
| GET | `/Customer/admin/getall` | Admin |
| POST | `/Customer/admin/add` | Admin |

## Create customer profile

After registering, create the customer profile using `POST /Customer/ADD`:

```json
{
  "name": "Mohamed Gamal",
  "phone": "+201000000000",
  "address": "Fayoum",
  "city": "Fayoum",
  "country": "Egypt",
  "gender": "male",
  "whatsapp_number": "+201000000000",
  "birthday": "2003-01-01"
}
```

The profile email is taken from the authenticated account, not from the request.

## Create shipment

`POST /Shipment/add` with a Bearer token:

```json
{
  "name": "Laptop shipment",
  "description": "Handle with care",
  "address_source": "Fayoum",
  "city_source": "Fayoum",
  "address_destination": "Nasr City",
  "city_destination": "Cairo",
  "state_destination": "Cairo",
  "items": [
    {
      "description": "Personal laptop",
      "quantity": 1,
      "price": "25000.00",
      "name": "Laptop",
      "type": "Electronics"
    }
  ]
}
```

## Changes made for the React frontend

1. Added `GET /Customer/me` so the frontend can check whether the logged-in customer already has a profile.
2. `POST /Customer/ADD` and `POST /Shipment/add` now return the saved object (with `id`) instead of the raw request data.

## Important conversion notes

1. The original source contains incomplete methods (customer update/delete) and a few logic issues. Those were not copied as-is.
2. The original Spring Security URL rules are contradictory in ordering. This version applies explicit role and ownership checks.
3. Customer profile data is separate from the login account, while connected by a one-to-one relationship.
4. Delivery and Order domain models are retained. Delivery onboarding/assignment and full order workflows were not exposed by complete endpoints in the source, so they are left as domain models for the next implementation stage.
5. The original JWT secret was hard-coded. This conversion uses Django's environment-based `SECRET_KEY`; set a strong private value in `.env` before deployment.
6. SQLite is the default for a quick first run. MySQL can be enabled using the environment variables above.
