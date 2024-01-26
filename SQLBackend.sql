/*CREATE SCHEMA `wind_data` ;

CREATE TABLE `wind_data`.`wind_table` (
  `timestamp` CHAR(21) NOT NULL,
  `wind_speed` DOUBLE NULL,
  `power` DOUBLE NULL,
  `energy` INT NULL,
  `yaw_position` FLOAT NULL,
  `yaw_delta` INT NULL,
  `temp_amb` FLOAT NULL,
  `turbine_state` TINYINT NULL,
  `dispatch_enable` TINYINT NULL,
  `env_condition` TINYINT NULL,
  PRIMARY KEY (`timestamp`));
  
  */
  
  SELECT * FROM wind_data.wind_table