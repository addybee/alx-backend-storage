--  creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
    BEGIN
        DECLARE W_avg FLOAT;
        SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight) INTO W_avg
        FROM corrections
        JOIN projects
        ON projects.id = corrections.project_id AND corrections.user_id = user_id;

        UPDATE users
        SET average_score = W_avg
        WHERE id = user_id;
    END//

DELIMITER ;