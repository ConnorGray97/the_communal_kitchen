// ------------------------ Materialize Initialization

$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
  });

  $(document).ready(function(){
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
      <div id="ingredient-row">
      <div class="input-field col s12 m8 l8">
          <input id="ingredient_name_1" name="ingredient_name" type="text" maxlength="100">
          <label for="ingredient_name_1">Ingredient</label>
      </div>
      <!-- Amount -->
      <div class="input-field col s4 m1 l2 right">
          <input id="amount_1" type="text" maxlength="10">
          <label for="amount_1">Amount</label>
      </div>
      <!-- Unit -->
      <div class="input-field col s4 m1 l2 right">
          <input id="unit_1" type="text" maxlength="10">
          <label for="unit_1">Unit</label>
      </div>
  </div>`;
      ingredientRow.append(newIngredientField);


    }
  };

  // Event Listeners

  addIngredient.addEventListener('click', appendIngredient);