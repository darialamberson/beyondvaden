class CreateThLocations < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_locations))
      create_table :th_locations do |t|
        t.integer :therapist_id
        t.text :addr
        t.integer :zip

        t.timestamps null: false
      end
    end
  end
end
