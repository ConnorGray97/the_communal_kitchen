// ------------------------ Materialize Initialization

$(document).ready(function () {
  $('.sidenav').sidenav({
    edge: "right"
  });
});

$(document).ready(function () {
  $('select').formSelect();
});

// ------------------------ End Materialize Initialization

$(document).ready(function () {
  $('flashes').delay(5000).slideUp(300);
});

// Credit: 
// Code inspired from https://github.com/rebeccatraceyt/bake-it-til-you-make-it/blob/master/static/js/recipe.js


var maxIngredients = 30;
var ingredientRow = document.getElementById('ingredient');
var addIngredient = document.getElementById('add-ingredient');
var ingredient = 1;

var maxSteps = 30;
var methodRow = document.getElementById('prep-step');
var addStep = document.getElementById('add-step');
var step = 1;

// Append new ingredient div

const appendIngredient = (e) => {
  e.preventDefault();

  if (ingredient < maxIngredients) {
    ingredient++;
    var newIngredientField = document.createElement('div');
    newIngredientField.innerHTML = `
                <div class="row">
                    <div class="input-field col s12">
                        <input id="ingredient_name_1" name="ingredient_name" type="text">
                        <label for="ingredient_name_1">Ingredient</label>
                    </div>
                </div>
                <!-- Amount -->
                <div class="row">
                    <div class="input-field col s6">
                        <input id="amount_1" name="amount" type="text">
                        <label for="amount_1">Amount</label>
                    </div>
                    <!-- Unit -->
                    <div class="input-field col s6 m6">
                        <input id="unit_1" type="text" name="unit">
                        <label for="unit_1">Unit</label>
                    </div>
                </div>
      
      <a href="#" class="remove-field text-shadow right"><i class="fas fa-trash-alt fa-2x"></i></a>
      
  `;
    ingredientRow.append(newIngredientField);


  }
};

const addNewStep = (e) => {
  // prevent default action
  e.preventDefault();
  // check if step is less than max
  if (step < maxSteps) {
    step++;
    // create new div element
    var newStepField = document.createElement('div');
    // set the inner HTML
    newStepField.innerHTML = `
  <div class="row recipe-item" id="prep-step">
      <div class="col s12">
          <div class="input-field prep_step col s12">
              <textarea name="prep_step" id="prep_step_1" maxlength="500"></textarea>
              <label for="prep_step_1">Enter Preparation Step</label>
          </div>
      </div>
  </div>
  <a href="#" class="remove-step text-shadow center-align right"><i class="fas fa-trash-alt fa-2x"></i></a>`;
    // append to parent element
    methodRow.append(newStepField);
  }
};
// Delete input field

$(ingredientRow).on('click', '.remove-field', function (e) {
  e.preventDefault();
  $(this).parent('div').remove();
  ingredient--;
});

$(methodRow).on('click', '.remove-step', function (e) {
  e.preventDefault();
  $(this).parent('div').remove();
  step--;
});



//End Delete input field

// Event Listeners

addStep.addEventListener('click', addNewStep);

addIngredient.addEventListener('click', appendIngredient);