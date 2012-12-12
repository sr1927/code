delimiter $$

CREATE TABLE `lender` (
  `lender_id` varchar(100) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `image_id` int(11) DEFAULT NULL,
  `template_id` int(11) DEFAULT NULL,
  `whereabouts` varchar(100) DEFAULT NULL,
  `country_code` varchar(100) DEFAULT NULL,
  `lender_uid` varchar(100) DEFAULT NULL,
  `member_since` date DEFAULT NULL,
  `personal_url` varchar(4000) DEFAULT NULL,
  `occupation` varchar(4000) DEFAULT NULL,
  `loan_because` text,
  `occupational_info` text,
  `loan_count` int(11) DEFAULT NULL,
  `invitee_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`lender_id`)
) ;



CREATE TABLE `loan` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `funded_amount` int(11) DEFAULT NULL,
  `paid_amount` int(11) DEFAULT NULL,
  `image_id` int(11) DEFAULT NULL,
  `template_id` int(11) DEFAULT NULL,
  `activity` varchar(100) DEFAULT NULL,
  `sector` varchar(100) DEFAULT NULL,
  `uses` varchar(4000) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `town` varchar(100) DEFAULT NULL,
  `geoLevel` varchar(100) DEFAULT NULL,
  `geoPairs` varchar(100) DEFAULT NULL,
  `geoType` varchar(100) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `disbursal_amount` int(11) DEFAULT NULL,
  `disbursal_currency` varchar(100) DEFAULT NULL,
  `disbursal_date` date DEFAULT NULL,
  `loan_amount` int(11) DEFAULT NULL,
  `nonpayment` varchar(100) DEFAULT NULL,
  `currency_exchange` varchar(100) DEFAULT NULL,
  `posted_date` date DEFAULT NULL,
  `funded_date` date DEFAULT NULL,
  `defaulted_date` date DEFAULT NULL,
  `paid_date` date DEFAULT NULL,
  `refunded_date` date DEFAULT NULL,
  `journal_entries` int(11) DEFAULT NULL,
  `journal_bulk_entries` int(11) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;



CREATE TABLE `partner` (
  `id` int(11) NOT NULL,
  `name` varchar(4000) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `image_id` int(11) DEFAULT NULL,
  `template_id` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `delinquency_rate` int(11) DEFAULT NULL,
  `default_rate` int(11) DEFAULT NULL,
  `total_amount_raised` int(11) DEFAULT NULL,
  `loans_posted` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;

