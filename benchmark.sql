-- ============================================================
-- 인덱스 성능 실험 벤치마크 쿼리
-- 사용법: 각 섹션을 인덱스 추가 전/후로 실행 후 실행시간 비교
-- ============================================================

-- 현재 인덱스 현황 확인
SHOW INDEX FROM guser;
SHOW INDEX FROM trade;

-- 실행 계획에서 rows, type, key 컬럼을 주목할 것
-- type: ALL(풀스캔) → range/ref/eq_ref 로 개선되면 성공

-- ============================================================
-- [1] grank 단일 컬럼 (낮은 카디널리티 - 인덱스 효과 제한적)
-- ============================================================

-- 1-1. 특정 등급 유저 조회
EXPLAIN ANALYZE
SELECT id, name, nickname, money
FROM guser
WHERE grank = 'D';

-- 1-2. 등급별 평균 보유금액
EXPLAIN ANALYZE
SELECT grank, COUNT(*) AS cnt, AVG(money) AS avg_money
FROM guser
GROUP BY grank
ORDER BY avg_money DESC;

-- ============================================================
-- [2] money 범위 조회 (높은 카디널리티 - 인덱스 효과 큼)
-- ============================================================

-- 2-1. 고액 유저 조회
EXPLAIN ANALYZE
SELECT id, name, nickname, money
FROM guser
WHERE money >= 9000000
ORDER BY money DESC
LIMIT 100;

-- 2-2. 특정 금액 범위
EXPLAIN ANALYZE
SELECT COUNT(*) FROM guser
WHERE money BETWEEN 5000000 AND 7000000;

-- ============================================================
-- [3] 날짜 범위 조회
-- ============================================================

-- 3-1. 최근 한 달 가입자
EXPLAIN ANALYZE
SELECT id, name, start_date
FROM guser
WHERE start_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY start_date DESC;

-- 3-2. 최근 일주일 내 접속한 유저
EXPLAIN ANALYZE
SELECT id, name, nickname, last_visit
FROM guser
WHERE last_visit >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY last_visit DESC;

-- 3-3. last_visit NULL 유저 (한 번도 안 온 유저)
EXPLAIN ANALYZE
SELECT COUNT(*) FROM guser WHERE last_visit IS NULL;

-- ============================================================
-- [4] trade 테이블 - seller 조회 (FK 컬럼)
-- ============================================================

-- 4-1. 특정 유저의 거래 내역
EXPLAIN ANALYZE
SELECT t.id, t.item_name, t.price, t.trade_date
FROM trade t
WHERE t.seller = 12345;

-- 4-2. 가장 많이 거래한 판매자 TOP 10
EXPLAIN ANALYZE
SELECT seller, COUNT(*) AS trade_cnt, SUM(price) AS total
FROM trade
GROUP BY seller
ORDER BY trade_cnt DESC
LIMIT 10;

-- ============================================================
-- [5] trade 테이블 - price / trade_date 범위
-- ============================================================

-- 5-1. 고가 거래 조회
EXPLAIN ANALYZE
SELECT id, seller, item_name, price
FROM trade
WHERE price >= 90000
ORDER BY price DESC
LIMIT 100;

-- 5-2. 최근 한 달 거래
EXPLAIN ANALYZE
SELECT COUNT(*), SUM(price)
FROM trade
WHERE trade_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

-- ============================================================
-- [6] JOIN 쿼리 (가장 인덱스 효과가 큰 케이스)
-- ============================================================

-- 6-1. 골드(G) 등급 유저의 거래 내역
EXPLAIN ANALYZE
SELECT u.name, u.nickname, t.item_name, t.price, t.trade_date
FROM guser u
JOIN trade t ON u.id = t.seller
WHERE u.grank = 'G'
ORDER BY t.trade_date DESC
LIMIT 50;

-- 6-2. 최근 접속한 유저의 최근 거래
EXPLAIN ANALYZE
SELECT u.nickname, u.grank, t.item_name, t.price
FROM guser u
JOIN trade t ON u.id = t.seller
WHERE u.last_visit >= DATE_SUB(NOW(), INTERVAL 7 DAY)
  AND t.trade_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY t.price DESC
LIMIT 100;

-- 6-3. 복합 조건: 부자 + 최근 가입 유저 조회
EXPLAIN ANALYZE
SELECT id, name, nickname, grank, money, start_date
FROM guser
WHERE money >= 8000000
  AND start_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
ORDER BY money DESC;

-- ============================================================
-- 인덱스 추가 (여기서부터 실행 후 위 쿼리 재실행)
-- ============================================================

-- ALTER TABLE guser ADD INDEX idx_grank (grank);
-- ALTER TABLE guser ADD INDEX idx_money (money);
-- ALTER TABLE guser ADD INDEX idx_start_date (start_date);
-- ALTER TABLE guser ADD INDEX idx_last_visit (last_visit);
-- ALTER TABLE trade ADD INDEX idx_seller (seller);
-- ALTER TABLE trade ADD INDEX idx_price (price);
-- ALTER TABLE trade ADD INDEX idx_trade_date (trade_date);

-- 복합 인덱스 (단일 인덱스보다 효과적인 경우)
-- ALTER TABLE guser ADD INDEX idx_rank_money (grank, money);
-- ALTER TABLE guser ADD INDEX idx_money_rank (money, grank);  -- 순서가 성능에 영향
-- ALTER TABLE trade ADD INDEX idx_seller_date (seller, trade_date);

-- ============================================================
-- 인덱스 제거 (초기화)
-- ============================================================

-- ALTER TABLE guser DROP INDEX idx_grank;
-- ALTER TABLE guser DROP INDEX idx_money;
-- ALTER TABLE guser DROP INDEX idx_start_date;
-- ALTER TABLE guser DROP INDEX idx_last_visit;
-- ALTER TABLE trade DROP INDEX idx_seller;
-- ALTER TABLE trade DROP INDEX idx_price;
-- ALTER TABLE trade DROP INDEX idx_trade_date;
-- ALTER TABLE guser DROP INDEX idx_rank_money;
-- ALTER TABLE guser DROP INDEX idx_money_rank;
-- ALTER TABLE trade DROP INDEX idx_seller_date;
