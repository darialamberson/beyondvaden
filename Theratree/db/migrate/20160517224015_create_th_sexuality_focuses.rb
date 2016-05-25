class CreateThSexualityFocuses < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_sexuality_focuses))
      create_table :th_sexuality_focuses do |t|
        t.integer :therapist_id
        t.text :sexuality

        t.timestamps null: false
      end
    end
  end
end
