# Little Lemon API 🍋

A RESTful API built with **Django REST Framework** for the Little Lemon restaurant application.

This project focuses on backend API development, authentication, role-based permissions, menu management, cart and order workflows, and API data validation using Django REST Framework.

## Technologies

- Python
- Django
- Django REST Framework
- SQLite
- Git & GitHub

## Features

### Menu Management

- List menu items
- Create menu items
- Retrieve individual menu items
- Update menu items
- Delete menu items
- Filter menu items by category and featured status
- Search by menu item title and category title
- Order results by price or title

### User Roles & Permissions

The API uses Django Groups to implement role-based access control.

There are three application roles:

- **Manager**
- **Delivery Crew**
- **Customer**

Custom DRF permissions are implemented for each role.

### Manager Management

Managers can:

- View users assigned to the Manager group
- Add users to the Manager group
- Remove users from the Manager group

### Delivery Crew Management

Managers can:

- View users assigned to the Delivery Crew group
- Add users to the Delivery Crew group
- Remove users from the Delivery Crew group

### Cart Management

Customers can:

- View their cart
- Add menu items to their cart
- Store item quantity and pricing information
- Clear their cart

The cart automatically calculates the item price using:

```text
price = unit_price × quantity
```

Each user can have a menu item only once in their cart.

### Order Management

Customers can:

- Create orders from their cart
- View their own orders

When an order is created:

- The current cart items are converted into order items
- The order total is calculated automatically
- The current date is stored
- The cart is cleared after the order is created

Managers can:

- View all orders
- Assign delivery crew members to orders
- Update order status
- Delete orders

Delivery crew members can:

- View orders assigned to them
- Update the order status

## API Endpoints

### Menu

| Method    | Endpoint           | Description          |
| --------- | ------------------ | -------------------- |
| GET       | `/menu-items`      | List menu items      |
| POST      | `/menu-items`      | Create a menu item   |
| GET       | `/menu-items/<id>` | Retrieve a menu item |
| PUT/PATCH | `/menu-items/<id>` | Update a menu item   |
| DELETE    | `/menu-items/<id>` | Delete a menu item   |

### Manager Group

| Method | Endpoint                     | Description                          |
| ------ | ---------------------------- | ------------------------------------ |
| GET    | `/groups/manager/users`      | List manager users                   |
| POST   | `/groups/manager/users`      | Add a user to the Manager group      |
| DELETE | `/groups/manager/users/<id>` | Remove a user from the Manager group |

### Delivery Crew Group

| Method | Endpoint                           | Description                                |
| ------ | ---------------------------------- | ------------------------------------------ |
| GET    | `/groups/delivery-crew/users`      | List delivery crew users                   |
| POST   | `/groups/delivery-crew/users`      | Add a user to the Delivery Crew group      |
| DELETE | `/groups/delivery-crew/users/<id>` | Remove a user from the Delivery Crew group |

### Cart

| Method | Endpoint           | Description                            |
| ------ | ------------------ | -------------------------------------- |
| GET    | `/cart/menu-items` | View the authenticated customer's cart |
| POST   | `/cart/menu-items` | Add a menu item to the cart            |
| DELETE | `/cart/menu-items` | Clear the customer's cart              |

### Orders

| Method    | Endpoint       | Description                                            |
| --------- | -------------- | ------------------------------------------------------ |
| GET       | `/orders`      | Retrieve orders based on the authenticated user's role |
| POST      | `/orders`      | Create an order from the customer's cart               |
| GET       | `/orders/<id>` | Retrieve an individual order                           |
| PUT/PATCH | `/orders/<id>` | Update an order based on user role                     |
| DELETE    | `/orders/<id>` | Delete an order                                        |

## Data Models

The project contains the following main models:

### Category

Stores menu categories.

- `id`
- `slug`
- `title`

### MenuItem

Represents an item available on the restaurant menu.

- `id`
- `title`
- `price`
- `featured`
- `category`

### Cart

Stores items selected by a customer.

- `user`
- `menuitem`
- `quantity`
- `unit_price`
- `price`

A unique constraint prevents the same menu item from being added more than once for the same user.

### Order

Represents a customer's order.

- `user`
- `delivery_crew`
- `status`
- `total`
- `date`

### OrderItem

Stores the individual menu items belonging to an order.

- `order`
- `menuitem`
- `quantity`
- `unit_price`
- `price`

## Serializers

The API uses Django REST Framework ModelSerializers.

### MenuItemSerializer

The category is returned as nested read-only data while `category_id` is accepted when creating or updating a menu item.

### CartSerializer

The following fields are calculated or controlled by the server:

- `user`
- `unit_price`
- `price`

### OrderSerializer

The following fields are read-only:

- `user`
- `total`
- `date`

This prevents clients from directly controlling calculated order information.

## Permissions

Custom permission classes are implemented using Django REST Framework's `BasePermission`.

### IsManager

Allows access to authenticated users who belong to the `Manager` group.

### IsDeliveryCrew

Allows access to authenticated users who belong to the `Delivery crew` group.

### IsCustomer

Allows authenticated users who are not members of the `Manager` or `Delivery crew` groups.

## API Query Features

The menu endpoint supports:

### Filtering

Filter by:

```text
category
featured
```

### Searching

Search by:

```text
title
category__title
```

### Ordering

Order by:

```text
price
title
```

## Project Structure

```text
LittleLemon/
│
├── LittleLemonAPI/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── littlelemon/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md
```

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/karenamgad/little-lemon-api.git
```

Navigate into the project:

```bash
cd little-lemon-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install django djangorestframework django-filter
```

Apply database migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Learning Focus

This project was built to practice backend development concepts including:

- Django models
- Model relationships
- Django REST Framework
- Generic API views
- Serializers
- Serializer validation and field control
- Authentication
- Custom permissions
- Django Groups
- Role-based access control
- CRUD operations
- Filtering
- Searching
- Ordering
- Cart and order workflows
- HTTP status codes
- Database relationships
- API design

## Author

**Karen Amgad**
GitHub: [@karenamgad](https://github.com/karenamgad)
