-- 데이터베이스 생서
CREATE DATABASE mysqldb
    DEFAULT CHARACTER SET = 'utf8mb4';

-- 사용할 데이터베이스 선택
USE mysqldb;

-- 테이블 생성
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    description VARCHAR(255)
);

-- 데이터 입력
INSERT INTO menu (name, price, description)
VALUES 
('시그니처 스테이크', 45000, '프리미엄 소고기 스테이크입니다.'),
('트러플 크림 파스타', 28000, '프러플 향의 크림 파스타입니다.'),
('해산물 토마토 파스타', 25000, '해산물과 토마토 베이스의 파스타입니다.');

-- 데이터 조회
SELECT * FROM menu;

-- 조건문을 이용한 조회
SELECT * FROM menu
WHERE name = '해산물 토마토 파스타';

-- 데이터 수정
UPDATE menu
SET price = 32000
WHERE name = '해산물 토마토 파스타'

UPDATE menu
SET price = 33000,
    description = '해산물과 토마토 베이스의 파스타에 모짜렐라 치즈가 올려져 있습니다.'
WHERE name = '해산물 토마토 파스타';


-- 데이터 삭제
DELETE FROM menu
WHERE id = 3;


CRUD
