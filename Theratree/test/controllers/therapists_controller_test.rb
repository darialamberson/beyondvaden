require 'test_helper'

class TherapistsControllerTest < ActionController::TestCase
  setup do
    @therapist = therapists(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:therapists)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create therapist" do
    assert_difference('Therapist.count') do
      post :create, therapist: { name: @therapist.name, phone: @therapist.phone, pt_id: @therapist.pt_id, summary: @therapist.summary }
    end

    assert_redirected_to therapist_path(assigns(:therapist))
  end

  test "should show therapist" do
    get :show, id: @therapist
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @therapist
    assert_response :success
  end

  test "should update therapist" do
    patch :update, id: @therapist, therapist: { name: @therapist.name, phone: @therapist.phone, pt_id: @therapist.pt_id, summary: @therapist.summary }
    assert_redirected_to therapist_path(assigns(:therapist))
  end

  test "should destroy therapist" do
    assert_difference('Therapist.count', -1) do
      delete :destroy, id: @therapist
    end

    assert_redirected_to therapists_path
  end
end
