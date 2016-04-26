CREATE TABLE therapists (
    id  INTEGER,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    description TEXT,
    location TEXT,
    specialties TEXT,
    area TEXT,
    ethnicity TEXT,
    age TEXT,
    treatment_orientation TEXT,
    modality TEXT,
    PRIMARY KEY (first_name, last_name, phone_number)
);