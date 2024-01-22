-- script that creates a function SafeDiv
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
	DECLARE result FLOAT;
	IF b != 0 then
		SET result = a / b;
	ELSE
		SET result = 0;
	END IF;

	RETURN result;
END //
DELIMITER ;
