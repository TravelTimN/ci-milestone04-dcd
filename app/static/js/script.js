$(document).ready(function () {

    // tooltip functionality for Materialize
    $(".tooltipped").tooltip();

    // Materialize dropdowns
    $("select").formSelect();
    // solution to dropdowns not enforcing validation: https://stackoverflow.com/questions/34248898/how-to-validate-select-option-for-a-materialize-dropdown
    $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: "absolute"});

    // Add new ingredient item if clicked
    let ingredientCount = $(".ingredient").length;
    $(".add-ingredient").on("click", function () {
        // 'destroy' is needed in order to clone select fields
        $("select").formSelect("destroy");
        // clone the ingredient line, and remove its values
        $(".new-ingredient:first").clone().insertBefore(".add-ingredient").find("input[type='text'], select").val("");
        $("select").formSelect();
        // increase counter so original ingredient never gets deleted
        ingredientCount += 1;
    });
    // Delete last item in ingredients if clicked
    $(".remove-ingredient").on("click", function () {
        if (ingredientCount > 1) {
            // only remove the :last item
            $(this).siblings(".new-ingredient:last").remove();
            // ensure original ingredient line never gets deleted
            ingredientCount -= 1;
        }
    });


    // Add new direction if clicked
    let directionCount = $(".direction").length;
    $(".add-direction").on("click", function () {
        // clone the direction line, and remove its value
        $(".new-direction:first").clone().insertBefore(".add-direction").find("input[type='text']").val("");
        // increase counter so original direction never gets deleted
        directionCount += 1;
    });
    // Delete last direction if clicked
    $(".remove-direction").on("click", function () {
        if (directionCount > 1) {
            // only remove the :last item
            $(this).siblings(".new-direction:last").remove();
            // ensure original direction line never gets deleted
            directionCount -= 1;
        }
    });

});