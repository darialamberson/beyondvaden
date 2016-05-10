class CreateTherapists < ActiveRecord::Migration
  def change
    create_table :therapists do |t|
      t.integer :pt_id
      t.text :name
      t.text :summary
      t.text :phone

      t.timestamps null: false
    end
  end
end
