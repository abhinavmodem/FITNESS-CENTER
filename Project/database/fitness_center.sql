-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 18, 2024 at 02:29 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fitness_center`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `equipment`
--

CREATE TABLE `equipment` (
  `equipment_id` int(11) NOT NULL,
  `equipment_name` varchar(255) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `equipment`
--

INSERT INTO `equipment` (`equipment_id`, `equipment_name`, `quantity`, `purchase_date`) VALUES
(1, 'dumbells', 10, '2024-02-16'),
(2, 'barbells', 4, '2024-02-23');

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `member_id` int(11) NOT NULL,
  `member_name` varchar(255) DEFAULT NULL,
  `member_contact` varchar(20) DEFAULT NULL,
  `email_id` text NOT NULL,
  `workout_plan_id` int(11) DEFAULT NULL,
  `start_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`member_id`, `member_name`, `member_contact`, `email_id`, `workout_plan_id`, `start_date`) VALUES
(107, 'abhinav', '9154224668', 'abhinavmodem@gmail.com', 5, '2024-02-18 05:47:01');

-- --------------------------------------------------------

--
-- Table structure for table `receptionist`
--

CREATE TABLE `receptionist` (
  `recep_id` int(11) NOT NULL,
  `recep_name` varchar(255) DEFAULT NULL,
  `recep_contact` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `receptionist`
--

INSERT INTO `receptionist` (`recep_id`, `recep_name`, `recep_contact`) VALUES
(92, 'abhinav', '3456789'),
(102, 'kumari', '3456789');

-- --------------------------------------------------------

--
-- Table structure for table `trainers`
--

CREATE TABLE `trainers` (
  `trainer_id` int(11) NOT NULL,
  `trainer_name` varchar(255) DEFAULT NULL,
  `trainer_contact` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trainers`
--

INSERT INTO `trainers` (`trainer_id`, `trainer_name`, `trainer_contact`) VALUES
(9, 'ashok', '890'),
(12, 'abhinav', '9154224668'),
(56, 'fhdjkl', '890'),
(101, 'jumba', 'HFDSKL'),
(2147483647, 'abhinav', '');

-- --------------------------------------------------------

--
-- Table structure for table `trainer_member_relationship`
--

CREATE TABLE `trainer_member_relationship` (
  `member_id` int(11) NOT NULL,
  `trainer_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin', 'admin'),
(9, 'ashok', 'ashok', 'trainer'),
(12, 'abhinavmodem', 'abhinav1', 'trainer'),
(56, 'fhdjkl', 'abhinav1', 'trainer'),
(78, '21071A1298', 'abhinav1', 'member'),
(89, '21071A1299', 'abhinav1', 'member'),
(92, 'abhinavmodem1', 'abhinav1', 'receptionist'),
(101, 'jumba', 'abhinav1', 'trainer'),
(102, 'kumari', 'abhinav1', 'receptionist'),
(107, 'kullu', 'abhinav1', 'member'),
(2147483647, 'sdfghjk', 'dgfhjkl;', 'trainer');

-- --------------------------------------------------------

--
-- Table structure for table `workout_plans`
--

CREATE TABLE `workout_plans` (
  `plan_id` int(11) NOT NULL,
  `plan_name` varchar(255) DEFAULT NULL,
  `monday` varchar(255) DEFAULT NULL,
  `tuesday` varchar(255) DEFAULT NULL,
  `wednesday` varchar(255) DEFAULT NULL,
  `thursday` varchar(255) DEFAULT NULL,
  `friday` varchar(255) DEFAULT NULL,
  `saturday` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `workout_plans`
--

INSERT INTO `workout_plans` (`plan_id`, `plan_name`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`) VALUES
(0, 'india', 'india', 'india', 'india', 'india', 'india', 'india'),
(1, 'Plan 1', 'Chest workout', 'Leg workout', 'Rest', 'Back workout', 'Shoulder workout', 'Rest'),
(2, 'Plan 2', 'Back workout', 'Leg workout', 'Rest', 'Chest workout', 'Cardio', 'Rest'),
(3, 'Plan 3', 'Leg workout', 'Cardio', 'Rest', 'Arm workout', 'Rest', 'Rest'),
(4, 'Plan 4', 'Cardio', 'Rest', 'Shoulder workout', 'Leg workout', 'Rest', 'Back workout'),
(5, 'Plan 5', 'Rest', 'Chest workout', 'Leg workout', 'Arm workout', 'Cardio', 'Rest'),
(6, 'Plan 6', 'Cardio', 'Back workout', 'Rest', 'Leg workout', 'Rest', 'Shoulder workout'),
(7, 'Plan 7', 'Leg workout', 'Rest', 'Chest workout', 'Rest', 'Arm workout', 'Cardio'),
(8, 'Plan 8', 'Rest', 'Shoulder workout', 'Cardio', 'Leg workout', 'Chest workout', 'Rest'),
(9, 'Plan 9', 'Back workout', 'Leg workout', 'Cardio', 'Rest', 'Chest workout', 'Rest'),
(10, 'Plan 10', 'Rest', 'Chest workout', 'Arm workout', 'Leg workout', 'Rest', 'Cardio'),
(11, 'Plan 11', 'Shoulder workout', 'Rest', 'Cardio', 'Back workout', 'Leg workout', 'Chest workout'),
(12, 'Plan 12', 'Cardio', 'Rest', 'Leg workout', 'Rest', 'Arm workout', 'Chest workout'),
(13, 'Plan 13', 'Leg workout', 'Rest', 'Back workout', 'Cardio', 'Rest', 'Shoulder workout'),
(14, 'Plan 14', 'Rest', 'Chest workout', 'Leg workout', 'Back workout', 'Rest', 'Cardio'),
(15, 'Plan 15', 'Cardio', 'Rest', 'Arm workout', 'Leg workout', 'Rest', 'Chest workout');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `equipment`
--
ALTER TABLE `equipment`
  ADD PRIMARY KEY (`equipment_id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`member_id`),
  ADD KEY `workout_plan_id` (`workout_plan_id`);

--
-- Indexes for table `receptionist`
--
ALTER TABLE `receptionist`
  ADD PRIMARY KEY (`recep_id`);

--
-- Indexes for table `trainers`
--
ALTER TABLE `trainers`
  ADD PRIMARY KEY (`trainer_id`);

--
-- Indexes for table `trainer_member_relationship`
--
ALTER TABLE `trainer_member_relationship`
  ADD PRIMARY KEY (`member_id`),
  ADD KEY `trainer_id` (`trainer_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `workout_plans`
--
ALTER TABLE `workout_plans`
  ADD PRIMARY KEY (`plan_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `members`
--
ALTER TABLE `members`
  ADD CONSTRAINT `members_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `members_ibfk_2` FOREIGN KEY (`workout_plan_id`) REFERENCES `workout_plans` (`plan_id`);

--
-- Constraints for table `receptionist`
--
ALTER TABLE `receptionist`
  ADD CONSTRAINT `receptionist_ibfk_1` FOREIGN KEY (`recep_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `trainers`
--
ALTER TABLE `trainers`
  ADD CONSTRAINT `trainers_ibfk_1` FOREIGN KEY (`trainer_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `trainer_member_relationship`
--
ALTER TABLE `trainer_member_relationship`
  ADD CONSTRAINT `trainer_member_relationship_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `trainer_member_relationship_ibfk_2` FOREIGN KEY (`trainer_id`) REFERENCES `trainers` (`trainer_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
