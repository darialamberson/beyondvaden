class CreateThModalities < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_modalities))
      create_table :th_modalities do |t|
        t.integer :therapist_id
        t.text :modality

        t.timestamps null: false
      end
    end
  end
end
