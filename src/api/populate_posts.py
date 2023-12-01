import sqlalchemy
import os
import dotenv
import numpy as np
import math
import random
from   faker import Faker


def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("POSTGRES_URI")


# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

with engine.begin() as conn:
    conn.execute(
        sqlalchemy.text(
        """
        DROP TABLE IF EXISTS volunteers CASCADE;
        DROP TABLE IF EXISTS organizations CASCADE;
        DROP TABLE IF EXISTS supervisors CASCADE;
        DROP TABLE IF EXISTS events;
        DROP TABLE IF EXISTS volunteer_schedule;

        CREATE TABLE
        volunteers (
            volunteer_id bigint generated by default as identity,
            created_at timestamp with time zone not null default now(),
            name text not null,
            city text not null,
            email text not null,
            birthday date null,
            constraint volunteers_pkey primary key (volunteer_id),
            constraint volunteers_email_key unique (email)
        ); 

        CREATE TABLE
        organizations (
            org_id bigint generated by default as identity,
            created_at timestamp with time zone not null default now(),
            name text not null,
            city text not null,
            constraint organizations_pkey primary key (org_id),
            constraint organizations_name_key unique (name),
            constraint organizations_org_id_key unique (org_id)
        );   

        CREATE TABLE
        supervisors (
            sup_id bigint generated by default as identity,
            created_at timestamp with time zone not null default now(),
            org_id bigint not null,
            sup_name text not null,
            email text not null,
            constraint supervisor_pkey primary key (sup_id),
            constraint supervisor_email_key unique (email),
            constraint supervisors_org_id_fkey foreign key (org_id) references organizations (org_id)
        );   

        CREATE TABLE
        events (
            event_id bigint generated by default as identity,
            created_at timestamp with time zone not null default now(),
            sup_id bigint not null,
            name text not null,
            total_spots integer not null default 0,
            min_age integer not null,
            activity_level integer not null default 0,
            location text not null,
            start_time timestamp with time zone not null,
            end_time timestamp with time zone not null,
            description text null,
            constraint event_pkey primary key (event_id),
            constraint events_sup_id_fkey foreign key (sup_id) references supervisors (sup_id)
        );   

        CREATE TABLE
        volunteer_schedule (
            schedule_id bigint generated by default as identity,
            volunteer_id bigint not null,
            event_id bigint not null,
            constraint volunteer_schedule_pkey primary key (schedule_id),
            constraint volunteer_schedule_volunteer_id_fkey foreign key (volunteer_id) references volunteers (volunteer_id) on delete cascade
        );    

        """))

num_vol_rows = 265500
num_event_rows = math.ceil(num_vol_rows / 25.9)
num_org_rows = math.ceil(num_event_rows / 4.3)
num_sup_rows = math.ceil(num_org_rows * 2.2)
num_sched_rows = math.ceil(num_vol_rows * 2.7)
total_rows = num_vol_rows + num_org_rows + num_sup_rows + num_event_rows + num_sched_rows
print("\nvolunteers: {}".format(num_vol_rows))
print("events: {}".format(num_event_rows))
print("organizations: {}".format(num_org_rows))
print("supervisors: {}".format(num_sup_rows))
print("schedules: {}".format(num_sched_rows))


fake = Faker()

with engine.begin() as conn:

    # Create volunteers
    for i in range(num_vol_rows):
        name = fake.name()
        city = fake.city()
        email = fake.unique.email()
        birthday = fake.date_of_birth(None, 6, 98)  # Sets a min and max age

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO volunteers (name, city, email, birthday) 
                VALUES (:name, :city, :email, :birthday);
                """), 
                {"name": name, 
                "city": city, 
                "email": email, 
                "birthday": birthday})
    
    # Create organizations
    for i in range(num_org_rows):
        name = fake.unique.company()
        city = fake.city()

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO organizations (name, city) 
                VALUES (:name, :city);
                """), 
                {"name": name, 
                "city": city})

    # Create supervisors
    for i in range(num_sup_rows):
        org_id = i % num_org_rows + 1
        sup_name = fake.name()
        email = fake.unique.email()

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO supervisors (org_id, sup_name, email) 
                VALUES (:org_id, :sup_name, :email);
                """), 
                {"org_id": org_id, 
                "sup_name": sup_name,
                "email": email})
    
    # Create events
    for i in range(num_event_rows):
        sup_id = random.randint(1, num_sup_rows)
        name = fake.bs()
        total_spots = random.randint(15, 100)
        min_age = random.randint(0, 18)
        activity_level = random.randint(0, 5)
        location = fake.city()
        start_time = fake.future_datetime()
        end_time = fake.future_datetime()
        description = fake.sentence(nb_words = 5)

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO events (sup_id, name, total_spots, min_age, activity_level, location, start_time, end_time, description) 
                VALUES (:sup_id, :name, :total_spots, :min_age, :activity_level, :location, :start_time, :end_time, :description);
                """), 
                {"sup_id": sup_id, 
                "name": name, 
                "total_spots": total_spots, 
                "min_age": min_age, 
                "activity_level": activity_level, 
                "location": location, 
                "start_time": start_time, 
                "end_time": end_time, 
                "description": description})

    # Create schedules
    for i in range(num_sched_rows):
        volunteer_id = random.randint(1, num_vol_rows)
        event_id = random.randint(1, num_event_rows)

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO volunteer_schedule (volunteer_id, event_id) 
                VALUES (:volunteer_id, :event_id);
                """), 
                {"volunteer_id": volunteer_id, 
                "event_id": event_id})

    print("total rows added: ", total_rows)