create table campanhas(
    id serial primary key,
	campanha_nome varchar(200),
	regiao varchar(200),
	local varchar(200),
	descricao varchar(200),
	metadados varchar(200)
);

create table estacoes(
    id serial primary key,
	estacao_nome varchar(200),
	campanha_id int references campanhas(id) on delete cascade,
	lat double precision,
	long double precision,
	date date,
	time time,
	descricao varchar(200)
);

create table limnologia(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	chla double precision default null,
	feofitina double precision default null,
	tss double precision default null,
	tsi double precision default null,
	tso double precision default null,
	secchi double precision default null,
	dtc double precision default null,
	dic double precision default null,
	doc double precision default null,
	acdom440 double precision default null,
	profundidade double precision default null,
	turbidez double precision default null,
	ficocianina double precision default null,
	clorofila_sonda double precision default null,
	ficocianina_sonda double precision default null,
	acdom_sonda double precision default null
);

create table rrs_completa(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null
);

create table rrs_mediana(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade
);

create table acs_atenuation_ts(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	profundidade double precision default null
);

create table acs_ts(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	profundidade double precision default null
);

create table acs_kirk(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	profundidade double precision default null
);

create table acs_flat(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	profundidade double precision default null
);

create table acdom(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade
);

create table kd(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade
);

create table adet_mean(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade
);

create table aphy_mean(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade
);

create table es(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null
);

create table ed(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null,
	profundidade double precision default null
);

create table eu(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null,
	profundidade double precision default null
);

create table lsky(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null
);

create table lw(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null
);

create table lu(
	id serial primary key,
	estacoes_id int references estacoes(id) on delete cascade,
	datetime timestamp default null,
	profundidade double precision default null
);

do $$
declare
    i integer;
    tabela varchar(25) := 'rrs_completa';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;
    

do $$
declare
    i integer;
    tabela varchar(25) := 'rrs_mediana';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'acs_atenuation_ts';
    lower_bound integer := 400;
    upper_bound integer := 750;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'acs_ts';
    lower_bound integer := 400;
    upper_bound integer := 750;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'acs_kirk';
    lower_bound integer := 400;
    upper_bound integer := 750;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'acs_flat';
    lower_bound integer := 400;
    upper_bound integer := 750;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;

do $$
declare
    i integer;
    tabela varchar(25) := 'acdom';
    lower_bound integer := 220;
    upper_bound integer := 800;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;

do $$
declare
    i integer;
    tabela varchar(25) := 'kd';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'adet_mean';
    lower_bound integer := 220;
    upper_bound integer := 800;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'aphy_mean';
    lower_bound integer := 220;
    upper_bound integer := 800;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'es';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'ed';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'eu';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'lsky';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'lw';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;


do $$
declare
    i integer;
    tabela varchar(25) := 'lu';
    lower_bound integer := 400;
    upper_bound integer := 900;
begin
    for i in lower_bound..upper_bound loop
        execute format('ALTER TABLE %s ADD COLUMN X%s DOUBLE PRECISION DEFAULT NULL', tabela, i);
    end loop;
end $$;