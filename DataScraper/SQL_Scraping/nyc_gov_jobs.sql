-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 27, 2020 at 05:30 PM
-- Server version: 5.7.24
-- PHP Version: 7.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nyc_gov_jobs`
--

-- --------------------------------------------------------

--
-- Table structure for table `job_info_details`
--

CREATE TABLE `job_info_details` (
  `add_info` text COMMENT 'Additional Info',
  `hours_shift` varchar(200) NOT NULL COMMENT 'Hours/Shift listed',
  `job_descrip` text COMMENT 'Job Description',
  `min_qual` text COMMENT 'Minimum Qualification Requirements',
  `preferred_skills` text COMMENT 'Preferred Skills',
  `recruit_contact` varchar(500) DEFAULT NULL COMMENT 'Recruitment contact for information',
  `residency_req` text COMMENT 'Residency Requirements',
  `to_apply` text COMMENT 'How to apply',
  `work_location` text COMMENT 'Work address or location',
  `jobNum` int(11) NOT NULL COMMENT 'PK-job ID number'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table with full job details stored as raw text dumps.';

-- --------------------------------------------------------

--
-- Table structure for table `job_info_short`
--

CREATE TABLE `job_info_short` (
  `hiring_agency` varchar(200) DEFAULT NULL COMMENT 'Hiring Agency',
  `jobLink` varchar(2083) DEFAULT NULL COMMENT 'Link to the Job',
  `jobNum` int(11) NOT NULL COMMENT 'PK- same as JobID',
  `job_ID` int(11) DEFAULT NULL COMMENT 'Job ID-may be NULL',
  `total_openings` int(11) DEFAULT NULL COMMENT 'Number of openings',
  `business_title` varchar(500) DEFAULT NULL COMMENT 'Office or Agency role',
  `title_code` varchar(100) DEFAULT NULL COMMENT 'DCAS Code',
  `level` varchar(20) DEFAULT NULL COMMENT 'For most is numeric, for managers use M prefix',
  `civil_title` varchar(200) DEFAULT NULL COMMENT 'DCAS title',
  `title_class` varchar(100) DEFAULT NULL COMMENT 'Non-Competitive, exempt, competitive',
  `job_category` varchar(200) DEFAULT NULL COMMENT 'List of categories it falls under',
  `proposed_salary_range` varchar(200) DEFAULT NULL COMMENT 'Salary range in $Min-$Max',
  `career_level` varchar(100) DEFAULT NULL COMMENT 'Expected level of experience ',
  `work_location` varchar(300) DEFAULT NULL COMMENT 'Work site address or Agency HQ address',
  `division_work_unit` varchar(300) DEFAULT NULL COMMENT 'Specific agency unit(EEO Office, General Counsel, etc)',
  `posted` date DEFAULT NULL COMMENT 'Date job posted',
  `post_until` date DEFAULT '2030-01-01' COMMENT 'Date Job expires. Unitl filled replaced with 3020-01-01'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Job Information short meta data information and descriptions';

-- --------------------------------------------------------

--
-- Table structure for table `search_by_agencycode`
--

CREATE TABLE `search_by_agencycode` (
  `jobNum` int(11) NOT NULL COMMENT 'Job ID Number',
  `Title` varchar(300) DEFAULT NULL COMMENT 'Job Title',
  `Link` varchar(2043) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'Job Link',
  `shortCategory` varchar(100) DEFAULT NULL COMMENT 'Shorthand(Code)',
  `LongCategory` varchar(300) DEFAULT NULL COMMENT 'Full Agency Name',
  `Department` varchar(300) DEFAULT NULL COMMENT 'Agency Department',
  `Location` varchar(300) DEFAULT NULL COMMENT 'Address',
  `Agency` varchar(300) DEFAULT NULL COMMENT 'Agency',
  `Posted_Date` date DEFAULT NULL COMMENT 'Wehn Job added'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Scrapes by Agency Code';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `job_info_details`
--
ALTER TABLE `job_info_details`
  ADD PRIMARY KEY (`jobNum`);

--
-- Indexes for table `job_info_short`
--
ALTER TABLE `job_info_short`
  ADD PRIMARY KEY (`jobNum`);

--
-- Indexes for table `search_by_agencycode`
--
ALTER TABLE `search_by_agencycode`
  ADD PRIMARY KEY (`jobNum`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
