
insert into user (id, name, login, password, user_group_id, created_at) values
(2, 'Vitor', 'vitor', '$2b$12$buSIlMGMp8F/bB.gN/OfquPD1MQDqBeEi0Fxq5J6Qd4EypsabFh.e', 1, '2020-09-22 19:56:28.757876'),
(3, 'User 3', 'user3', '$2b$12$61JKNlydwEJYEBXZH1j6suJD2QEnyQS2PY3BSyDxmKLt/uuDouuU.', 2, '2020-09-22 19:56:28.757876'), -- password: pass3
(4, 'User 4', 'user4', '$2b$12$buSIlMGMp8F/bB.gN/OfquPD1MQDqBeEi0Fxq5J6Qd4EypsabFh.e', 3, '2020-09-22 19:56:28.757876');

insert into brand (id, name, is_private, created_by_id, created_at) values
(1, 'Brand 1', 0, 1, '2020-09-22 19:56:28.757876'),
(2, 'Brand 2', 0, 1, '2020-09-22 19:56:28.757876'),
(3, 'Brand 3', 0, 1, '2020-09-22 19:56:28.757876'),
(4, 'Brand 4', 1, 1, '2020-09-22 19:56:28.757876'),
(5, 'Brand 5', 1, 1, '2020-09-22 19:56:28.757876'),
(6, 'Brand 6', 1, 3, '2020-09-22 19:56:28.757876');

