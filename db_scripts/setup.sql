CREATE TABLE therapists (
	therapist_id INTEGER PRIMARY KEY AUTOINCREMENT,
	pt_id INTEGER, 
	name TEXT NOT NULL,
	summary TEXT,
	phone TEXT
);

CREATE TABLE th_location (
	therapist_id INTEGER,
	addr TEXT,
	zip INTEGER
);

CREATE TABLE th_specialties (
	therapist_id INTEGER,
	specialty TEXT
);

CREATE TABLE th_issues (
	therapist_id INTEGER,
	issue TEXT
);

CREATE TABLE th_mental_health_focus (
	therapist_id INTEGER,
	focus TEXT
);

CREATE TABLE th_sexuality_focus(
	therapist_id INTEGER,
	sexuality TEXT
);

CREATE TABLE th_categories (
	therapist_id INTEGER,
	category TEXT
);

CREATE TABLE th_languages (
	therapist_id INTEGER,
	language TEXT
);

CREATE TABLE th_treatment_orientation (
	therapist_id INTEGER,
	orientation TEXT
);

CREATE TABLE th_modality (
	therapist_id INTEGER,
	modality TEXT
);

CREATE TABLE th_insurance (
	therapist_id INTEGER,
	insurance TEXT
);