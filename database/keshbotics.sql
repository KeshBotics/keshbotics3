-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 26, 2021 at 09:18 AM
-- Server version: 5.7.32-0ubuntu0.16.04.1
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
-- Table structure for table `logging`
--

CREATE TABLE `logging` (
  `id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `level` int(11) NOT NULL,
  `pathname` text COLLATE utf8mb4_bin,
  `class_name` text COLLATE utf8mb4_bin,
  `function_name` text COLLATE utf8mb4_bin,
  `exc_info` text COLLATE utf8mb4_bin,
  `message` text COLLATE utf8mb4_bin
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
-- Table structure for table `twitch_channels`
--

CREATE TABLE `twitch_channels` (
  `twitch_user_id` int(11) NOT NULL,
  `twitch_username` text COLLATE utf8mb4_bin NOT NULL,
  `streaming` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `twitch_notifications`
--

CREATE TABLE `twitch_notifications` (
  `id` int(11) NOT NULL,
  `twitch_user_id` text COLLATE utf8_bin NOT NULL,
  `discord_guild_id` text COLLATE utf8_bin,
  `discord_channel_id` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `youtube_channels`
--

CREATE TABLE `youtube_channels` (
  `id` int(11) NOT NULL,
  `yt_channel_id` text COLLATE utf8mb4_bin NOT NULL,
  `yt_display_name` text COLLATE utf8mb4_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `youtube_notifications`
--

CREATE TABLE `youtube_notifications` (
  `id` int(11) NOT NULL,
  `yt_channel_id` text COLLATE utf8_bin NOT NULL,
  `discord_guild_id` text COLLATE utf8_bin,
  `discord_channel_id` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `youtube_submissions`
--

CREATE TABLE `youtube_submissions` (
  `id` int(11) NOT NULL,
  `yt_video_id` text COLLATE utf8_bin NOT NULL
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
-- Indexes for table `logging`
--
ALTER TABLE `logging`
  ADD PRIMARY KEY (`id`);

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
-- Indexes for table `twitch_channels`
--
ALTER TABLE `twitch_channels`
  ADD PRIMARY KEY (`twitch_user_id`);

--
-- Indexes for table `twitch_notifications`
--
ALTER TABLE `twitch_notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `youtube_channels`
--
ALTER TABLE `youtube_channels`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `youtube_notifications`
--
ALTER TABLE `youtube_notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `youtube_submissions`
--
ALTER TABLE `youtube_submissions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cron_event`
--
ALTER TABLE `cron_event`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4388;
--
-- AUTO_INCREMENT for table `logging`
--
ALTER TABLE `logging`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
  MODIFY `setting_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `stream_metrics_time`
--
ALTER TABLE `stream_metrics_time`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1563;
--
-- AUTO_INCREMENT for table `twitch_notifications`
--
ALTER TABLE `twitch_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;
--
-- AUTO_INCREMENT for table `youtube_channels`
--
ALTER TABLE `youtube_channels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT for table `youtube_notifications`
--
ALTER TABLE `youtube_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;
--
-- AUTO_INCREMENT for table `youtube_submissions`
--
ALTER TABLE `youtube_submissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1734;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
