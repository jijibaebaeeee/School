CREATE TABLE `category` (
	`main_id`	int4	NOT NULL,
	`sub_id`	int4	NOT NULL,
	`name`	varchar(20)	NOT NULL
);

CREATE TABLE `Sub_category` (
	`sub_id`	int4	NOT NULL,
	`name`	varchar(20)	NOT NULL
);

CREATE TABLE `Product` (
	`product_id`	bigint	NOT NULL,
	`main_id`	int4	NOT NULL,
	`sub_id`	int4	NOT NULL,
	`event_id`	int4	NOT NULL,
	`price`	int	NOT NULL,
	`Field`	VARCHAR(255)	NULL
);

CREATE TABLE `Event` (
	`event_id`	int4	NOT NULL,
	`event_name`	varchar(30)	NOT NULL,
	`card_name`	varchar(20)	NULL
);

CREATE TABLE `Store` (
	`id`	int	NOT NULL,
	`area_id`	int4	NOT NULL,
	`name`	varchar(30)	NOT NULL
);

CREATE TABLE `management` (
	`store_id`	int	NOT NULL,
	`product_id`	bigint	NOT NULL,
	`count`	int	NULL
);

CREATE TABLE `sigg_areas` (
	`id`	int4	NOT NULL,
	`sido_area_id`	int4	NOT NULL,
	`name`	varchar(50)	NOT NULL
);

CREATE TABLE `emd_areas` (
	`id`	int4	NOT NULL,
	`sigg_area_id`	int4	NOT NULL,
	`name`	varchar(50)	NOT NULL
);

CREATE TABLE `sido_areas` (
	`id`	int	NOT NULL,
	`name`	varchar(50)	NOT NULL
);

CREATE TABLE `order` (
	`id2`	int	NOT NULL,
	`product_id`	bigint	NOT NULL
);

ALTER TABLE `category` ADD CONSTRAINT `PK_CATEGORY` PRIMARY KEY (
	`main_id`,
	`sub_id`
);

ALTER TABLE `Sub_category` ADD CONSTRAINT `PK_SUB_CATEGORY` PRIMARY KEY (
	`sub_id`
);

ALTER TABLE `Product` ADD CONSTRAINT `PK_PRODUCT` PRIMARY KEY (
	`product_id`
);

ALTER TABLE `Event` ADD CONSTRAINT `PK_EVENT` PRIMARY KEY (
	`event_id`
);

ALTER TABLE `Store` ADD CONSTRAINT `PK_STORE` PRIMARY KEY (
	`id`
);

ALTER TABLE `management` ADD CONSTRAINT `PK_MANAGEMENT` PRIMARY KEY (
	`store_id`,
	`product_id`
);

ALTER TABLE `sigg_areas` ADD CONSTRAINT `PK_SIGG_AREAS` PRIMARY KEY (
	`id`
);

ALTER TABLE `emd_areas` ADD CONSTRAINT `PK_EMD_AREAS` PRIMARY KEY (
	`id`
);

ALTER TABLE `sido_areas` ADD CONSTRAINT `PK_SIDO_AREAS` PRIMARY KEY (
	`id`
);

ALTER TABLE `order` ADD CONSTRAINT `PK_ORDER` PRIMARY KEY (
	`id2`,
	`product_id`
);

ALTER TABLE `category` ADD CONSTRAINT `FK_Sub_category_TO_category_1` FOREIGN KEY (
	`sub_id`
)
REFERENCES `Sub_category` (
	`sub_id`
);

ALTER TABLE `management` ADD CONSTRAINT `FK_Store_TO_management_1` FOREIGN KEY (
	`store_id`
)
REFERENCES `Store` (
	`id`
);

ALTER TABLE `management` ADD CONSTRAINT `FK_Product_TO_management_1` FOREIGN KEY (
	`product_id`
)
REFERENCES `Product` (
	`product_id`
);

ALTER TABLE `order` ADD CONSTRAINT `FK_Store_TO_order_1` FOREIGN KEY (
	`id2`
)
REFERENCES `Store` (
	`id`
);

ALTER TABLE `order` ADD CONSTRAINT `FK_Product_TO_order_1` FOREIGN KEY (
	`product_id`
)
REFERENCES `Product` (
	`product_id`
);

