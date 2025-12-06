-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 06, 2025 at 11:59 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bloodbank`
--

-- --------------------------------------------------------

--
-- Table structure for table `blood_requests`
--

CREATE TABLE `blood_requests` (
  `request_id` int(11) NOT NULL,
  `patient_name` varchar(100) NOT NULL,
  `blood_type` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
  `quantity_needed` int(11) NOT NULL,
  `urgency` enum('Low','Medium','High','Critical') DEFAULT 'Medium',
  `hospital_name` varchar(100) DEFAULT NULL,
  `contact_phone` varchar(15) NOT NULL,
  `request_date` date DEFAULT curdate(),
  `status` enum('Pending','Fulfilled','Cancelled') DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `blood_requests`
--

INSERT INTO `blood_requests` (`request_id`, `patient_name`, `blood_type`, `quantity_needed`, `urgency`, `hospital_name`, `contact_phone`, `request_date`, `status`) VALUES
(1, 'abs', 'O+', 450, '', 'city hostpital', '123456781', '2025-09-26', 'Cancelled'),
(2, 'kanishka', 'A+', 450, 'High', 'central hostpital', '8596578415', '2025-09-26', 'Fulfilled'),
(3, 'Roshni', 'A+', 450, 'Critical', 'city hospital', '5328578359', '2025-09-26', 'Fulfilled');

-- --------------------------------------------------------

--
-- Table structure for table `blood_stock`
--

CREATE TABLE `blood_stock` (
  `stock_id` int(11) NOT NULL,
  `blood_type` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
  `donor_id` int(11) DEFAULT NULL,
  `collection_date` date NOT NULL,
  `expiry_date` date NOT NULL,
  `quantity_ml` int(11) DEFAULT 450,
  `status` enum('Available','Used','Expired') DEFAULT 'Available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `blood_stock`
--

INSERT INTO `blood_stock` (`stock_id`, `blood_type`, `donor_id`, `collection_date`, `expiry_date`, `quantity_ml`, `status`) VALUES
(1, 'O+', 1, '2025-09-26', '2025-09-30', 450, 'Available'),
(3, 'O+', 2, '2025-09-10', '2025-10-10', 450, 'Available'),
(4, 'AB+', NULL, '2025-09-28', '2025-10-28', 450, 'Available'),
(5, 'O+', NULL, '2025-12-06', '2026-01-05', 450, 'Available');

-- --------------------------------------------------------

--
-- Table structure for table `donors`
--

CREATE TABLE `donors` (
  `donor_id` int(11) NOT NULL,
  `donor_name` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `blood_type` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `last_donation_date` date DEFAULT NULL,
  `eligible_next_donation` date DEFAULT NULL,
  `registration_date` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donors`
--

INSERT INTO `donors` (`donor_id`, `donor_name`, `age`, `gender`, `blood_type`, `phone`, `email`, `address`, `last_donation_date`, `eligible_next_donation`, `registration_date`) VALUES
(1, 'abc ', 19, 'Female', 'O+', '1234567891', 'abc@gmail.com', '22, ramchandra nagar, dhule', '2023-05-09', '2024-05-09', '2023-05-12'),
(2, 'kanishka wani', 19, 'Female', 'O+', '1254783691', 'kanishka@gmail.com', 'Ramchandra Nagar, dhule', '2024-09-10', '2024-12-09', '2025-09-26'),
(3, 'Vaishnavi Pachapute', 20, 'Female', 'AB+', '9856231475', 'vaishnavai@gmail.com', 'Pawan nagar, dhule', '2024-06-12', '2024-09-10', '2025-09-28'),
(4, 'Ram Kulkarni', 25, 'Male', 'AB-', '9876541236', 'ram@gmail.com', 'dhule', '2021-09-05', '2021-12-04', '2025-09-28'),
(5, 'shakil shaikh', 35, 'Male', 'A+', '1234567985', 'pqr@gmail.com', 'deopur dhule', '2323-04-12', '2323-07-11', '2025-09-29'),
(6, 'neha behare', 19, 'Female', 'B+', '5468468111', 'pqr@gmail.com', 'deopur', '2023-09-21', '2023-12-20', '2025-10-04'),
(7, 'Yashraj Wani', 20, 'Male', 'O+', '9936549877', 'yashraj@gmail.com', 'ramchandra nagar, dhule', '2025-03-03', '2025-06-01', '2025-12-06');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`) VALUES
(1, 'kanishka', 'kanishka@123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blood_requests`
--
ALTER TABLE `blood_requests`
  ADD PRIMARY KEY (`request_id`);

--
-- Indexes for table `blood_stock`
--
ALTER TABLE `blood_stock`
  ADD PRIMARY KEY (`stock_id`),
  ADD KEY `donor_id` (`donor_id`);

--
-- Indexes for table `donors`
--
ALTER TABLE `donors`
  ADD PRIMARY KEY (`donor_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blood_requests`
--
ALTER TABLE `blood_requests`
  MODIFY `request_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `blood_stock`
--
ALTER TABLE `blood_stock`
  MODIFY `stock_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `donors`
--
ALTER TABLE `donors`
  MODIFY `donor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `blood_stock`
--
ALTER TABLE `blood_stock`
  ADD CONSTRAINT `blood_stock_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `donors` (`donor_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
