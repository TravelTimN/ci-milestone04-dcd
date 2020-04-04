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
    // add new cloned 'ingredient'
    $(".add-ingredient").on("click", function () {
        addIngredient($(this).parent(".new-ingredient"));
    });
    function addIngredient(thisObj) {
        // 'destroy' is required to clone <select> elements
        $("select").formSelect("destroy");
        // clone and remove existing values
        $(".new-ingredient:first").clone(true, true).insertAfter(thisObj).find("input[type='text'], select, textarea").val("").addClass("invalid");
        $("select").formSelect();
        ingredientCount += 1;
        // custom Materialize validation (not built-in natively)
        let thisMeasurement = thisObj.closest("div").find(".dropdown-trigger").dropdown();
        let classInvalid = {"border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336"};
        let classValid = {"border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50"};
        if ($(thisMeasurement).val() != "unit of measurement") {
            $(thisMeasurement).css(classValid);
        } else {
            $(thisMeasurement).css(classInvalid);
        }
        thisObj.closest("div").find("input").focus();
        thisObj.next("div").find(".dropdown-trigger").dropdown().css(classInvalid);
        disableRemoveIngredient();
        validateMaterializeSelect();
        thisObj.next("div").find("input:first").focus();
        // end custom validation
    }
    // delete selected 'ingredient'
    $(".remove-ingredient").on("click", function () {
        removeIngredient($(this).parent(".new-ingredient"));
    });
    function removeIngredient(thisObj) {
        $(thisObj).remove();
        ingredientCount -= 1;
        disableRemoveIngredient();
    }
    // disable 'remove-ingredient' if only one ingredient exists
    let ingredientCount = $(".ingredient").length;
    disableRemoveIngredient();
    function disableRemoveIngredient() {
        if (ingredientCount === 1) {
            $("button.remove-ingredient").prop("disabled", true);
        } else {
            $("button.remove-ingredient").prop("disabled", false);
        }
    }


    /*
    ---------------------------------------------------------
        Clone a new 'Direction' line on user-click event
    ---------------------------------------------------------
    */
    // add new cloned 'direction'
    $(".add-direction").on("click", function () {
        addDirection($(this).parent(".new-direction"));
    });
    function addDirection(thisObj) {
        // clone and remove existing values
        $(".new-direction:first").clone(true, true).insertAfter(thisObj).find("textarea").val("");
        directionCount += 1;
        // custom Materialize validation (not built-in natively)
        thisObj.closest("div").find("textarea").focus();
        disableRemoveDirection();
        validateMaterializeSelect();
        thisObj.next("div").find("textarea").focus();
        // end custom validation
    }
    // delete selected 'direction'
    $(".remove-direction").on("click", function () {
        removeDirection($(this).parent(".new-direction"));
    });
    function removeDirection(thisObj) {
        $(thisObj).remove();
        directionCount -= 1;
        disableRemoveDirection();
    }
    // disable 'remove-direction' if only one direction exists
    let directionCount = $(".direction").length;
    disableRemoveDirection();
    function disableRemoveDirection() {
        if (directionCount === 1) {
            $("button.remove-direction").prop("disabled", true);
        } else {
            $("button.remove-direction").prop("disabled", false);
        }
    }


    /*
    -----------------------------------------------------------------------
        Mark ingredients / directions as 'Complete' on user-click event
    -----------------------------------------------------------------------
    */
    // ingredients
    $(".ingredient-item").on("click", function () {
        $(this).children("i").toggleClass("fa-circle fa-check-circle green-text");
        $(this).closest("li").find("span").toggleClass("grey-text strike");
    });
    // directions
    $(".direction-item").on("click", function () {
        $(this).toggleClass("grey-text strike completed");
    });


    /*
    -------------------------------------------------------------
        Only enable 'Search' if user selects one of two items
    -------------------------------------------------------------
    */
    let search_keyword = $("#search_keyword").val();
    let search_dessert = $("#search_dessert").val();
    // on page reload
    if (search_keyword > "" || search_dessert > "") {
        $("#search_allergen, #sort").prop("disabled", false);
        $("i.fa-ban, i.fa-sort-amount-down").removeClass("grey-text").addClass("purple-text");
        $("select").formSelect();
        $("#search_btn").prop("disabled", false).addClass("text-shadow-2");
        // collapsible should be 'open' if search function used
        let instance = M.Collapsible.getInstance($(".collapsible"));
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


    /*
    ----------------------------------------------------------------------
        Populate the 'Order By' text and icons based on user-selection
    ----------------------------------------------------------------------
    */
    // on page reload
    sortIcons();
    // on user selection
    $("#sort").on("change", function () {
        sortIcons();
    });
    function sortIcons() {
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
    }


    /*
    -------------------------------------
        Carousel 'auto-play' function
    -------------------------------------
    */
    // slides every 4 seconds
    let timer = 4000;
    let autoplay = setInterval(function () {
        $(".carousel.carousel-slider").carousel("next");
    }, timer);
    // pause carousel if user hovers
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
     // insert URL into <input>
    let recipeUrl = $(location).attr("href");
    $("#share-btn").on("click", function () {
        $("#share-url").val(recipeUrl);
    });
    // copy value of <input>
    $("#copy-btn").on("click", function () {
        let copyUrl = $("#share-url").val(recipeUrl);
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
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = {"border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50"};
        let classInvalid = {"border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336"};
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(233, 30, 99, 0.15)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }


    /*
    -----------------------------------------------------
        Conversion for 'Weight' (cup-gram | gram-cup)
    -----------------------------------------------------
    */
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
        }
    });


    /*
    ------------------------------------------------
        Show image if valid on entry
    ------------------------------------------------
    */
    // on image url source focus-out
    $("input#img_src.validate").blur(function () {
        // show error if invalid image type / url
        if ($("input#img_src.validate").hasClass("invalid")) {
            $("#img_error").html(`Invalid Image URL Type<br>
                <small>.jpg .jpeg .gif .bmp .png .tiff</small><br>
                <a id="clearUrl" class="btn btn-small red text-shadow-2">Fix Error?</a>`);
            // fix error to remove invalid text/class for submit
            $("#clearUrl").click(function () {
                $("input#img_src.validate").val("").focusout().removeClass("invalid");
                $("#img_error").empty();
            });
        } else {
            $("#img_error").empty();
        }
        // update picture based on category
        let dessertCategory;
        if ($("#dessert_type option:selected").text() == "Dessert Category") {
            dessertCategory = "other-desserts";
        } else {
            dessertCategory = $("#dessert_type option:selected").text().replace(" + ", "-").replace(" + ", "-").replace(" ", "-").toLowerCase();
        }
        // add image tag, with fallback option for dessert-category default image
        $("#img_new").empty().prepend(`<img class="recipe-img-small" src="${$(this).val()}" onError="this.onerror=null;this.src='../../../static/img/desserts/${dessertCategory}.png';">`);
    });

    // on dessert-type change
    $("#dessert_type").change(function () {
        // focus back on img_src url to check if already a valid image
        $("input#img_src.validate").focus();
        let dessertCategory;
        if ($("#dessert_type option:selected").text() == "Dessert Category") {
            dessertCategory = "other-desserts";
        } else {
            dessertCategory = $("#dessert_type option:selected").text().replace(" + ", "-").replace(" + ", "-").replace(" ", "-").toLowerCase();
        }
        // add image tag, with fallback option for dessert-category default image
        $("#img_new").empty().prepend(`<img class="recipe-img-small" src="${$(this).val()}" onError="this.onerror=null;this.src='../../../static/img/desserts/${dessertCategory}.png';">`);
    });


    /*
    ------------------------------------------------
        Current year for 'Copyright' in <footer>
    ------------------------------------------------
    */
    $("#year").html(new Date().getFullYear());


});