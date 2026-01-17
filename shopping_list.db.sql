-- Таблица 1: Категории товаров
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица 2: Магазины
CREATE TABLE stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT
);

-- Таблица 3: Товары
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    unit TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Таблица 4: Списки покупок
CREATE TABLE shopping_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_date TEXT NOT NULL
);

-- Таблица 5: Позиции в списке покупок
CREATE TABLE list_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    store_id INTEGER,
    quantity REAL NOT NULL,
    is_purchased INTEGER DEFAULT 0,
    FOREIGN KEY (list_id) REFERENCES shopping_lists(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

-- Наполнение тестовыми данными

-- Категории
INSERT INTO categories (name) VALUES ('Овощи и фрукты');
INSERT INTO categories (name) VALUES ('Молочные продукты');
INSERT INTO categories (name) VALUES ('Мясные продукты');
INSERT INTO categories (name) VALUES ('Бакалея');
INSERT INTO categories (name) VALUES ('Напитки');

-- Магазины
INSERT INTO stores (name, address) VALUES ('Пятерочка', 'ул. Ленина, 10');
INSERT INTO stores (name, address) VALUES ('Магнит', 'ул. Советская, 25');
INSERT INTO stores (name, address) VALUES ('Лента', 'пр. Мира, 100');

-- Товары
INSERT INTO products (name, category_id, unit) VALUES ('Яблоки', 1, 'кг');
INSERT INTO products (name, category_id, unit) VALUES ('Молоко', 2, 'л');
INSERT INTO products (name, category_id, unit) VALUES ('Куриное филе', 3, 'кг');
INSERT INTO products (name, category_id, unit) VALUES ('Хлеб', 4, 'шт');
INSERT INTO products (name, category_id, unit) VALUES ('Сок апельсиновый', 5, 'л');
INSERT INTO products (name, category_id, unit) VALUES ('Бананы', 1, 'кг');
INSERT INTO products (name, category_id, unit) VALUES ('Сыр', 2, 'кг');
INSERT INTO products (name, category_id, unit) VALUES ('Говядина', 3, 'кг');
INSERT INTO products (name, category_id, unit) VALUES ('Рис', 4, 'кг');
INSERT INTO products (name, category_id, unit) VALUES ('Минеральная вода', 5, 'л');

-- Списки покупок
INSERT INTO shopping_lists (name, created_date) VALUES ('Покупки на неделю', '2026-01-16');
INSERT INTO shopping_lists (name, created_date) VALUES ('Праздничный стол', '2026-01-20');

-- Позиции в списке покупок (10 тестовых позиций)
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (1, 1, 1, 2.0, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (1, 2, 1, 2.0, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (1, 3, 2, 1.5, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (1, 4, 1, 2.0, 1);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (1, 5, 1, 1.0, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (1, 6, 1, 1.5, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (2, 7, 2, 0.5, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (2, 8, 2, 2.0, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (2, 9, 3, 1.0, 0);
INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased) VALUES (2, 10, 1, 3.0, 1);