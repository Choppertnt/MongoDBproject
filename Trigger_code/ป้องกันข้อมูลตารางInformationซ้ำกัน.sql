
DECLARE
    new_id INT;
BEGIN
    -- ตรวจสอบว่ามีข้อมูลซ้ำในตารางหรือไม่
    IF EXISTS (
        SELECT 1 FROM information
        WHERE customername = NEW.customername
        AND sale_date = NEW.sale_date
        AND phone_number = NEW.phone_number
    ) THEN
        -- ถ้ามีข้อมูลซ้ำ ให้ตัดข้อมูลนี้ออก
        RETURN NULL; 
    END IF;
    
    -- กำหนด ID ใหม่ โดยใช้ค่า MAX ของ ID ในตาราง
    SELECT COALESCE(MAX(id), 0) + 1 INTO new_id FROM information;
    NEW.id := new_id; -- กำหนด ID ใหม่ให้กับแถวที่จะแทรก

    RETURN NEW; 
END;