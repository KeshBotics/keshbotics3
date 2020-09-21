-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 21, 2020 at 04:03 PM
-- Server version: 5.7.31-0ubuntu0.16.04.1
-- PHP Version: 7.2.33-1+ubuntu16.04.1+deb.sury.org+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `keshbotics`
--

-- --------------------------------------------------------

--
-- Table structure for table `cron_event`
--

CREATE TABLE `cron_event` (
  `event_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `setting_id` int(11) NOT NULL,
  `setting_key` text COLLATE utf8_bin,
  `setting_value` text COLLATE utf8_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `stream_metrics_time`
--

CREATE TABLE `stream_metrics_time` (
  `id` int(11) NOT NULL,
  `twitch_user_id` text COLLATE utf8_bin NOT NULL,
  `stream_start` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `stream_stop` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `twitch`
--

CREATE TABLE `twitch` (
  `id` int(11) NOT NULL,
  `twitch_username` text COLLATE utf8_bin NOT NULL,
  `twitch_user_id` text COLLATE utf8_bin NOT NULL,
  `discord_channel_id` text COLLATE utf8_bin NOT NULL,
  `streaming` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cron_event`
--
ALTER TABLE `cron_event`
  ADD PRIMARY KEY (`event_id`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`setting_id`);

--
-- Indexes for table `stream_metrics_time`
--
ALTER TABLE `stream_metrics_time`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `twitch`
--
ALTER TABLE `twitch`
  ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
