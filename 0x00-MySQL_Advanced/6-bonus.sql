--  adds a new correction for a student.

DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN

    DECLARE project_id INT;
    
    -- Find the project ID by project name
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;
    
    -- Check if the project name exists
    IF project_id IS NULL THEN
        -- If not found, insert a default project
        INSERT INTO projects (name) VALUES (project_name);
        -- Get the ID of the newly inserted default project
        SET project_id = LAST_INSERT_ID();
    END IF;
    
    -- Insert the new correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);

END //

DELIMITER ;
