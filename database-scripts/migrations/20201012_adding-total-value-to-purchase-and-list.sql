ALTER TABLE purchase ADD COLUMN total_value FLOAT NOT NULL DEFAULT 0;
ALTER TABLE purchase_list ADD COLUMN total_estimated_value FLOAT NOT NULL DEFAULT 0;
