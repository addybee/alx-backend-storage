--  creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
    BEGIN
        UPDATE users, (
		SELECT corrections.user_id as user_id, SUM(corrections.score * projects.weight) / SUM(projects.weight) as average_score
		FROM corrections
		JOIN projects
		ON projects.id = corrections.project_id
		GROUP BY corrections.user_id
	    ) AS result
        SET users.average_score = result.average_score
        WHERE users.id = result.user_id;
END//
DELIMITER ;
