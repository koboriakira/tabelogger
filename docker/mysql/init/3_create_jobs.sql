CREATE TABLE tabelogger.jobs (
  `job_id` varchar(100) NOT NULL PRIMARY KEY
  , `status` varchar(1000) NOT NULL
  , `url` varchar(767) NOT NULL
  , `limit_page_count` smallint NOT NULL
  , `create_datetime` datetime NOT NULL
  , `update_datetime` datetime NOT NULL
);
commit;
