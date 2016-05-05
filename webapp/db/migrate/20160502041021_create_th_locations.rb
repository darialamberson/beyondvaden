class CreateThLocations < ActiveRecord::Migration
  def change
    create_table :th_locations do |t|
      t.integer :therapist_id
      t.text :addr
      t.integer :zip

      t.timestamps null: false
    end
  end
end
