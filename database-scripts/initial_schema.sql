
drop table if exists purchase_has_product;
drop table if exists purchase;
drop table if exists purchase_list_has_product;
drop table if exists purchase_list;
drop table if exists product;
drop table if exists brand;
drop table if exists product_type;
drop table if exists user;
drop table if exists user_group;


create table user_group (
    id int not null auto_increment,
    name varchar(255) not null,
    description varchar(255) null default null,
    created_at timestamp not null default now(),
    primary key (id)
);

create table user (
    id int not null auto_increment,
    name varchar(255) not null,
    login varchar(255) not null,
    password varchar(255) not null,
    user_group_id int not null,
    created_at timestamp not null default now(),
    primary key (id),
    foreign key (user_group_id) references user_group(id)
);

create table product_type (
    id int not null auto_increment,
    name varchar(255) not null,
    description varchar(255) null default null,
    parent_product_type_id int null,
    is_private tinyint not null default 1,
    created_by int not null,
    created_at timestamp not null default now(),
    primary key (id),
    foreign key (parent_product_type_id) references product_type(id),
    foreign key (created_by) references user(id)
);

create table brand (
    id int not null auto_increment,
    name VARCHAR(255) not null,
    is_private tinyint not null default 1,
    created_by int not null,
    created_at timestamp not null default now(),
    primary key (id)
);

create table product (
    id int not null auto_increment,
    name varchar(255) not null,
    product_type_id int null,
    brand_id int null,
    created_by int not null,
    created_at timestamp not null default now(),
    is_private tinyint not null default 1,
    image_url varchar(255) null default null,
    primary key (id),
    foreign key (created_by) references user(id),
    foreign key (product_type_id) references product_type(id),
    foreign key (brand_id) references brand(id)
);

create table purchase_list (
    id int not null auto_increment,
    name varchar(255) not null,
    created_by int not null,
    created_at timestamp not null default now(),
    primary key (id),
    foreign key (created_by) references user(id)
);

create table purchase_list_has_product (
    purchase_list_id int not null,
    product_id int not null,
    estimated_value float null,
    quantity int not null default 1,
    primary key (purchase_list_id, product_id),
    foreign key (purchase_list_id) references purchase_list(id),
    foreign key (product_id) references product(id)
);

create table purchase (
    id int not null auto_increment,
    purchase_list_id int null,
    name varchar(255) null,
    created_by int not null,
    created_at timestamp not null default now(),
    primary key (id),
    foreign key (created_by) references user(id),
    foreign key (purchase_list_id) references purchase_list(id)
);

create table purchase_has_product (
    purchase_id int not null,
    product_id int not null,
    value float null,
    quantity int not null default 1,
    primary key (purchase_id, product_id),
    foreign key (purchase_id) references purchase(id),
    foreign key (product_id) references product(id)
);
