$(function() {
  function initPageFilter() {
    var $pageFilter = $(".page-filter");
    if ($pageFilter.length) {
      var $container = $pageFilter.find(".container"),
          checkForActiveFilters = function() {
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
      if (! $pageFilter.hasClass("is-visible")) {
        $container.hide();
      }

      $(".toggle-button").on("click", function(e) {
        e.preventDefault();
        if ($pageFilter.hasClass("is-visible")) {
          $pageFilter.removeClass("is-visible");
          $container.slideUp(500);
        } else {
          $pageFilter.addClass("is-visible");
          $container.slideDown(500);
        }

        checkForActiveFilters();
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

      $selectField.selectize({
        allowEmptyOption: true,
        plugins: ["active_css_classes"]
      });
    }
  }

  function initSearchForm() {
    initSelectize();
    var $searchForm = $(".search-form-header");
    if ($searchForm.length) {
      $("[data-action=toggle-search-form]").on("click", function() {
        $searchForm.toggleClass("is-hidden");
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

  function initBookHeader() {
    var $bookHeader = $("#book-header");
    if (! $bookHeader.length) {
      return false;
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
                offset = 64;
            if (navLinkSelectors.length) {
              if ($body.scrollTop() < offset) {
                var $this = $(navLinkSelectors[0]);
                $(".item-navigation-link").removeClass(activeClass);
                $(".item-navigation-link[href=#"+$this.attr("name")+"]").addClass(activeClass);
              } else {
                $(navLinkSelectors.join(",")).each(function() {
                  var $this = $(this);
                  if ($this.position().top < $body.scrollTop() + offset ) {
                    $(".item-navigation-link").removeClass(activeClass);
                    $(".item-navigation-link[href=#"+$this.attr("name")+"]").addClass(activeClass);
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
        trigger: "hover",
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
      $this.addClass("is-active").siblings(".is-active").removeClass("is-active")
      authorList.filter(function(item) {
        var name = item.values().name.toLowerCase();
        return name.substr(0, 1) == letter.toLowerCase();
      });
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
        var isOpen = $(this).parent().addClass("is-open");
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

    $("body").on("click.filter-author", function(e) {
      var $target = $(e.target),
          $openInput = $authorFilter.prev(".is-open"),
          isOpenText = $target.is(".is-open") || $target.parents(".is-open").length,
          $filter = $target.is(".filter") ? $target : $target.parents(".filter").first();

      if (! $filter.length && ! isOpenText && $openInput.length) {
        $authorFilter.slideUp();
        $openInput.removeClass("is-open").removeClass("is-focused");
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

  initSearchForm();
  initPageFilter();
  initBookHeader();
  initVisualization();
  initCustomActions();
});
