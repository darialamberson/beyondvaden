class CreateThIssues < ActiveRecord::Migration
  def change
    if !(table_exists?(:th_issues))
      create_table :th_issues do |t|
        t.integer :therapist_id
        t.text :issue

        t.timestamps null: false
      end
    end
  end
end
