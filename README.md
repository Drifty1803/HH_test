
# Marketplace API

This is a test task


## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd marketplace-api
```

2. Install dependencies using poetry:
```bash
poetry install
```
3. Run the API server:
```bash
poetry run uvicorn app.main:app --reload
```

## API Usage

Access the API documentation at http://127.0.0.1:8000/docs.

Use the following endpoints to manage products and categories:

### Products Endpoints

    POST /products/ - Add a new product.
    GET /products/ - Retrieve all products (supports filtering and pagination).
    GET /products/{id} - Retrieve a product by ID.
    PUT /products/{id} - Update an existing product.
    DELETE /products/{id} - Delete a product by ID.

### Categories Endpoints

    POST /categories/ - Add a new category.
    GET /categories/ - Retrieve all categories.
    GET /categories/{id} - Retrieve a category by ID.
    PUT /categories/{id} - Update an existing category.
    DELETE /categories/{id} - Delete a category by ID.
## Running Tests

Run tests with pytest:

```bash
poetry run pytest

```

