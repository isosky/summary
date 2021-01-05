CREATE TABLE nga_post (
    post_id VARCHAR (200) PRIMARY KEY COMMENT 'id',
    replies INT COMMENT '姓名',
    post_title VARCHAR (2000) COMMENT '主题',
    poster_id VARCHAR (15) COMMENT "楼主id",
    sub VARCHAR (10) COMMENT "社区",
    post_time DATETIME COMMENT "发帖时间",
    collect_time DATETIME COMMENT "上次采集时间",
    is_finish INT COMMENT "是否过期"
);
CREATE TABLE nga_reply(
    post_id varchar(200) COMMENT 'id',
    poster_id VARCHAR(15) COMMENT '回复id',
    replys INT,
    reply_time DATETIME,
    reply_content VARCHAR(2000)
);
CREATE table nga_attach(
    post_id varchar(200) COMMENT 'id',
    poster_id VARCHAR(15) COMMENT '回复id',
    attach_url varchar(100),
    is_download INT
);