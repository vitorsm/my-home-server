
insert into user (id, name, login, password, user_group_id, created_at) values
(2, 'Vitor', 'vitor', '$2b$12$buSIlMGMp8F/bB.gN/OfquPD1MQDqBeEi0Fxq5J6Qd4EypsabFh.e', 1, '2020-09-22 19:56:28.757876'),
(3, 'User 3', 'user3', '$2b$12$61JKNlydwEJYEBXZH1j6suJD2QEnyQS2PY3BSyDxmKLt/uuDouuU.', 2, '2020-09-22 19:56:28.757876'), -- password: pass3
(4, 'User 4', 'user4', '$2b$12$buSIlMGMp8F/bB.gN/OfquPD1MQDqBeEi0Fxq5J6Qd4EypsabFh.e', 3, '2020-09-22 19:56:28.757876');


insert into brand (id, name, is_private, created_by_id, created_at) values
(100, 'Brand 1', 0, 1, '2020-09-22 19:56:28.757876'),
(102, 'Brand 2', 0, 1, '2020-09-22 19:56:28.757876'),
(103, 'Brand 3', 0, 1, '2020-09-22 19:56:28.757876'),
(104, 'Brand 4', 1, 1, '2020-09-22 19:56:28.757876'),
(105, 'Brand 5', 1, 1, '2020-09-22 19:56:28.757876'),
(106, 'Brand 6', 1, 4, '2020-09-22 19:56:28.757876'),
(107, 'Brand 7', 1, 4, '2020-09-22 19:56:28.757876'),

-- to use in product test
(108, 'Brand 8', 0, 3, '2020-09-22 19:56:28.757876'),
(109, 'Brand 9', 0, 1, '2020-09-22 19:56:28.757876'),
(110, 'Brand 10', 0, 1, '2020-09-22 19:56:28.757876');


insert into product_type (id, name, description, parent_product_type_id, is_private, created_by_id, created_at) values
(1, 'ProductType1', 'Product Type 1', null, 0, 1, '2020-09-22 19:56:28.757876'),
(2, 'ProductType2', 'Product Type 2', null, 1, 4, '2020-09-22 19:56:28.757876'),
(3, 'ProductType3', 'Product Type 3', null, 1, 1, '2020-09-22 19:56:28.757876'),
(4, 'ProductType4', 'Product Type 4', null, 1, 1, '2020-09-22 19:56:28.757876'),
(5, 'ProductType41', 'Product Type 41', 4, 1, 1, '2020-09-22 19:56:28.757876'),
(6, 'ProductType411', 'Product Type 411', 5, 1, 1, '2020-09-22 19:56:28.757876'),
(7, 'ProductType7', 'Product Type 7', 5, 0, 4, '2020-09-22 19:56:28.757876'),

-- to use in product test
(8, 'ProductType8', 'Product Type 7', 5, 0, 3, '2020-09-22 19:56:28.757876'),
(9, 'ProductType9', 'Product Type 7', 5, 0, 1, '2020-09-22 19:56:28.757876'),
(10, 'ProductType10', 'Product Type 7', 5, 0, 1, '2020-09-22 19:56:28.757876');


insert into product (id, name, product_type_id, brand_id, created_by_id, created_at, is_private, image_url) values
(1, 'Product 1', 8, 108, 1, '2020-09-22 19:56:28.757876', 1, null),
(2, 'Product 2', 9, 108, 4, '2020-09-22 19:56:28.757876', 1, null),
(3, 'Product 3', 9, 108, 4, '2020-09-22 19:56:28.757876', 0, null),
(4, 'Product 4', 8, 108, 1, '2020-09-22 19:56:28.757876', 0, null),
(5, 'Product 5', null, null, 1, '2020-09-22 19:56:28.757876', 0, null),

-- to use in purchase_list_test
(6, 'Product 6', null, null, 1, '2020-09-22 19:56:28.757876', 1, null),
(7, 'Product 7', null, null, 4, '2020-09-22 19:56:28.757876', 1, null),
(8, 'Product 8', null, null, 4, '2020-09-22 19:56:28.757876', 0, null),
(9, 'Product 9', null, null, 1, '2020-09-22 19:56:28.757876', 0, null),
(10, 'Product 10', null, null, 1, '2020-09-22 19:56:28.757876', 0, null),
(11, 'Product 11', null, null, 1, '2020-09-22 19:56:28.757876', 0, null),
(12, 'Product 12', null, null, 1, '2020-09-22 19:56:28.757876', 0, null);

insert into purchase_list (id, name, created_by_id, created_at) values
(1, 'List 1', 1, '2020-09-22 19:56:28.757876'),
(2, 'List 2', 4, '2020-09-22 19:56:28.757876'),
(3, 'List 3', 1, '2020-09-22 19:56:28.757876'),
(4, 'List 4', 1, '2020-09-22 19:56:28.757876'),
(5, 'List 5', 1, '2020-09-22 19:56:28.757876');

insert into purchase_list_has_product (purchase_list_id, product_id, estimated_value, quantity) values
(1, 10, 12.5, 3),
(1, 11, 4.7, 2),
(2, 10, 12.5, 3),
(2, 11, 12.5, 3),
(3, 12, 6.5, 6),
(4, 10, 3.5, 2),
(4, 11, 6.5, 1),
(4, 12, 6.5, 3),
(5, 11, 6.5, 1);

