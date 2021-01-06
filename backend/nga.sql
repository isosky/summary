drop table nga_post;
CREATE TABLE nga_post (
    post_id VARCHAR (200) PRIMARY KEY COMMENT 'id',
    replies INT COMMENT '姓名',
    post_title VARCHAR (2000) COMMENT '主题',
    poster_id VARCHAR (15) COMMENT "楼主id",
    sub VARCHAR (20) COMMENT "社区",
    post_time DATETIME COMMENT "发帖时间",
    collect_time DATETIME COMMENT "上次采集时间",
    is_finish INT COMMENT "是否过期"
);
drop table nga_reply;
CREATE TABLE nga_reply(
    post_id varchar(200) COMMENT 'id',
    poster_id VARCHAR(15) COMMENT '回复id',
    replys INT COMMENT '楼层',
    reply_time DATETIME COMMENT '评论时间',
    reply_content text COMMENT '评论',
    PRIMARY KEY (post_id, replys)
);
drop table nga_attach;
CREATE table nga_attach(
    post_id varchar(200) COMMENT 'id',
    poster_id VARCHAR(15) COMMENT '回复id',
    replys INT COMMENT '楼层',
    attach_url varchar(100) COMMENT '附件链接',
    is_download INT default 0 COMMENT '是否下载',
    PRIMARY KEY (post_id, replys, attach_url)
);
-- insert into nga_post (post_id,replies,post_title,poster_id,sub) values ('24978680',123,'','','') 
-- on duplicate key update replies=VALUES(replies);
-- select * from nga_post where post_id='24978680';
truncate table nga_post;
truncate table nga_reply;
truncate table nga_attach;