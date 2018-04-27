$(function() {

  // Clear the text inputs initially so that they are set properly
  // based on the checked boxes when users hit back/forward in the browser
  $('.mdl-textfield__input:not([name=query])').val(''); // but don't clear the header search bar...let it persist

  function initNavigationButton() {
    var $drawerButton = $("<div/>").addClass("mdl-layout__drawer-button").addClass("active"),
        $svg = $("<svg/>")
          .addClass("svg-icon")
          .attr({
            xmlns: "http://www.w3.org/2000/svg",
            viewBox: "0 0 20 20"
          })
          .html(
            '<rect x="2.4" y="3.3" width="15.2" height="2" fill="#979797"/><rect x="2.4" y="9" width="15.2" height="2" fill="#979797"/><rect x="2.4" y="14.7" width="15.2" height="2" fill="#979797"/>'
          );
    $("body").append($drawerButton.append($svg));
  }

  function submitFilterForm() {
    $(".mdl-layout").addClass("is-submitting");
    $(".page-filter__form").submit();
  }

  /**
   * Scrub empty values from form fields - don't need to submit them because
   * solr has defaults
   */
  $(".page-filter__form").submit(function () {
    $(this)
        .find('input[name]')
        .filter(function () {
            return !this.value;
        })
        .prop('name', '');
  });

  function initPageFilter() {
    var $pageFilter = $(".page-filter");
    if ($pageFilter.length) {
      var checkForActiveFilters = function() {
            var $filterInputs = $pageFilter.find(".mdl-textfield__input, .mdl-switch__input"),
                activeFilters = $filterInputs.filter(function() {
                  var $this = $(this);
                  if ($this.is(".mdl-switch__input")) {
                    return $this.prop("checked");
                  } else {
                    return $this.val();
                  }
                });
            if (activeFilters.length) {
              $pageFilter.addClass("is-active");
            } else {
              $pageFilter.removeClass("is-active");
            }
          };

      $(".toggle-button").on("click", function(e) {
        e.preventDefault();
        if ($pageFilter.hasClass("is-visible")) {
          $pageFilter.removeClass("is-visible");
        } else {
          $pageFilter.addClass("is-visible");
        }

        checkForActiveFilters();
      });

      var $filterForm = $(".page-filter__form");
      $filterForm.on("change", "input[type='checkbox']", function() {
        // submitFilterForm();
      });

    checkForActiveFilters();
    initAuthorFilter();
    initOrderBy();
    }
  }

  function initSelectize() {
    var $selectField = $(".mdl-selectfield__select");
    if ($selectField.length) {
      Selectize.define("active_css_classes", function(options) {
        var self = this;

        this.onFocus = (function() {
          var original = self.onFocus;
            return function() {
              var $select_field = self.$control.parents(".mdl-selectfield");
              $select_field.addClass("is-active");
              return original.apply(this, arguments);
            }
        })();

        this.onBlur = (function() {
          var original = self.onBlur;
            return function() {
              var $select_field = self.$control.parents(".mdl-selectfield");
              $select_field.removeClass("is-active");
              return original.apply(this, arguments);
            }
        })();

        this.onChange = (function() {
          var original = self.onBlur;
            return function(value) {
              var $select_field = self.$control.parents(".mdl-selectfield");
              if (value.length) {
                $select_field.addClass("is-dirty");
              } else {
                $select_field.removeClass("is-dirty");
              }
              return original.apply(this, arguments);
            }
        })();
      });

      var $selectizedFields = $selectField.selectize({
        allowEmptyOption: true,
        plugins: ["active_css_classes"]
      });

      window.selectizedFields = [];
      $selectizedFields.each(function() {
        window.selectizedFields.push($(this)[0].selectize);
      });
    }
  }

  function initFixedScrollSearchHeader() {
    var $searchFormHeader = $(".search-form-header");
    if ($searchFormHeader.length) {
      var headerHeight = $searchFormHeader.height();
      $("body").on("scroll", function() {
        var scrollTop = $(this).scrollTop(),
            cutoff = $searchFormHeader.position().top + headerHeight;
        if (scrollTop > cutoff) {
          $searchFormHeader.addClass("is-fixed");
        } else {
          $searchFormHeader.removeClass("is-fixed");
        }
      });
    }
  }

  function initSearchFormOnFocus() {
    var $searchHeaderForm = $(".search-form-header__form");
    if ($searchHeaderForm.length) {
      $(".search-form-header__form .mdl-textfield__input").on("focus.mainSearch", function() {
          $searchHeaderForm.addClass("is-focused");
        }).on("blur.mainSearch", function() {
          $searchHeaderForm.removeClass("is-focused");
        });
    }
  }

  function initSearchForm() {
    initSelectize();
    initFixedScrollSearchHeader();
    initSearchFormOnFocus();

    var $searchForm = $(".search-form-header");
    if ($searchForm.length) {
      $("[data-action=toggle-search-form]").on("click", function() {
        $searchForm.toggleClass("is-hidden");
        if (! $searchForm.hasClass("is-hidden")) {
          $("#id_query").focus();
        }
      });
    }
  }

  function initCustomActions() {
    var $itemImageLinks = $(".item__image__link");
    if ($itemImageLinks.length) {
      $itemImageLinks.on("mouseenter", function() {
        $(this).parents(".collection__item").find(".item__heading .item__link").addClass("is-hovered");
      }).on("mouseleave", function() {
        $(this).parents(".collection__item").find(".item__heading .item__link").removeClass("is-hovered");
      });
    }

    var $drawerCloseButton = $(".mdl-layout__drawer__close_button");
    if ($drawerCloseButton.length) {
      $drawerCloseButton.on("click", function(e) {
        e.preventDefault();
        $(".search-form-header").addClass("is-hidden");
        $(".mdl-layout__drawer.is-visible, .mdl-layout__obfuscator.is-visible").removeClass("is-visible");
      });
    }
  }

  var initBookHeaderAttempts = 0,
      maxNumberOfBookHeaderAttempts = 4;
  function initBookHeader() {
    var $bookHeader = $("#book-header"),
        maxAttempts = initBookHeaderAttempts < maxNumberOfBookHeaderAttempts,
        retryInit = function() {
         setTimeout(initBookHeader, 300);
         initBookHeaderAttempts ++;
       };

    if (! $bookHeader.length) {
      return false;
    }

    var $imageGalleryImg = $(".item-gallery .img");
    if ($imageGalleryImg.length > 0) {
      var imageGalleryImagesLoaded = $imageGalleryImg.last().height();
      if (maxAttempts && ! imageGalleryImagesLoaded) {
        retryInit();
        return;
      }
    }

    var imageHasLoaded = $bookHeader.find(".item-header__image").height()
    if (maxAttempts && ! imageHasLoaded) {
      retryInit();
      return;
    }
    $bookHeader.stickySidebar({
      topSpacing: 20,
      containerSelector: "#books-detail article",
      minWidth: 649,
      resizeSensor: false
    });

    var $body = $("body"),
        $navLinks = $(".item-navigation-link"),
        activeClass = "item-navigation-link--active";

    $navLinks.on("click", function(e) {
      var $this = $(this),
          hash = $this.attr("href"),
          $target = $("[name=" + hash.slice(1) + "]");

      if ($target.length) {
        e.preventDefault();
        $this.siblings().removeClass(activeClass);
        $this.addClass(activeClass);
        $this.blur();

        $body.animate({
          scrollTop: $target.position().top
        }, 500);
      }
    });

    var navLinkTargets = [],
        navLinkSelectors = [];
    $navLinks.each(function() {
      navLinkTargets.push($(this).attr("href"));
    });

    if (navLinkTargets.length) {
      $.each(navLinkTargets, function() {
        navLinkSelectors.push(".item-gallery__title a[name=" + this.slice(1) + "]");
      })
    }

    $body.scroll(function() {
        clearTimeout($.data(this, "scrollTimer"));
        $.data(this, "scrollTimer", setTimeout(function() {
            var activeTab = "",
                offset = 64,
                toggleFocus = function(name) {
                  $(".item-navigation-link").removeClass(activeClass);
                  var $focus = $(".item-navigation-link[href='#"+name+"']");
                  if ($focus.length > 0) {
                    $focus.addClass(activeClass);
                  }
                };
            if (navLinkSelectors.length) {
              if ($body.scrollTop() < offset) {
                var $this = $(navLinkSelectors[0]);
                toggleFocus($this.attr("name"));
              } else {
                $(navLinkSelectors.join(",")).each(function() {
                  var $this = $(this);
                  if ($this.position().top < $body.scrollTop() + offset ) {
                    toggleFocus($this.attr("name"));
                  }
                });
              }
            }
        }, 250));
    });
  }

  function initVisualization() {
    var $visualizationMarkers = $(".visualization-chapter-marker");
    if ($visualizationMarkers.length) {
      $visualizationMarkers.webuiPopover({
        trigger: "manual",
        animation: "fade",
        placement: "auto-top",
        arrow: true,
        delay: {
          show: 300,
          hide: 1000
        },
        style: "visualization",
        type: "async",
        async: {
           error: function(that, xhr, data) {
             that.$contentElement.children(".icon-refresh").addClass("error");
           }
        }
      });
    }
  }

  function initAuthorFilter() {
    var $authorFilter = $(".filter.filter--author");
    if (! $authorFilter.length) {
      return false;
    }

    //transform list items
    var $oldLabels = $(".filter__check-list--authors label"),
        $newLabels = $("<div/>"),
        sortLetters = [];

    $oldLabels.remove();
    $oldLabels.each(function() {
      var $this = $(this),
          $countLabel = $this.children("span"),
          count = $countLabel.text();
      $countLabel.remove();

      var authorName = $this.text().trim(),
          $input = $this.find("input"),
          $label = $("<label/>")
            .addClass("mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect")
            .append(
              $("<input/>").attr({
                id: $input.attr("id"),
                name: $input.attr("name"),
                value: $input.attr("value"),
                checked: $input.attr("checked"),
                type: "checkbox"
              }).addClass("mdl-checkbox__input"))
            .append($("<span/>").addClass("name").text(authorName))
            .append($("<span/>").addClass("filter__count").text(count));

        $newLabels.append($label);
        sortLetters.push(authorName.substr(0, 1));
    });

    $(".filter__check-list--authors").append($newLabels.html());

    var $filterNav = $(".filter__nav"),
        alphabetArray = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""),
        unavailableLetters = alphabetArray.filter(function(i) { return $.unique(sortLetters).indexOf(i) < 0 });

    $.each(alphabetArray, function() {
      var $filterLink = (unavailableLetters.indexOf(this[0]) > -1) ?
        $("<span/>").addClass("filter__nav-link--disabled") :
        $("<a/>").attr({ href: "#" });

      $filterNav.append($filterLink.addClass("filter__nav-link").text(this));
    });

    var authorList = new List("authors", {
      valueNames: [ "name" ],
      listClass: "filter__check-list--authors",
      searchClass: "filter__search-field--authors"
    });

    $(".filter__nav a").on("click", function(e) {
      e.preventDefault();
      var $this = $(this),
          letter = $this.text();
      if ($this.hasClass("is-active")) {
        $this.removeClass("is-active");
        authorList.filter();
      } else {
        $this.addClass("is-active").siblings(".is-active").removeClass("is-active")
        authorList.filter(function(item) {
          var name = item.values().name.toLowerCase();
          return name.substr(0, 1) == letter.toLowerCase();
        });
      }
    });

    var $authorSelectionInput = $("#author-selection"),
        clearSelectionInput = function() {
          $authorSelectionInput.val("");
          $authorSelectionInput.parent().removeClass("is-dirty");
        };

    $(".filter--author .clear-link").on("click", function(e) {
      e.preventDefault();
      var $checkboxes = $(this).parents(".filter").find(".mdl-checkbox__input");
      $checkboxes.each(function() {
        var $checkbox = $(this);
        $checkbox.removeProp("checked");
        $checkbox.removeAttr("checked");
        $checkbox.parent().removeClass("is-checked");
      });
      authorList.filter();
      clearSelectionInput();
    });

    $authorFilter.hide();

    $authorSelectionInput
      .on("focus", function() {
        $(this).parent().addClass("is-open");
        $authorFilter.slideDown();
      })
      .on("blur", function(e) {
        e.preventDefault();
        var isOpen = $(this).parent().hasClass("is-open");
        if (! isOpen) {
          $authorFilter.slideUp();
        }
      });

    var setSelectedOptionsValues = function(context) {
      var $elem = $(context),
          optionText = $elem.val(),
          authorSelectionVal = $authorSelectionInput.val() ? $authorSelectionInput.val().split("; ") : [];
      if ($elem.prop("checked")) {
        authorSelectionVal.push(optionText)
      } else {
        authorSelectionVal = $.grep(authorSelectionVal, function(value) {
          return value != optionText;
        });
      }
      if (authorSelectionVal.length) {
        $authorSelectionInput.parent().addClass("is-dirty");
      }
      $authorSelectionInput.val(authorSelectionVal.join("; "));
    }

    $(".filter__check-list--authors input:checked").each(function() {
      setSelectedOptionsValues(this);
    });

    $(".filter__check-list--authors input").on("change", function() {
      setSelectedOptionsValues(this);
    });

    var initialValue = $authorSelectionInput.val();
    var closeFilter = function($openInput) {
      $authorFilter.slideUp();
      $openInput.removeClass("is-open").removeClass("is-focused");

      if ($authorSelectionInput.val() !== initialValue) {
        submitFilterForm();
      }
    }

    $(".filter--author.is-not-ready").removeClass("is-not-ready");

    $("body").on("click.filter--author", function(e) {
      var $target = $(e.target),
          filterSelector = ".filter--author",
          $openInput = $authorFilter.prev(".is-open"),
          isOpenText = $target.is(".is-open") || $target.parents(".is-open").length,
          $filter = $target.is(filterSelector) ? $target : $target.parents(filterSelector).first();

      if (! $filter.length && ! isOpenText && $openInput.length) {
        closeFilter($openInput);
      } else if ($openInput.length && ! $target.parent().next().is(filterSelector) && ! $target.parents(filterSelector).length) {
        closeFilter($openInput);
      } else if ($openInput.length) {
        $openInput.addClass("is-focused");
      }
    });
  }

  function initOrderBy() {
    var $orderbyLabels = $(".order_by #id_order_by label");
    if (! $orderbyLabels.length) {
      return false;
    }

    $orderbyLabels.each(function() {
      var $this = $(this),
          $parent = $this.parent(),
          $checkbox = $this.children("input").addClass("hidden"),
          $label = $("<span/>").text($.trim($this.text()));
      $this.text("");
      $this.append($checkbox).append($label);

      $parent.addClass("sort-link");
      if ($checkbox.prop("checked")) {
        $parent.addClass("sort-link--active");
      }
    });

    $("form.order_by .sort-link").on("click", function(e) {
      e.preventDefault();
      $(this).find("input").prop("checked", "checked");
      $("form.order_by").submit();
    });

    $("form.order_by input[type='radio']").on("change", function() {
      $("form.order_by").submit();
    });
  }

  function initAnnotatorDropdown() {
    var $marginContainer = $(".margin-container");

    if ($marginContainer.length) {
      $marginContainer.on("click", ".dropdown-toggle", function() {
        var $menu = $(this).parent().find(".dropdown-menu");
        if ($menu.css("display") === "none") {
          $menu.css({ display: "block" });
        } else {
          $menu.css({ display: "none" });
        }
      });
    }
  }

  function arraysAreEqual(array1, array2) {
    return $(array1).not(array2).length === 0 && $(array2).not(array1).length === 0
  }

  function initGlobalFunctions() {
    window.initYearSelector = function(options) {
      var selector = options.selector,
          fieldName = options.fieldName;

      var $yearFilter = $(selector),
          $filterInput = $("#" + fieldName + "-year-selection"),
          $yearRangeInputs = $yearFilter.find(".filter__search-field"),
          getValues = function() {
            return $yearRangeInputs.map(function() { return this.value });
          },
          setValueForFilterInput = function(values) {
            values = values || getValues();
            var displayValue = (values[0] || values[1]) ?
              values[0] + " - " + values[1] : "";
            $filterInput.val(displayValue);
          };

      $yearFilter.hide();
      setValueForFilterInput();

      var $inputs = $yearFilter.find(".filter__search input"),
          $firstInput = $inputs.first(),
          $lastInput = $inputs.last();
      $lastInput.attr({placeholder: "End"}).before($("<label/>").addClass("filter__search-label").text("to"));

      $yearFilter.find(".clear-link").on("click", function(e) {
        e.preventDefault();
        $yearRangeInputs.each(function() {
           $(this).val("");
        });
      });

      var initialValues = getValues();
      var closeFilter = function($openInput) {
        var currentValues = getValues();
        $yearFilter.slideUp();
        $openInput.removeClass("is-open").removeClass("is-focused");

        if (! arraysAreEqual(initialValues, currentValues)) {
          setValueForFilterInput(currentValues);
          submitFilterForm();
        }
      };

      $filterInput.on("focus", function() {
          $(this).parent().addClass("is-open");
          $yearFilter.slideDown();
        })
        .on("blur", function(e) {
          e.preventDefault();
          var isOpen = $(this).parent().addClass("is-open");
          if (! isOpen) {
            $yearFilter.slideUp();
          }
        });

      var namedClickEvent = "click.filter--" + fieldName;

      var $histogramBars = $yearFilter.find(".frequency_chart__bar"),
          prefillRanges = function() {
            $histogramBars.each(function(index, histogramBar) {
              var $histogramBar = $(histogramBar),
                  year = $histogramBar.data("year"),
                  firstYear = $firstInput.val(),
                  lastYear = $lastInput.val();

              if (year == firstYear == lastYear) {
                $histogramBar.addClass("is-selected");
                $histogramBar.addClass("is-selected--end");
                return false;
              } else if (year == firstYear) {
                $histogramBar.addClass("is-selected");
              } else if (year == lastYear) {
                $histogramBar.addClass("is-selected");
              }

              if ($histogramBars.find(".is-selected").length == 2) {
                return false;
              }
            });
          };

      $histogramBars.on(namedClickEvent, function(e) {
        var $this = $(this),
            $selected = $this.siblings(".is-selected"),
            addSelection = function(options) {
              options = options || {};
              $this.addClass("is-selected");
              if (options.isSingleYear === true) {
                $this.addClass("is-selected--end");
              }
            },
            clearSelection = function() {
              $selected.removeClass("is-selected");
              $selected.removeClass("is-selected--end");
              $firstInput.val("");
              $lastInput.val("");
            };

        switch ($selected.length) {
          case 0:
            if ($this.hasClass("is-selected")) {
              addSelection({isSingleYear: true});
              $firstInput.val($this.data("year"));
              $lastInput.val($this.data("year"));
            } else {
              addSelection();
              $firstInput.val($this.data("year"));
            }
            break;
          case 1:
            var selectedIndex = $histogramBars.index($selected),
                thisIndex = $histogramBars.index($this);
            if (selectedIndex < thisIndex) {
              if ($this.hasClass("is-selected")) {
                $selected.removeClass("is-selected");
                addSelection({isSingleYear: true});
                $firstInput.val($this.data("year"));
              } else {
                $selected.removeClass("is-selected--end");
                addSelection();
                $lastInput.val($this.data("year"));
              }
            } else {
              clearSelection();
              addSelection();
              $firstInput.val($this.data("year"));
            }
            break;
          case 2:
            clearSelection();
            addSelection();
            $firstInput.val($this.data("year"));
            break;
        }
      });

      $("body").on(namedClickEvent, function(e) {
        var $target = $(e.target),
            filterSelector = selector,
            $openInput = $yearFilter.prev(".is-open"),
            isOpenText = $target.is(".is-open") || $target.parents(".is-open").length,
            $filter = $target.is(filterSelector) ? $target : $target.parents(filterSelector).first();

        if (! $filter.length && ! isOpenText && $openInput.length) {
          closeFilter($openInput);
        } else if ($openInput.length && ! $target.parent().next().is(filterSelector) && ! $target.parents(filterSelector).length) {
          closeFilter($openInput);
        } else if ($openInput.length) {
          $openInput.addClass("is-focused");
        }
      });
    };

    window.initCheckboxSelector = function(options) {
      var filterInputSelector = options.filterInputSelector,
          filterCheckListSelector = options.filterCheckListSelector,
          filterSelector = options.filterSelector,
          filterClickEvent = options.filterClickEvent,
          isDisabled = options.isDisabled;

      //transform list items
      var $oldLabels = $(filterCheckListSelector + " label"),
          $newLabels = $("<div/>");

      $oldLabels.remove();
      $oldLabels.each(function() {
        var $this = $(this),
            $countLabel = $this.children("span"),
            count = $countLabel.text();
        $countLabel.remove();

        var labelText = $this.text().trim(),
            $input = $this.find("input"),
            inputAttr = {
              id: $input.attr("id"),
              name: $input.attr("name"),
              value: $input.attr("value"),
              checked: $input.attr("checked"),
              type: "checkbox"
            };
        if (isDisabled || $input.attr("disabled")) {
          inputAttr.disabled = "disabled";
        }

        var $label = $("<label/>")
              .addClass("mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect")
              .append(
                $("<input/>").attr(inputAttr).addClass("mdl-checkbox__input"))
              .append($("<span/>").addClass("name").text(labelText))
              .append($("<span/>").addClass("filter__count").text(count));

          $newLabels.append($label);
      });

      var $checkboxFilter = $(filterSelector);
      $checkboxFilter.hide();

      $(filterCheckListSelector).append($newLabels.html());

      var $checkboxFilterSelectionInput = $(filterInputSelector),
          clearSelectionInput = function() {
            $checkboxFilterSelectionInput.val("");
          };

      $checkboxFilter.find(".clear-link").on("click", function(e) {
        e.preventDefault();
        var $checkboxes = $(this).parents(".filter").find(".mdl-checkbox__input");
        $checkboxes.each(function() {
          var $checkbox = $(this);
          $checkbox.removeProp("checked");
          $checkbox.removeAttr("checked");
          $checkbox.parent().removeClass("is-checked");
        });
        clearSelectionInput();
      });

      $checkboxFilterSelectionInput.on("focus", function() {
          $(this).parent().addClass("is-open");
          $checkboxFilter.slideDown();
        })
        .on("blur", function(e) {
          e.preventDefault();
          var isOpen = $(this).parent().addClass("is-open");
          if (! isOpen) {
            $checkboxFilter.slideUp();
          }
        });

        var setSelectedOptionsValues = function($checklist) {
          var $checklists = $checklist || $(".filter__check-list").has("input[checked=checked]");

          $checklists.each(function() {
            var $this = $(this),
                $checkedOptions = $this.find("input[checked=checked]"),
                name = $checkedOptions.first().attr("name"),
                $input = $("#" + name + "-selection");

            if ($checkedOptions.length > 1) {
              $input.val($checkedOptions.length + " selected");
            } else if ($checkedOptions.length === 1) {
              $input.val($checkedOptions.first().val());
            } else {
              $input.val();
            }
          });
        }

        setSelectedOptionsValues();

        $(filterCheckListSelector + " input").on("change", function() {
          var $this = $(this);
          if (! $this.attr("checked")) {
            $this.attr("checked", "checked");
          } else {
            $this.removeAttr("checked");
          }
          setSelectedOptionsValues($this.parents(".filter__check-list"));
        });

        var initialValue = $checkboxFilterSelectionInput.val();
        var closeFilter = function($openInput) {
          $checkboxFilter.slideUp();
          $openInput.removeClass("is-open").removeClass("is-focused");

          if ($checkboxFilterSelectionInput.val() !== initialValue) {
            submitFilterForm();
          }
        };

        $(filterSelector + ".is-not-ready").removeClass("is-not-ready");

        var clickEvent = "click.filter--" + filterClickEvent;
        $("body").on(clickEvent, function(e) {
          var $target = $(e.target),
              $openInput = $checkboxFilter.prev(".is-open"),
              isOpenText = $target.is(".is-open") || $target.parents(".is-open").length,
              $filter = $target.is(filterSelector) ? $target : $target.parents(filterSelector).first();

          if (! $filter.length && ! isOpenText && $openInput.length) {
            closeFilter($openInput);
          } else if ($openInput.length && ! $target.parent().next().is(filterSelector) && ! $target.parents(filterSelector).length) {
            closeFilter($openInput);
          } else if ($openInput.length) {
            $openInput.addClass("is-focused");
          }
        });
    }

    $.getElementSize = $.getElementSize || function(selector) {
      var $element = $(selector);
      return {
        x: $element.width(),
        y: $element.height()
      };
    }

    $.getPageScroll = $.getPageScroll || function(selector) {
      var $element = $(selector)
      return {
        x: $element.scrollLeft(),
        y: $element.scrollTop()
      };
    }

    $.addClass = $.addClass || function(selector, className) {
      $(selector).addClass(className);
    }

    $.getWindowSize = $.getWindowSize || function() {
      var $window = $(window);
      return {
        x: $window.width(),
        y: $window.height()
      };
    }

    $.isFullScreen = function() {
      return (screen.availHeight || screen.height-30) <= window.innerHeight;
    }

    $.delegate = function( selector, types, data, fn ) {
      return this.on( types, selector, data, fn );
    }

    $.undelegate = function( selector, types, fn ) {
      // ( namespace ) or ( selector, types [, fn] )
      return arguments.length === 1 ? this.off( selector, "**" ) : this.off( types, selector || "**", fn );
    }
  }

  initNavigationButton();
  initSearchForm();
  initPageFilter();
  initBookHeader();
  initVisualization();
  initCustomActions();
  initAnnotatorDropdown();
  initGlobalFunctions();

  /**
   * Add handlers for the visualization since the default hover doesn't handle
   * tablets at all.
  */
  $vizMarkers = $(".visualization-chapter-marker");
  $vizMarkers.on("mouseenter touchstart focus", function() {
    $(this).webuiPopover('show');
  });
  $vizMarkers.on("mouseleave touchend blur", function() {
    $(this).webuiPopover('hide');
  });
});
