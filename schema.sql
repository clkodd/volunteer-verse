create table
  public.events (
    event_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    sup_id uuid not null,
    name text not null,
    total_spots integer not null default 0,
    min_age integer not null,
    activity_level integer not null default 0,
    location text not null,
    start_time timestamp with time zone not null,
    end_time timestamp with time zone not null,
    description text null,
    constraint event_pkey primary key (event_id),
    constraint events_sup_id_fkey foreign key (sup_id) references supervisors (sup_id) on update cascade on delete cascade
  ) tablespace pg_default;

create table
  public.organizations (
    org_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    name text not null,
    city text not null,
    constraint organizations_pkey primary key (org_id),
    constraint organizations_name_key unique (name),
    constraint organizations_org_id_key unique (org_id)
  ) tablespace pg_default;

create table
  public.supervisors (
    sup_id uuid not null default uuid_generate_v4 (),
    created_at timestamp with time zone not null default now(),
    org_id bigint not null,
    sup_name text not null,
    email text not null,
    constraint supervisor_pkey primary key (sup_id),
    constraint supervisor_email_key unique (email),
    constraint supervisors_org_id_fkey foreign key (org_id) references organizations (org_id) on update cascade on delete cascade
  ) tablespace pg_default;

create table
  public.volunteer_schedule (
    volunteer_id uuid not null,
    event_id bigint not null,
    constraint volunteer_schedule_pkey primary key (volunteer_id, event_id),
    constraint volunteer_schedule_event_id_fkey foreign key (event_id) references events (event_id) on delete cascade,
    constraint volunteer_schedule_volunteer_id_fkey foreign key (volunteer_id) references volunteers (volunteer_id) on delete cascade
  ) tablespace pg_default;

create table
  public.volunteers (
    volunteer_id uuid not null default uuid_generate_v4 (),
    created_at timestamp with time zone not null default now(),
    name text not null,
    city text not null,
    email text not null,
    birthday date null,
    constraint volunteers_pkey primary key (volunteer_id),
    constraint volunteers_email_key unique (email)
  ) tablespace pg_default;

/* INSERTS
-- Flow 1 Inserts: Volunteer Registering for an Event
TRUNCATE TABLE organizations
RESTART IDENTITY
CASCADE;

TRUNCATE TABLE volunteers
RESTART IDENTITY
CASCADE;

INSERT INTO organizations (name, city)
VALUES ('Generic Helper Nonprofit', 'Los Angeles');

INSERT INTO supervisors (org_id, sup_name, email)
VALUES (1, 'Michael Scott', 'mscott@dundermifflin.com');

INSERT INTO events (sup_id, name, total_spots, min_age, activity_level, location, start_time, end_time, description) 
VALUES (1, 'Soup kitchen', 30, 15, 1, 'Long Beach',  '2023-11-10T19:00:00+00:00', '2023-11-10T22:00:00+00:00', 'Hand out meals to the hungry.'), 
(1, 'Beach cleanup', 15, 10, 2, 'Los Angeles', '2023-11-13T12:00:00+00:00', '2023-11-13T15:00:00+00:00', 'Come and collect trash from the beach!');

----------

-- Flow 2 Inserts: Volunteer Site Event Coordinator Event Posting
TRUNCATE TABLE organizations
RESTART IDENTITY
CASCADE;

TRUNCATE TABLE volunteers
RESTART IDENTITY
CASCADE;

INSERT INTO organizations (name, city)
VALUES ('Midnight Mission', 'Los Angeles');

INSERT INTO supervisors (org_id, sup_name, email)
VALUES (1, 'Ronnie Badonnie', 'ronnieb@midnightmish.com');

----------

-- Flow 3 Inserts: Volunteer Deleting an Event
TRUNCATE TABLE organizations
RESTART IDENTITY
CASCADE;

TRUNCATE TABLE volunteers
RESTART IDENTITY
CASCADE;

INSERT INTO organizations (name, city)
VALUES ('Midnight Mission', 'Los Angeles');

INSERT INTO supervisors (org_id, sup_name, email)
VALUES (1, 'Ronnie Badonnie', 'ronnieb@midnightmish.com');

INSERT INTO events (sup_id, name, total_spots, min_age, activity_level, location, start_time, end_time, description) 
VALUES (1, 'Midnight Mission Mania', 50, 15, 1, 'Los Angeles',  '2023-11-04T20:00:00Z', '2023-11-04T23:59:59Z', 'Serve food to the homeless at the Midnight Mission to help those in need.'); 

----------

-- Flow 4 Inserts: Admin Resetting the Site
TRUNCATE TABLE organizations
RESTART IDENTITY
CASCADE;

TRUNCATE TABLE volunteers
RESTART IDENTITY
CASCADE;

INSERT INTO organizations (name, city)
VALUES ('Midnight Mission', 'Los Angeles'),
('Generic Helper Nonprofit', 'Los Angeles');

INSERT INTO supervisors (org_id, sup_name, email)
VALUES (1, 'Ronnie', 'ronnie@midnightmish.com'),
(2, 'Michael Scott', 'mscott@dundermifflin.com');

INSERT INTO events (sup_id, name, total_spots, min_age, activity_level, location, start_time, end_time, description) 
VALUES (1, 'Soup kitchen', 30, 15, 1, 'Add me on Genshin Impact',  '2023-11-10T19:00:00+00:00', '2023-11-10T22:00:00+00:00', 'Hand out meals to the hungry.'), 
(2, 'Beach cleanup', 15, 10, 2, 'Add me on Genshin Impact', '2023-11-13T12:00:00+00:00', '2020-11-13T15:00:00+00:00', 'Come and collect trash from the beach!');

*/
