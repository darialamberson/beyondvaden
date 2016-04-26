var ENTER_KEY_CODE = 13;

var searchInput = document.getElementById('search-enter');
var searchList = document.getElementById('search-results');

searchInput.addEventListener("keydown", function(event) {
  if (event.keyCode === ENTER_KEY_CODE) {
    event.preventDefault();
    showTherapists();
  }
});

/* Shows relevant therapists from search request.
 *
 * Arguments:
 * searchInput -- the HTMLElement search input tag
 */
function showTherapists() {
  if (searchInput.value)  {
    var li = document.createElement('li');
    li.textContent = searchInput.value;
    li.innerHTML += " <a href=\"#\" class=\"delete\"></a> <a href=\"#\" class=\"check\"></a>";

    addTaskListeners(li);
    searchInput.value = "";
    searchList.appendChild(li);
  }
}

/* Handles check/delete events for the given task.
 *
 * Arguments:
 * taskLi -- the HTMLElement li tag
 */
function addTaskListeners(li) {
  var checkbox = li.querySelector('.check');
  checkbox.addEventListener('click', function(event) {
    event.preventDefault();

    if (li.classList.contains('checked')) {
      li.classList.remove('checked');
    } else {
      li.classList.add('checked');
    }
  });

  var deleteButton = li.querySelector('.delete');
  deleteButton.addEventListener('click', function(event) {
    event.preventDefault();
    li.parentNode.removeChild(li);
  });
}
