-- script that creates a trigger that resets the attribute valid_email
DELIMiTER //
CREATE TRIGGER reset_email_trigger
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
	IF NEW.email != OLD.email THEN
		SET NEW.valid_email = 0;
	END IF;
END;
//
DELIMiTER ;
