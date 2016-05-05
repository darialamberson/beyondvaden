class CreateThSpecialties < ActiveRecord::Migration
  def change
    create_table :th_specialties do |t|
      t.integer :therapist_id
      t.text :specialty

      t.timestamps null: false
    end
  end
end
