
CREATE TABLE customerregions (
    id VARCHAR(255) PRIMARY KEY,
    region VARCHAR(255)
);

CREATE TABLE orders (
    order_id VARCHAR(255) PRIMARY KEY,
    status VARCHAR(255),
    date TIMESTAMP,
    amount DECIMAL(10, 2),
    customer_region_id VARCHAR(255),
    FOREIGN KEY (customer_region_id) REFERENCES customerregions(id)
)

