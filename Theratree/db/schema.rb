# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20160517224015) do

  create_table "th_categories", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "category"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_insurance", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "insurance"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_insurances", force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "insurance"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_issues", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "issue"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_languages", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "language"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_location", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "addr"
    t.integer  "zip"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_locations", force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "addr"
    t.integer  "zip"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_mental_health_focus", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "focus"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_mental_health_focuses", force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "focus"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_modalities", force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "modality"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_modality", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "modality"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_sexuality_focus", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "sexuality"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_sexuality_focuses", force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "sexuality"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_specialties", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "specialty"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_treatment_orientation", id: false, force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "orientation"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "th_treatment_orientations", force: :cascade do |t|
    t.integer  "therapist_id"
    t.text     "orientation"
    t.datetime "created_at",   null: false
    t.datetime "updated_at",   null: false
  end

  create_table "therapists", primary_key: "therapist_id", force: :cascade do |t|
    t.integer  "pt_id"
    t.text     "name",       null: false
    t.text     "summary"
    t.text     "phone"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
