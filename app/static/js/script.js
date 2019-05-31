$(document).ready(function () {

    /*
    ---------------------------------------
        Initialize Materialize Elements
    ---------------------------------------
    */
    function initMaterialize() {
        $(".collapsible").collapsible();
        $(".tabs").tabs();
        $(".modal").modal();
        $(".tooltipped").tooltip();
        $(".sidenav").sidenav();
        $(".dropdown-trigger").dropdown();
        $("select").formSelect();
        $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: "absolute"});
        $("input#search_keyword, input#recipe_name, textarea#description").characterCounter();
        $(".carousel.carousel-slider").carousel({fullWidth: true, indicators: true});
        $(".fixed-action-btn").floatingActionButton({hoverEnabled: false});
    }
    initMaterialize();


    /*
    ------------------------------------------------------------------------------
        Custom function to mimic a 'Toast' for my Flash Messages for 4 seconds
    ------------------------------------------------------------------------------
    */
    function flashToast() {
        $("#flashToast").addClass("show");
        setTimeout(function () {
            $("#flashToast").removeClass("show");
        }, 4000);
    }
    flashToast();


    /*
    ---------------------------------------------------------
        Clone a new 'Ingredient' line on user-click event
    ---------------------------------------------------------
    */
    var ingredientCount = $(".ingredient").length;
    /* add new cloned item */
    $(".add-ingredient").on("click", function () {
        /* 'destroy' is required to clone <select> elements */
        $("select").formSelect("destroy");
        /* clone and remove existing values */
        $(".new-ingredient:first").clone().insertBefore(".add-ingredient").find("input[type='text'], select, textarea").val("");
        $("select").formSelect();
        /* increase counter so original ingredient is never removed */
        ingredientCount += 1;
    });
    /* delete last cloned item */
    $(".remove-ingredient").on("click", function () {
        if (ingredientCount > 1) {
            /* only remove the :last item */
            $(this).siblings(".new-ingredient:last").remove();
            /* ensure original ingredient line never gets deleted */
            ingredientCount -= 1;
        }
    });


    /*
    ---------------------------------------------------------
        Clone a new 'Direction' line on user-click event
    ---------------------------------------------------------
    */
    var directionCount = $(".direction").length;
    /* add new cloned item */
    $(".add-direction").on("click", function () {
        /* clone and remove existing values */
        $(".new-direction:first").clone().insertBefore(".add-direction").find("input[type='text'], select, textarea").val("");
        /* increase counter so original direction is never removed */
        directionCount += 1;
    });
    /* delete last cloned item */
    $(".remove-direction").on("click", function () {
        if (directionCount > 1) {
            /* only remove the :last item */
            $(this).siblings(".new-direction:last").remove();
            /* ensure original direction line never gets deleted */
            directionCount -= 1;
        }
    });


    /*
    -----------------------------------------------------------------------
        Mark ingredients / directions as 'Complete' on user-click event
    -----------------------------------------------------------------------
    */
    /* ingredients */
    $(".ingredient-item").on("click", function () {
        $(this).children("i").toggleClass("fa-circle fa-check-circle green-text");
        $(this).closest("li").find("span").toggleClass("grey-text strike");
    });
    /* directions */
    $(".direction-item").on("click", function () {
        $(this).toggleClass("grey-text strike");
        $(this).toggleClass("completed");
    });


    /*
    -------------------------------------------------------------
        Only enable 'Search' if user selects one of two items
    -------------------------------------------------------------
    */
    var search_keyword = $("#search_keyword").val();
    var search_dessert = $("#search_dessert").val();
    /* on page reload */
    if (search_keyword > "" || search_dessert > "") {
        $("#search_allergen, #sort").prop("disabled", false);
        $("i.fa-ban, i.fa-sort-amount-down").removeClass("grey-text").addClass("purple-text");
        $("select").formSelect();
        $("#search_btn").prop("disabled", false).addClass("text-shadow-2");
        /* collapsible should be 'open' if search function used */
        var instance = M.Collapsible.getInstance($(".collapsible"));
        instance.open();
    } else {
        $("#search_allergen, #sort").prop("disabled", true);
        $("i.fa-ban, i.fa-sort-amount-down").removeClass("purple-text").addClass("grey-text");
        $("select").formSelect();
        $("#search_btn").prop("disabled", true).removeClass("text-shadow-2");
    }
    /* on user interaction */
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


    /*
    ----------------------------------------------------------------------
        Populate the 'Order By' text and icons based on user-selection
    ----------------------------------------------------------------------
    */
    /* on page reload */
    var sort_value = $("#sort").val();
    switch (sort_value) {
        case "author":
        case "recipe_name":
            $(".order-span-asc").html("<i class='fas fa-sort-alpha-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(A-Z)</strong>");
            $(".order-span-desc").html("<i class='fas fa-sort-alpha-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(Z-A)</strong>");
            break;
        case "user_favs":
        case "views":
            $(".order-span-asc").html("<i class='fas fa-sort-numeric-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Lowest first");
            $(".order-span-desc").html("<i class='fas fa-sort-numeric-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Highest first");
            break;
        case "last_edit":
            $(".order-span-asc").html("<i class='fas fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Oldest first");
            $(".order-span-desc").html("<i class='far fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Newest first");
            break;
        case "total_time":
            $(".order-span-asc").html("<i class='fas fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Shortest first");
            $(".order-span-desc").html("<i class='far fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Longest first");
            break;
    }
    /* on user selection */
    $("#sort").on("change", function () {
        switch ($("#sort").val()) {
            case "author":
            case "recipe_name":
                $(".order-span-asc").html("<i class='fas fa-sort-alpha-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(A-Z)</strong>");
                $(".order-span-desc").html("<i class='fas fa-sort-alpha-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Alphabetical <strong>(Z-A)</strong>");
                break;
            case "user_favs":
            case "views":
                $(".order-span-asc").html("<i class='fas fa-sort-numeric-down materialize-icons hide-on-small-only' aria-hidden='true'></i> Lowest first");
                $(".order-span-desc").html("<i class='fas fa-sort-numeric-up materialize-icons hide-on-small-only' aria-hidden='true'></i> Highest first");
                break;
            case "last_edit":
                $(".order-span-asc").html("<i class='fas fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Oldest first");
                $(".order-span-desc").html("<i class='far fa-calendar-check materialize-icons hide-on-small-only' aria-hidden='true'></i> Newest first");
                break;
            case "total_time":
                $(".order-span-asc").html("<i class='fas fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Shortest first");
                $(".order-span-desc").html("<i class='far fa-clock materialize-icons hide-on-small-only' aria-hidden='true'></i> Longest first");
                break;
        }
    });


    /*
    -------------------------------------
        Carousel 'auto-play' function
    -------------------------------------
    */
    /* slides every 4 seconds */
    var timer = 4000;
    var autoplay = setInterval(function () {
        $(".carousel.carousel-slider").carousel("next");
    }, timer);
    /* pause carousel if user hovers */
    $(".carousel").mouseover(function () {
        clearInterval(autoplay);
    }).mouseout(function () {
        autoplay = setInterval(function () {
            $(".carousel.carousel-slider").carousel("next");
        }, timer);
    });


    /*
    ------------------------
        Print the Recipe
    ------------------------
    */
    $("#print-btn").on("click", function () {
        window.print();
    });


    /*
    ------------------------
        Share the Recipe
    ------------------------
    */
     /* insert URL into <input> */
    var recipeUrl = $(location).attr("href");
    $("#share-btn").on("click", function () {
        $("#share-url").val(recipeUrl);
    });
    /* copy value of <input> */
    $("#copy-btn").on("click", function () {
        var copyUrl = $("#share-url").val(recipeUrl);
        copyUrl.select();
        document.execCommand("copy");
        M.toast({html: "<i class='fas fa-clipboard-check material-icons left' aria-hidden='true'></i> Copied to Clipboard"});
    });


    /*
    ------------------------------------------------
        Save the Recipe to Favorites on Creation
    ------------------------------------------------
    */
    $("#add_favs").on("change", function () {
        switch ($("#add_favs").prop("checked")) {
            case true:
                M.toast({html: "<i class='fas fa-heart material-icons pink-text text-lighten-2 left' aria-hidden='true'></i> Sweet! This will be saved to your favorites!"});
                break;
            case false:
                M.toast({html: "<i class='fas fa-heart-broken material-icons red-text left' aria-hidden='true'></i> OK - but you can always add it later!"});
                break;
        }
    });


    /*
    ---------------------------------------------
        Auto-open the 'Card-Reveal' on :hover
    ---------------------------------------------
    */
    $(".card").hover(function () {
        $(this).find("> .card-image > img.activator").click();
    }, function () {
        $(this).find("> .card-reveal > .card-title").click();
    });


    /*
    --------------------------------------------------------------
        Custom validation on <select> if 'required' property.
        This function is not supported by Materialize natively
    --------------------------------------------------------------
    */
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
        $(this).parent(".select-wrapper").on("change", function () {
            if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                $(this).children("input").css({"border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50"});
            }
        });
    }).on("click", function () {
        if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(233, 30, 99, 0.15)") {
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


    /*
    -----------------------------------------------------
        Conversion for 'Weight' (cup-gram | gram-cup)
    -----------------------------------------------------
    */
    $("#convert-ingredient").on("change", function () {
        $("#convert-method").prop("disabled", false).val("");
        $("#convert-result").html("");
        $("select").formSelect();

        var selectedVal = $("#convert-ingredient option:selected").text();
        var ingredientVal = $("#convert-ingredient").val();

        var gramToCup1 = "<h4><strong>100 grams</strong> of <span class='purple-text'>" + selectedVal + "</span><br>=<br><strong>";
        var gramToCup2 = " cups</strong> of <span class='purple-text'>" + selectedVal + "</span></h4>";
        var cupToGram = "<h4><strong>1 cup</strong> of <span class='purple-text'>" + selectedVal + "</span><br>=<br><strong>" + ingredientVal + " grams</strong> of <span class='purple-text'>" + selectedVal + "</span></h4>";

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
        }
    });


    /*
    ------------------------------------------------
        Current year for 'Copyright' in <footer>
    ------------------------------------------------*/
    $("#year").html(new Date().getFullYear());


});