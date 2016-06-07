class CreateThPhotos < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_photos))
      create_table :th_photos do |t|
        t.integer :therapist_id
        t.text :img_url

        t.timestamps null: false
      end
    end
  end
end
