class Therapist < ActiveRecord::Base
  has_many :th_category
  has_many :th_insurance
  has_many :th_issue
  has_many :th_language
  has_many :th_location
  has_many :th_mental_health_focus
  has_many :th_modality
  has_many :th_sexuality_focus
  has_many :th_specialty
  has_many :th_treatment_orientation
  has_one  :th_photo
end
