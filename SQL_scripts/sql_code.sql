-- Database creation
-- create Database MobileFirst_Task;

-- Table creation
use MobileFirst_Task;
create table PlaceHolders(
id int auto_increment primary key,
First_name varchar(100),
Last_name varchar(100),
Age varchar(3),
Gender varchar(15),
Phone_number varchar(20),
Email varchar(50),
Address varchar(150),
Nationality varchar(20),
Organizations varchar(100),
Languages_known varchar(100)
);