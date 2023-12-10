DROP DATABASE store

CREATE


#어떤 데이터 베이스들이 있는지 확인
SHOW DATABASES;

#많은 데이터베이스중에서 원하는 것을 선택
USE Convience_store;

#테이블이 무엇이 있는지 보고싶으면 이것 사용
SHOW TABLES;



#자동으로 열 번호 증가시키고 싶으면 이거 사용
ALTER TABLE Sub_category MODIFY COLUMN sub_id INT AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE Sub_category MODIFY sub_id INT;
DROP TABLE category;
DROP TABLE Sub_category;
# 테이블 내의 내용 확인이 필요하면 이것 수정
SELECT * FROM Sub_category;
SELECT * FROM category;

CREATE TABLE `category` (
    `main_id` VARCHAR(10) NOT NULL,
    `sub_id` INT NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    PRIMARY KEY (main_id, sub_id)
);

CREATE TABLE `Sub_category` (
	`sub_id`	INT	NOT NULL,
	`name`	varchar(20)	NOT NULL,
	FOREIGN KEY sub_id REFERENCES category(sub_id)
);

ALTER TABLE Sub_category add FOREIGN KEY(sub_id) REFERENCES category(sub_id);



CREATE TABLE `Product` (
	`product_id`	bigint	NOT NULL,
	`main_id`	INT	NOT NULL,
	`sub_id`	INT	NOT NULL,
	`event_id`	INT	NOT NULL,
	`price`	int	NOT NULL,
	`Field`	VARCHAR(255)	NULL
);

CREATE TABLE `Event` (
	`event_id`	INT	NOT NULL AUTO_INCREMENT,
	`event_name`	varchar(30)	NOT NULL,
	`card_name`	varchar(20)	NULL
);

CREATE TABLE `Store` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`area_id`	INT	NOT NULL,
	`name`	varchar(30)	NOT NULL
);

CREATE TABLE `management` (
	`store_id`	int	NOT NULL,
	`product_id`	bigint	NOT NULL,
	`count`	int	NULL
);

CREATE TABLE `sigg_areas` (
	`id`	INT	NOT NULL,
	`sido_area_id`	INT	NOT NULL,
	`name`	varchar(50)	NOT NULL
);

CREATE TABLE `emd_areas` (
	`id`	INT	NOT NULL,
	`sigg_area_id`	INT	NOT NULL,
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

