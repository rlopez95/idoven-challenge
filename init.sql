CREATE TABLE IF NOT EXISTS users (
    user_id UUID NOT NULL,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id)
);

INSERT INTO public.users (user_id, username, hashed_password, role) VALUES
('0d6e5f50-5277-11ec-8b28-0242ac130003', 'johndoe', '$2b$12$b2YV8Q8TuHS1Hfrrtf1EFehdYYtqz2xN3HjTEi1LFjkxdZzQrJsni', 'USER'),
('7b60c94e-7795-11ec-8067-080027c0cb42', 'daviddoe', '$2b$12$dd4XUZ/ZRaUuoGHJURJnmea.LgsgR1aVNMVuw/KxKZZBnyiBuEEym', 'USER'),
('15f4305a-5277-11ec-8b28-0242ac130003', 'alice', '$2b$12$IY7mAOnXN3HSEp1QJcWP0OU3t2RFbbxj3Eo8fS0dGJy7nT/2bOxqu', 'ADMIN');

-- johndoe, password1
-- daviddoe, pwd
-- alice, password2