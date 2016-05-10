class CreateThTreatmentOrientations < ActiveRecord::Migration
  def change
    create_table :th_treatment_orientations do |t|
      t.integer :therapist_id
      t.text :orientation

      t.timestamps null: false
    end
  end
end
