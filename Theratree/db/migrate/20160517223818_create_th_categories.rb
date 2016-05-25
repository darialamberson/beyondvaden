class CreateThCategories < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_categories))
      create_table :th_categories do |t|
        t.integer :therapist_id
        t.text :category

        t.timestamps null: false
      end
    end
  end
end
