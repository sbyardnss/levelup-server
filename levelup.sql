-- SELECT * FROM levelupapi_gametype;
-- SELECT * FROM auth_user;
-- SELECT * FROM authtoken_token;
-- SELECT * FROM levelupapi_gamer;
-- SELECT * FROM levelupapi_game;
-- SELECT * FROM levelupapi_event;


-- SELECT g.title, u.first_name FROM levelupapi_game g 
-- JOIN levelupapi_gamer ga on ga.id = g.gamer_id
-- JOIN auth_user u on ga.user_id = u.id


-- SELECT 
--     *,
--     u.first_name || ' ' || u.last_name as `full_name`,
--     g.id
-- FROM levelupapi_event e
-- JOIN levelupapi_gamer g on g.id = e.organizer_id
-- JOIN auth_user u on u.id = g.user_id

CREATE VIEW GAMES_BY_USER AS
SELECT 
    *,
    u.first_name || ' ' || u.last_name as `full_name`
FROM levelupapi_game g 
JOIN levelupapi_gamer ga on ga.id = g.gamer_id
JOIN auth_user u on ga.user_id = u.id;


CREATE VIEW EVENTS_BY_USER AS
SELECT 
    *,
    u.first_name || ' ' || u.last_name as `full_name`,
    g.id
FROM levelupapi_event e
JOIN levelupapi_gamer g on g.id = e.organizer_id
JOIN auth_user u on u.id = g.user_id;