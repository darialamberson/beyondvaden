class CreateThSexualityFocuses < ActiveRecord::Migration
  def change
    create_table :th_sexuality_focuses do |t|
      t.integer :therapist_id
      t.text :sexuality

      t.timestamps null: false
    end
  end
end
