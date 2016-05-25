class CreateThInsurances < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_insurances))
      create_table :th_insurances do |t|
        t.integer :therapist_id
        t.text :insurance

        t.timestamps null: false
      end
    end
  end
end
