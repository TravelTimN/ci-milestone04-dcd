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
    $("select[required]").css({
        display: "block",
        height: 0,
        padding: 0,
        width: 0,
        position: "absolute"
    });

    // initialize input character count
    $("input#search_keyword, input#recipe_name, textarea#description").characterCounter();

    // initialize carousel slider
    $(".carousel.carousel-slider").carousel({
        fullWidth: true,
        indicators: true
    });

    // initialize floating action button
    $(".fixed-action-btn").floatingActionButton({hoverEnabled: false});


    /*----- CUSTOMIZATION -----*/

    // custom Flash Toast
    function flashToast() {
        $("#flashToast").addClass("show");
        setTimeout(function () {
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
        var instance = M.Collapsible.getInstance($(".collapsible"));
        instance.open();
    } else {
        $("#search_allergen, #sort").prop("disabled", true);
        $("i.fa-ban, i.fa-sort-amount-down").removeClass("purple-text").addClass("grey-text");
        $("select").formSelect();
        $("#search_btn").prop("disabled", true).removeClass("text-shadow-2");
    }
    // on user interaction
    $("#search_keyword, #search_dessert").on("keyup input change", function () {
        if ($("#search_keyword").val().length >= 3 || $("#search_dessert").val().length > 0) {
            $("#search_allergen, #sort").prop("disabled", false);
            $("i.fa-ban, i.fa-sort-amount-down").removeClass("grey-text").addClass("purple-text");
            $("select").formSelect();
            $("#search_btn").prop("disabled", false).addClass("text-shadow-2");
        } else {
            $("#search_allergen, #sort").prop("disabled", true);
            $("i.fa-ban, i.fa-sort-amount-down").removeClass("purple-text").addClass("grey-text");
            $("select").formSelect();
            $("#search_btn").prop("disabled", true).removeClass("text-shadow-2");
        }
    });


    // Sorting + Order By
    // on load
    if (sort_value == "author" || sort_value == "recipe_name") {
        $(".order-span-asc").html("<i class='fas fa-sort-alpha-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(A-Z)</strong>");
        $(".order-span-desc").html("<i class='fas fa-sort-alpha-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(Z-A)</strong>");
    } else if (sort_value == "user_favs" || sort_value == "views") {
        $(".order-span-asc").html("<i class='fas fa-sort-numeric-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Lowest first");
        $(".order-span-desc").html("<i class='fas fa-sort-numeric-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Highest first");
    } else if (sort_value == "last_edit") {
        $(".order-span-asc").html("<i class='fas fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Oldest first");
        $(".order-span-desc").html("<i class='far fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Newest first");
    } else if (sort_value == "total_time") {
        $(".order-span-asc").html("<i class='fas fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Shortest first");
        $(".order-span-desc").html("<i class='far fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Longest first");
    }
    // on selection
    $("#sort").on("change", function () {
        if ($("#sort").val() == "author" || $("#sort").val() == "recipe_name") {
            $(".order-span-asc").html("<i class='fas fa-sort-alpha-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(A-Z)</strong>");
            $(".order-span-desc").html("<i class='fas fa-sort-alpha-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(Z-A)</strong>");
        } else if ($("#sort").val() == "user_favs" || $("#sort").val() == "views") {
            $(".order-span-asc").html("<i class='fas fa-sort-numeric-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Lowest first");
            $(".order-span-desc").html("<i class='fas fa-sort-numeric-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Highest first");
        } else if ($("#sort").val() == "last_edit") {
            $(".order-span-asc").html("<i class='fas fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Oldest first");
            $(".order-span-desc").html("<i class='far fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Newest first");
        } else if ($("#sort").val() == "total_time") {
            $(".order-span-asc").html("<i class='fas fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Shortest first");
            $(".order-span-desc").html("<i class='far fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Longest first");
        }
    });


    // autoplay recipe carousel
    const timer = 4000;
    let autoplay = setInterval(function () {
        $(".carousel.carousel-slider").carousel("next");
    }, timer);
    $(".carousel").mouseover(function () {
        clearInterval(autoplay);
    }).mouseout(function () {
        autoplay = setInterval(function () {
            $(".carousel.carousel-slider").carousel("next");
        }, timer);
    });


    // print recipe page
    $("#print-btn").on("click", function () {
        window.print();
    });


    // insert current URL into input text
    $("#share-btn").on("click", function () {
        recipeUrl = $(location).attr("href");
        $("#share-url").val(recipeUrl);
    });
    // copy value of input text
    $("#copy-btn").on("click", function () {
        let copyUrl = $("#share-url").val(recipeUrl);
        copyUrl.select();
        document.execCommand("copy");
        M.toast({
            html: "<i class='fas fa-clipboard-check material-icons left' aria-hidden='true'></i> Copied to Clipboard"
        });
    });


    // advise user that recipe will be saved to their favorites (if selected)
    $("#add_favs").on("change", function () {
        if ($("#add_favs").prop("checked") == true) {
            M.toast({
                html: "<i class='fas fa-heart material-icons pink-text text-lighten-2 left' aria-hidden='true'></i> Sweet! This will be saved to your favorites!"
            });
        } else {
            M.toast({
                html: "<i class='fas fa-heart-broken material-icons red-text left' aria-hidden='true'></i> OK - but you can always add it later!"
            });
        }
    });


    // auto-open card-reveal
    $(".card").hover(function () {
        $(this).find("> .card-image > img.activator").click();
    }, function () {
        $(this).find("> .card-reveal > .card-title").click();
    });


    // Materialize doesn't validate select/dropdown fields, so this is my code to change it red if it's 'required'
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
        $(this).parent(".select-wrapper").on("change", function () {
            if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                $(this).children("input").css({"border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50"});
            }
        });
    }).on("click", function () {
        if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") == "rgba(233, 30, 99, 0.15)") {
            $(this).parent(".select-wrapper").children("input").css({"border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50"});
        } else {
            $(".select-wrapper input.select-dropdown").on("focusout", function () {
                if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                    if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                        $(this).parent(".select-wrapper").children("input").css({"border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336"});
                    }
                }
            });
        }
    });


    // Weight Conversion from cup-gram or gram-cup
    $("#convert-ingredient").on("change", function () {
        $("#convert-method").prop("disabled", false).val("");
        $("#convert-result").html("");
        $("select").formSelect();

        let selectedVal = $("#convert-ingredient option:selected").text();
        let ingredientVal = $("#convert-ingredient").val();

        let gramToCup1 = "<h4><strong>100 grams</strong> of <span class='purple-text'>" + selectedVal + "</span><br>=<br><strong>";
        let gramToCup2 = " cups</strong> of <span class='purple-text'>" + selectedVal + "</span></h4>";
        let cupToGram = "<h4><strong>1 cup</strong> of <span class='purple-text'>" + selectedVal + "</span><br>=<br><strong>" + ingredientVal + " grams</strong> of <span class='purple-text'>" + selectedVal + "</span></h4>";

        switch ($("#convert-ingredient").val()) {
            case "85":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "&frac34;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "100":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "1" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "120":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "1 &frac14;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "140":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "1 &frac13;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "150":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "1 &frac12;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "200":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "2" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "225":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "2 &frac14;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "325":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "3 &frac14;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            case "340":
                $("#convert-method").on("change", function () {
                    switch ($("#convert-method").val()) {
                        case "g-c":
                            $("#convert-result").html(gramToCup1 + "3 &frac13;" + gramToCup2);
                            break;
                        case "c-g":
                            $("#convert-result").html(cupToGram);
                            break;
                    }
                });
                break;
            default:
                "Please Select an Ingredient";
        }
    });

});