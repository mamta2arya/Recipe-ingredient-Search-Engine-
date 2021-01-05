USE receipes;

DROP PROCEDURE IF EXISTS getingredients;
DROP PROCEDURE if exists getrecipelist;
DROP PROCEDURE if exists getrecipeasperid;

DELIMITER //

CREATE PROCEDURE getingredients ()
 BEGIN
  SELECT ingredients  FROM receipe_ingre Limit 100;
 END;
//

CREATE PROCEDURE getrecipelist (in param1 VARCHAR(255))
 BEGIN
  select RT.recipe_id, RT.title, GROUP_CONCAT(ingredients,  ' ') FROM receipe_title RT
JOIN receipe_ingre RI ON RT.recipe_id=RI.recipe_id WHERE RT.recipe_id IN(
SELECT RT.recipe_id FROM receipe_title RT
JOIN receipe_ingre RI ON RT.recipe_id=RI.recipe_id 
WHERE RI.ingredients IN (param1)
)  GROUP BY RT.recipe_id;
END;
//

CREATE PROCEDURE getrecipeasperid (in param1 int)
 BEGIN
select RT.recipe_id, RT.title, GROUP_CONCAT(ingredients,  ' ') AS ingredients, RIN.instruc FROM receipe_title RT
JOIN receipe_ingre RI ON RT.recipe_id=RI.recipe_id 
JOIN receipe_instru RIN ON RT.recipe_id=RIN.recipe_id
WHERE RT.recipe_id=param1;
END;
//
DELIMITER ;

