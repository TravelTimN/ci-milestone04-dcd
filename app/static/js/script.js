$(document).ready(function () {

    /*----- MATERIALIZE -----*/

    // initialize collapsible
    $(".collapsible").collapsible();

    // initialize tabs
    $(".tabs").tabs();

    // initialize modals
    $(".modal").modal();

    // initialize tooltips
    $(".tooltipped").tooltip();

    // initialize sidenav
    $(".sidenav").sidenav();

    // initialize dropdowns
    $(".dropdown-trigger").dropdown();
    $("select").formSelect();
    // solution to dropdowns not enforcing validation: https://stackoverflow.com/questions/34248898/how-to-validate-select-option-for-a-materialize-dropdown
    $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: "absolute"});

    // initialize input character count
    $("input#search_keyword, textarea").characterCounter();

    // initialize floating action button
    $(".fixed-action-btn").floatingActionButton({toolbarEnabled: true});

    

    /*----- CUSTOMIZATION -----*/

    // custom Flash Toast
    function flashToast() {
        $("#flashToast").addClass("show");
        setTimeout(function() {
            $("#flashToast").removeClass("show");
        }, 4000);
    };
    flashToast();


    // Add new ingredient item if clicked
    let ingredientCount = $(".ingredient").length;
    $(".add-ingredient").on("click", function () {
        // 'destroy' is needed in order to clone select fields
        $("select").formSelect("destroy");
        // clone the ingredient line, and remove its values
        $(".new-ingredient:first").clone().insertBefore(".add-ingredient").find("input[type='text'], select, textarea").val("");
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
        $(".new-direction:first").clone().insertBefore(".add-direction").find("input[type='text'], select, textarea").val("");
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


    // Toggle Classes for Ingredients + Directions once user 
    $(".ingredient-item").on("click", function () {
        $(this).children("i").toggleClass("fa-circle fa-check-circle green-text");
        $(this).closest("li").find("span").toggleClass("grey-text strike");
    });
    $(".direction-item").on("click", function () {
        $(this).toggleClass("grey-text strike");
        $(this).toggleClass("completed");
    });


    // get current year for Copyright
    $("#year").html(new Date().getFullYear());


    // only enable allergen filter + submit button if user searches with one of the other fields
    search_keyword = $("#search_keyword").val();
    search_dessert = $("#search_dessert").val();
    sort_value = $("#sort").val();
    // on load
    if (search_keyword > "" || search_dessert > "") {
        $("#search_allergen, #sort").prop("disabled", false);
        $("i.fa-ban, i.fa-sort-amount-down").removeClass("grey-text").addClass("purple-text");
        $("select").formSelect();
        $("#search_btn").prop("disabled", false).addClass("text-shadow-2");
        // if results, collapsible should be open
        var instance = M.Collapsible.getInstance($(".collapsible")); instance.open();
    }
    else {
        $("#search_allergen, #sort").prop("disabled", true);
            $("i.fa-ban, i.fa-sort-amount-down").removeClass("purple-text").addClass("grey-text");
            $("select").formSelect();
            $("#search_btn").prop("disabled", true).removeClass("text-shadow-2");
    }
    // on user interaction
    $("#search_keyword, #search_dessert").on("keyup input change", function() {
        if ($("#search_keyword").val().length >= 3 || $("#search_dessert").val().length > 0) {
            $("#search_allergen, #sort").prop("disabled", false);
            $("i.fa-ban, i.fa-sort-amount-down").removeClass("grey-text").addClass("purple-text");
            $("select").formSelect();
            $("#search_btn").prop("disabled", false).addClass("text-shadow-2");
        }
        else {
            $("#search_allergen, #sort").prop("disabled", true);
            $("i.fa-ban, i.fa-sort-amount-down").removeClass("purple-text").addClass("grey-text");
            $("select").formSelect();
            $("#search_btn").prop("disabled", true).removeClass("text-shadow-2");
        }
    });


    // Sorting + Order By
    // on load
    if (sort_value == "author" || sort_value == "recipe_name") {
        $(".order-span-asc").html("<i class='fas fa-sort-alpha-down materialize-icons hide-on-small-only'></i> Alphabetical <strong>(A-Z)</strong>");
        $(".order-span-desc").html("<i class='fas fa-sort-alpha-up materialize-icons hide-on-small-only'></i> Alphabetical <strong>(Z-A)</strong>");
    }
    else if (sort_value == "user_favs" || sort_value == "views") {
        $(".order-span-asc").html("<i class='fas fa-sort-numeric-down materialize-icons hide-on-small-only'></i> Lowest first");
        $(".order-span-desc").html("<i class='fas fa-sort-numeric-up materialize-icons hide-on-small-only'></i> Highest first");
    }
    else if (sort_value == "last_edit") {
        $(".order-span-asc").html("<i class='fas fa-calendar-check materialize-icons hide-on-small-only'></i> Oldest first");
        $(".order-span-desc").html("<i class='far fa-calendar-check materialize-icons hide-on-small-only'></i> Newest first");
    }
    else if (sort_value == "total_time") {
        $(".order-span-asc").html("<i class='fas fa-clock materialize-icons hide-on-small-only'></i> Shortest first");
        $(".order-span-desc").html("<i class='far fa-clock materialize-icons hide-on-small-only'></i> Longest first");
    }
    // on selection
    $("#sort").on("change", function() {
        if ($("#sort").val() == "author" || $("#sort").val() == "recipe_name") {
            $(".order-span-asc").html("<i class='fas fa-sort-alpha-down materialize-icons hide-on-small-only'></i> Alphabetical <strong>(A-Z)</strong>");
            $(".order-span-desc").html("<i class='fas fa-sort-alpha-up materialize-icons hide-on-small-only'></i> Alphabetical <strong>(Z-A)</strong>");
        }
        else if ($("#sort").val() == "user_favs" || $("#sort").val() == "views") {
            $(".order-span-asc").html("<i class='fas fa-sort-numeric-down materialize-icons hide-on-small-only'></i> Lowest first");
            $(".order-span-desc").html("<i class='fas fa-sort-numeric-up materialize-icons hide-on-small-only'></i> Highest first");
        }
        else if ($("#sort").val() == "last_edit") {
            $(".order-span-asc").html("<i class='fas fa-calendar-check materialize-icons hide-on-small-only'></i> Oldest first");
            $(".order-span-desc").html("<i class='far fa-calendar-check materialize-icons hide-on-small-only'></i> Newest first");
        }
        else if ($("#sort").val() == "total_time") {
            $(".order-span-asc").html("<i class='fas fa-clock materialize-icons hide-on-small-only'></i> Shortest first");
            $(".order-span-desc").html("<i class='far fa-clock materialize-icons hide-on-small-only'></i> Longest first");
        }
    });

});