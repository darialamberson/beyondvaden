class TherapistsController < ApplicationController
  before_action :set_therapist, only: [:show, :edit, :update, :destroy]

  # GET /therapists
  # GET /therapists.json
  def index
    @therapists = Therapist.all
  end

  # GET /therapists/1
  # GET /therapists/1.json
  def show
  end

  # GET /therapists/new
  def new
    @therapist = Therapist.new
  end

  # GET /therapists/1/edit
  def edit
  end

  def home
  end

  def search
    @search_therapists = getCategoriesAndTherapists(params[:query]).last
    @therapists = Therapist.all
  end

  # POST /therapists
  # POST /therapists.json
  def create
    @therapist = Therapist.new(therapist_params)

    respond_to do |format|
      if @therapist.save
        format.html { redirect_to @therapist, notice: 'Therapist was successfully created.' }
        format.json { render :show, status: :created, location: @therapist }
      else
        format.html { render :new }
        format.json { render json: @therapist.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /therapists/1
  # PATCH/PUT /therapists/1.json
  def update
    respond_to do |format|
      if @therapist.update(therapist_params)
        format.html { redirect_to @therapist, notice: 'Therapist was successfully updated.' }
        format.json { render :show, status: :ok, location: @therapist }
      else
        format.html { render :edit }
        format.json { render json: @therapist.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /therapists/1
  # DELETE /therapists/1.json
  def destroy
    @therapist.destroy
    respond_to do |format|
      format.html { redirect_to therapists_url, notice: 'Therapist was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  #Returns a pair where p[0] is an array containing the
  #top three categories, and p[1] is an array containing
  #therapist ids in descending order of relevance
  def getCategoriesAndTherapists(query)
    query = query.gsub("'", "")

    f = open("|python ../nlp/FindTherapistsByQuery.py #{query}")
    output = f.read().strip().gsub("\n", ", ").split(", ")
    categories = Array.new()

    output[0..2].each do |x|
      x.sub!('[', '')
      x.sub!(']', '')
      categories << x
    end

    therapists = Array.new()
    output[3..-1].each do |x|
      x.sub!('[', '')
      x.sub!(']', '')
      therapists << x.to_i
    end
    return [categories,therapists]
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_therapist
      @therapist = Therapist.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def therapist_params
      params.require(:therapist).permit(:pt_id, :name, :summary, :phone)
    end
end
