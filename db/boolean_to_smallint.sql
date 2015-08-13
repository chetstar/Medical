CREATE OR REPLACE FUNCTION boolean_to_smallint(torf boolean)
RETURNS smallint AS $$
BEGIN
	IF torf THEN
	   RETURN 1;
	ELSE
	   RETURN 0;
	END IF;
END;
$$ LANGUAGE plpgsql;
