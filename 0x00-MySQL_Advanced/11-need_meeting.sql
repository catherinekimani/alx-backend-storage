-- script that creates a view need_meeting
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE (score < 80 AND (students.last_meeting IS NULL OR students.last_meeting < CURDATE() - INTERVAL 1 MONTH));
