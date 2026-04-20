Bulk insert 시에 사용하는 일반적인 성능향상 팁들

## 인덱스 비활성화

```sql
ALTER TABLE your_table DISABLE KEYS;
-- 데이터 로드
ALTER TABLE your_table ENABLE KEYS;
```

## 제약 조건 비활성화

```sql
SET foreign_key_checks = 0;
-- 데이터 로드
SET foreign_key_checks = 1;
```

## 자동 커밋 끄기

```sql
SET autocommit = 0;
-- 데이터 로드
COMMIT;
```

## 테이블 잠금

```sql
LOCK TABLES your_table WRITE;
-- 데이터 로드
UNLOCK TABLES;
```

## 쓰기 버퍼 크기 조정

```
SET GLOBAL bulk_insert_buffer_size = 512 * 1024 * 1024;  -- 예: 512MB
```
