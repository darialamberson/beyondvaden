json.array!(@therapists) do |therapist|
  json.extract! therapist, :id, :pt_id, :name, :summary, :phone
  json.url therapist_url(therapist, format: :json)
end
