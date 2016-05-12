class SearchController < ApplicationController
  before_action :set_therapist, only: [:show, :edit, :update, :destroy]

  # returns list of therapist IDs in ranked order
  def getTherapists(query)
  end

end
