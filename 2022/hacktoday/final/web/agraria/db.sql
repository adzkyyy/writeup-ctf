DROP DATABASE IF EXISTS `hackshop`;
CREATE DATABASE `hackshop`;
USE `hackshop`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+02:00";


CREATE TABLE `item` (
  `id` int(5) NOT NULL,
  `id_user` int(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(250) NOT NULL,
  `price` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `item` (`id`, `id_user`, `name`, `description`, `price`) VALUES
(1, 1, 'Raspery Pi 4', 'Latest Raspberry Pi 4 Model B with 2/4/8GB RAM raspberry pi 4 BCM2711 Quad core Cortex-A72 ARM v8 1.5GHz Speeder Than Pi 3B', 92),
(2, 1, 'ALFA WIFI Adapter', 'ALFA WIFI Adapter', 12),
(3, 1, 'Mask', 'Mask', 22),
(4, 1, 'T-Shirt', 'Anonymous Quote T Shirt Fake Society Funny Hacker Parody Guy Fawkes Unisex Tee Style Round Tee Shirt', 7);


CREATE TABLE `level` (
  `id` int(5) NOT NULL,
  `name` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `level` (`id`, `name`) VALUES
(1, 'admin'),
(2, 'user');


CREATE TABLE `user` (
  `id` int(5) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `id_level` int(5) NOT NULL,
  `token` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `user` (`id`, `username`, `password`, `email`, `gender`, `id_level`, `token`) VALUES
(1, 'admin', 'c8dbe2bcacf33f885ddf635786f8d655', 'admin@hackshop.com', 'Male', 1, ''),
(2, 'customer', '3c46a846a9e9fd4b2e0a8054080b850a', 'customer@hackshop.com', 'Female', 2, '');


ALTER TABLE `item`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);


ALTER TABLE `level`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_level` (`id_level`);


ALTER TABLE `item`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;


ALTER TABLE `user`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


ALTER TABLE `item`
  ADD CONSTRAINT `item_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`id_level`) REFERENCES `level` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;
