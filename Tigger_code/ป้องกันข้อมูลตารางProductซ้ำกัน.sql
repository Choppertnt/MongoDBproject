
BEGIN
    -- ตรวจสอบว่ามีข้อมูลซ้ำในตารางหรือไม่
    IF EXISTS (
        SELECT 1 FROM product
        WHERE customername = NEW.customername
        AND sale_date = NEW.sale_date
        AND band = NEW.band
        AND unit = NEW.unit
        AND price = NEW.price
    ) THEN
        -- ถ้ามีข้อมูลซ้ำ ให้ตัดข้อมูลนี้ออก
        RETURN NULL; 
    END IF;
    
    -- ถ้าไม่มีข้อมูลซ้ำ ให้แทรกข้อมูลใหม่
    RETURN NEW; 
END;
