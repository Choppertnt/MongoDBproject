
DECLARE
    row_count INT;
BEGIN
    -- นับจำนวนแถวในตาราง
    SELECT COUNT(*) INTO row_count FROM information;

    -- เมื่อมีการลบข้อมูล
    IF TG_OP = 'DELETE' THEN
        IF row_count = 0 THEN
            EXECUTE format('ALTER SEQUENCE %I RESTART WITH 1', 'information_id_seq');
        ELSE
            EXECUTE format('SELECT setval(''%I'', COALESCE((SELECT MAX(id) FROM %I), 1))', 'information_id_seq', 'information');
        END IF;
    END IF;

    RETURN OLD;
END;
