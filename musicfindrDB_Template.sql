-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2024 at 09:11 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `musicfindrdb`
--
CREATE DATABASE IF NOT EXISTS `musicfindrdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `musicfindrdb`;

-- --------------------------------------------------------

--
-- Table structure for table `playlist`
--

CREATE TABLE `playlist` (
  `id` int(11) NOT NULL COMMENT 'Playlist ID',
  `title` varchar(32) NOT NULL,
  `description` varchar(259) NOT NULL,
  `link` varchar(256) NOT NULL,
  `createdBy` int(11) NOT NULL COMMENT 'Foreign Key -> User ID',
  `createdAt` bigint(20) NOT NULL COMMENT 'Unixtime',
  `updatedAt` bigint(20) NOT NULL COMMENT 'Unixtime'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `id` int(11) NOT NULL COMMENT 'Tag ID',
  `title` varchar(32) NOT NULL,
  `createdAt` bigint(20) NOT NULL COMMENT 'Unixtime'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tagplaylist_relationship`
--

CREATE TABLE `tagplaylist_relationship` (
  `id` int(11) NOT NULL,
  `tid` int(11) NOT NULL COMMENT 'Foreign Key -> Tag ID',
  `pid` int(11) NOT NULL COMMENT 'Foreign Key -> Playlist ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL COMMENT 'User ID',
  `username` varchar(20) NOT NULL,
  `password` varchar(69) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'bcrypt Hash',
  `createdAt` bigint(20) NOT NULL COMMENT 'unixtime',
  `updatedAt` bigint(20) NOT NULL COMMENT 'unixtime'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `votes`
--

CREATE TABLE `votes` (
  `id` int(11) NOT NULL COMMENT 'Vote ID',
  `uid` int(11) NOT NULL COMMENT 'Foreign Key -> User ID',
  `tid` int(11) NOT NULL COMMENT 'Foreign Key -> Tag ID',
  `pid` int(11) NOT NULL COMMENT 'Foreign Key -> Playlist ID',
  `value` tinyint(4) NOT NULL COMMENT '-1 = Downvote\r\n 1 = Upvote',
  `createdAt` bigint(20) NOT NULL COMMENT 'Unixtime',
  `updatedAt` bigint(20) NOT NULL COMMENT 'Unixtime'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `playlist`
--
ALTER TABLE `playlist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tagplaylist_relationship`
--
ALTER TABLE `tagplaylist_relationship`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `votes`
--
ALTER TABLE `votes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `playlist`
--
ALTER TABLE `playlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Playlist ID', AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Tag ID', AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `tagplaylist_relationship`
--
ALTER TABLE `tagplaylist_relationship`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=290;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'User ID', AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `votes`
--
ALTER TABLE `votes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Vote ID', AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
