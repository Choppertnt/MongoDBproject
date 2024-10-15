
BEGIN
    -- ปรับปรุงค่า id ของแถวที่มี id สูงกว่าค่าที่ถูกลบ
    UPDATE information
    SET id = id - 1
    WHERE id > OLD.id;

    RETURN OLD; -- คืนค่าข้อมูลที่ถูกลบ
END;
