create table users(
    id integer primary key,
    users_id integer UNIQUE
);

create table wordCategory(
    id integer primary key,
    category_name varchar(50),
    category_description varchar(255)
);

CREATE TABLE words(
   id integer primary key,
   word varchar(50),
   word_transcription varchar(50),
   word_translate varchar(50),
   category_id integer,
   FOREIGN KEY (category_id)
       REFERENCES wordCategory (id)
);

create table users_words(
    id integer primary key,
    word_id integer,
    user_id integer,
    true_answer integer DEFAULT 0,
    false_answer integer DEFAULT 0,
    stage integer DEFAULT 0,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
    FOREIGN KEY (word_id)
        REFERENCES words (id)
);





