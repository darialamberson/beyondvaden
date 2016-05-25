class CreateThMentalHealthFocuses < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_mental_health_focuses))
      create_table :th_mental_health_focuses do |t|
        t.integer :therapist_id
        t.text :focus

        t.timestamps null: false
      end
    end
  end
end
