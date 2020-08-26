CREATE TABLE public.anime (
    id int,
    title varchar(64) not null,
    aka varchar(256),
    genre varchar(64) not null,
    mediaType varchar(32) not null,
    numEpisodes int,
    minsPerEpisode int not null,
    distributor varchar(64) not null,
    contentRating varchar(10) not null,
    revURL varchar(32) not null,
    primary key (id)
);