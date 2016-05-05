class CreateThLanguages < ActiveRecord::Migration
  def change
    create_table :th_languages do |t|
      t.integer :therapist_id
      t.text :language

      t.timestamps null: false
    end
  end
end
