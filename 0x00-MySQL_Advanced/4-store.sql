--  trigger that decreases the quantity of an item after adding a new order.
DELIMITER $$

CREATE TRIGGER `holberton`.`orders`
AFTER INSERT ON `holberton`.`orders`
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END$$

DELIMITER ;
