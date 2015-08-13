CREATE OR REPLACE FUNCTION boolean_to_varchar(torf boolean)
RETURNS varchar(1) AS $$
BEGIN
	IF torf THEN
	   RETURN '1';
	ELSE
	   RETURN '0';
	END IF;
END;
$$ LANGUAGE plpgsql;
