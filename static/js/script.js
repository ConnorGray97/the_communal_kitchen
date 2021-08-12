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


// Credit: 
// Code inspired from https://github.com/rebeccatraceyt/bake-it-til-you-make-it/blob/master/static/js/recipe.js


let maxIngredients = 30;
let ingredientRow = document.getElementById('ingredient-row');
let addIngredient = document.getElementById('add-ingredient');
let ingredient = 1;

let maxSteps = 30;
let methodRow = document.getElementById('prep-step');
let addStep = document.getElementById('add-step');
let step = 1;

// Append new ingredient div

const appendIngredient = (e) => {
  e.preventDefault();

  if (ingredient < maxIngredients) {
    ingredient++;
    let newIngredientField = document.createElement('div');
    newIngredientField.innerHTML = `
    
      <div class="input-field col s12 m8 l8">
          <input id="ingredient_name_1" name="ingredient_name" type="text" maxlength="100">
          <label for="ingredient_name_1">Ingredient</label>
      </div>
      <!-- Amount -->
      <div class="input-field col s4 m1 l2">
          <input id="amount_1" type="text" maxlength="10">
          <label for="amount_1">Amount</label>
      </div>
      <!-- Unit -->
      <div class="input-field col s4 m1 l2 right">
          <input id="unit_1" type="text" maxlength="10">
          <label for="unit_1">Unit</label>
      </div>
      
      <a href="#" class="remove-field text-shadow"><i class="fas fa-trash-alt fa-2x"></i></a>
      
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
      let newStepField = document.createElement('div');
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
  <a href="#" class="remove-step text-shadow"><i class="fas fa-trash-alt"></i></a>`;
      // append to parent element
      methodRow.append(newStepField);
  }
};
// Delete input field

$(ingredientRow).on('click', '.remove-field', function(e) {
  e.preventDefault();
  $(this).parent('div').remove();
  ingredient--;
});

$(methodRow).on('click', '.remove-step', function(e) {
  e.preventDefault();
  $(this).parent('div').remove();
  step--;
});



//End Delete input field

// Event Listeners

addStep.addEventListener('click', addNewStep);

addIngredient.addEventListener('click', appendIngredient);